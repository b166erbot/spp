from random import choices
from re import findall
from time import sleep
from webbrowser import open as openn

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, Gtk

from .bancodedados.bancodedados import (adminInsert, adminQuery,
                                        create_table_admin, create_table_dados,
                                        data_entry, delete_all_dados,
                                        delete_data, getLastId, read_data,
                                        update_data)
from .functions import (criptaes, cripthash, salt, trocar_senhas,
                        verificar_admin)


senhaAdmin = ''


def copy(cb, texto):
    """ Função que copia o texto para a área de transferência. """
    cb.set_text(texto, -1)
    cb.store()


class Janela:
    def __init__(self):
        # criando objetos.
        self.cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self._nv = False
        self._builder = Gtk.Builder()
        self._liststore = Gtk.ListStore(int, str, str, str)
        renderText = Gtk.CellRendererText()
        renderText2 = Gtk.CellRendererText()
        renderText3 = Gtk.CellRendererText()
        renderText4 = Gtk.CellRendererText()
        coluna = Gtk.TreeViewColumn("id", renderText, text=0)
        coluna2 = Gtk.TreeViewColumn("site", renderText2, text=1)
        coluna3 = Gtk.TreeViewColumn("login", renderText3, text=2)
        coluna4 = Gtk.TreeViewColumn("senha", renderText4, text=3)

        # obtendo a interface glade.
        self._builder.add_from_file('spp.glade')

        # obtendo objetos.
        self._janela1 = self._builder.get_object('janela1')
        self._janela2 = self._builder.get_object('janela2')
        self._verificar = self._builder.get_object('verificar')
        self._status = self._builder.get_object('status')
        self._box_n_u = self._builder.get_object('novo_usuario')
        self._trocar_senha = self._builder.get_object('check_trocar_senha')
        self._treeview = self._builder.get_object('treeview')
        self._selecao = self._treeview.get_selection()
        self._senha = self._builder.get_object('senha')
        self._senha2 = self._builder.get_object('senha2')
        self._senha3 = self._builder.get_object('senha3')
        self._adicionar = self._builder.get_object('adicionar')
        self._remover = self._builder.get_object('remover')
        self._remover_tudo = self._builder.get_object('remover_tudo')
        self._copiar = self._builder.get_object('copiar')
        self._box_senha = self._builder.get_object('box_senha')
        self._inserir_site = self._builder.get_object('inserir_site')
        self._inserir_login = self._builder.get_object('inserir_login')
        self._inserir_senha = self._builder.get_object('inserir_senha')
        self._atualizar = self._builder.get_object('atualizar')
        texto = ('Essa ação removerá todos as contas armazenadas. Tem certeza'
                 ' que deseja remover todas as contas? essa ação é'
                 ' irreversível!')
        self._confirmacao = Gtk.MessageDialog(
            text='Atenção!',
            secondary_text=texto,
            buttons=Gtk.ButtonsType.OK_CANCEL)
        self._confirmacao2 = Gtk.MessageDialog(
            secondary_text='Remover?',
            buttons=Gtk.ButtonsType.OK_CANCEL)

        # configurando.
        self._treeview.append_column(coluna)
        self._treeview.append_column(coluna2)
        self._treeview.append_column(coluna3)
        self._treeview.append_column(coluna4)
        self._treeview.set_model(self._liststore)
        self._janela1.set_title('Super Protect Password')
        self._janela2.set_title('spp')
        self._status.push(0, 'status:')
        self._confirmacao.set_transient_for(self._janela2)
        self._janela1.set_transient_for(self._janela2)
        self._confirmacao2.set_transient_for(self._janela2)
        # self._verificar.set_sensitive(False)
        if not any(adminQuery()):
            self._nv = True
            self._builder.get_object('texto_primeira_vez').set_visible(True)
            self._box_n_u.set_visible(True)
            self._box_senha.set_visible(False)
            self._trocar_senha.set_visible(False)
            self._verificar.set_label('Confirmar')

        # conectando objetos.
        self._verificar.connect('clicked', self.verificar_clicado)
        self._janela1.connect('destroy', Gtk.main_quit)
        self._janela2.connect('destroy', Gtk.main_quit)
        self._trocar_senha.connect('toggled', self._trocar_senha_alterado)
        self._senha.connect('activate', self._enter_senha)
        self._senha2.connect('activate', self._enter_senha)
        self._senha3.connect('activate', self._enter_senha)
        self._adicionar.connect('clicked', self.adicionar_clicado)
        self._remover.connect('clicked', self.remover_clicado)
        self._remover_tudo.connect('clicked', self.remover_tudo_clicado)
        self._copiar.connect('clicked', self.copiar_clicado)
        self._atualizar.connect('clicked', self.atualizar_clicado)
        self._inserir_senha.connect('activate', self.adicionar_clicado)
        self._confirmacao.connect('response', lambda a, b: (a, b))
        self._confirmacao2.connect('response', lambda a, b: (a, b))
        self._treeview.connect('row-activated', self.treeviewcolumn_clicado)
        self._inserir_site.connect(
            'activate',
            lambda a, *_: a.do_grab_focus(self._inserir_login))
        self._inserir_login.connect(
            'activate',
            lambda a, *_: a.do_grab_focus(self._inserir_senha))
        # coluna.connect('clicked', self.treeviewcolumn_clicado)
        # coluna2.connect('clicked', self.treeviewcolumn_clicado)
        # coluna3.connect('clicked', self.treeviewcolumn_clicado)
        # coluna4.connect('clicked', self.treeviewcolumn_clicado)

    def verificar_clicado(self, widget):
        senha, senha2 = self._senha.get_text(), self._senha2.get_text()
        senha3 = self._senha3.get_text()
        self._limpar_senhas()
        if all([not self._nv, self._trocar_senha.get_active(), senha]):
            self.trocar_senhas(senha, senha2, senha3)
        elif self._nv:
            self.novo_usuario(senha2, senha3)
        elif all([not self._nv, not self._trocar_senha.get_active(), senha]):
            self.velho_usuario(senha)

    def trocar_senhas(self, senha, senha2, senha3):  # refatorar
        global senhaAdmin
        condicoes = (senha2 == senha3, verificar_admin(senha), senha2, senha3)
        if all(condicoes):
            senhaAdmin = senha
            trocar_senhas(senhaAdmin, senha2)
            senhaAdmin = senha2
            self._nova_janela()
            self._exibir_senhas()
        elif senha2 != senha3:
            self._status.push(0, 'status: senhas desiguais')
        elif not verificar_admin(senha):
            self._status.push(0, 'status: senha admin errada')
            sleep(3)
        elif not all(condicoes[2:]):
            self._status.push(0, 'status: colunas não preenchidas')
        else:
            Gtk.main_quit()

    def novo_usuario(self, senha2, senha3):
        global senhaAdmin
        if all([senha2, senha2 == senha3]):
            sal = salt()
            adminInsert(cripthash(sal + senha2), sal)
            self._nova_janela()
            senhaAdmin = senha2
            self._exibir_senhas()
        else:
            self._status.push(0, 'status: senhas desiguais')

    def velho_usuario(self, senha):
        global senhaAdmin
        if verificar_admin(senha):
            self._nova_janela()
            senhaAdmin = senha
            self._exibir_senhas()
        else:
            self._status.push(0, 'status: senha admin errada')
            sleep(3)

    def _nova_janela(self):
        self._janela1.hide()
        self._janela2.show()

    def _exibir_senhas(self):
        global senhaAdmin
        for usuario in read_data():
            usuario = list(usuario)
            usuario[3] = criptaes(senhaAdmin, usuario[3], True)[5:]
            self._liststore.append(usuario[:4])

    def _enter_senha(self, widget):
        if widget.get_text():
            self._verificar.activate()

    def _trocar_senha_alterado(self, widget):
        self._limpar_senhas()
        self._box_n_u.set_visible(widget.get_active())
        self._verificar.set_label('Trocar senha' if widget.get_active()
                                  else 'Verificar')

    def adicionar_clicado(self, widget):
        global senhaAdmin
        site, login, senha = self._obter_itens()
        if all((site, login, senha)):
            sal = salt()
            data_entry(site, login, criptaes(senhaAdmin, sal + senha), sal)
            numero = getLastId()[0][0]
            self._liststore.append([numero, site, login, senha])
        self._limpar_dados_inserir()
        self._inserir_site.do_grab_focus(self._inserir_site)

    def remover_clicado(self, widget):
        data, item = self._selecao.get_selected()
        if all((data, item)):
            if self._confirmacao2.run() == -5:
                delete_data(data[item][0])
                self._liststore.remove(item)
            self._confirmacao2.hide()

    def remover_tudo_clicado(self, widget):
        if self._confirmacao.run() == -5:
            self._liststore.clear()
            self._selecao = self._treeview.get_selection()
            delete_all_dados()
        self._confirmacao.hide()

    def atualizar_clicado(self, widget):
        global senhaAdmin
        site, login, senha = self._obter_itens()
        data, item = self._selecao.get_selected()
        if all((data, item, site, login, senha)):
            sal = salt()
            update_data(data[item][0], site, login,
                        criptaes(senhaAdmin, sal + senha), sal)
            self._liststore[item] = [data[item][0], site, login, senha]
        self._limpar_dados_inserir()

    def _obter_itens(self):
        site = self._inserir_site.get_text()
        login = self._inserir_login.get_text()
        senha = self._inserir_senha.get_text()
        return site, login, senha

    def _limpar_dados_inserir(self):
        self._inserir_site.set_text('')
        self._inserir_login.set_text('')
        self._inserir_senha.set_text('')

    def _limpar_senhas(self):
        self._senha.set_text('')
        self._senha2.set_text('')
        self._senha3.set_text('')

    def copiar_clicado(self, widget):
        data, item = self._selecao.get_selected()
        copy(self.cb, data[item][3])

    def treeviewcolumn_clicado(self, widget, path, column):
        items = zip(('site', 'login', 'senha'), self._liststore[path][1:])
        items = dict(items)
        if column:
            nome_coluna = column.get_title()
            if nome_coluna == 'site':
                temp = findall(r'^(http|https)://', items[nome_coluna])
                openn(('' if temp else 'https://') + items[nome_coluna])
            elif nome_coluna in items:
                copy(self.cb, items[nome_coluna])
                # exiba uma mensagem na tela copiando
                # f'{nome_coluna} copiado(a) para a área de transferência'
                # refatorar?


def main():
    create_table_admin()
    create_table_dados()
    app = Janela()
    Gtk.main()


# TODO:
# aviso na tela que senha ou login foram copiados
# aviso na tela quando o item não foi selecionado e algum botão foi precionado
# usar a função read_data(login=?) ou remover?
# botão de editar envia os dados para as caixas de texto, lá vc edita?
# self._atualizar.set_use_stock(self._cor_red)   # reutilizar?

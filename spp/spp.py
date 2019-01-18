#!\usr\bin\python3
import gi
from time import sleep
from bancodedados import create_table, read_data
from functions import (
caracteresInvalidos, senha_admin, verificar_admin, criptaes, string,
adicionar, atualizar, deletar, trocar_senha_admin, salt
) # noqa
from random import shuffle
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk  # noqa


def copy(cb, texto):
    cb.set_text(texto, -1)
    cb.store()


def paste():
    # função atoa ou somente para testar com o arquivo testes.py
    return Gtk.Clipboard().wait_for_text()


class Janela:
    def __init__(self):
        # criando objetos.
        self.cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self._senha_admin = ''
        self._nv = False
        self._builder = Gtk.Builder()
        self._liststore = Gtk.ListStore(int, str, str, str)
        renderText = Gtk.CellRendererText()
        self._renderTextEditable = Gtk.CellRendererText()
        self._renderTextEditable2 = Gtk.CellRendererText()
        self._renderTextEditable3 = Gtk.CellRendererText()
        self._coluna = Gtk.TreeViewColumn("id", renderText, text=0)
        coluna2 = Gtk.TreeViewColumn("site", self._renderTextEditable, text=1)
        coluna3 = Gtk.TreeViewColumn("login",
                                     self._renderTextEditable2, text=2)
        coluna4 = Gtk.TreeViewColumn("senha",
                                     self._renderTextEditable3, text=3)

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
        self._senha = self._builder.get_object('senha')
        self._senha2 = self._builder.get_object('senha2')
        self._senha3 = self._builder.get_object('senha3')
        self._adicionar = self._builder.get_object('adicionar')
        self._remover = self._builder.get_object('remover')
        self._atualizar = self._builder.get_object('atualizar')
        self._remover_tudo = self._builder.get_object('remover_tudo')
        self._copiar = self._builder.get_object('copiar')
        self._box_senha = self._builder.get_object('box_senha')

        # configurando.
        self._renderTextEditable.set_property('editable', True)
        self._renderTextEditable2.set_property('editable', True)
        self._renderTextEditable3.set_property('editable', True)
        self._treeview.append_column(self._coluna)
        self._treeview.append_column(coluna2)
        self._treeview.append_column(coluna3)
        self._treeview.append_column(coluna4)
        self._treeview.set_model(self._liststore)
        self._janela1.set_title('Super Protect Password')
        self._janela2.set_title('spp')
        self._status.push(0, 'status:')
        self._cor_ori = self._atualizar.get_use_stock()
        self._cor_red = Gtk.ColorButton('red')
        # self._verificar.set_sensitive(False)
        salSenha = senha_admin()
        if not any(salSenha):
            self._nv = True
            self._builder.get_object('texto_primeira_vez').set_visible(True)
            self._box_n_u.set_visible(True)
            self._box_senha.set_visible(False)
            self._trocar_senha.set_visible(False)

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
        self._atualizar.connect('clicked', self.atualizar_clicado)
        self._remover_tudo.connect('clicked', self.remover_tudo_clicado)
        self._copiar.connect('clicked', self.copiar_clicado)
        self._renderTextEditable.connect("edited", self._alterado)
        self._renderTextEditable2.connect("edited", self._alterado2)
        self._renderTextEditable3.connect("edited", self._alterado3)
        self._selecao = self._treeview.get_selection()

    def verificar_clicado(self, widget):
        senha, senha2 = self._senha.get_text(), self._senha2.get_text()
        senha3 = self._senha3.get_text()
        self._limpar_senhas()
        if self._nv:
            # novo usuário
            if all([senha2 == senha3,
                    not caracteresInvalidos(senha2), senha2]):
                adicionar(senha2, admin=True)
                self._senha_admin = criptaes(string, senha2)
                self._status.push(0, 'status: senha admin criada')
                self._nova_janela()
                self._exibir_senhas(senha2)
            else:
                mensagem = ('status: senhas desiguais ou caracteres inválidos'
                            ': __1, __2 ... __45')
                self._status.set_text(0, mensagem)
        elif all([not self._nv, not self._trocar_senha.get_active(), senha]):
            # velho usuário
            if verificar_admin(senha):
                self._senha_admin = criptaes(string, senha)
                self._nova_janela()
                self._exibir_senhas(senha)
            else:
                self._status.push(0, 'status: senha admin errada')
                sleep(3)
        elif all([not self._nv, self._trocar_senha.get_active(), senha]):
            # trocar senha
            condicoes = [senha2 == senha3, not caracteresInvalidos(senha2),
                         verificar_admin(senha), senha, senha2, senha3]
            if all(condicoes):
                trocar_senha_admin(senha, senha2)
                self._nova_janela()
                self._exibir_senhas(senha2)
            elif senha2 != senha3:
                self._status.push(0, 'status: senhas desiguais')
            elif caracteresInvalidos(senha2):
                self._status.push(0, ('status: caracteres inválidos: __1, __2'
                                      ' ... __45'))
            elif not condicoes[2]:
                self._status.push(0, 'status: senha admin errada')
                sleep(3)
            elif not all(condicoes[3:6]):
                self._status.push(0, 'status: colunas não preenchidas')
            else:
                Gtk.quit()

    def _nova_janela(self):
        self._janela1.hide()
        self._janela2.show()

    def _exibir_senhas(self, senha):
        for usuario in read_data()[1:]:
            usuario = list(usuario)
            su = criptaes(senha, aes_senha=usuario[3])[5:]
            usuario[0], usuario[3] = usuario[0] - 1, su
            self._liststore.append(usuario[:4])
        self.adicionar_clicado(self._adicionar)

    def _enter_senha(self, widget):
        if widget.get_text():
            self._verificar.activate()

    def _trocar_senha_alterado(self, widget):
        self._limpar_senhas()
        self._box_n_u.set_visible(True if widget.get_active() else False)

    def adicionar_clicado(self, widget):
        data = list(map(list, self._liststore))
        if any(data) and any(data[-1][1:]):
            # a linha abaixo funciona mas não como o esperado? verificar
            numero = data[-1][0] + 1 if len(data) else 1
            self._liststore.append([numero, '', '', ''])
        elif not any(data):
            self._liststore.append([1, '', '', ''])
        self._atualizar.set_use_stock(self._cor_red)

    def remover_clicado(self, widget):
        data, item = self._selecao.get_selected()
        data2 = list(map(list, self._liststore))
        if all([data, item]):
            deletar(data[item][0])
            self._liststore.remove(item)
            if not any(data2):
                self.adicionar_clicado(self._adicionar)
        else:
            print('você não selecionou nada')

    def atualizar_clicado(self, widget):
        senha = criptaes(string, aes_senha=self._senha_admin)
        liststore = list(map(list, self._liststore))
        for n, *items in liststore:
            if any(items):
                dados = read_data(id=n+1)
                if any(dados):
                    dados = list(dados[0])
                    dados[3] = criptaes(senha,
                                        aes_senha=dados[3])[5:]
                    if all([items != dados[1:4], n+1 == dados[0]]):
                        atualizar(senha, n, *items, salt())
                else:
                    adicionar(senha, *items)
        if len(liststore) == 1 and not any(liststore[0][1:]):
            for a in read_data()[1:]:
                deletar(a[0]-1)
        self._liststore.clear()
        self._exibir_senhas(senha)
        self._selecao = self._treeview.get_selection()
        self._atualizar.set_use_stock(self._cor_ori)

    def remover_tudo_clicado(self, widget):
        self._liststore.clear()
        self._selecao = self._treeview.get_selection()
        self.adicionar_clicado(self._adicionar)
        self._atualizar.set_use_stock(self._cor_red)

    def _limpar_senhas(self):
        self._senha.set_text('')
        self._senha2.set_text('')
        self._senha3.set_text('')

    def copiar_clicado(self, widget):
        data, item = self._selecao.get_selected()
        copy(self.cb, data[item][3])

    def _alterado(self, widget, path, text):
        self._liststore[path][1] = text

    def _alterado2(self, widget, path, text):
        self._liststore[path][2] = text

    def _alterado3(self, widget, path, text):
        self._liststore[path][3] = text


def main(string=string):
    string = list(string)
    shuffle(string)
    string = ''.join(string)
    create_table()
    app = Janela()  # noqa
    Gtk.main()

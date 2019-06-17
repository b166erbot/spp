import gi
from time import sleep
from .bancodedados.bancodedados import create_table_dados
from .bancodedados.bancodedados import create_table_admin
from .bancodedados.bancodedados import read_data
from .bancodedados.bancodedados import update_data
from .bancodedados.bancodedados import adminQuery
from .bancodedados.bancodedados import adminInsert
from .bancodedados.bancodedados import data_entry
from .bancodedados.bancodedados import delete_data
from .bancodedados.bancodedados import getLastId
from .bancodedados.bancodedados import delete_all_dados
from .functions import salt
from .functions import caracteresInvalidos
from .functions import verificar_admin
from .functions import trocar_senhas
from .functions import criptaes
from random import choices
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk  # noqa

senhaAdmin = ''


def copy(cb, texto):
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
        self._coluna = Gtk.TreeViewColumn("id", renderText, text=0)
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

        # configurando.
        self._treeview.append_column(self._coluna)
        self._treeview.append_column(coluna2)
        self._treeview.append_column(coluna3)
        self._treeview.append_column(coluna4)
        self._treeview.set_model(self._liststore)
        self._janela1.set_title('Super Protect Password')
        self._janela2.set_title('spp')
        self._status.push(0, 'status:')
        # self._verificar.set_sensitive(False)
        if not any(adminQuery()):
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
        self._remover_tudo.connect('clicked', self.remover_tudo_clicado)
        self._copiar.connect('clicked', self.copiar_clicado)
        self._selecao = self._treeview.get_selection()
        self._atualizar.connect('clicked', self.atualizar_clicado)
        self._inserir_senha.connect('activate', self.adicionar_clicado)

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

    def trocar_senhas(self, senha, senha2, senha3):
        global senhaAdmin
        condicoes = (senha2 == senha3, not caracteresInvalidos(senha2),
                     verificar_admin(senha), senha2, senha3)
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
        elif not all(condicoes[3:]):
            self._status.push(0, 'status: colunas não preenchidas')
        else:
            Gtk.quit()

    def novo_usuario(self, senha2, senha3):
        global senhaAdmin
        if all([senha2, senha3, senha2 == senha3,]):
            adminInsert(senha2)
            self._nova_janela()
            senhaAdmin = senha2
            self._exibir_senhas()
        else:
            mensagem = ('status: senhas desiguais ou caracteres inválidos'
                        ': __1, __2 ... __45')
            self._status.push(0, mensagem)

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

    def adicionar_clicado(self, widget):
        global senhaAdmin
        data = list(map(list, self._liststore))
        site, login, senha = self._obter_itens()
        if all([site, login, senha]):
            data_entry(senhaAdmin, site, login, senha)
            numero = getLastId()[0][0]
            self._liststore.append([numero, site, login, senha])
        self._limpar_dados_inserir()
        self._inserir_site.do_grab_focus(self._inserir_site)

        # self._atualizar.set_use_stock(self._cor_red)   # reutilizar?

    def remover_clicado(self, widget):
        data, item = self._selecao.get_selected()
        if all((data, item)):
            delete_data(data[item][0])
            self._liststore.remove(item)
        else:
            print('você não selecionou nada')

    def remover_tudo_clicado(self, widget):
        self._liststore.clear()
        self._selecao = self._treeview.get_selection()
        delete_all_dados()

    def atualizar_clicado(self, widget):
        global senhaAdmin
        site, login, senha = self._obter_itens()
        data, item = self._selecao.get_selected()
        if all((data, item)):
            update_data(senhaAdmin, data[item][0], site, login, senha)
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

    def _alterado(self, widget, path, text):
        self._liststore[path][1] = text

    def _alterado2(self, widget, path, text):
        self._liststore[path][2] = text

    def _alterado3(self, widget, path, text):
        self._liststore[path][3] = text


def main():
    create_table_admin()
    create_table_dados()
    app = Janela()
    Gtk.main()


# TODO: trocar o nome do botão 'verificar' para 'trocar' quando clicado
# em alterar senha.
# TODO: alterar o nome do botão 'verificar' para 'criar' ou algo assim
# quando o usuário for novato.

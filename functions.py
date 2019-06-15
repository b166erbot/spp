from bancodedados.bancodedados import (decorator, data_entry, read_data,
                                       update_data, delete_data)  # noqa
from criptografia.criptografia_simetrica import AESCipher, dicionario
from string import printable as string
from random import choices
from hashlib import sha512


def salt() -> str:
    """
    Função que retorna um sal para ser acrescentado a senha.
    """
    return ''.join(choices(string, k=5))


def caracteresInvalidos(texto: str) -> bool:
    """
    Função que verifica se existe caracteres inválidos no texto.
    """
    for a in dicionario.values():
        if a in texto:
            print(f'\nCaracteres inválidos: ___1, ___2 ... ___45\n')
            return True
    return False


def criptaes(senha_admin, senha: str = False, aes_senha: str = False):
    """
    Função que cifra e descifra uma frase com criptografia aes.
    """
    des_cifrador = AESCipher(senha_admin)
    if senha:
        return des_cifrador.encrypt(senha)
    return des_cifrador.decrypt(aes_senha)


def cripthash(senha):
    """
    Função que retorna a criptografia sha256 da senha.
    """
    password = senha.encode()
    return sha512(password).hexdigest()


def verificar_admin(senha) -> bool:
    """
    Função que lê a senha principal, compara e retorna bool.
    """
    senha_admin_, sal = senha_admin()[0][3:5]
    sha = cripthash(sal + senha)
    return senha_admin_ == sha


@decorator('spp.db')
def senha_admin():
    """
    Função que retorna a senha admin do banco de dados.
    """
    return 'SELECT * FROM dados WHERE id = 1',


def adicionar(senhaAdmin, site='', login='', senha='', admin=False):
    """
    Método que adiciona uma conta do usuário ou a senha admin do programa.
    """
    sal = salt()
    if admin:
        admin_(senhaAdmin)
    else:
        senha = criptaes(senhaAdmin, senha=sal + senha)
        data_entry(login, senha, sal, site)


def atualizar(senhaAdmin, id='', site='', login='',
              senha='', sal='', admin=False):
    """
    Método que atualiza uma conta do banco de dados.
    """
    id = int(id) + 1
    if admin:
        admin_(senhaAdmin, admin)
    else:
        senha = criptaes(senhaAdmin, senha=sal + senha)
        update_data(id, login, senha, sal, site)


def deletar(id):
    """
    Método que remove uma conta do banco de dados.
    """
    id = int(id)+1
    data = read_data(id=id)
    if data:
        delete_data(id)


def admin_(senha, update=False):
    """
    Método que insere ou atualiza a senha admin.
    """
    site = ''
    sal = salt()
    senha = cripthash(sal + senha)
    if update:
        update_data(1, 'admin', senha, sal, site)
    else:
        data_entry('admin', senha, sal, site)


def trocar_senha_admin(senhaAntiga, senhaAtual):
    """
    Método que altera a senha admin do programa.
    """
    atualizar(senhaAtual, 0, admin=True)
    for row in read_data()[1:]:
            sal = salt()
            senha = criptaes(senhaAntiga, aes_senha=row[3])[5:]
            senha = criptaes(senhaAtual, sal + senha)
            update_data(row[0], row[2], senha, sal, row[1])

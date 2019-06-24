from hashlib import sha512
from random import choices
from string import printable as string
from sys import argv

from .bancodedados.bancodedados import (adminQuery, adminUpdate, read_data,
                                        update_data)
from .criptografia.criptografia_simetrica import AESCipher


def salt() -> str:
    """
    Função que retorna um sal para ser acrescentado a senha.
    """
    return ''.join(choices(string, k=5))


def criptaes(senhaAdmin, senha: str, decript: bool = False):
    """
    Função que cifra e descifra uma frase com criptografia aes.
    """
    des_cifrador = AESCipher(senhaAdmin)
    if decript:
        return des_cifrador.decrypt(senha)
    return des_cifrador.encrypt(senha)


def cripthash(senha):
    """
    Função que retorna a criptografia sha256 da senha.
    """
    return sha512(senha.encode()).hexdigest()


def verificar_admin(senha) -> bool:
    """
    Função que lê a senha principal, compara se são iguais e retorna um bool.
    """
    sha_admin, sal = adminQuery()[0]
    sha = cripthash(sal+senha)
    return sha_admin == sha


def trocar_senhas(senhaAdmin, novaSenha):
    """
    Método que altera a senha admin das senhas do programa.
    """
    sal = salt()
    adminUpdate(cripthash(sal + novaSenha), sal)
    for row in read_data():
        row, sal = list(row), salt()
        row[3] = criptaes(senhaAdmin, row[3], True)[5:]  # slice remove o sal
        senhaAdmin, novaSenha = novaSenha, senhaAdmin
        row[3: 5] = criptaes(senhaAdmin, sal + row[3]), sal
        update_data(*row)
        senhaAdmin, novaSenha = novaSenha, senhaAdmin

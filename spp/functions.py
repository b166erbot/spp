from spp.criptografia.criptografia_simetrica import AESCipher, dicionario
from hashlib import sha512
from string import printable as string
from random import choices
from spp.bancodedados import bancodedados
from sys import argv
# bancodedados -> adminQuery, adminUpdate, read_data


def salt() -> str:
    """
    Função que retorna um sal para ser acrescentado a senha.
    """
    return ''.join(choices(string, k=5))


def caracteresInvalidos(texto: str) -> bool:  # refatorar?
    """
    Função que verifica se existe caracteres inválidos no texto.
    """
    for a in dicionario.values():
        if a in texto:
            return True
    return False


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
    sha_admin, sal = bancodedados.adminQuery()[0]
    sha = cripthash(sal+senha)
    return sha_admin == sha


def trocar_senhas(senhaAdmin, novaSenha):
    """
    Método que altera a senha admin das senhas do programa.
    """
    bancodedados.adminUpdate(novaSenha)
    for row in bancodedados.read_data():
        row = list(row)
        senha = criptaes(senhaAdmin, row[3], True)[5:]  # slice remove o sal
        row[3] = senha
        senhaAdmin, novaSenha = novaSenha, senhaAdmin
        row.pop()
        bancodedados.update_data(senhaAdmin, *row)
        senhaAdmin, novaSenha = novaSenha, senhaAdmin


if __name__ == '__main__':
    print(criptaes(1, argv[2], True))

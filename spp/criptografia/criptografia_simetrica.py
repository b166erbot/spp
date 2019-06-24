"Módulo de criptografia simétrica."
# qualquer alteração nesse código, é recomendado criar um novo banco de dados.

import base64
from hashlib import sha256

from Crypto import Random
from Crypto.Cipher import AES

dicionario = {'á': '___0', 'é': '___1', 'í': '___2', 'ó': '___3', 'ú': '___4',
              'Á': '___5', 'É': '___6', 'Í': '___7', 'Ó': '___8', 'Ú': '___9',
              'à': '___10', 'è': '___11', 'ì': '___12', 'ò': '___13',
              'ù': '___14', 'ã': '___15', 'ẽ': '___16', 'ĩ': '___17',
              'õ': '___18', 'ũ': '___19', 'Ã': '___20', 'Ẽ': '___21',
              'Ĩ': '___22', 'Õ': '___23', 'Ũ': '___24', 'â': '___25',
              'ê': '___26', 'î': '___27', 'ô': '___28', 'û': '___29',
              'Â': '___30', 'Ê': '___31', 'Î': '___32', 'Ô': '___33',
              'Û': '___34', 'ä': '___35', 'ë': '___36', 'ï': '___37',
              'ö': '___38', 'ü': '___39', 'Ä': '___40', 'Ë': '___41',
              'Ï': '___42', 'Ö': '___43', 'Ü': '___44', '¨': '___45',
              'ç': '___46', 'Ç': '___47'}

dicionario = dict(list(dicionario.items())[::-1])


def caracteresEspeciais(texto: str, dicionario: dict, reverso=False):
    """
    Função que troca os caracteres acentuados por palavras aceitáveis pela
    encodificação binária.
    """
    if not reverso:
        for i, j in dicionario.items():
            texto = texto.replace(i, j)
        return texto
    elif reverso:
        for i, j in dicionario.items():
            texto = texto.replace(j, i)
        return texto


class AESCipher(object):
    def __init__(self, key):
        self.bs = 32
        self.key = sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = caracteresEspeciais(raw, dicionario)
        raw = self._pad(raw).encode('utf-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        pas = self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
        pas = caracteresEspeciais(pas, dicionario, True)
        return pas

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s)
                                                      % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


def main():
    msg = input('Message...: ')
    pwd = input('Password..: ')

    ciphermsg = AESCipher(pwd).encrypt(msg)
    print('Ciphertext:', ciphermsg)
    print('Deciphertext:', AESCipher(pwd).decrypt(ciphermsg))


if __name__ == '__main__':
    main()

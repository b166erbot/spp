"Módulo de criptografia simétrica."
# qualquer alteração nesse código, é recomendado criar um novo banco de dados.

import base64
from hashlib import sha256

from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):
    def __init__(self, key):
        self.bs = 32
        self.key = sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw).encode('utf-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        pas = self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
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

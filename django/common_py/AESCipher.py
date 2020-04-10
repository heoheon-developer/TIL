from Crypto import Random
from Crypto.Cipher import AES
import sys

import hashlib
import base64

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1:])]

class AESCipher:

    def __init__( self, key ):

        self.key    = hashlib.sha256(self.strToByte(key)).digest()

    def encrpt(self, msg):
        raw         = self.strToByte(pad(msg))
        iv		    = Random.new().read(AES.block_size)
        cipher 	    = AES.new(self.key, AES.MODE_CFB, iv)
        enc_data    = iv + cipher.encrypt(raw)

        return self.bytesToStr(self.byte_base64_encode(enc_data))

    def decrypt(self, msg):
        enc_data = self.byte_base64_decode(self.strToByte(msg))
        iv       = enc_data[:16]
        cipher   = AES.new(self.key, AES.MODE_CFB, iv)
        dec_data = cipher.decrypt(enc_data[16:])

        return unpad(dec_data).decode('utf-8')

    def strToByte(self, str_msg):
        return str_msg.encode('utf8')

    def byte_base64_encode(self, byte_msg):
        return base64.b64encode(byte_msg)

    def bytesToStr(self, bytes_msg):
        return bytes_msg.decode('ascii')

    def byte_base64_decode(self, byte_msg):
        return base64.b64decode(byte_msg)

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
import base64

# 암호화 된 private key 생성
def createPrivateKey():
    private_key = RSA.generate(2048)
    binPrivaKey = private_key.exportKey('DER')

    return bytesToStr(byte_base64_encode(binPrivaKey))

# 암호화
def rsa_enc(privateKey, msg):

    privateKey  = RSA.importKey(byte_base64_decode(strToByte(privateKey)))
    publicKey   = privateKey.publickey()

    encryptor   = PKCS1_OAEP.new(publicKey)
    encdata     = encryptor.encrypt(msg.encode('utf-8'))

    return bytesToStr(byte_base64_encode(encdata))

#복호화
def rsa_desc(key, msg):
    key         = RSA.importKey(byte_base64_decode(strToByte(key)))
    decryptor   = PKCS1_OAEP.new(key)
    decdata     = decryptor.decrypt(byte_base64_decode(strToByte(msg)))

    return byte_decode(decdata)

def byte_base64_encode(byte_msg):
    return base64.b64encode(byte_msg)

def bytesToStr(bytes_msg):
    return bytes_msg.decode('ascii')

def strToByte(str_msg):
    return str_msg.encode('utf-8')

def byte_base64_decode(byte_msg):
    return base64.b64decode(byte_msg)

def byte_decode(byte_msg):
    return byte_msg.decode('utf-8')

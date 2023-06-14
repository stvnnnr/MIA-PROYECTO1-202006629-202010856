from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii

class Encrypt:
    @staticmethod
    def encrypt_message(message, key):
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        padded_message = pad(message.encode(), AES.block_size)
        encrypted_message = cipher.encrypt(padded_message)
        return binascii.hexlify(encrypted_message).decode()
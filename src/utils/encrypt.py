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

# Ejemplo de uso
# mensaje = "panesdulces"

# encrypted_message = encrypt_message(mensaje)
# print("Mensaje encriptado:",encrypted_message)
# salida = "172038F14223CE8E75208821F0897DA5"

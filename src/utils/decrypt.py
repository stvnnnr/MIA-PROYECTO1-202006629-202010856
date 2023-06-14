from Crypto.Cipher import AES
import binascii

class Decrypt:
    
    def decrypt_aes_ecb(ciphertext, key):
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(ciphertext)
        return decrypted

    def hex_to_bytes(hex_string):
        return binascii.unhexlify(hex_string)

    def bytes_to_string(byte_string):
        return byte_string.decode('utf-8')

    def remove_padding(message):
        padding_length = ord(message[-1])
        return message[:-padding_length]

    @staticmethod
    def decrypt_message(ciphertext_hex,key):
        key = key.encode('utf-8')
        ciphertext_bytes = Decrypt.hex_to_bytes(ciphertext_hex)
        decrypted_bytes = Decrypt.decrypt_aes_ecb(ciphertext_bytes, key)
        decrypted_message = Decrypt.bytes_to_string(decrypted_bytes)
        decrypted_message = Decrypt.remove_padding(decrypted_message)
        return decrypted_message
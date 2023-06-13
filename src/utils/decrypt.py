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

# # Ejemplo de uso
# entradaCifrada = "C732CE9C34CF705B16A96471821F8B71C010C9E036D2B2E79D5F815D5EC48F3C11599D1FF76098711CCEFF06EADDE54E24F02B4C7F1B61259ED3AB309BA8B918CBF18370D1463A98F9AF91F004340848C17C13A75BA760D9438D9B2894718C9CC77F6766CEEEC2FADADB735129DABDDBB7A10EA20ACFD3566FB96A595EB87740D5395203CC7B5380F862E2FEC2C59F468DAD8247391D49B1C1B056BD50B56C6F538231D591758B21CAE05C233DFCEB143C7BAF8342F517B3560B511C0C9EFBCDF3D2B4B1BFF527A0CCC10B26AB52D038A8137768D1C2142F59010BE08FE421CB395C51B9CC0947809579D8BA3DDC303B24EE59B8304A53AF487A1D9F53416F57814A00E9732368810C7D6F0BDC34F5EC8A0AABD6A66370382321B222E2CD884E"
# jaja = Decrypt()
# decrypted_message = Decrypt().decrypt_message(entradaCifrada,key="miaproyecto12345")

# print("Mensaje desencriptado:", decrypted_message)
# # salida esperada = "panesdulces"
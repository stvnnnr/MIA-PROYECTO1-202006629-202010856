from src.utils.decrypt import Decrypt
from src.utils.bitacora import write_log
from src.utils.parameters import get_parameters
class ReadUsers:
    @staticmethod
    def readTxtUsers():
        write_log("Output - Lectura de usuarios.")
        usersAux = []
        usersReturn = []
        with open("C:\\Users\\Edwin Sandoval\\Documents\\universidad\\archivos\\Proyecto1\\Archivos\\miausuarios.txt", "r") as archive:
            for line in archive:
                line = line.replace("\n", "")
                usersAux.append(line)
        count = len(usersAux)

        decrypt = Decrypt()
        key = get_parameters()["key"]
        for i in range(0, count, 2):
            decryptPass = decrypt.decrypt_message(usersAux[i+1],key)
            userNew = [usersAux[i], decryptPass]
            print(decryptPass)
            usersReturn.append(userNew)
        return usersReturn


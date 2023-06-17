from src.utils.decrypt import Decrypt
from src.utils.bitacora import write_log
from src.utils.parameters import get_parameters
pathUsers = r"D:\VACAS JUNIO 2023\Archivos\
MIA_PROYECTO1_202006629_202010856\Archivos\miausuarios.txt"
class ReadUsers:
    @staticmethod
    def readTxtUsers():
        write_log("Output - Lectura de usuarios.")
        usersAux = []
        usersReturn = []
        with open(pathUsers, "r") as archive:
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


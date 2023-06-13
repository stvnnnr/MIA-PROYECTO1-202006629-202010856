# from decrypt import Decrypt

class ReadUsers:
    @staticmethod
    def readTxtUsers():
        usersAux = []
        usersReturn = []
        with open("..\Archivos\miausuarios.txt", "r") as archive:
            for line in archive:
                line = line.replace("\n", "")
                usersAux.append(line)
        count = len(usersAux)

        # decrypt = Decrypt()
        key = "miaproyecto12345"
        for i in range(0, count, 2):
            # decryptPass = decrypt.decrypt_message(usersAux[i+1],key)
            decryptPass = usersAux[i+1]
            userNew = [usersAux[i], decryptPass]
            usersReturn.append(userNew)
        return usersReturn

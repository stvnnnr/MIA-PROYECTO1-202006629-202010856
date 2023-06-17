import os
from datetime import datetime
from src.utils.encrypt import Encrypt
from src.utils.parameters import get_parameters
@staticmethod
def write_log(message):
    encrypt_log = get_parameters()["encrypt_log"]
    key = get_parameters()["key"]
    path = create_folder()
    with open(f'{path}\log.txt' , "a") as file:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if encrypt_log:
            encrypt = Encrypt()
            message = f'{date} - {message}'
            message = encrypt.encrypt_message(message, key)
        file.write(f'{message}\n')

def create_folder():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    path = f'D:\VACAS JUNIO 2023\Archivos\MIA_PROYECTO1_202006629_202010856\Archivos\logs\{year}\{month}\{day}'
    if not os.path.exists(path):
        os.makedirs(path)
    return path
from pydrive2.auth import GoogleAuth
from src.utils.bitacora import write_log

write_log("Output - Inicio de google drive.")
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

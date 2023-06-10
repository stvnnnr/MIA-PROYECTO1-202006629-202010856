import os
import re
import shutil
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError

directorio_credenciales = 'credentials_module.json' 


#--------------------------------------------Create----------------------------
def createLocal(name, body, path):
    if "\"" in name:
        name = name.replace("\"", "")
    pathEntrada = path
    if "\"" in pathEntrada:
        pathEntrada = pathEntrada.replace("\"", "")
    pathEntrada = pathEntrada.replace("/", "\\")
    ruta_actual = "d:\VACAS JUNIO 2023\Archivos\proyectoCopia\src"
    ruta_nueva_carpeta = os.path.join(ruta_actual + pathEntrada)

    try:
        if not os.path.exists(ruta_nueva_carpeta):
            os.makedirs(ruta_nueva_carpeta, exist_ok=True)
            # print(f"Carpeta '{pathEntrada}' creada correctamente en '{ruta_actual}'.")
        # else:
            # print(f"La carpeta '{pathEntrada}' ya existe en '{ruta_actual}'.")
    except:
        print("No se pudo crear la carpeta local")
    ruta_nueva_carpeta = ruta_nueva_carpeta + name

    try:
        with open(ruta_nueva_carpeta, "w") as archivo:
            archivo.write(body)
        print(f"Create -name:'{name}' creado con exito.")
    except IOError:
        print("Error al crear el archivo.")

def createCloud(name, body, path):
    pathNuevo = path[1:]
    pathNuevo = pathNuevo[:-1]
    if "\"" in name:
        name = name.replace("\"", "")
    if "\"" in pathNuevo:
        pathNuevo = pathNuevo.replace("\"", "")
    listPath = pathNuevo.split("/")
    currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
    for x in listPath:
        aux = createFile_cloud(x, currentId)
        currentId = aux
    createTxt_Cloud(name, body, currentId)
    print(f"Create -name:'{name}' creado con exito.")


#--------------------------------------------Delete----------------------------

def deleteLocal(path, name=None):
    path = path.replace("\"","")
    ruta_actual = r"d:\VACAS JUNIO 2023\Archivos\proyectoCopia\src"
    ruta_nueva_carpeta = os.path.join(ruta_actual+path.replace("/", "\\"))
    if name:
        ruta_completa = os.path.join(ruta_nueva_carpeta, name)
        if os.path.exists(ruta_completa):
            if os.path.isfile(ruta_completa):
                os.remove(ruta_completa)
                print(f"Delete -name:'{name}'.txt eliminado con exito.")
            else:
                print(f"{name} en la ruta {path} no es un archivo válido.")
        else:
            print(f"No se encontró el archivo {name} en la ruta {path}.")
    else:
        if os.path.exists(ruta_nueva_carpeta):
            if os.path.isdir(ruta_nueva_carpeta):
                shutil.rmtree(ruta_nueva_carpeta)
                print(f"Delete -name:'{path}' eliminado con exito.")
            else:
                print(f"{path} no es una carpeta válida.")
        else:
            print(f"No se encontró la carpeta en la ruta {path}.")

def deleteCloud(path, name=None):
    pathNuevo = path[1:]
    pathNuevo = pathNuevo[:-1]
    if "\"" in pathNuevo:
        pathNuevo = pathNuevo.replace("\"", "")
    listPath = pathNuevo.split("/")
    currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
    for x in listPath:
        aux = searchFile(x, currentId)
        currentId = aux
    if name is not None:
        if "\"" in name:
            name = name.replace("\"", "")
        name = name.replace(".txt","")
        print(name)
        print(currentId)
        aux = searchTxt(name, currentId)
        currentId = aux
        deleteFile(currentId)
        print(f"Delete -name:'{name}'.txt eliminado con exito.")
    else:
        deleteFile(currentId)
        print(f"Delete -name:'{path}' eliminado con exito.")


#----------------------------------------------Metodos de cloud----------------------------------------------------

def login():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales

@staticmethod
def createFile_cloud(query, parent_folder_id):
    name = query
    resultado = ""
    credenciales = login()
    query = f"title contains '{query}' and mimeType = 'application/vnd.google-apps.folder' and '{parent_folder_id}' in parents"
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    
    for f in lista_archivos:
        if f['labels']['trashed'] == 'true':
            f.Delete()
            continue
        resultado = f['id']
        return resultado

    folder = credenciales.CreateFile({'title': name,
                                      'mimeType': 'application/vnd.google-apps.folder',
                                      'parents': [{"kind": "drive#fileLink",
                                                   "id": parent_folder_id}]})
    folder.Upload()
    resultado = folder['id']
    return resultado

@staticmethod
def searchFile(query, parent_folder_id):
    name = query
    resultado = ""
    credenciales = login()
    query = f"title contains '{query}' and mimeType = 'application/vnd.google-apps.folder' and '{parent_folder_id}' in parents"
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    
    for f in lista_archivos:
        if f['labels']['trashed'] == 'true':
            continue
        resultado = f['id']
        return resultado
    return resultado

@staticmethod
def searchTxt(query, parent_folder_id):
    name = query
    resultado = ""
    credenciales = login()
    query = f"title contains '{query}' and '{parent_folder_id}' in parents"
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    
    for f in lista_archivos:
        if f['labels']['trashed'] == 'true':
            continue
        resultado = f['id']
        return resultado
    return resultado

@staticmethod
def createTxt_Cloud(name, body, id_folder):
    credenciales = login()
    file_list = credenciales.ListFile(
        {'q': f"title='{name}' and '{id_folder}' in parents"}).GetList()

    if len(file_list) == 0:
        archivo = credenciales.CreateFile(
            {'title': name, 'parents': [{"kind": "drive#fileLink", "id": id_folder}]})
    else:
        archivo = file_list[0]

    archivo.SetContentString(body)
    archivo.Upload()

@staticmethod
def deleteFile(id_archivo):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_archivo})
    archivo.Delete()



# Ejemplo de uso

# createLocal("prueba.txt","hola","/\"juanito 2\"/\"perrito 3\"/")
# deleteLocal("/\"juanito 2\"/")
# createCloud("hola.txt","prueba prueba editada","/carpeta1/")
# deleteCloud("/carpeta1/")
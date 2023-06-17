import os
import re
import shutil
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from src.utils.parameters import get_parameters
from src.utils.parameters import update_parameters

directorio_credenciales = r"D:\VACAS JUNIO 2023\Archivos\proyect\src\storage\credentials_module.json"

myPath = (
    r"D:\VACAS JUNIO 2023\Archivos\proyect\Archivos"
    # r"C:\Users\Edwin Sandoval\Documents\universidad\archivos\Proyecto1\Archivos\local"
)

pathDownload = (
    r"D:\VACAS JUNIO 2023\Archivos\proyect\Archivos\Archivos"
)

def execute(command, parameters):
    try:
        for key in parameters:
            parameters[key] = parameters[key].strip()
        function = globals().get(command)
        response = function(**parameters)

        parameters = get_parameters()
        if parameters["init_exec"]:
            parameters["count_exec_nube"] = parameters["count_exec_nube"] + 1
        update_parameters(parameters)

        return response
    except:
        print("Hubo un error, consulta al admin")


def create(name, path, body):
    nameEntrada = name
    pathNuevo = path[1:]
    pathNuevo = pathNuevo[:-1]
    if '"' in nameEntrada:
        nameEntrada = nameEntrada.replace('"', "")
    if '"' in pathNuevo:
        pathNuevo = pathNuevo.replace('"', "")
    listPath = pathNuevo.split("/")
    currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
    for x in listPath:
        aux = createFile_cloud(x, currentId)
        currentId = aux
    flag = createTxt_Cloud(nameEntrada, body, currentId)
    if flag:
        return {
            "msg": f"- Archivo creado exitosamente: name='{name}', path='{path}', body='{body}'",
            "status": "success"
        }
    else:
        return {
            "msg": f"- Error al crear el archivo: name='{name}', path='{path}', body='{body}' ya existe",
            "status": "error"
        }


def delete(path, name=None):
    pathNuevo = path[1:]
    pathNuevo = pathNuevo[:-1]
    if '"' in pathNuevo:
        pathNuevo = pathNuevo.replace('"', "")
    listPath = pathNuevo.split("/")
    currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
    for x in listPath:
        aux = searchFile(x, currentId)
        currentId = aux
    if currentId == "":
        return {
                "msg": f"- No se encontró el archivo en la ruta {path}.",
                "status": "error"
            }
    if name is not None:
        nameEntrada = name
        if '"' in nameEntrada:
            nameEntrada = nameEntrada.replace('"', "")
        aux = searchTxt(nameEntrada, currentId)
        currentId = aux
        if currentId != "":
            deleteFile(currentId)
            return {
                "msg": f"- Delete -name:'{name}' eliminado con exito.",
                "status": "success"
            }
        else:
            return {
                "msg": f"- No se encontró el archivo {name} en la ruta{path}.",
                "status": "error"
            }
    else:
        deleteFile(currentId)
        return {
            "msg": f"- Delete -path:'{path}' eliminado con exito.",
            "status": "success"
        }


def copy(from_path, to):
    sou = from_path
    des = to
    if '"' in sou:
        sou = sou.replace('"', "")
    if "/" in sou:
        sou = sou.replace("/", "\\")
    if '"' in des:
        des = des.replace('"', "")
    if "/" in des:
        des = des.replace("/", "\\")
    sou = sou[1:]
    des = des[1:]
    des = des[:-1]
    listPath = des.split("\\")
    currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
    for x in listPath:
        aux = searchFile(x, currentId)
        currentId = aux
    if currentId == "":
        return {"msg": f"- ruta -to:'{to}' no existe.", "status": "error"}
    idTo = currentId
    if sou[-1] == "\\":
        sou = sou[:-1]
        listPath = sou.split("\\")
        currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
        for x in listPath:
            aux = searchFile(x, currentId)
            currentId = aux
        if currentId == "":
            return {"msg": f"- ruta -from:'{from_path}' no existe.", "status": "error"}
        idFrom = currentId
        copyFile(idFrom, idTo)
        return {
            "msg": f"- Copy -from:'{from_path}' -to: '{to}' copiado con exito.",
            "status": "success"
        }
    else:
        listPath = sou.split("\\")
        fileActual = listPath[-1]#archivo
        listPath = listPath[:-1]#su ruta
        currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
        for x in listPath:
            aux = searchFile(x, currentId)
            currentId = aux
        if currentId != "":
            aux = searchTxt(fileActual, currentId)#revisa si existe e archivo en la carpeta from
            ss = searchTxt(fileActual, idTo)#revisa si existe archivo en la carpeta del to
            if ss == "":
                if aux == "":
                    return {"msg": f"- archivo -from:'{from_path}' no existe.", "status": "error"}
                idFrom = aux
                copyTxt(idFrom, idTo)
                return {
                    "msg": f"- Copy -from:'{from_path}' -to: '{to}' copiado con exito.",
                    "status": "success"
                }
            else:
                return { "msg": f"- No se pudo copiar -from:'{from_path}' -to: '{to}' el archivo ya existe.", "status": "error" }
        else:
            return {"msg": f"- ruta -from:'{from_path}' no existe.", "status": "error"}


def transfer(from_path, to, mode):
    if mode == "local":
        return {
                    "msg": "- No es valido el -mode:{} en la configuracion actual".format(mode),
                    "status": "error"
                }
    elif mode == "cloud":
        sou = from_path
        des = to
        if '"' in sou:
            sou = sou.replace('"', "")
        if "/" in sou:
            sou = sou.replace("/", "\\")
        if '"' in des:
            des = des.replace('"', "")
        if "/" in des:
            des = des.replace("/", "\\")
        sou = sou[1:]
        des = des[1:]
        des = des[:-1]
        listPath = des.split("\\")
        currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
        for x in listPath:
            aux = searchFile(x, currentId)
            currentId = aux
        if currentId == "":
            return {"msg": f"- ruta -to:'{to}' no existe.", "status": "error"}
        idTo = currentId
        if sou[-1] == "\\":
            sou = sou[:-1]
            listPath = sou.split("\\")
            currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
            for x in listPath:
                aux = searchFile(x, currentId)
                currentId = aux
            if currentId == "":
                return {"msg": f"- ruta -from:'{sou}' no existe.", "status": "error"}
            idFrom = currentId
            moveFolder2(idFrom, idTo)
            return { "msg": f"- Transfer -from:'{sou}' -to: '{des}' movido con exito.", "status": "success" }
        else:
            listPath = sou.split("\\")
            fileActual = listPath[-1]#archivo
            listPath = listPath[:-1]#su ruta
            currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
            for x in listPath:
                aux = searchFile(x, currentId)
                currentId = aux
            aux = searchTxt(fileActual, currentId)
            if aux == "":
                return { "msg": f"- ruta -from:'{from_path}' no existe.", "status": "error" }
            idFrom = aux
            moveFile2(idFrom, idTo)
            return { "msg": f"- Transfer -from:'{from_path}' -to: '{to}' movido con exito.", "status": "success" }
    else:
        return { "msg": f"- mode:'{mode}' no es valido.", "status": "error" }


def rename(path, name):
    sou = path
    des = name
    if '"' in sou:
        sou = sou.replace('"', "")
    if '"' in des:
        des = des.replace('"', "")
    if "/" in sou:
        sou = sou.replace("/", "\\")
    sou = sou[1:]
    if (".txt") in sou:
        listPath = sou.split("\\")
        finalTxt = listPath[-1]
        listPath = listPath[:-1]
        currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
        for x in listPath:
            aux = searchFile(x, currentId)
            currentId = aux
        if currentId == "":
            return { "msg": f"- ruta -path:'{sou}' no existe.", "status": "error" }
        pathFrom = currentId
        x = searchTxt(finalTxt, pathFrom)
        if x == "":
            return { "msg": f"- ruta -path:'{sou}' no existe.", "status": "error" }
        else:
            renameTxt(x, des)
            return { "msg": f"- Rename -path:'{sou}' con '{des}' renombrado con exito.", "status": "success" }
    else:
        sou = sou[:-1]
        listPath = sou.split("\\")
        currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
        for x in listPath:
            aux = searchFile(x, currentId)
            currentId = aux
        if currentId == "":
            return { "msg": f"- ruta -path:'{sou}' no existe.", "status": "error" }
        pathFrom = currentId
        renameFolder(pathFrom, des)
        return { "msg": f"- Rename -path:'{sou}' con '{des}' renombrado con exito.", "status": "success" }


def modify(path, body):
    sou = path
    if '"' in sou:
        sou = sou.replace('"', "")
    if "/" in sou:
        sou = sou.replace("/", "\\")
    sou = sou[1:]
    if (".txt") in sou:
        listPath = sou.split("\\")
        finalTxt = listPath[-1]
        listPath = listPath[:-1]
        currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
        for x in listPath:
            aux = searchFile(x, currentId)
            currentId = aux
        if currentId == "":
            return { "msg": f"- ruta -path:'{path}' no existe.", "status": "error" }
        pathFrom = currentId
        x = searchTxt(finalTxt, pathFrom)
        if x == "":
            return { "msg": f"- archivo -path:'{path}' no existe.", "status": "error" }
        else:
            modifyTxt(x, body)
            return { "msg": f"- Modify -path:'{path}' con '{body}' modificado con exito.", "status": "success" }
    else:
        return { "msg": f"-ruta -path:'{path}' no existe es un archivo", "status": "error" }


def add(path, body):
    sou = path
    if '"' in sou:
        sou = sou.replace('"', "")
    if "/" in sou:
        sou = sou.replace("/", "\\")
    sou = sou[1:]
    if (".txt") in sou:
        listPath = sou.split("\\")
        finalTxt = listPath[-1]
        listPath = listPath[:-1]
        currentId = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
        for x in listPath:
            aux = searchFile(x, currentId)
            currentId = aux
        if currentId == "":
            return { "msg": f"- ruta -path:'{path}' no existe.", "status": "error" }
        pathFrom = currentId
        x = searchTxt(finalTxt, pathFrom)
        if x == "":
            return { "msg": f"- archivo -path:'{path}' no existe.", "status": "error" }
        else:
            addTxt(x, body)
            return { "msg": f"- Add -path:'{path}' con '{body}' agregado con exito.", "status": "success" }
    else:
        return { "msg": f"- ruta -path:'{path}' no es un archivo valido.", "status": "error" }


def backup():
    id_drive = "1eLTdiEeaTRGtNSQbkZ73SZPL_JOYcaen"
    ruta_descarga = myPath
    ruta_copia = pathDownload
    downloadFile(id_drive,ruta_descarga)
    rutaFrom = ruta_copia
    rutaTo = ruta_descarga
    try:
        if os.path.exists(rutaFrom):
            if os.path.isfile(rutaFrom):
                filename = os.path.basename(rutaFrom)
                rutaNew = os.path.join(rutaTo + filename)
                if os.path.exists(rutaTo):
                    if os.path.exists(rutaNew):
                        filename = os.path.basename(rutaFrom)
                        filename_without_extension, file_extension = os.path.splitext(filename)
                        i = 1
                        while os.path.exists(os.path.join(rutaTo + f"{filename_without_extension}({i}){file_extension}")):
                            i += 1
                        new_filename = f"{filename_without_extension}({i}){file_extension}"
                        new_filepath = os.path.join(rutaTo +"\\"+ new_filename)
                        shutil.move(rutaFrom, new_filepath)
                        shutil.rmtree(ruta_copia)
                        return { "msg": f"- Backup cloud to local realizado con exito.", "status": "success" }
                    else:
                        shutil.move(rutaFrom, rutaTo)
                        shutil.rmtree(ruta_copia)
                        return { "msg": f"- Backup cloud to local realizado con exito.", "status": "success" }
                else:
                    return { "msg": f"- No se pudo realizar Backup cloud to local.", "status": "error" }
            elif os.path.isdir(rutaFrom):
                for item in os.listdir(rutaFrom):
                    source = os.path.join(rutaFrom +"\\"+ item)
                    rutaNew = os.path.join(rutaTo +"\\"+ item)
                    if os.path.exists(rutaTo):
                        if os.path.exists(rutaNew):
                            if os.path.isfile(source):
                                filename = os.path.basename(source)
                                (
                                    filename_without_extension,
                                    file_extension,
                                ) = os.path.splitext(filename)
                                i = 1
                                while os.path.exists(
                                    os.path.join(
                                        rutaTo
                                        + f"{filename_without_extension}({i}){file_extension}"
                                    )
                                ):
                                    i += 1
                                new_filename = (
                                    f"{filename_without_extension}({i}){file_extension}"
                                )
                                new_filepath = os.path.join(rutaTo +"\\"+ new_filename)
                                shutil.move(source, new_filepath)
                            elif os.path.isdir(source):
                                foldername = os.path.basename(os.path.normpath(source))
                                i = 1
                                while os.path.exists(
                                    os.path.join(rutaTo + f"{foldername}({i})")
                                ):
                                    i += 1
                                new_foldername = f"{foldername}({i})"
                                new_folderpath = os.path.join(rutaTo +"\\"+ new_foldername)
                                shutil.move(source, new_folderpath)
                        else:
                            shutil.move(source, rutaTo)
                    else:
                        return { "msg": f"- No se pudo realizar Backup cloud to local.", "status": "error" }
                shutil.rmtree(ruta_copia)
                return { "msg": f"- Backup cloud to local realizado con exito.", "status": "success" }
        else:
            return { "msg": f"- No se pudo realizar Backup cloud to local.", "status": "error" }
    except Exception as e:
        return { "msg": f"- No se pudo realizar Backup cloud to local.", "status": "error" }


def backup_with_path(path):
    print("Function: backup_with_path")
    print("Parameters: path={}".format(path))


# Metodos auxiliares

@staticmethod
def downloadFile(folder_id, destination_path):
    credenciales = login()
    folder = credenciales.CreateFile({'id': folder_id})
    folder_title = folder['title']
    folder_path = os.path.join(destination_path, folder_title)
    os.makedirs(folder_path, exist_ok=True)
    file_list = credenciales.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    for file in file_list:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            downloadFile(file['id'], folder_path)
        else:
            file_path = os.path.join(folder_path, file['title'])
            file.GetContentFile(file_path)

@staticmethod
def login():
    GoogleAuth.DEFAULT_SETTINGS["client_config_file"] = directorio_credenciales
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
    lista_archivos = credenciales.ListFile({"q": query}).GetList()
    for f in lista_archivos:
        if f["labels"]["trashed"] == "true":
            f.Delete()
            continue
        resultado = f["id"]
        return resultado
    folder = credenciales.CreateFile(
        {
            "title": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [{"kind": "drive#fileLink", "id": parent_folder_id}],
        }
    )
    folder.Upload()
    resultado = folder["id"]
    return resultado

@staticmethod
def createTxt_Cloud(name, body, id_folder):
    credenciales = login()
    file_list = credenciales.ListFile(
        {"q": f"title='{name}' and '{id_folder}' in parents"}
    ).GetList()
    if len(file_list) == 0:
        archivo = credenciales.CreateFile(
            {"title": name, "parents": [{"kind": "drive#fileLink", "id": id_folder}]}
        )
        archivo.SetContentString(body)
        archivo.Upload()
        return True
    else:
        return False

@staticmethod
def searchFile(query, parent_folder_id):
    resultado = ""
    credenciales = login()
    query = f"title contains '{query}' and mimeType = 'application/vnd.google-apps.folder' and '{parent_folder_id}' in parents"
    lista_archivos = credenciales.ListFile({"q": query}).GetList()
    for f in lista_archivos:
        if f["labels"]["trashed"] == "true":
            continue
        resultado = f["id"]
        return resultado
    return resultado

@staticmethod
def searchTxt(query, parent_folder_id):
    name = query
    resultado = ""
    credenciales = login()
    query = f"title = '{name}' and '{parent_folder_id}' in parents"
    lista_archivos = credenciales.ListFile({"q": query}).GetList()
    for f in lista_archivos:
        if f["labels"]["trashed"] == "true":
            continue
        if f["title"] == name:
            resultado = f["id"]
            return resultado
    return resultado

@staticmethod
def deleteFile(id_archivo):
    credenciales = login()
    archivo = credenciales.CreateFile({"id": id_archivo})
    archivo.Delete()

@staticmethod
def copyFile(idFrom, idTo):
    credenciales = login()
    folder_content = credenciales.ListFile(
        {"q": f"'{idFrom}' in parents and trashed=false"}
    ).GetList()
    for item in folder_content:
        x = item["title"]
        if item["mimeType"] == "application/vnd.google-apps.folder":
            ss = searchFile(x, idTo)
            if ss == "":
                copyFolder(item["id"], idTo)
        else:
            x = x + ".txt"
            ss = searchTxt(x, idTo)
            if ss == "":
                copyTxt(item["id"], idTo)

@staticmethod
def copyTxt(idFrom, idTo):
    credenciales = login()
    folder = credenciales.CreateFile({"id": idFrom})
    folder_title = folder["title"]
    new_folder = credenciales.CreateFile(
        {"title": folder_title, "parents": [{"id": idTo}]}
    )
    contenido = folder.GetContentString()
    new_folder.SetContentString(contenido)
    new_folder.Upload()

@staticmethod
def copyFolder(folder_id, destination_folder_id):
    credenciales = login()
    folder = credenciales.CreateFile({"id": folder_id})
    folder_title = folder["title"]
    new_folder = credenciales.CreateFile(
        {
            "title": folder_title,
            "parents": [{"id": destination_folder_id}],
            "mimeType": "application/vnd.google-apps.folder",
        }
    )
    new_folder.Upload()
    folder_content = credenciales.ListFile(
        {"q": f"'{folder_id}' in parents and trashed=false"}
    ).GetList()
    for item in folder_content:
        if item["mimeType"] == "application/vnd.google-apps.folder":
            copyFolder(item["id"], new_folder["id"])
        else:
            copyTxt(item["id"], new_folder["id"])

@staticmethod
def moveFile2(id_archivo, id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({"id": id_archivo})
    propiedades_ocultas = archivo["parents"]
    archivo["parents"] = [
        {
            "isRoot": False,
            "kind": "drive#parentReference",
            "id": id_folder,
            "selfLink": "https://www.googleapis.com/drive/v2/files/"
            + id_archivo
            + "/parents/"
            + id_folder,
            "parentLink": "https://www.googleapis.com/drive/v2/files/" + id_folder,
        }
    ]
    file_name = archivo["title"]
    existing_files = credenciales.ListFile(
        {"q": f"'{id_folder}' in parents and title='{file_name}'", "spaces": "drive"}
    ).GetList()
    if existing_files:
        index = 1
        while True:
            if ".txt" in file_name:
                file_extension = file_name.split('.')[-1]
                file_name_without_extension = '.'.join(file_name.split('.')[:-1])
                new_file_name = f"{file_name_without_extension}({index}).{file_extension}"
            else:
                new_file_name = f"{file_name}({index})"
            existing_files = credenciales.ListFile(
                {
                    "q": f"'{id_folder}' in parents and title='{new_file_name}'",
                    "spaces": "drive",
                }
            ).GetList()
            if not existing_files:
                break
            index += 1
        archivo["title"] = new_file_name
    archivo.Upload(param={"supportsTeamDrives": True})

@staticmethod
def moveFolder2(idFrom, idTo):
    credenciales = login()
    folder_content = credenciales.ListFile(
        {"q": f"'{idFrom}' in parents and trashed=false"}
    ).GetList()
    for item in folder_content:
        moveFile2(item["id"], idTo)

@staticmethod
def renameTxt(idFrom, name):
    credenciales = login()
    archivo = credenciales.CreateFile({"id": idFrom})
    archivo["title"] = name
    archivo.Upload(param={"supportsTeamDrives": True})

@staticmethod
def renameFolder(id_carpeta, nuevo_nombre):
    credenciales = login()
    carpeta = credenciales.CreateFile({"id": id_carpeta})
    carpeta["title"] = nuevo_nombre
    carpeta.Upload(param={"supportsTeamDrives": True})


@staticmethod
def modifyTxt(idFrom, content):
    credenciales = login()
    archivo = credenciales.CreateFile({"id": idFrom})
    archivo.SetContentString(content)
    archivo.Upload()


@staticmethod
def addTxt(idFrom, content):
    credenciales = login()
    archivo = credenciales.CreateFile({"id": idFrom})
    archivo.FetchContent()
    contenido_actual = archivo.GetContentString()
    nuevo_contenido = contenido_actual + str(content)
    archivo.SetContentString(nuevo_contenido)
    archivo.Upload()

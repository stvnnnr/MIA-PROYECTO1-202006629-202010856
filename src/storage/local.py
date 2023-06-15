import os
import shutil
from src.utils.parameters import get_parameters
from src.utils.parameters import update_parameters

myPath = r"d:\VACAS JUNIO 2023\Archivos\proyectoCopia\src"

def execute(command, parameters):
    function = globals().get(command)
    response = function(**parameters)
    
    parameters = get_parameters()
    if parameters["init_exec"]:
        parameters["count_exec_local"] = parameters["count_exec_local"] + 1
    update_parameters(parameters)
    return response

def configure(type, encrypt_log, encrypt_read, key=None):
    bool_encrypt_log = bool(encrypt_log.lower() == 'true')
    bool_encrypt_read = bool(encrypt_read.lower() == 'true')
    parameters = get_parameters()
    parameters["encrypt_log"] = bool_encrypt_log
    parameters["encrypt_read"] = bool_encrypt_read
    type = type.replace(" ", "")
    parameters["type"] = type
    if key != None:
        parameters["key"] = key

    update_parameters(parameters)

    return "Configuración exitosa: encrypt_log={}, encrypt_read={}, type={}, key={}".format(bool_encrypt_log, bool_encrypt_read, type, key)       

def create(name, path, body):
    nameEntrada = name
    if "\"" in name:
        name = name.replace("\"", "")
    pathEntrada = path
    if "\"" in pathEntrada:
        pathEntrada = pathEntrada.replace("\"", "")
    if "/" in pathEntrada:
        pathEntrada = pathEntrada.replace("/", "\\")
    ruta_actual = myPath
    ruta_nueva_carpeta = os.path.join(ruta_actual + pathEntrada)
    try:
        if not os.path.exists(ruta_nueva_carpeta):
            os.makedirs(ruta_nueva_carpeta, exist_ok=True)
    except:
        return (f"No se pudo crear la carpeta '{path}'")
    ruta_nueva_carpeta = ruta_nueva_carpeta + name
    try:
        if not os.path.exists(ruta_nueva_carpeta):
            with open(ruta_nueva_carpeta, "w") as archivo:
                archivo.write(body)
                archivo.close()
            return(f"Create -name:'{nameEntrada}' creado con exito en -path:'{path}'.")
        else:
            return (f"No se pudo crear el archivo'{nameEntrada}' porque ya existe")
    except IOError:
        return (f"No se pudo crear el archivo'{nameEntrada}'")
    # print("Parameters: name={}, path={}, body={}".format(name, path, body))
    # return "Archivo creado exitosamente: name={}, path={}, body={}".format(name, path, body)

def delete(path, name=None):
    pathEntrada = path
    if "\"" in path:
        path = path.replace("\"","")
    ruta_actual = myPath
    ruta_nueva_carpeta = os.path.join(ruta_actual+path.replace("/", "\\"))
    if name:
        ruta_completa = os.path.join(ruta_nueva_carpeta, name)
        if os.path.exists(ruta_completa):
            if os.path.isfile(ruta_completa):
                #Hacer pregunta si está seguro
                os.remove(ruta_completa)
                return(f"Delete -name:'{name}'.txt eliminado con exito.")
            else:
                return(f"{name}.txt en la ruta {pathEntrada} no es un archivo válido.")
        else:
            return(f"No se encontró el archivo {name}.txt en la ruta {pathEntrada}.")
    else:
        if os.path.exists(ruta_nueva_carpeta):
            if os.path.isdir(ruta_nueva_carpeta):
                #Hacer pregunta si está seguro
                shutil.rmtree(ruta_nueva_carpeta)
                return(f"Delete -name:'{pathEntrada}' eliminado con exito.")
            else:
                return(f"{pathEntrada} no es una carpeta válida.")
        else:
            return(f"No se encontró la carpeta en la ruta {pathEntrada}.")
    # print("Function: delete")
    # print("Parameters: path={}, name={}".format(path, name))

def copy(from_path, to):
    sou = from_path
    des = to
    ruta_actual = myPath
    if "\"" in from_path:
        from_path = from_path.replace("\"", "")
    if "/" in from_path:
        from_path = from_path.replace("/", "\\")
    if "\"" in to:
        to = to.replace("\"", "")
    if "/" in to:
        to = to.replace("/", "\\")
    rutaFrom = os.path.join(ruta_actual + from_path)
    rutaTo = os.path.join(ruta_actual + to)
    try:
        if os.path.exists(rutaFrom):
            if os.path.isfile(rutaFrom):
                filename = os.path.basename(rutaFrom)
                rutaNew = rutaTo+filename
                if os.path.exists(rutaNew):
                    return(f"El archivo '{sou}' ya existe en la ruta '{des}'.")
                else:
                    shutil.copy2(rutaFrom, rutaTo)
                    return(f"Copy -from:'{sou}' -to: '{des}' copiado con éxito.")
            elif os.path.isdir(rutaFrom):
                isFile(rutaFrom,rutaTo)
                return(f"Copy -from:'{sou}' -to: '{des}' copiado lo posible.")
        else:
            return(f"La ruta'{sou}' no existe.")
    except Exception as e:
        return(f"No se pudo copiar -from:'{sou}' -to: '{des}'")
    # print("Function: copy")
    # print("Parameters: from_path={}, to={}".format(from_path, to))

def transfer(from_path, to, mode):
    if mode == "cloud":
        return(f"No se pudo mover porque no es el ambito esperado")
    sou = from_path
    des = to
    ruta_actual = myPath
    if "\"" in from_path:
        from_path = from_path.replace("\"", "")
    if "/" in from_path:
        from_path = from_path.replace("/", "\\")
    if "\"" in to:
        to = to.replace("\"", "")
    if "/" in to:
        to = to.replace("/", "\\")
    rutaFrom = os.path.join(ruta_actual + from_path)
    rutaTo = os.path.join(ruta_actual + to)
    try:
        if os.path.exists(rutaFrom):
            if os.path.isfile(rutaFrom):
                filename = os.path.basename(rutaFrom)
                rutaNew = os.path.join(rutaTo+filename)
                if os.path.exists(rutaNew):
                    filename = os.path.basename(rutaFrom)
                    filename_without_extension, file_extension = os.path.splitext(filename)
                    i = 1
                    while os.path.exists(os.path.join(rutaTo+f"{filename_without_extension}({i}){file_extension}")):
                        i += 1
                    new_filename = f"{filename_without_extension}({i}){file_extension}"
                    new_filepath = os.path.join(rutaTo+new_filename)
                    shutil.move(rutaFrom, new_filepath)
                    return(f"Move -from:'{sou}' -to: '{des}' movido con éxito.")
                else:
                    shutil.move(rutaFrom, rutaTo)
                    return(f"Move -from:'{sou}' -to: '{des}' movido con éxito.")
            elif os.path.isdir(rutaFrom):
                for item in os.listdir(rutaFrom):
                    source = os.path.join(rutaFrom + item)
                    rutaNew = os.path.join(rutaTo+item)
                    if os.path.exists(rutaNew):
                        if os.path.isfile(source):
                            filename = os.path.basename(source)
                            filename_without_extension, file_extension = os.path.splitext(filename)
                            i = 1
                            while os.path.exists(os.path.join(rutaTo+f"{filename_without_extension}({i}){file_extension}")):
                                i += 1
                            new_filename = f"{filename_without_extension}({i}){file_extension}"
                            new_filepath = os.path.join(rutaTo+new_filename)
                            shutil.move(source, new_filepath)
                        elif os.path.isdir(source):
                            foldername = os.path.basename(os.path.normpath(source))
                            i = 1
                            while os.path.exists(os.path.join(rutaTo+f"{foldername}({i})")):
                                i += 1
                            new_foldername = f"{foldername}({i})"
                            new_folderpath = os.path.join(rutaTo+new_foldername)
                            shutil.move(rutaFrom, new_folderpath)
                    else:
                        shutil.move(source, rutaTo)
                return(f"Move -from:'{sou}' -to: '{des}' movido con éxito.")
        else:
            return(f"ruta -from:'{sou}' no existe.")
    except Exception as e:
        return(f"No se pudo mover -from:'{sou}' -to: '{des}'")
    # print("Function: transfer")
    # print("Parameters: from_path={}, to={}, mode={}".format(from_path, to, mode))

def rename(path, new_name):
    nameOriginal = new_name
    if "\"" in new_name:
        new_name = new_name.replace("\"", "")
    pathEntrada = path
    if "\"" in pathEntrada:
        pathEntrada = pathEntrada.replace("\"", "")
    if "/" in pathEntrada:
        pathEntrada = pathEntrada.replace("/", "\\")
    ruta_actual = myPath
    ruta_nueva_carpeta = os.path.join(ruta_actual + pathEntrada)
    if os.path.exists(ruta_nueva_carpeta):
        if os.path.isdir(ruta_nueva_carpeta):
            ruta_nueva_carpeta = ruta_nueva_carpeta[:-1]
            new_name = "\\" + new_name
            parent_dir = os.path.dirname(ruta_nueva_carpeta)
            new_path = os.path.join(parent_dir+new_name)
            try:
                os.rename(ruta_nueva_carpeta, new_path)
                return(f"rename -path:'{pathEntrada}' -name: '{nameOriginal}' realizado con éxito.")
            except OSError as e:
                return(f"no se pudo renombrar -path:'{pathEntrada}' -name: '{nameOriginal}'")
        elif os.path.isfile(ruta_nueva_carpeta):
            try:
                parent_dir = os.path.dirname(ruta_nueva_carpeta)
                new_path = os.path.join(parent_dir+"\\"+new_name)
                os.rename(ruta_nueva_carpeta, new_path)
                return(f"rename -path:'{pathEntrada}' -name: '{nameOriginal}' realizado con éxito.")
            except OSError as e:
                return(f"no se pudo renombrar -path:'{pathEntrada}' -name: '{nameOriginal}'")
    else:
        return(f"ruta -path:'{pathEntrada}' no existe")
    # print("Function: rename")
    # print("Parameters: path={}, new_name={}".format(path, new_name))

def modify(path, body):
    pathEntrada = path
    if "\"" in path:
        path = path.replace("\"", "")
    if "/" in path:
        path = path.replace("/", "\\")
    ruta_actual = myPath
    ruta_archivo = os.path.join(ruta_actual+path)
    if os.path.exists(ruta_archivo):
        if os.path.isfile(ruta_archivo):
            try:
                with open(ruta_archivo, 'w') as file:
                    file.write(body)
                return(f"modify -path:'{pathEntrada}' realizado con éxito.")
            except OSError as e:
                return(f"no se pudo modificar -path:'{pathEntrada}'")
        else:
            return(f"no se pudo modificar -path:'{pathEntrada}' porque no corresponde a ningun archivo valido")
    else:
        return(f"no se pudo modificar -path:'{pathEntrada}' porque no existe")
    # print("Function: modify")
    # print("Parameters: path={}, body={}".format(path, body))

def add(path, body):
    pathEntrada = path
    if "\"" in path:
        path = path.replace("\"", "")
    if "/" in path:
        path = path.replace("/", "\\")
    ruta_actual = myPath
    ruta_archivo = os.path.join(ruta_actual + path)
    if os.path.exists(ruta_archivo):
        if os.path.isfile(ruta_archivo):
            try:
                with open(ruta_archivo, 'a') as file:
                    file.write(body)
                return(f"add -path:'{pathEntrada}' realizado con éxito.")
            except OSError as e:
                return(f"no se pudo añadir el contenido a -path:'{pathEntrada}'")
        else:
            return(f"no se pudo añadir contenido a -path:'{pathEntrada}' porque no corresponde a ningun archivo valido")
    else:
        return(f"no se pudo añadir contenido a -path:'{pathEntrada}' porque no existe")
    # print("Function: add")
    # print("Parameters: path={}, body={}".format(path, body))

def backup():
    print("Function: backup")
    print("Parameters: No parameters")

def backup_with_path(path):
    print("Function: backup_with_path")
    print("Parameters: path={}".format(path))

#metodo auxiliar
def isFile(rutaFrom, rutaTo):
    if len(os.listdir(rutaFrom)) != 0:
        for item in os.listdir(rutaFrom):
            if ".txt" in item:
                source = os.path.join(rutaFrom + item)
            else:
                source = os.path.join(rutaFrom + item + "\\")
            rutaNew = rutaTo+item
            if not os.path.exists(rutaNew):
                if os.path.isdir(source):
                    isFile(source,rutaTo)
                elif os.path.isfile(source):
                    shutil.copy2(source, rutaTo)

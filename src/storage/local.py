import os
import shutil
from src.utils.parameters import get_parameters
from src.utils.parameters import update_parameters

myPath = (
    r"C:\Users\Edwin Sandoval\Documents\universidad\archivos\Proyecto1\Archivos\local"
)


def execute(command, parameters):
    function = globals().get(command)
    print("function", command, function)
    response = function(**parameters)

    parameters = get_parameters()
    if parameters["init_exec"]:
        parameters["count_exec_local"] = parameters["count_exec_local"] + 1
    update_parameters(parameters)
    return response


def configure(type, encrypt_log, encrypt_read, key=None):
    bool_encrypt_log = bool(encrypt_log.lower().replace(" ", "") == "true")
    bool_encrypt_read = bool(encrypt_read.lower().replace(" ", "") == "true")
    parameters = get_parameters()
    parameters["encrypt_log"] = bool_encrypt_log
    parameters["encrypt_read"] = bool_encrypt_read
    type = type.replace(" ", "")
    parameters["type"] = type
    if key != None:
        parameters["key"] = key

    update_parameters(parameters)

    return {
        "msg": "Configuración exitosa: encrypt_log={}, encrypt_read={}, type={}, key={}".format(
            bool_encrypt_log, bool_encrypt_read, type, key
        ),
        "status": "success",
    }


def create(name, path, body):
    nameEntrada = name
    if '"' in name:
        name = name.replace('"', "")
    pathEntrada = path
    if '"' in pathEntrada:
        pathEntrada = pathEntrada.replace('"', "")
    if "/" in pathEntrada:
        pathEntrada = pathEntrada.replace("/", "\\")
    ruta_actual = myPath
    ruta_nueva_carpeta = os.path.join(ruta_actual + pathEntrada)
    try:
        if not os.path.exists(ruta_nueva_carpeta):
            os.makedirs(ruta_nueva_carpeta, exist_ok=True)
    except:
        return {
            "msg": "No se pudo crear el archivo: name={}, path={}, body={}".format(
                name, path, body
            ),
            "status": "error",
        }
    ruta_nueva_carpeta = ruta_nueva_carpeta + name
    try:
        if not os.path.exists(ruta_nueva_carpeta):
            with open(ruta_nueva_carpeta, "w") as archivo:
                archivo.write(body)
                archivo.close()
            return {
                "msg": "Archivo creado exitosamente: name={}, path={}, body={}".format(
                    name, path, body
                ),
                "status": "success",
            }
        else:
            return {
                "msg": "El archivo ya existe: name={}, path={}, body={}".format(
                    name, path, body
                ),
                "status": "error",
            }
    except IOError:
        return {
            "msg": "No se pudo crear el archivo: name={}, path={}, body={}".format(
                name, path, body
            ),
            "status": "error",
        }
    # print("Parameters: name={}, path={}, body={}".format(name, path, body))
    # return "Archivo creado exitosamente: name={}, path={}, body={}".format(name, path, body)


def delete(path, name=None):
    pathEntrada = path
    if '"' in path:
        path = path.replace('"', "")
    ruta_actual = myPath
    ruta_nueva_carpeta = os.path.join(ruta_actual + path.replace("/", "\\"))
    if name:
        ruta_completa = os.path.join(ruta_nueva_carpeta, name)
        if os.path.exists(ruta_completa):
            if os.path.isfile(ruta_completa):
                # Hacer pregunta si está seguro
                os.remove(ruta_completa)
                return {
                    "msg": "Delete -name:'{}' eliminado con exito.".format(name),
                    "status": "success",
                }
            else:
                return {
                    "msg": "{} no es un archivo válido.".format(name),
                    "status": "error",
                }
        else:
            return {
                "msg": "No se encontró el archivo en la ruta {}".format(path),
                "status": "error",
            }
    else:
        if os.path.exists(ruta_nueva_carpeta):
            if os.path.isdir(ruta_nueva_carpeta):
                # Hacer pregunta si está seguro
                shutil.rmtree(ruta_nueva_carpeta)
                return {
                    "msg": "Delete -path:'{}' eliminado con exito.".format(path),
                    "status": "success",
                }
            else:
                return {
                    "msg": "{} no es una carpeta válida.".format(path),
                    "status": "error",
                }
        else:
            return {
                "msg": "No se encontró la carpeta {}".format(path),
                "status": "error",
            }
    # print("Function: delete")
    # print("Parameters: path={}, name={}".format(path, name))


def copy(from_path, to):
    sou = from_path
    des = to
    ruta_actual = myPath
    if '"' in from_path:
        from_path = from_path.replace('"', "")
    if "/" in from_path:
        from_path = from_path.replace("/", "\\")
    if '"' in to:
        to = to.replace('"', "")
    if "/" in to:
        to = to.replace("/", "\\")
    rutaFrom = os.path.join(ruta_actual + from_path)
    rutaTo = os.path.join(ruta_actual + to)
    try:
        if os.path.exists(rutaFrom):
            if os.path.isfile(rutaFrom):
                filename = os.path.basename(rutaFrom)
                rutaNew = rutaTo + filename
                if os.path.exists(rutaNew):
                    return {
                        "msg": "El archivo ya existe en la ruta {}".format(to),
                        "status": "error",
                    }
                else:
                    shutil.copy2(rutaFrom, rutaTo)
                    return {
                        "msg": "Copy -from:'{}' -to: '{}' copiado con exito.".format(
                            sou, des
                        ),
                        "status": "success",
                    }
            elif os.path.isdir(rutaFrom):
                isFile(rutaFrom, rutaTo)
                return {
                    "msg": "Copy -from:'{}' -to: '{}' copiado con exito.".format(
                        sou, des
                    ),
                    "status": "success",
                }
        else:
            return {
                "msg": "No se encontró el archivo en la ruta {}".format(from_path),
                "status": "error",
            }
    except Exception as e:
        return {
            "msg": "Copy -from:'{}' -to: '{}' no se pudo copiar.".format(sou, des),
            "status": "error",
        }
    # print("Function: copy")
    # print("Parameters: from_path={}, to={}".format(from_path, to))


def transfer(from_path, to, mode):
    if mode == "cloud":
        return {
            "msg": "Transfer -from:'{}' -to: '{}' -mode: '{}' no se pudo copiar.".format(
                from_path, to, mode
            ),
            "status": "error",
        }
    sou = from_path
    des = to
    ruta_actual = myPath
    if '"' in from_path:
        from_path = from_path.replace('"', "")
    if "/" in from_path:
        from_path = from_path.replace("/", "\\")
    if '"' in to:
        to = to.replace('"', "")
    if "/" in to:
        to = to.replace("/", "\\")
    rutaFrom = os.path.join(ruta_actual + from_path)
    rutaTo = os.path.join(ruta_actual + to)
    try:
        if os.path.exists(rutaFrom):
            if os.path.isfile(rutaFrom):
                filename = os.path.basename(rutaFrom)
                rutaNew = os.path.join(rutaTo + filename)
                if os.path.exists(rutaNew):
                    filename = os.path.basename(rutaFrom)
                    filename_without_extension, file_extension = os.path.splitext(
                        filename
                    )
                    i = 1
                    while os.path.exists(
                        os.path.join(
                            rutaTo
                            + f"{filename_without_extension}({i}){file_extension}"
                        )
                    ):
                        i += 1
                    new_filename = f"{filename_without_extension}({i}){file_extension}"
                    new_filepath = os.path.join(rutaTo + new_filename)
                    shutil.move(rutaFrom, new_filepath)
                    return {
                        "msg": "Transfer -from:'{}' -to: '{}' -mode: '{}' movido con exito.".format(
                            sou, des, mode
                        ),
                        "status": "success",
                    }
                else:
                    shutil.move(rutaFrom, rutaTo)
                    return {
                        "msg": "Transfer -from:'{}' -to: '{}' -mode: '{}' movido con exito.".format(
                            sou, des, mode
                        ),
                        "status": "success",
                    }
            elif os.path.isdir(rutaFrom):
                for item in os.listdir(rutaFrom):
                    source = os.path.join(rutaFrom + item)
                    rutaNew = os.path.join(rutaTo + item)
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
                            new_filepath = os.path.join(rutaTo + new_filename)
                            shutil.move(source, new_filepath)
                        elif os.path.isdir(source):
                            foldername = os.path.basename(os.path.normpath(source))
                            i = 1
                            while os.path.exists(
                                os.path.join(rutaTo + f"{foldername}({i})")
                            ):
                                i += 1
                            new_foldername = f"{foldername}({i})"
                            new_folderpath = os.path.join(rutaTo + new_foldername)
                            shutil.move(rutaFrom, new_folderpath)
                    else:
                        shutil.move(source, rutaTo)
                return {
                    "msg": "Transfer -from:'{}' -to: '{}' -mode: '{}' movido con exito.".format(
                        sou, des, mode
                    ),
                    "status": "success",
                }
        else:
            return {
                "msg": "No se encontró el archivo en la ruta {}".format(from_path),
                "status": "error",
            }
    except Exception as e:
        return {
            "msg": "Transfer -from:'{}' -to: '{}' -mode: '{}' no se pudo mover.".format(
                sou, des, mode
            ),
            "status": "error",
        }
    # print("Function: transfer")
    # print("Parameters: from_path={}, to={}, mode={}".format(from_path, to, mode))


def rename(path, name):
    new_name = name
    nameOriginal = new_name
    if '"' in new_name:
        new_name = new_name.replace('"', "")
    pathEntrada = path
    if '"' in pathEntrada:
        pathEntrada = pathEntrada.replace('"', "")
    if "/" in pathEntrada:
        pathEntrada = pathEntrada.replace("/", "\\")
    ruta_actual = myPath
    ruta_nueva_carpeta = os.path.join(ruta_actual + pathEntrada)
    if os.path.exists(ruta_nueva_carpeta):
        if os.path.isdir(ruta_nueva_carpeta):
            ruta_nueva_carpeta = ruta_nueva_carpeta[:-1]
            new_name = "\\" + new_name
            parent_dir = os.path.dirname(ruta_nueva_carpeta)
            new_path = os.path.join(parent_dir + new_name)
            try:
                os.rename(ruta_nueva_carpeta, new_path)
                return {
                    "msg": "rename -path:'{}' -name: '{}' realizado con éxito.".format(
                        pathEntrada, nameOriginal
                    ),
                    "status": "success",
                }
            except OSError as e:
                return {
                    "msg": "no se pudo renombrar -path:'{}' -name: '{}'".format(
                        pathEntrada, nameOriginal
                    ),
                    "status": "error",
                }
        elif os.path.isfile(ruta_nueva_carpeta):
            try:
                parent_dir = os.path.dirname(ruta_nueva_carpeta)
                new_path = os.path.join(parent_dir + "\\" + new_name)
                os.rename(ruta_nueva_carpeta, new_path)
                return {
                    "msg": "rename -path:'{}' -name: '{}' realizado con éxito.".format(
                        pathEntrada, nameOriginal
                    ),
                    "status": "success",
                }
            except OSError as e:
                return {
                    "msg": "no se pudo renombrar -path:'{}' -name: '{}'".format(
                        pathEntrada, nameOriginal
                    ),
                    "status": "error",
                }
    else:
        return {
            "msg": "no se pudo renombrar -path:'{}' -name: '{}'".format(
                pathEntrada, nameOriginal
            ),
            "status": "error",
        }
    # print("Function: rename")
    # print("Parameters: path={}, new_name={}".format(path, new_name))


def modify(path, body):
    pathEntrada = path
    if '"' in path:
        path = path.replace('"', "")
    if "/" in path:
        path = path.replace("/", "\\")
    ruta_actual = myPath
    ruta_archivo = os.path.join(ruta_actual + path)
    if os.path.exists(ruta_archivo):
        if os.path.isfile(ruta_archivo):
            try:
                with open(ruta_archivo, "w") as file:
                    file.write(body)
                return {
                    "msg": "modify -path:'{}' realizado con éxito.".format(pathEntrada),
                    "status": "success",
                }
            except OSError as e:
                return {
                    "msg": "no se pudo modificar -path:'{}'".format(pathEntrada),
                    "status": "error",
                }
        else:
            return {
                "msg": "no se pudo modificar -path:'{}' porque no es un archivo".format(
                    pathEntrada
                ),
                "status": "error",
            }
    else:
        return {
            "msg": "no se pudo modificar -path:'{}'".format(pathEntrada),
            "status": "error",
        }
    # print("Function: modify")
    # print("Parameters: path={}, body={}".format(path, body))


def add(path, body):
    pathEntrada = path
    if '"' in path:
        path = path.replace('"', "")
    if "/" in path:
        path = path.replace("/", "\\")
    ruta_actual = myPath
    ruta_archivo = os.path.join(ruta_actual + path)
    if os.path.exists(ruta_archivo):
        if os.path.isfile(ruta_archivo):
            try:
                with open(ruta_archivo, "a") as file:
                    file.write(body)
                return {
                    "msg": "add -path:'{}' realizado con éxito.".format(pathEntrada),
                    "status": "success",
                }
            except OSError as e:
                return {
                    "msg": "no se pudo añadir contenido a -path:'{}'".format(
                        pathEntrada
                    ),
                    "status": "error",
                }
        else:
            return {
                "msg": "no se pudo añadir contenido a -path:'{}' porque no es un archivo".format(
                    pathEntrada
                ),
                "status": "error",
            }
    else:
        return {
            "msg": "no se pudo añadir contenido a -path:'{}'".format(pathEntrada),
            "status": "error",
        }


def backup():
    print("Function: backup")
    print("Parameters: No parameters")

    return { "msg": "backup realizado con éxito.", "status": "success" }


def backup_with_path(path):
    print("Function: backup_with_path")
    print("Parameters: path={}".format(path))


# metodo auxiliar
def isFile(rutaFrom, rutaTo):
    if len(os.listdir(rutaFrom)) != 0:
        for item in os.listdir(rutaFrom):
            if ".txt" in item:
                source = os.path.join(rutaFrom + item)
            else:
                source = os.path.join(rutaFrom + item + "\\")
            rutaNew = rutaTo + item
            if not os.path.exists(rutaNew):
                if os.path.isdir(source):
                    isFile(source, rutaTo)
                elif os.path.isfile(source):
                    shutil.copy2(source, rutaTo)

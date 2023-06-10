import os
import re
import shutil


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


# Ejemplo de uso


# createLocal("prueba.txt","hola","/\"juanito 2\"/\"perrito 3\"/")
# deleteLocal("/\"juanito 2\"/")
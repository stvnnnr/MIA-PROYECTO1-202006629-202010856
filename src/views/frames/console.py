import customtkinter
import src.utils.analyzer as analyzer
import src.utils.parameters as parameters
import src.storage.cloud as storage_cloud
import src.storage.local as storage_local
from src.utils.bitacora import write_log
from src.utils.parameters import get_parameters
from src.utils.parameters import update_parameters
from src.utils.decrypt import Decrypt
import os
import time
from tkinter import messagebox


class Console(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.console = customtkinter.CTkTextbox(self, corner_radius=6)
        self.console.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=10, rowspan=9
        )

        self.input_set_command_entry = customtkinter.CTkEntry(self)
        self.input_set_command_entry.grid(
            row=9, column=0, columnspan=10, padx=10, pady=10, sticky="ew"
        )
        self.input_set_command_entry.bind(
            "<Return>", self.input_set_command_entry_return_event
        )

    def input_set_command_entry_return_event(self, event):
        command = self.input_set_command_entry.get()
        self.input_set_command_entry.delete(0, "end")
        self.console.insert("end","\n" + "User:\Consola>" + command + "\n")
        self.console.see("end")
        self.read_command(command)

    def read_command(self, command):
        self.analyzer = analyzer.Analyzer()
        response = self.analyzer.read_command(command)
        write_log("Input - Comando: {}, parameters: {}".format(command, response[1]))
        if response[0] != None:
            if response[1].get("from"):
                response[1]["from_path"] = response[1].pop("from")

            if response[1].get("llave"):
                response[1]["key"] = response[1].pop("llave")

            if response[0].lower() == "delete":
                # recorrer response[1]
                parameters_delete = ""
                for key in response[1]:
                    parameters_delete += "{}: {}\n".format(key, response[1][key])

                result = messagebox.askyesno(
                    "Eliminar archivo",
                    "¿Estás seguro de que deseas eliminar el archivo?" + "\n" + parameters_delete,
                )
                if result == False:
                    return
                
            if response[0].lower() == "exec":
                response_command = self.exec(**response[1])
            elif response[0].lower() == "configure":
                response_command = storage_local.configure(**response[1])
            elif not parameters.get_parameters()["type"]:
                self.console.insert("end", "Has las configuraciones iniciales\n")
                write_log("error: No se ha configurado el sistema")
                return
            elif parameters.get_parameters()["type"] == "cloud":
                response_command = storage_cloud.execute(response[0], response[1])
            elif parameters.get_parameters()["type"] == "local":
                response_command = storage_local.execute(response[0], response[1])
            else:
                response_command = {
                    "status": "error",
                    "msg": "No hemos encontrado algo para ejecutar el comando",
                }
        else:
            for alert in response[1]:
                self.console.insert("end", alert + "\n")
                write_log("error: {}".format(alert))

        self.console.insert("end", response_command["msg"] + "\n")
        write_log(
            "Output - Comando: {}, response: {}".format(
                command, response_command["msg"]
            )
        )
        self.console.see("end")

    def exec(self, path):
        path = path.replace("\\", "/")
        path = path.replace("//", "/")
        path = path.replace("/", "\\")
        if os.path.exists(path):
            if os.path.isfile(path):
                return self.exec_file(path)
            else:
                return {"msg": "Error: El path no es un archivo", "status": "error"}
        else:
            return {"msg": "Error: El path no existe", "status": "error"}

    def exec_file(self, path):
        tiem_start = time.time()
        try: 
            count = 1
            file = open(path, "r")
            command = file.readline().replace("\n", "")
            self.read_command(command)
            file.close()

            parameters = get_parameters()
            parameters["init_exec"] = True
            parameters["count_exec_local"] = 0
            parameters["count_exec_nube"] = 0
            update_parameters(parameters)

            if get_parameters()["encrypt_read"]:
                file = open(path, "r")
                file.readline()
                decrypt = Decrypt()
                key = get_parameters()["key"]
                decrypt_lines = decrypt.decrypt_message(
                    file.readline().replace("\n", ""), key
                )
                file.close()

                decrypt_lines = decrypt_lines.split("\n")
                for line in decrypt_lines:
                    if line != "":
                        self.read_command(line)
                        count += 1
            else:
                file = open(path, "r")
                file.readline()
                for line in file:
                    self.read_command(line.replace("\n", ""))
                    count += 1
                file.close()

        except Exception as e:
            print(e)
            return {"msg": "Error: El archivo al ejecutar archivo, consulte al admin", "status": "error"}


        parameters = get_parameters()
        self.console.insert(
            "end",
            "Comandos ejecutados en local: "
            + str(parameters["count_exec_local"])
            + "\n",
        )
        self.console.insert(
            "end",
            "Comandos ejecutados en nube: " + str(parameters["count_exec_nube"]) + "\n",
        )

        write_log(
            "Output - "
            + "Comandos ejecutados en local: "
            + str(parameters["count_exec_local"])
        )
        write_log(
            "Output - "
            + "Comandos ejecutados en nube: "
            + str(parameters["count_exec_nube"])
        )

        parameters["count_exec_local"] = 0
        parameters["count_exec_nube"] = 0
        parameters["init_exec"] = False
        update_parameters(parameters)
        time_end = time.time()
        times = round(time_end - tiem_start, 2)
        times = self.prepare_time(times)

        return {"msg": "Ejecución exitosa, {} comandos ejecutados, {} tiempo de ejecución".format(count), "status": "success"}
    
    def prepare_time(self, time):
        if time < 60:
            return f"{time} segundos"
        else:
            minutos = time // 60
            segundos = time % 60
            return f"{minutos} minutos y {segundos} segundos"

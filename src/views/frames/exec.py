import customtkinter
import src.storage.cloud as storage_cloud
import src.storage.local as storage_local
from src.utils.bitacora import write_log
import src.utils.parameters as parameters

class Exec(customtkinter.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.logo_label = customtkinter.CTkLabel(self, text="Ejecutar Comando", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.path_label = customtkinter.CTkLabel(self, text="Ruta del archivo", anchor="w")
        self.path_label.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.path_entry = customtkinter.CTkEntry(self)
        self.path_entry.grid(row=2, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5)

        self.execute_button = customtkinter.CTkButton(self, text="Ejecutar")
        self.execute_button.grid(row=3, column=6, padx=20, pady=(10, 20), sticky="w", columnspan=5)

        self.execute_button.bind("<Button-1>", self.execute_button_left_click_event)

    def execute_button_left_click_event(self, event):
        file_path = self.path_entry.get()

        if file_path:
            # Ejecutar comando
            response_command = self.execute_command(file_path)
            write_log("Output - Comando: {}, response: {}".format("Execute", response_command["msg"]))
        else:
            write_log("Error - Falta especificar la ruta del archivo")

    def execute_command(self, file_path):
        if parameters.get_parameters()["type"] == "cloud":
            response_command = storage_cloud.exec(file_path)
        elif parameters.get_parameters()["type"] == "local":
            response_command = storage_local.exec(file_path)

        return response_command

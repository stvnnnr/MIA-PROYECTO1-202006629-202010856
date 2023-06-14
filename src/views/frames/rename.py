import customtkinter
import src.storage.cloud as storage_cloud
import src.storage.local as storage_local
from src.utils.bitacora import write_log
import src.utils.parameters as parameters

class Rename(customtkinter.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.logo_label = customtkinter.CTkLabel(self, text="Renombrar Archivo", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), columnspan=5)

        self.path_label = customtkinter.CTkLabel(self, text="Ruta del archivo", anchor="w")
        self.path_label.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.path_entry = customtkinter.CTkEntry(self)
        self.path_entry.grid(row=2, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5)

        self.name_label = customtkinter.CTkLabel(self, text="Nuevo nombre", anchor="w")
        self.name_label.grid(row=3, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.name_entry = customtkinter.CTkEntry(self)
        self.name_entry.grid(row=4, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5)

        self.rename_button = customtkinter.CTkButton(self, text="Renombrar")
        self.rename_button.grid(row=5, column=6, padx=20, pady=(10, 20), sticky="w")

        self.rename_button.bind("<Button-1>", self.rename_button_left_click_event)

    def rename_button_left_click_event(self, event):
        file_path = self.path_entry.get()
        new_name = self.name_entry.get()

        if file_path and new_name:
            # Renombrar archivo
            response_command = self.rename_file(file_path, new_name)
            write_log("Output - Comando: {}, response: {}".format("Rename", response_command))
        else:
            write_log("Error - Faltan parámetros para renombrar el archivo")

    def rename_file(self, file_path, new_name):
        if parameters.get_parameters()["type"] == "cloud":
            response_command = storage_cloud.rename(file_path, new_name)
        elif parameters.get_parameters()["type"] == "local":
            response_command = storage_local.rename(file_path, new_name)

        return response_command

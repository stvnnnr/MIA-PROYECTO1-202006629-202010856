import customtkinter
import src.storage.cloud as storage_cloud
import src.storage.local as storage_local
from src.utils.bitacora import write_log
import src.utils.parameters as parameters

class Transfer(customtkinter.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.logo_label = customtkinter.CTkLabel(self, text="Transferir Archivo", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), columnspan=5)

        self.from_label = customtkinter.CTkLabel(self, text="Ruta de origen", anchor="w")
        self.from_label.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.from_entry = customtkinter.CTkEntry(self)
        self.from_entry.grid(row=2, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5)

        self.to_label = customtkinter.CTkLabel(self, text="Ruta de destino", anchor="w")
        self.to_label.grid(row=3, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.to_entry = customtkinter.CTkEntry(self)
        self.to_entry.grid(row=4, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5)

        self.mode_label = customtkinter.CTkLabel(self, text="Modo", anchor="w")
        self.mode_label.grid(row=5, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.mode_entry = customtkinter.CTkEntry(self)
        self.mode_entry.grid(row=6, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5)

        self.transfer_button = customtkinter.CTkButton(self, text="Transferir")
        self.transfer_button.grid(row=7, column=6, padx=20, pady=(10, 20), sticky="w")

        self.transfer_button.bind("<Button-1>", self.transfer_button_left_click_event)

    def transfer_button_left_click_event(self, event):
        source_path = self.from_entry.get()
        destination_path = self.to_entry.get()
        mode = self.mode_entry.get()

        if source_path and destination_path and mode:
            # Transferir archivo
            response_command = self.transfer_file(source_path, destination_path, mode)
            write_log("Output - Comando: {}, response: {}".format("Transfer", response_command))
        else:
            write_log("Error - Faltan parámetros para transferir el archivo")

    def transfer_file(self, source_path, destination_path, mode):
        if parameters.get_parameters()["type"] == "cloud":
            response_command = storage_cloud.transfer(source_path, destination_path, mode)
        elif parameters.get_parameters()["type"] == "local":
            response_command = storage_local.transfer(source_path, destination_path, mode)

        return response_command

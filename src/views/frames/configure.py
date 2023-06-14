import customtkinter
import src.utils.parameters as parameters
import src.storage.cloud as storage_cloud
import src.storage.local as storage_local
from src.utils.bitacora import write_log

class Configure(customtkinter.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.logo_label = customtkinter.CTkLabel(self, text="Configuración", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.type_label = customtkinter.CTkLabel(self, text="Tipo de almacenamiento", anchor="w")
        self.type_label.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.type_entry = customtkinter.CTkEntry(self)
        self.type_entry.grid(row=2, column=1, padx=20, pady=(10, 20), sticky="ew")

        self.encrypt_log_label = customtkinter.CTkLabel(self, text="Encriptar log", anchor="w")
        self.encrypt_log_label.grid(row=3, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.encrypt_log_entry = customtkinter.CTkEntry(self)
        self.encrypt_log_entry.grid(row=4, column=1, padx=20, pady=(10, 20), sticky="ew")

        self.encrypt_read_label = customtkinter.CTkLabel(self, text="Encriptar lectura", anchor="w")
        self.encrypt_read_label.grid(row=5, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.encrypt_read_entry = customtkinter.CTkEntry(self)
        self.encrypt_read_entry.grid(row=6, column=1, padx=20, pady=(10, 20), sticky="ew")

        self.key_label = customtkinter.CTkLabel(self, text="Clave", anchor="w")
        self.key_label.grid(row=7, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.key_entry = customtkinter.CTkEntry(self)
        self.key_entry.grid(row=8, column=1, padx=20, pady=(10, 20), sticky="ew")

        self.configure_button = customtkinter.CTkButton(self, text="Configurar")
        self.configure_button.grid(row=9, column=2, padx=20, pady=(10, 20), sticky="w")

        self.configure_button.bind("<Button-1>", self.configure_button_left_click_event)

    def configure_button_left_click_event(self, event):
        parameters.set_parameter("type", self.type_entry.get())
        parameters.set_parameter("encrypt_log", self.encrypt_log_entry.get())
        parameters.set_parameter("encrypt_read", self.encrypt_read_entry.get())
        parameters.set_parameter("key", self.key_entry.get())

        write_log("Output - Comando: Configure")
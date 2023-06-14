import customtkinter
import src.utils.parameters as parameters
import src.storage.cloud as storage_cloud
import src.storage.local as storage_local
from src.utils.bitacora import write_log

class Add(customtkinter.CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.logo_label = customtkinter.CTkLabel(self, text="Añadir contenido", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.content_label = customtkinter.CTkLabel(self, text="Contenido del archivo", anchor="w")
        self.content_label.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.content_entry = customtkinter.CTkTextbox(self)
        self.content_entry.grid(row=2, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5)

        self.path_label = customtkinter.CTkLabel(self, text="Ruta del archivo", anchor="w")
        self.path_label.grid(row=3, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.path_entry = customtkinter.CTkEntry(self)
        self.path_entry.grid(row=4, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5)

        self.create_button = customtkinter.CTkButton(self, text="Actualizar")
        self.create_button.grid(row=7, column=6, padx=20, pady=(10, 20), sticky="w")

        self.create_button.bind("<Button-1>", self.create_button_left_click_event)

    def create_button_left_click_event(self):
        if parameters.get_parameters()["type"] == "cloud":
            response_command = storage_cloud.create(self.name_entry.get(), self.content_entry.get(), self.path_entry.get())
        elif parameters.get_parameters()["type"] == "local":
            response_command = storage_local.create(self.name_entry.get(), self.content_entry.get(), self.path_entry.get())

        write_log("Output - Comando: {}, response: {}".format("Create", response_command))
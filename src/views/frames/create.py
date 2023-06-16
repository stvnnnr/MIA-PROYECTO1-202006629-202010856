import customtkinter
import src.utils.parameters as parameters
import src.storage.cloud as storage_cloud
import src.storage.local as storage_local
from src.utils.bitacora import write_log
from tkinter import messagebox


class Create(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self,
            text="Crear Archivo",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.name_label = customtkinter.CTkLabel(
            self, text="Nombre del archivo", anchor="w"
        )
        self.name_label.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.name_entry = customtkinter.CTkEntry(self)
        self.name_entry.grid(
            row=2, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5
        )

        self.content_label = customtkinter.CTkLabel(
            self, text="Contenido del archivo", anchor="w"
        )
        self.content_label.grid(row=3, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.content_entry = customtkinter.CTkTextbox(self)
        self.content_entry.grid(
            row=4, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5
        )

        self.path_label = customtkinter.CTkLabel(
            self, text="Ruta del archivo", anchor="w"
        )
        self.path_label.grid(row=5, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.path_entry = customtkinter.CTkEntry(self)
        self.path_entry.grid(
            row=6, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5
        )

        self.create_button = customtkinter.CTkButton(self, text="Crear")
        self.create_button.grid(row=7, column=6, padx=20, pady=(10, 20), sticky="w")

        self.create_button.bind("<Button-1>", self.create_button_left_click_event)

    def create_button_left_click_event(self, event):
        parameter = [
            self.name_entry.get(),
            self.path_entry.get(),
            self.content_entry.get("0.0", "end"),
        ]
        if parameter[0] == "" or parameter[1] == "" or parameter[2] == "":
            messagebox.showerror(
                "Error", "Por favor ingrese todos los campos requeridos"
            )
            return
        
        if parameters.get_parameters()["type"] == "cloud":
            response_command = storage_cloud.create(
                parameter[0], parameter[1], parameter[2]
            )
        elif parameters.get_parameters()["type"] == "local":
            response_command = storage_local.create(
                parameter[0], parameter[1], parameter[2]
            )

        if response_command["status"] == "error":
            messagebox.showerror("Error", response_command["msg"])
            return
        
        messagebox.showinfo("Info", response_command["msg"])
        # clear entry and text
        self.name_entry.delete(0, "end")
        self.path_entry.delete(0, "end")
        self.content_entry.delete("0.0", "end")

        write_log(
            "Output - Comando: {}, response: {}".format(
                "Create", response_command["msg"]
            )
        )

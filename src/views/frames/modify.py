import customtkinter
import src.storage.cloud as storage_cloud
import src.storage.local as storage_local
from src.utils.bitacora import write_log
import src.utils.parameters as parameters
from tkinter import messagebox

class Modify(customtkinter.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.logo_label = customtkinter.CTkLabel(self, text="Modificar Archivo", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.path_label = customtkinter.CTkLabel(self, text="Ruta del archivo", anchor="w")
        self.path_label.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.path_entry = customtkinter.CTkEntry(self)
        self.path_entry.grid(row=2, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5)

        self.body_label = customtkinter.CTkLabel(self, text="Contenido del archivo", anchor="w")
        self.body_label.grid(row=3, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.body_entry = customtkinter.CTkTextbox(self)
        self.body_entry.grid(row=4, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5)

        self.modify_button = customtkinter.CTkButton(self, text="Modificar")
        self.modify_button.grid(row=5, column=6, padx=20, pady=(10, 20), sticky="w")

        self.modify_button.bind("<Button-1>", self.modify_button_left_click_event)

    def modify_button_left_click_event(self, event):
        file_path = self.path_entry.get()
        new_body = self.body_entry.get("1.0", "end-1c")

        if file_path and new_body:
            # Modificar archivo
            response_command = self.modify_file(file_path, new_body)
            write_log("Output - Comando: {}, response: {}".format("Modify", response_command["msg"]))
            messagebox.showinfo("Información", response_command["msg"])
        else:
            write_log("Error - Faltan parámetros para modificar el archivo")
            messagebox.showerror("Error", "Faltan parámetros para modificar el archivo")

    def modify_file(self, file_path, new_body):
        if parameters.get_parameters()["type"] == "cloud":
            response_command = storage_cloud.modify(file_path, new_body)
        elif parameters.get_parameters()["type"] == "local":
            response_command = storage_local.modify(file_path, new_body)

        return response_command

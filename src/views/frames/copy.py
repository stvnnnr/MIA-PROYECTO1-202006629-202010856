import customtkinter
import src.utils.parameters as parameters
import src.storage.cloud as storage_cloud
import src.storage.local as storage_local
from src.utils.bitacora import write_log
from tkinter import messagebox

class Copy(customtkinter.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)


        self.logo_label = customtkinter.CTkLabel(self, text="Copiar Archivo", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.from_label = customtkinter.CTkLabel(self, text="Ruta de origen", anchor="w")
        self.from_label.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.from_entry = customtkinter.CTkEntry(self)
        self.from_entry.grid(row=2, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5)

        self.to_label = customtkinter.CTkLabel(self, text="Ruta de destino", anchor="w")
        self.to_label.grid(row=3, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.to_entry = customtkinter.CTkEntry(self)
        self.to_entry.grid(row=4, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=5)

        self.copy_button = customtkinter.CTkButton(self, text="Copiar")
        self.copy_button.grid(row=7, column=6, padx=20, pady=(10, 20), sticky="w")

        self.copy_button.bind("<Button-1>", self.copy_button_left_click_event)

    def copy_button_left_click_event(self, event):
        source_path = self.from_entry.get()
        destination_path = self.to_entry.get()

        if source_path and destination_path:
            # Copiar archivo
            response_command = self.copy_file(source_path, destination_path)
            write_log("Output - Comando: {}, response: {}".format("Copy", response_command["msg"]))
            messagebox.showinfo("Copiar", response_command["msg"])
            #clear entry
            self.from_entry.delete(0, 'end')
            self.to_entry.delete(0, 'end')
        else:
            write_log("Error - Faltan parámetros para copiar el archivo")
            messagebox.showerror("Error", "Faltan parámetros para copiar el archivo")

    def copy_file(self, source_path, destination_path):
        if parameters.get_parameters()["type"] == "cloud":
            response_command = storage_cloud.copy(source_path, destination_path)
        elif parameters.get_parameters()["type"] == "local":
            response_command = storage_local.copy(source_path, destination_path)

        return response_command

import customtkinter
import src.utils.parameters as parameters
import src.storage.cloud as storage_cloud
import src.storage.local as storage_local
from src.utils.bitacora import write_log
from tkinter import messagebox

class Delete(customtkinter.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)


        self.logo_label = customtkinter.CTkLabel(self, text="Eliminar Archivo", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.path_label = customtkinter.CTkLabel(self, text="Ruta del archivo", anchor="w")
        self.path_label.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.path_entry = customtkinter.CTkEntry(self)
        self.path_entry.grid(row=2, column=1, padx=20, pady=(10, 0), sticky="ew", columnspan=5)

        self.name_label = customtkinter.CTkLabel(self, text="Nombre del archivo", anchor="w")
        self.name_label.grid(row=3, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.name_entry = customtkinter.CTkEntry(self)
        self.name_entry.grid(row=4, column=1, padx=20, pady=(10, 0), sticky="ew", columnspan=5)

        self.delete_button = customtkinter.CTkButton(self, text="Eliminar")
        self.delete_button.grid(row=7, column=6, padx=20, pady=(10, 0), sticky="w")

        self.delete_button.bind("<Button-1>", self.delete_button_left_click_event)

    def delete_button_left_click_event(self, event):
        path = self.path_entry.get()
        name = self.name_entry.get()
        if path:
            result = messagebox.askyesno("Eliminar archivo", "¿Estás seguro de que deseas eliminar el archivo?")
            if result == False:
                return
            # Eliminar archivo
            response_command = self.delete_file(path, name)
            #clear entries
            print(response_command)
            self.path_entry.delete(0, "end")
            self.name_entry.delete(0, "end")
            messagebox.showinfo("Eliminar Archivo", response_command["msg"])
            write_log("Output - Comando: {}, response: {}".format("Delete", response_command["msg"]))
            # clear entries
            self.path_entry.delete(0, "end")
            self.name_entry.delete(0, "end")
        else:
            write_log("Error - Faltan parámetros para eliminar el archivo")
            messagebox.showerror("Eliminar Archivo", "Faltan parámetros para eliminar el archivo")


    def delete_file(self, path, name):
        if parameters.get_parameters()["type"] == "cloud":
            response_command = storage_cloud.delete(path, name)
        elif parameters.get_parameters()["type"] == "local":
            response_command = storage_local.delete(path, name)

        return response_command

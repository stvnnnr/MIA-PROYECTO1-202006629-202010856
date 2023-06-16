import customtkinter
import src.storage.local as storage_local
from src.utils.bitacora import write_log
from tkinter import messagebox
from src.utils.parameters import get_parameters


class Configure(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self,
            text="Configuración",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.type_label = customtkinter.CTkLabel(
            self, text="Tipo de almacenamiento", anchor="w"
        )
        self.type_label.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="ew")
        # create combobox
        self.type_combobox = customtkinter.CTkComboBox(self, values=["Local", "Cloud"])
        self.type_combobox.grid(
            row=2, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=2
        )

        self.encrypt_log_label = customtkinter.CTkLabel(
            self, text="Encriptar log", anchor="w"
        )
        self.encrypt_log_label.grid(row=3, column=1, padx=20, pady=(10, 0), sticky="ew")
        # create true false radiobuttons
        self.encrypt_log_combobox = customtkinter.CTkComboBox(
            self, values=["True", "False"]
        )
        self.encrypt_log_combobox.grid(
            row=4, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=2
        )

        self.encrypt_read_label = customtkinter.CTkLabel(
            self, text="Encriptar lectura", anchor="w"
        )
        self.encrypt_read_label.grid(
            row=5, column=1, padx=20, pady=(10, 0), sticky="ew"
        )

        self.encrypt_read_combobox = customtkinter.CTkComboBox(
            self, values=["True", "False"]
        )
        self.encrypt_read_combobox.grid(
            row=6, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=2
        )

        self.key_label = customtkinter.CTkLabel(self, text="Clave", anchor="w")
        self.key_label.grid(row=7, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.key_entry = customtkinter.CTkEntry(self)
        self.key_entry.grid(
            row=8, column=1, padx=20, pady=(10, 20), sticky="ew", columnspan=2
        )

        self.configure_button = customtkinter.CTkButton(self, text="Configurar")
        self.configure_button.grid(row=9, column=2, padx=20, pady=(10, 20), sticky="w")

        self.configure_button.bind("<Button-1>", self.configure_button_left_click_event)

    def configure_button_left_click_event(self, event):
        type = self.type_combobox.get().lower()
        encrypt_log = self.encrypt_log_combobox.get()
        encrypt_read = self.encrypt_read_combobox.get()
        key = self.key_entry.get()
        if key == "":
            key = get_parameters()["key"]

        if type == "" or encrypt_log == "" or encrypt_read == "":
            messagebox.showerror(
                "Error", "Debe llenar todos los type, encrypt_log y encrypt_read"
            )
            return

        response_command = storage_local.configure(type, encrypt_log, encrypt_read, key)
        messagebox.showinfo("Info", response_command["msg"])
        write_log("Output - Comando: Configure - Respuesta: " + response_command["msg"])

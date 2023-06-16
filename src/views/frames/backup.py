import customtkinter
import src.storage.cloud as storage_cloud
import src.storage.local as storage_local
from src.utils.bitacora import write_log
import src.utils.parameters as parameters
from tkinter import messagebox


class Backup(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self,
            text="Realizar Backup",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.backup_button = customtkinter.CTkButton(self, text="Realizar Backup")
        self.backup_button.grid(row=2, column=6, padx=20, pady=(10, 20), sticky="w")

        self.backup_button.bind("<Button-1>", self.backup_button_left_click_event)

    def backup_button_left_click_event(self, event):
        # Realizar backup
        response_command = self.perform_backup()

        if response_command["status"] == "success":
            messagebox.showinfo("Backup", response_command["msg"])
        else:
            messagebox.showerror("Backup", response_command["msg"])

        write_log(
            "Output - Comando: {}, response: {}".format(
                "Backup", response_command["msg"]
            )
        )

    def perform_backup(self):
        if parameters.get_parameters()["type"] == "cloud":
            response_command = storage_cloud.backup()
        elif parameters.get_parameters()["type"] == "local":
            response_command = storage_local.backup()

        return response_command

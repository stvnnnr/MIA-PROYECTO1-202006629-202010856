import customtkinter
from src.utils.loadUsers import ReadUsers
import customtkinter as ctk
import main as view_main
from src.utils.bitacora import write_log

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class Login:
    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.title("Login")

        window_width = 700
        window_height = 700

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}")
        self.root.update_idletasks()  # Aplicar la geometría antes de centrar

        self.root.geometry(f"+{x}+{y}")  # Centrar la ventana en las coordenadas calculadas

        self.frame = customtkinter.CTkFrame(master=self.root)
        self.frame.pack(pady=100, padx=100, fill="both", expand=True)

        self.label = customtkinter.CTkLabel(master=self.frame, text="Login", font=("Cooper", 30))
        self.label.pack(pady=80, padx=20)

        self.entry1 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Username")
        self.entry1.pack(pady=10, padx=10)

        self.entry2 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
        self.entry2.pack(pady=10, padx=10)

        self.button = customtkinter.CTkButton(master=self.frame, text="Login", command=self.login)
        self.button.pack(pady=10, padx=10)

        # self alert 
        self.alert = customtkinter.CTkLabel(master=self.frame, text="Usuarios o contraseña no coinciden", font=("Cooper", 15), text_color="red")
        
        
    def login(self):

        # remove alert
        self.alert.pack_forget()
        flag = False
        listUsers = ReadUsers().readTxtUsers()
        username = self.entry1.get()
        password = self.entry2.get()
        write_log("Input - Inicio de sesión: " + username)
        for user in listUsers:
            if user[0] == username and user[1] == password:
                flag = True
                break
        if flag:
            # close login window
            self.root.destroy()
            # open principal window
            write_log("Output - Inicio de sesión: " + username)
            ventana_principal = view_main.Main()
            ventana_principal.run()
        else:
            self.alert.pack(pady=10, padx=10)
            print("Bad")


    def run(self):
        self.root.mainloop()
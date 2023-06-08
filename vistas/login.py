import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class LoginApp:
    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.geometry("700x700")
        self.root.title("Login")

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

    def login(self):
        flag = False
        username = self.entry1.get().lower()
        password = self.entry2.get().lower()
        
    def run(self):
        self.root.mainloop()
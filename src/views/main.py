import tkinter
import tkinter.messagebox
import customtkinter
import src.views.login as view_login
import src.views.frames.console as frame_console

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class Main(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Proyecto 1")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Proyecto 1", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Cerrar sesion",command=self.logout_button_event, corner_radius=0, bg_color="#f1f5f9", fg_color="#515a69")
        self.sidebar_button_1.grid(row=5, column=0, padx=20, pady=10)

        self.operations_label = customtkinter.CTkLabel(self.sidebar_frame, text="Operaciones", anchor="w")
        self.operations_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.operations_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=[
            'consola',
            'create',
            'delete',
            'backup',
            'logout',
            'copy',
            'transfer',
            'rename',
            'modify',
            'add',
            'exec'],
            command=self.change_operation_event)
        self.operations_optionemenu.grid(row=3, column=0, padx=20, pady=(10, 20))

        self.content_frame = customtkinter.CTkFrame(self, corner_radius=6)
        self.content_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.form_console()

    def form_console(self):
        self.frame_console = frame_console.Console(self.content_frame)
        self.frame_console.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def change_operation_event(self, text):
        print("change_scaling_event", text)
               
    def input_set_command_entry_return_event(self, event):
        print("input_set_command_entry return", event)
        self.console.insert("end", self.input_set_command_entry.get() + "\n")
        self.input_set_command_entry.delete(0, "end")
        self.console.see("end")

    def logout_button_event(self):
        self.destroy()
        view_login.Login().run()

    def run(self):
        self.mainloop()

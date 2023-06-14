import tkinter
import tkinter.messagebox
import customtkinter
import src.views.login as view_login
import src.views.frames.console as frame_console
import src.views.frames.create as frame_create
import src.views.frames.delete as frame_delete
import src.views.frames.copy as frame_copy
import src.views.frames.transfer as frame_transfer
import src.views.frames.rename as frame_rename
import src.views.frames.modify as frame_modify
import src.views.frames.add as frame_add
import src.views.frames.backup as frame_backup
import src.views.frames.configure as frame_configure
import src.views.frames.exec as frame_exec

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
            'copy',
            'transfer',
            'rename',
            'modify',
            'add',
            'exec',
            'configure',
            ],
            command=self.change_operation_event)
        
        self.functions = {
            'consola': self.form_console,
            'create': self.form_create,
            'delete': self.form_delete,
            'backup': self.form_backup,
            'copy': self.form_copy,
            'transfer': self.form_transfer,
            'rename': self.form_rename,
            'modify': self.form_modify,
            'add': self.form_add,
            'exec': self.form_exec,
            'configure': self.form_configure,
        }
        self.operations_optionemenu.grid(row=3, column=0, padx=20, pady=(10, 20))
        self.form_content()
        self.form_console()

    def form_content(self):
        self.content_frame = customtkinter.CTkFrame(self, corner_radius=6)
        self.content_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def form_console(self):
        self.frame_console = frame_console.Console(self.content_frame)
        self.frame_console.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def form_create(self):
        self.frame_create = frame_create.Create(self.content_frame)
        self.frame_create.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
    def form_delete(self):
        self.frame_delete = frame_delete.Delete(self.content_frame)
        self.frame_delete.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def form_backup(self):
        self.frame_backup = frame_backup.Backup(self.content_frame)
        self.frame_backup.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def form_copy(self):
        self.frame_copy = frame_copy.Copy(self.content_frame)
        self.frame_copy.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
    def form_transfer(self):
        self.frame_transfer = frame_transfer.Transfer(self.content_frame)
        self.frame_transfer.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def form_rename(self):
        self.frame_rename = frame_rename.Rename(self.content_frame)
        self.frame_rename.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def form_modify(self):
        self.frame_modify = frame_modify.Modify(self.content_frame)
        self.frame_modify.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def form_add(self):
        self.frame_add = frame_add.Add(self.content_frame)
        self.frame_add.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def form_exec(self):
        self.frame_exec = frame_exec.Exec(self.content_frame)
        self.frame_exec.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def form_configure(self):
        self.frame_configure = frame_configure.Configure(self.content_frame)
        self.frame_configure.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def change_operation_event(self, name):   
        self.content_frame.destroy()
        self.form_content()
        self.functions[name]()

    def input_set_command_entry_return_event(self, event):
        self.console.insert("end", self.input_set_command_entry.get() + "\n")
        self.input_set_command_entry.delete(0, "end")
        self.console.see("end")

    def logout_button_event(self):
        self.destroy()
        view_login.Login().run()

    def run(self):
        self.mainloop()

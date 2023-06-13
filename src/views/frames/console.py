import customtkinter
class Console(customtkinter.CTkFrame):

    def __init__(self, master, **kwargs):
        print("ConsoleForm")
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.console = customtkinter.CTkTextbox(self, corner_radius=6)
        self.console.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=10, rowspan=9)

        self.input_set_command_entry = customtkinter.CTkEntry(self)
        self.input_set_command_entry.grid(row=9, column=0, columnspan=10,  padx=10, pady=10, sticky="ew")
        self.input_set_command_entry.bind("<Return>", self.input_set_command_entry_return_event)

    def input_set_command_entry_return_event(self, event):
        command = self.input_set_command_entry.get()
        self.input_set_command_entry.delete(0, "end")
        self.console.insert("end", command + "\n")
        self.execute_command(command)

    def execute_command(self, command):
        pass
import customtkinter
import src.utils.analyzer as analyzer
import src.utils.parameters as parameters
import src.storage.cloud as storage_cloud
import src.storage.local as storage_local
from src.utils.bitacora import write_log
class Console(customtkinter.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        print(parameters.get_parameters()["type"])
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
        self.read_command(command)

    def read_command(self, command):
        self.analyzer = analyzer.Analyzer()
        response = self.analyzer.read_command(command)
        write_log("Input - Comando: {}, parameters: {}".format(command, response[1]))
        if response[0] != None:
            if response[0].lower() == "configure":
                response_command = storage_local.configure(**response[1])

            elif response[0].lower() == "exec":
                response_command = self.exec(**response[1])

            elif parameters.get_parameters()["type"] == "cloud":
                response_command = storage_cloud.execute(response[0], response[1])
                
            else:
                response_command = storage_local.execute(response[0], response[1])
        else:
            for alert in response[1]:
                self.console.insert("end", alert + "\n")
                write_log("error: {}".format(alert))

        self.console.insert("end", response_command + "\n")
        write_log("Output - Comando: {}, response: {}".format(command, response_command))
    
    def exec(self, path):
        path = path.replace("\\", "/")
        path = path.replace("//", "/")
        path = path.replace("/", "\\")

        file = open(path, "r")
        for line in file:
            command = line.replace("\n", "")
            self.read_command(command)
        file.close()
        
        return "Ejecución exitosa\n"        
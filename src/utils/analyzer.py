import re
import os

class Analyzer():
    def __init__(self):
        self.commands = [
            {
                'name': 'configure', 
                'description': 'comando para configurar el tipo de almacenamiento', 
                'parameters': ["type", "encrypt_log", "encrypt_read", "key"],
                'optional': ["key"],
            },
            {
                'name': 'create', 
                'description': 'comando para crear', 
                'parameters': ["name", "path", "body"],
            },
            {
                'name': 'delete', 
                'description': 'comando para eliminar', 
                'parameters': ["path", "name"],
                'optional': ["name"],
            },
            {
                'name': 'copy', 
                'description': 'comando para copiar', 
                'parameters': ["from", "to"],
            },
            {
                'name': 'transfer', 
                'description': 'comando para copiar', 
                'parameters': ["from", "to", "mode"],
            },
            {
                'name': 'rename',
                'description': 'comando para renombrar',
                'parameters': ["path", "name"],
            },
            {
                'name': 'modify',
                'description': 'comando para renombrar',
                'parameters': ["path", "body"],
            },
            {
                'name': 'add',
                'description': 'comando para renombrar',
                'parameters': ["path", "body"],
            },
            {
                'name': 'backup',
                'description': 'comando para renombrar',
                'parameters': [],
            },
            {
                'name': 'exec',
                'description': 'comando para renombrar',
                'parameters': ["path"],
            }
        ]

    def read_command(self, command):
        name_command = command.split()[0].lower()

        parameters_values = re.findall(r'-\s*(\w+)\s*->\s*([^->]+)', command)
        
        command_found = next((cmd for cmd in self.commands if cmd['name'] == name_command), None)
        print(parameters_values, name_command)
        if command_found:
            parameters = {}
            valid = True
            alerts = []
            parameters_requireds = []
            for parameter, value in parameters_values:
                if parameter in command_found['parameters']:
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    parameters[parameter] = value
                else:
                    alerts.append(f"El parámetro '{parameter}' no es válido para el comando '{name_command}'.")
                    valid = False
                
                optionals = command_found.get('optional') or []

                parameters_requireds = list(set(command_found['parameters']) - set(optionals))

            for parameter_required in parameters_requireds:
                if parameter_required not in parameters:
                    alerts.append(f"El parámetro '{parameter_required}' es requerido para el comando '{name_command}'.")
                    valid = False

            if len(alerts) > 0:
                return None, alerts

            if valid:
                return name_command, parameters
        else:
            return None, [f"El command '{name_command}' no es válido."]



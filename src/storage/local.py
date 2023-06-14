from src.utils.parameters import get_parameters
from src.utils.parameters import update_parameters

def execute(command, parameters):
    function = globals().get(command)
    function(**parameters)

def configure(type, encrypt_log, encrypt_read, key=None):
    bool_encrypt_log = bool(encrypt_log.lower() == 'true')
    bool_encrypt_read = bool(encrypt_read.lower() == 'true')

    parameters = get_parameters()
    parameters["encrypt_log"] = bool_encrypt_log
    parameters["encrypt_read"] = bool_encrypt_read
    parameters["type"] = type
    if key != None:
        parameters["key"] = key

    update_parameters(parameters)

    return "Configuración exitosa\n"       
    
def create(name, path, body):
    print("Function: create")
    print("Parameters: name={}, path={}, body={}".format(name, path, body))

def delete(path, name=None):
    print("Function: delete")
    print("Parameters: path={}, name={}".format(path, name))

def copy(from_path, to):
    print("Function: copy")
    print("Parameters: from_path={}, to={}".format(from_path, to))

def transfer(from_path, to, mode):
    print("Function: transfer")
    print("Parameters: from_path={}, to={}, mode={}".format(from_path, to, mode))

def rename(path, new_name):
    print("Function: rename")
    print("Parameters: path={}, new_name={}".format(path, new_name))

def modify(path, body):
    print("Function: modify")
    print("Parameters: path={}, body={}".format(path, body))

def add(path, body):
    print("Function: add")
    print("Parameters: path={}, body={}".format(path, body))

def backup():
    print("Function: backup")
    print("Parameters: No parameters")

def backup_with_path(path):
    print("Function: backup_with_path")
    print("Parameters: path={}".format(path))

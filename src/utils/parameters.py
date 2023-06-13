import json

def get_parameters():
    with open('.\src\storage\parameters.json' , "r") as file:
        return json.load(file)
    
def update_parameters(parameters):
    with open('.\src\storage\parameters.json' , "w") as file:
        json.dump(parameters, file, indent=4)
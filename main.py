
import src.views.login as view_login
import src.views.main as view_main
from src.utils.bitacora import write_log
def main():
    write_log("Input - Inicio de la aplicación.")
    test = True
    if test:
        view_main.Main().run()
    else:
        view_login.Login().run()
if __name__ == "__main__":
    main()
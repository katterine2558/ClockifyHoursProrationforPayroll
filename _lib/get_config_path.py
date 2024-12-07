import os
import sys

def get_config_path():
    if hasattr(sys, '_MEIPASS'):  # Cuando está ejecutado desde un archivo compilado
        base_path = sys._MEIPASS
        return os.path.join(base_path, "_lib\\config.ini")
    else:  # Cuando está ejecutado como un script
        base_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(base_path, "config.ini")
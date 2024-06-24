import subprocess
import sys


def import_or_install(module_name):
    try:
        return __import__(module_name)
    except ModuleNotFoundError:
        print(f"Module '{module_name}' not found. Installing it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        return __import__(module_name)


# Automatically install and import 'inquirer'
inquirer = import_or_install("inquirer")

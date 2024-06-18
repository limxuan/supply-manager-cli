import os

from utils.textfiles_database import load_data, save_value
from utils.cli import select_from_list, clear_screen

controlllers_data_filepath = "data/controllers.txt"


def controller_manager():
    numberOfFailures = 0
    try:
        values = load_data(controlllers_data_filepath)
    except Exception:
        values = {}
    while numberOfFailures < 3:
        user_input = select_from_list(
            "Controller System: Please choose an option", ["Register", "Login"]
        )

        if user_input.lower() == "register":
            if len(values) >= 4:
                clear_screen()
                print("[Error]: There has already been 4 users registered")
                continue
            registration_details = {}
            username = input("what is the username >>")
            if username in values:
                print("This username already exists")
                continue
            password = input("what is the password? >>")
            registration_details[username] = password
            values.update(registration_details)
            save_value(values, controlllers_data_filepath)
        elif user_input.lower() == "login":
            username_input = input("Username >>")
            if username_input not in values:
                clear_screen()
                print("User doesn't exists")
                numberOfFailures += 1
                continue

            password_input = input("Password >>")
            if not values[username_input] == password_input:
                print("Wrong password")
                numberOfFailures += 1
                continue
            os.system("cls" if os.name == "nt" else "clear")
            return username_input
    else:
        os.system("cls" if os.name == "nt" else "clear")
        return None

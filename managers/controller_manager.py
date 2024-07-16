import bcrypt

from utils.cli import clear_screen, select_from_list
from utils.textfiles_database import load_data, save_value

controlllers_data_filepath = "data/controllers.txt"


def controller_manager():
    numberOfFailures = 0
    try:
        user_hash_map = load_data(controlllers_data_filepath)
    except Exception:
        user_hash_map = {}
    while numberOfFailures < 3:
        user_input = select_from_list(
            "Controller System: Please choose an option", ["Login", "Register"]
        )

        if user_input.lower() == "register":
            if len(user_hash_map) >= 4:
                clear_screen()
                print(
                    "[Error]: There has already been 4 users registered, please login as admin and remove a user before registering!"
                )
                continue
            registration_details = {}
            username = input("Please enter your username: ")
            if username in user_hash_map:
                clear_screen()
                print(f'[Error]: Username "{username}" already exists')
                continue
            password = input("Please enter your password: ")
            registration_details[username] = hash(password)
            user_hash_map.update(registration_details)
            save_value(user_hash_map, controlllers_data_filepath)
            clear_screen()
            print(f'[Controller Manager]: Registered user "{username}" successfully!')
        elif user_input.lower() == "login":
            username_input = input("Username: ")
            if username_input not in user_hash_map:
                clear_screen()
                print("User doesn't exists")
                numberOfFailures += 1
                continue

            password_input = input("Password: ")
            match = check_password(password_input, user_hash_map[username_input])
            if not match:
                clear_screen()
                print(f"[Error]: Invalid password for {username_input}!")
                numberOfFailures += 1
                continue
            clear_screen()
            return username_input
    else:
        clear_screen()
        return None


def hash(password):
    # Hashes the password with a random salt
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed


def check_password(password, hashed_password):
    match = bcrypt.checkpw(password.encode("utf-8"), hashed_password)
    return match

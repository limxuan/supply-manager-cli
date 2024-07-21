from getpass import getpass

from utils.cli import clear_screen, select_from_list
from utils.dependencies import bcrypt, tabulate
from utils.textfiles_database import load_data, save_value

controllers_data_filepath = "data/controllers.txt"


def controller_manager():
    numberOfFailures = 0
    try:
        user_hash_map = load_data(controllers_data_filepath)
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
            password = getpass("Please enter your password: ")
            clear_screen()
            password_confirmation = getpass("Please re-enter your password: ")
            if password != password_confirmation:
                print("[Error]: password confirmation and password doesn't match!")
                continue
            registration_details[username] = hash(password)
            user_hash_map.update(registration_details)
            save_value(user_hash_map, controllers_data_filepath)
            clear_screen()
            print(f'[Controller Manager]: Registered user "{username}" successfully!')
        elif user_input.lower() == "login":
            username_input = input("Username: ")
            if username_input not in user_hash_map:
                clear_screen()
                print("User doesn't exists")
                numberOfFailures += 1
                continue

            password_input = getpass("Password: ")
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


def retrieve_controllers() -> dict:
    controller_data = load_data(controllers_data_filepath)
    return controller_data


def remove_controller() -> str:
    controller_data = retrieve_controllers()
    options = list(controller_data.keys())
    options.remove("admin")
    options.append("Cancel")

    controller_to_remove = select_from_list(
        "Which controller do you want to remove?", options
    )

    if controller_to_remove == "Cancel":
        return None

    controller_data.pop(controller_to_remove)
    save_value(controller_data, controllers_data_filepath)
    return controller_to_remove


def print_removed_controllers():
    removed_controller = remove_controller()
    # check if removed_conrroller is none
    clear_screen()
    if removed_controller is None:
        print("[Controller Manager]: Action cancelled successfully")
    else:
        print(f"[Controller Manager] {removed_controller} has been removed")


def print_controllers():
    controllers = retrieve_controllers()
    output_table = []
    clear_screen()
    print("[Controller manager]: List of controllers:")
    for username in controllers:
        output_table.append([username])

    print(
        tabulate(
            output_table,
            headers=["Username"],
            showindex=range(1, len(controllers) + 1),
            tablefmt="simple_grid",
        )
    )


def hash(password):
    # Hashes the password with a random salt
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed


def check_password(password, hashed_password):
    match = bcrypt.checkpw(password.encode("utf-8"), hashed_password)
    return match

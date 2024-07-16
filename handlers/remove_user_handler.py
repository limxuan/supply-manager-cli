from handlers.continue_handler import continue_handler
from utils.cli import clear_screen, select_from_list
from utils.textfiles_database import load_data, save_value

controllers_data_filepath = "data/controllers.txt"


def remove_user_handler(controller):
    controllers = load_data(controllers_data_filepath)
    exclude_admin = list(controllers.keys())
    exclude_admin.remove("admin")
    if len(exclude_admin) == 0:
        print("There are no controllers to remove.")
    else:
        controller_to_remove = select_from_list(
            "Which controller do you want to remove", exclude_admin
        )
        confirmation = select_from_list(
            f'Are you sure you want to remove controller "{controller_to_remove}"',
            ["Yes", "No"],
        )
        if confirmation == "Yes":
            controllers.pop(controller_to_remove)
            save_value(controllers, controllers_data_filepath)
            clear_screen()
            print(f'Removed controller "{controller_to_remove}" successfully!')

    continue_handler(controller)

from handlers.continue_handler import continue_handler
from managers.controller_manager import (print_controllers,
                                         print_removed_controllers)
from utils.cli import select_from_list

controllers_file_path = "data/controllers.txt"


def admin_handler(controller):
    choices = ["View all controllers", "Remove a controller"]
    choice = select_from_list("What action would you like to take", choices)

    if choice == choices[0]:
        print_controllers()

    elif choice == choices[1]:
        print_removed_controllers()

    continue_handler(controller)

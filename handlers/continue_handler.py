from utils.cli import select_from_list, clear_screen


def continue_handler(controller):
    choices = ["Yes", "Exit the program"]

    print(">>\n")
    choice = select_from_list("Do you wish to continue?", choices)

    if choice == choices[0]:
        from handlers.action_handler import action_handler

        clear_screen()
        action_handler(controller)
    elif choice == choices[1]:
        from handlers.exit_handler import exit_handler

        exit_handler(controller)

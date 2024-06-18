from utils.cli import select_from_list, clear_screen


def continue_handler(controller):
    choices = ["Yes", "Exit the program"]

    print(">>\n")
    choice = select_from_list("Do you wish to continue?", choices)

    if choice == choices[0]:
        from handlers.choose_action import choose_action

        clear_screen()
        choose_action(controller)
    elif choice == choices[1]:
        from handlers.exit import exit_handler

        exit_handler(controller)

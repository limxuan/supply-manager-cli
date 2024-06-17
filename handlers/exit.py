from utils.cli import clear_screen


def exit_handler(controller):
    clear_screen()
    print(f"Goodbye {controller}")
    exit()

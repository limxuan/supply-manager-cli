from utils.cli import clear_screen


def exit_handler(controller):
    clear_screen()
    print(f"[System Message]: Goodbye {controller}!")
    exit()

from systems.controller import controller_selector
from utils.cli import clear_screen
from systems.choose_action import choose_action


def controller_login() -> str | None:
    controller = controller_selector()
    if controller:
        print(f"[Controller]: Logged in as {controller} successfully")
        return controller
    else:
        print("You have been terminated because 3 consecutive failed login attempts")
        return None


# Login System
def main():
    clear_screen()
    controller = controller_login()
    if controller is None:
        return

    choose_action(controller)


main()
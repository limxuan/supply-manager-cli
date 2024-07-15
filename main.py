from handlers.action_handler import action_handler
from managers.controller_manager import controller_manager
from utils.cli import clear_screen


def controller_login() -> str | None:
    controller = controller_manager()
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

    action_handler(controller)


main()

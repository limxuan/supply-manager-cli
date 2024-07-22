import os
from time import sleep

from utils.dependencies import inquirer


def select_from_list(question: str, options: list, back_button=True) -> str:
    options = list(options)
    if back_button == True:
        options.append("[Back]")
    prompt_content = [inquirer.List("x", message=question, choices=options)]
    result = inquirer.prompt(prompt_content)["x"]
    if result == "[Back]":
        return "Back"
    return result


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def go_back(controller):
    from handlers.action_handler import action_handler

    clear_screen()

    print("Going back to homepage..")
    sleep(0.8)

    clear_screen()
    action_handler(controller)

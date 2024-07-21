import os

from utils.dependencies import inquirer


def select_from_list(question: str, options: list) -> str:
    prompt_content = [inquirer.List("x", message=question, choices=options)]
    results = inquirer.prompt(prompt_content)
    return results["x"]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

import re


def get_between_parantheses(text: str) -> list:
    return re.findall(r"\((.+)\)", text)


def convert_to_snake_case(text: str) -> str:
    return "_".join(text.lower().split(" "))

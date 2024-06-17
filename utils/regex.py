import re


def get_between_parantheses(text: str) -> list:
    return re.findall(r"\((.+)\)", text)

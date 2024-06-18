from utils.prompts import prompt_for_items
from managers.distribution_manager import print_distributions
from handlers.continue_handler import continue_handler


def search_handler(controller):
    item = prompt_for_items("Which item are you searching for?")
    print_distributions(item["item_code"])

    continue_handler(controller)

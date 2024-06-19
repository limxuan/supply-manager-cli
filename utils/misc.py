from datetime import datetime
from managers.inventory_manager import retrieve_inventory, retrieve_item
from utils.cli import select_from_list
from utils.text_manipulation import get_between_parantheses


def prompt_for_items(question) -> dict:
    inventory = retrieve_inventory()
    item_selection = []
    for entry in inventory:
        item_selection.append(
            f"{entry['item_name']} ({entry['item_code']}) - {entry['quantity']} boxes"
        )

    unparsed_item_code = select_from_list(question, item_selection)
    item_code = get_between_parantheses(unparsed_item_code)[0]
    item = retrieve_item(item_code)
    return item


def timestamp_tostring(timestamp) -> str:
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")


def timestamp_to_monthyear(timestamp) -> str:
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%B %Y")

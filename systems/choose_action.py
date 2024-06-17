from utils.cli import select_from_list
from handlers.update_inventory import update_inventory_handler
from handlers.exit import exit_handler


def choose_action(controller):
    action = select_from_list(
        "What action do you want to perform?",
        [
            "Update Inventory",
            "Update Supplier Details",
            "Update Hospital Details" "Item Inventory Tracking",
            "Search Item",
            "Generate Report",
            "Exit",
        ],
    )

    handlers = {
        "Update Inventory": update_inventory_handler,
        "Update Supplier Details": print,
        "Update Hospital Details": print,
        "Item Inventory Tracking": print,
        "Search Item": print,
        "Generate Report": print,
        "Exit": exit_handler,
    }

    handlers[action](controller)

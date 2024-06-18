from utils.cli import select_from_list
from handlers.update_inventory import update_inventory_handler
from handlers.exit import exit_handler
from handlers.item_inventory_tracker import item_inventory_tracker_handler
from handlers.update_details import update_details_handler


def choose_action(controller):
    handlers = {
        "Distribute / Receive Supply": update_inventory_handler,
        "Update Details": update_details_handler,
        "Item Inventory Tracking": item_inventory_tracker_handler,
        "Search Item": print,
        "Generate Report": print,
        "Exit": exit_handler,
    }
    action = select_from_list("What action do you want to perform?", handlers.keys())

    handlers[action](controller)

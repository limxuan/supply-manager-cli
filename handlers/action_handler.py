from handlers.admin_handler import admin_handler
from handlers.details_handler import details_handler
from handlers.exit_handler import exit_handler
from handlers.item_inventory_tracker import item_inventory_tracker_handler
from handlers.report_handler import report_handler
from handlers.search_handler import search_handler
from handlers.update_inventory import (distribute_inventory_handler,
                                       receive_supplies_handler)
from utils.cli import select_from_list


def action_handler(controller):

    handlers = {
        "Distribute Inventory": distribute_inventory_handler,
        "Receive Supplies": receive_supplies_handler,
        "Details (View / Update)": details_handler,
        "Item Inventory Tracking": item_inventory_tracker_handler,
        "Search": search_handler,
        "Generate Report": report_handler,
        "Exit": exit_handler,
    }
    if controller == "admin":
        handlers["Admin Actions"] = admin_handler
    action = select_from_list(
        "What action do you want to perform?", handlers.keys(), False
    )

    handlers[action](controller)

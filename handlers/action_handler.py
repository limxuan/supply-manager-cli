from handlers.admin_handler import admin_handler
from handlers.details_handler import details_handler
from handlers.exit_handler import exit_handler
from handlers.item_inventory_tracker import item_inventory_tracker_handler
from handlers.report_handler import report_handler
from handlers.search_handler import search_handler
from managers.distribution_manager import distribute_inventory
from managers.supplier_manager import receive_supplies
from utils.cli import select_from_list


def action_handler(controller):

    handlers = {
        "Distribute Inventory": distribute_inventory,
        "Receive Supplies": receive_supplies,
        "Details (View / Update)": details_handler,
        "Item Inventory Tracking": item_inventory_tracker_handler,
        "Search": search_handler,
        "Generate Report": report_handler,
        "Exit": exit_handler,
    }
    if controller == "admin":
        handlers["Admin Actions"] = admin_handler
    action = select_from_list("What action do you want to perform?", handlers.keys())

    handlers[action](controller)

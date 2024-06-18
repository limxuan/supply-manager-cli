from utils.cli import clear_screen, select_from_list
from systems.inventory_manager import retrieve_inventory


def item_inventory_tracker_handler(controller):
    clear_screen()
    action_selection = ["Quantity of All Items", "Items that has lesser than 25 boxes"]
    action = select_from_list(
        "[Inventory Manager]: Which action do you wish to perform?", action_selection
    )
    inventory = retrieve_inventory()
    clear_screen()

    if action == action_selection[0]:
        inventory.sort(key=lambda x: x["quantity"])
        print("[Inventory Manager]: List of items with quantity in ascending order: \n")
        for entry in inventory:
            print(
                f"{entry['item_name']} ({entry['item_code']}) - {entry['quantity']} boxes"
            )
    elif action == action_selection[1]:
        res = filter(lambda x: x["quantity"] < 25, inventory)
        filtered_list = list(res)
        if len(filtered_list) == 0:
            print("[Inventory Manager]: There are no items that has less than 25 boxes")
        else:
            print(
                "[Inventory Manager]: List of items with quantity is lesser than 25 boxes: \n"
            )
            for entry in filtered_list:
                print(
                    f"{entry['item_name']} ({entry['item_code']}) - {entry['quantity']} boxes"
                )

    from handlers.continue_handler import continue_handler

    continue_handler(controller)

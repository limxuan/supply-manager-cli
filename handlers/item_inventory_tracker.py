from tabulate import tabulate

from managers.inventory_manager import retrieve_inventory
from managers.supplier_manager import get_supplier_info
from utils.cli import clear_screen, go_back, select_from_list


def item_inventory_tracker_handler(controller):
    clear_screen()
    action_selection = [
        "Quantity of All Items",
        "Items that has lesser than 25 boxes",
        "Custom item quantity range",
    ]
    action = select_from_list(
        "[Inventory Manager]: Which action do you wish to perform?", action_selection
    )
    if action == "Back":
        return go_back(controller)
    inventory = retrieve_inventory()
    clear_screen()

    if action == action_selection[0]:
        inventory.sort(key=lambda x: x["quantity"])
        print("[Inventory Manager]: List of items with quantity in ascending order: \n")
        # item code, item name, item quantity, supplier
        display_items(inventory)
    elif action == action_selection[1]:
        res = filter(lambda x: x["quantity"] < 25, inventory)
        filtered_list = list(res)
        if len(filtered_list) == 0:
            print("[Inventory Manager]: There are no items that has less than 25 boxes")
        else:
            print(
                "[Inventory Manager]: List of items with quantity is lesser than 25 boxes: \n"
            )
            display_items(filtered_list)
    else:
        display_items_between_range(inventory)

    from handlers.continue_handler import continue_handler

    continue_handler(controller)


def get_valid_input(prompt):
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
        else:
            print("That is not a valid number")


def display_items_between_range(inventory):
    starting_range = get_valid_input("What is the starting range: ")
    ending_range = get_valid_input("What is the ending range: ")
    filtered_list = list(
        filter(lambda x: starting_range <= x["quantity"] <= ending_range, inventory)
    )
    if len(filtered_list) == 0:
        print(
            f"[Inventory Manager]: There are no items that fit in the range of ({starting_range} - {ending_range})"
        )
    else:
        display_items(filtered_list)


def display_items(data):
    output_table = []
    for entry in data:
        supplier = get_supplier_info(entry["supplier_code"])
        output_table.extend(
            [
                [
                    entry["item_code"],
                    entry["item_name"],
                    str(entry["quantity"]),
                    f"{supplier['supplier_company_name']} ({supplier['supplier_code']})",
                ]
            ]
        )
    print(
        tabulate(
            output_table,
            headers=["Item Code", "Item Name", "Quantity in boxes", "Supplier"],
            tablefmt="simple_grid",
        )
    )

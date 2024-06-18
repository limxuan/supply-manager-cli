from utils.cli import clear_screen, select_from_list
from utils.text_manipulation import get_between_parantheses
from systems.inventory_manager import (
    retrieve_inventory,
    distribute_inventory,
    retrieve_item,
    receive_supplies,
)
from systems.hospital_manager import retrieve_hospital_data, retrieve_hospital


def update_inventory_handler(controller):
    clear_screen()
    action = select_from_list(
        "What do you want to perform?", ["Distribute Items", "Receive Supply"]
    )
    inventory = retrieve_inventory()
    item_selection = []
    for entry in inventory:
        item_selection.append(
            f"{entry['item_name']} ({entry['item_code']}) - {entry['quantity']} boxes"
        )

    unparsed_item_code = select_from_list("Which item is involved?", item_selection)
    item_code = get_between_parantheses(unparsed_item_code)[0]
    item = retrieve_item(item_code)

    if action == "Distribute Items":
        quantity: int = 0
        while True:
            quantity = input("How much boxes are being distributed (numbers only) >> ")
            if quantity.isdigit():
                quantity = int(quantity)
                # Check if its distributing  that the currently avaiable
                if quantity < item["quantity"]:
                    break
                else:
                    print(
                        f"We only have {item['quantity']} boxes of {item['item_name']}"
                    )
            else:
                print("That is not a valid number")

        hospitals_data = retrieve_hospital_data()
        hospital_selection = []
        for entry in hospitals_data:
            hospital_selection.append(
                f"{entry['hospital_name']} ({entry['hospital_code']})"
            )

        unparsed_hospital_code = select_from_list(
            "Which hospital do you want to distribute to?", hospital_selection
        )
        hospital_code = get_between_parantheses(unparsed_hospital_code)[0]
        hospital = retrieve_hospital(hospital_code)

        res = distribute_inventory(item_code, hospital_code, quantity, controller)
        if res:
            clear_screen()
            print(
                f"[Inventory Manager]: Distributed {quantity} boxes of {item['item_name']} to {hospital['hospital_name']}"
            )

    elif action == "Receive Supply":
        quantity: int = 0
        while True:
            quantity = input("How much boxes are being supplied (numbers only) >> ")
            if quantity.isdigit():
                quantity = int(quantity)
                break
            else:
                print("That is not a valid number")

        res = receive_supplies(item_code, quantity, controller)
        if res:
            clear_screen()
            print(
                f"[Inventory Manager]: Received {quantity} boxes of {item['item_name']}, now we have {item['quantity'] + quantity} boxes!"
            )
    from handlers.continue_handler import continue_handler

    continue_handler(controller)

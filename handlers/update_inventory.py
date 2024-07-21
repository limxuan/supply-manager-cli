from managers.distribution_manager import distribute_inventory
from managers.hospital_manager import retrieve_hospital, retrieve_hospital_data
from managers.supplier_manager import receive_supplies
from utils.cli import clear_screen, select_from_list
from utils.misc import prompt_for_items
from utils.text_manipulation import get_between_parantheses


def distribute_inventory(controller):
    clear_screen()
    item = prompt_for_items("Which item are you performing it on?")
    quantity: int = 0
    while True:
        quantity = input("How much boxes are being distributed (numbers only) >> ")
        if not quantity.isdigit():
            print("That is not a valid number")
            continue
        quantity = int(quantity)
        # Check if its distributing  that the currently avaiable
        if quantity > item["quantity"]:
            print(f"We only have {item['quantity']} boxes of {item['item_name']}")
            continue
        break

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

    res = distribute_inventory(item["item_code"], hospital_code, quantity, controller)
    if res:
        clear_screen()
        print(
            f"[Inventory Manager]: Distributed {quantity} boxes of {item['item_name']} to {hospital['hospital_name']}"
        )


def receive_supplies(controller):
    clear_screen()
    item = prompt_for_items("Which item are you performing it on?")
    quantity: int = 0
    while True:
        quantity = input("How much boxes are being received (numbers only) >> ")
        if not quantity.isdigit():
            print("That is not a valid number")
            continue
        quantity = int(quantity)
        break
    res = receive_supplies(item["item_code"], quantity, controller)
    if res:
        clear_screen()
        print(f"[Inventory Manager]: Received {quantity} boxes of {item['item_name']}")

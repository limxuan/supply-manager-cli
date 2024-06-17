import time
from utils.textfiles_database import save_value, load_data
from utils.cli import select_from_list, clear_screen
from systems.supplier_manager import retrieve_supplier_codes

# Item code, name, suppliercode, quantity
ppe_data_filepath = "data/ppe.txt"
distribution_data_filepath = "data/distribution_transactions.txt"


def inventory_initial_creation():
    ppe_list = []
    entries = {
        "HC": "Head Cover",
        "FS": "Face Shield",
        "MS": "Mask",
        "GL": "Gloves",
        "GW": "Gown",
        "SC": "Shoe Covers",
    }

    supplier_codes = retrieve_supplier_codes()
    if len(supplier_codes) == 0:
        print("Error: No valid supplier data in data/suppliers.txt")
        return

    for key in entries:
        supplier_code = select_from_list(
            f"Which supplier supplied {entries[key]}", supplier_codes
        )
        ppe_list.append(
            {
                "item_code": key,
                "item_name": entries[key],
                "supplier_code": supplier_code,
                "quantity": 100,
            }
        )
        clear_screen()

    save_value(ppe_list, ppe_data_filepath)


def retrieve_inventory() -> list:
    try:
        inventory = load_data(ppe_data_filepath)
    except Exception:
        inventory = []
    return inventory


def retrieve_item(item_code: str):
    inventory = retrieve_inventory()
    for entry in inventory:
        if entry["item_code"] == item_code:
            return entry
    else:
        return None


def add_item_quantity(item_code: str, num_to_add: int):
    inventory = retrieve_inventory()
    for entry in inventory:
        if entry["item_code"] == item_code:
            entry["quantity"] += num_to_add
    save_value(inventory, ppe_data_filepath)


def add_distribution(item_code, hospital_code, quantity, date, controller):
    try:
        distribution_data = load_data(distribution_data_filepath)
    except Exception:
        distribution_data = []

    entry = {
        "item_code": item_code,
        "hospital_code": hospital_code,
        "quantity": quantity,
        "date": date,
        "controller": controller,
    }
    distribution_data.append(entry)
    save_value(distribution_data, distribution_data_filepath)
    add_item_quantity(item_code, -quantity)


# - ppe Item Code, Hospital Code, Quantity, Date
def distribute_inventory(item_code, hospital_code, quantity, controller) -> bool:
    targetted_item = retrieve_item(item_code)
    if targetted_item is None:
        print("Error: item doesn't exist")
        return False

    if targetted_item["quantity"] < quantity:
        return False
    add_distribution(
        item_code=item_code,
        hospital_code=hospital_code,
        quantity=quantity,
        date=time.time(),
        controller=controller,
    )
    return True

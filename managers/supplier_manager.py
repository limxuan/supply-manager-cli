import time
from utils.textfiles_database import load_data, save_value
from managers.inventory_manager import add_item_quantity

supplier_data_filepath = "data/suppliers.txt"
supply_transactions_data_filepath = "data/supply_transactions.txt"


def retrieve_supplier_codes() -> list:
    try:
        supplier_data = load_data(supplier_data_filepath)
    except Exception:
        supplier_data = []

    supplier_codes = []
    for entry in supplier_data:
        supplier_codes.append(entry["supplier_code"])

    return supplier_codes


def get_supplier_info(supplier_code):
    try:
        supplier_data = load_data(supplier_data_filepath)
    except Exception:
        supplier_data = []

    for entry in supplier_data:
        if entry["supplier_code"] == supplier_code:
            return entry
    else:
        return None


def retreive_supplier_data() -> list:
    try:
        data = load_data(supplier_data_filepath)
    except Exception:
        data = []
    return data


def update_supplier_data(supplier_code, data):
    supplier_data = retreive_supplier_data()
    for i, entry in enumerate(supplier_data):
        if entry["supplier_code"] == supplier_code:
            supplier_data[i] = data

    print(supplier_data)

    save_value(supplier_data, supplier_data_filepath)


def receive_supplies(item_code, quantity, controller) -> bool:
    try:
        supply_transaction_data = load_data(supply_transactions_data_filepath)
    except Exception:
        supply_transaction_data = []
        return False

    entry = {
        "item_code": item_code,
        "quantity": quantity,
        "date": time.time(),
        "controller": controller,
    }
    supply_transaction_data.append(entry)
    save_value(supply_transaction_data, supply_transactions_data_filepath)
    add_item_quantity(item_code, quantity)
    return True


def retreive_supply_transactions_data() -> list:
    try:
        data = load_data(supply_transactions_data_filepath)
    except Exception:
        data = []
    return data

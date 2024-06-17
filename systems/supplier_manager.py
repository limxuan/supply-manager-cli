from utils.textfiles_database import load_data

supplier_data_filepath = "data/suppliers.txt"


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

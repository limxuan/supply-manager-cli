from utils.textfiles_database import load_data, save_value

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

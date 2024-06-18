from utils.textfiles_database import load_data, save_value

hospital_data_filepath = "data/hospitals.txt"


def retrieve_hospital_data() -> list:
    try:
        hospitals = load_data(hospital_data_filepath)
        return hospitals
    except Exception:
        hospitals = []
    return hospitals


def retrieve_hospital(hospital_code: str):
    inventory = retrieve_hospital_data()
    for entry in inventory:
        if entry["hospital_code"] == hospital_code:
            return entry
    else:
        return None


def retrieve_hospital_codes() -> list:
    try:
        supplier_data = load_data(hospital_data_filepath)
    except Exception:
        supplier_data = []

    supplier_codes = []
    for entry in supplier_data:
        supplier_codes.append(entry["hospital_code"])

    return supplier_codes


def update_hospital_data(hospital_code, data):
    hospital_data = retrieve_hospital_data()
    for i, entry in enumerate(hospital_data):
        if entry["hospital_code"] == hospital_code:
            hospital_data[i] = data

    save_value(hospital_data, hospital_data_filepath)

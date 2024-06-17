from utils.textfiles_database import load_data

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

import time

from tabulate import tabulate

from managers.hospital_manager import retrieve_hospital
from managers.inventory_manager import retrieve_item
from utils.cli import clear_screen, select_from_list
from utils.misc import timestamp_tostring
from utils.textfiles_database import load_data, save_value

distribution_transactions_data_filepath = "data/distribution_transactions.txt"


def add_distribution_transaction(item_code, hospital_code, quantity, date, controller):
    try:
        distribution_transaction_data = load_data(
            distribution_transactions_data_filepath
        )
    except Exception:
        distribution_transaction_data = []

    entry = {
        "item_code": item_code,
        "hospital_code": hospital_code,
        "quantity": quantity,
        "date": date,
        "controller": controller,
    }
    distribution_transaction_data.append(entry)
    save_value(distribution_transaction_data, distribution_transactions_data_filepath)
    from managers.inventory_manager import add_item_quantity

    add_item_quantity(item_code, -quantity)


# - ppe Item Code, Hospital Code, Quantity, Date
def distribute_inventory(item_code, hospital_code, quantity, controller) -> bool:
    from managers.inventory_manager import retrieve_item

    targetted_item = retrieve_item(item_code)
    if targetted_item is None:
        print("Error: item doesn't exist")
        return False

    if targetted_item["quantity"] < quantity:
        return False
    add_distribution_transaction(
        item_code,
        hospital_code,
        quantity,
        time.time(),
        controller,
    )
    return True


def retrieve_distribution_data():
    try:
        distribution = load_data(distribution_transactions_data_filepath)
    except Exception:
        distribution = []
    return distribution


def retrieve_distributions_from_item_code(item_code) -> list:
    distribution_data = retrieve_distribution_data()
    filtered = filter(lambda x: x["item_code"] == item_code, distribution_data)
    return list(filtered)


#  iii.	If the item has been distributed to the same hospital for more than once, then their quantities have to be summed up together.


def print_distributions(item_code: str):
    distribution_data = retrieve_distributions_from_item_code(item_code)
    summed_distribution_data = {}

    # syntax itemcode:hospitalcode
    for entry in distribution_data:
        key = entry["hospital_code"]
        if key in summed_distribution_data:
            summed_distribution_data[key] += entry["quantity"]
        else:
            summed_distribution_data[key] = entry["quantity"]

    item = retrieve_item(item_code)
    clear_screen()
    print(
        f'[Distribution Manager]: Distribution data for {item["item_name"]} ({item["item_code"]})\n'
    )
    output_table = []
    for hospital_code in summed_distribution_data:
        hospital = retrieve_hospital(hospital_code)
        output_table.append(
            [
                hospital_code,
                hospital["hospital_name"],
                summed_distribution_data[hospital_code],
            ]
        )
    print(
        tabulate(
            output_table,
            headers=["Hospital Code", "Hospital Name", "Quantity Distributed (boxes)"],
            tablefmt="mixed_grid",
        )
    )

    print(">>\n")
    options = ["Yes", "No"]
    option = select_from_list(
        "Do you want to view a detailed list of transactions along with the dates?",
        options,
    )

    if option == options[0]:
        transactions_table = []
        for entry in distribution_data:
            timestamp = entry["date"]
            readable_date_time = timestamp_tostring(timestamp)
            hospital = retrieve_hospital(entry["hospital_code"])
            transactions_table.append(
                [
                    readable_date_time,
                    entry["hospital_code"],
                    entry["quantity"],
                    entry["controller"],
                ]
            )

            # print(
            #     f'[{readable_date_time}] {entry["quantity"]} was distributed to {hospital["hospital_name"]} ({entry["hospital_code"]}) [Controller: {entry["controller"]}]'
            # )
        print(
            tabulate(
                transactions_table,
                headers=[
                    "Date & Time",
                    "Hospital Code",
                    "Quantity Distributed (boxes)",
                    "Controller",
                ],
            )
        )

from tabulate import tabulate

from handlers.continue_handler import continue_handler
from managers.distribution_manager import print_distributions
from managers.hospital_manager import retrieve_hospital_data
from managers.supplier_manager import retrieve_supplier_data
from utils.cli import clear_screen, select_from_list
from utils.misc import prompt_for_items
from utils.text_manipulation import get_between_parantheses


def search_handler(controller):
    options = ["Item", "Hospital", "Supplier"]
    selection = select_from_list("Which category do you want to search?", options)
    if selection == options[0]:
        search_item()
    elif selection == options[1]:
        search_hospital()
    elif selection == options[2]:
        search_supplier()

    continue_handler(controller)


def search_item():
    item = prompt_for_items("Which item are you searching for?")
    print_distributions(item["item_code"])


def search_hospital():
    hospital_data = retrieve_hospital_data()
    hospital_options = list(
        f"{hospital['hospital_name']} ({hospital['hospital_code']})"
        for hospital in hospital_data
    )
    hospital_selection = select_from_list(
        "Which hospital do you want to search?", hospital_options
    )
    hospital_code = get_between_parantheses(hospital_selection)[0]
    hospital = list(
        filter(lambda x: x["hospital_code"] == hospital_code, hospital_data)
    )[0]
    hospital_values = [hospital.values()]
    clear_screen()
    print(f"[Search Handler]: Hospital details for {hospital_selection}")
    print(
        tabulate(
            hospital_values,
            headers=["Hospital Code", "Hospital Name", "Hospital Address"],
            tablefmt="simple_grid",
        )
    )


def search_supplier():
    supplier_data = retrieve_supplier_data()
    supplier_options = list(
        f"{supplier['supplier_company_name']} ({supplier['supplier_code']})"
        for supplier in supplier_data
    )
    supplier_selection = select_from_list(
        "Which supplier do you want to search?", supplier_options
    )
    supplier_code = get_between_parantheses(supplier_selection)[0]
    supplier = list(
        filter(lambda x: x["supplier_code"] == supplier_code, supplier_data)
    )[0]
    supplier_values = [supplier.values()]
    clear_screen()
    print(f"[Search Handler]: Supplier details for {supplier_selection}")
    print(
        tabulate(
            supplier_values,
            headers=[
                "Supplier Code",
                "Supplier Person Name",
                "Supplier Company Name",
                "Supplier Address",
            ],
            tablefmt="simple_grid",
        )
    )

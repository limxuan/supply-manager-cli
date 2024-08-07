from tabulate import tabulate

from handlers.continue_handler import continue_handler
from managers.hospital_manager import (retrieve_hospital,
                                       retrieve_hospital_codes,
                                       update_hospital_data)
from managers.supplier_manager import (get_supplier_info,
                                       retrieve_supplier_codes,
                                       update_supplier_data)
from utils.cli import clear_screen, go_back, select_from_list
from utils.text_manipulation import (convert_to_snake_case,
                                     get_between_parantheses)
from utils.textfiles_database import load_data


def details_handler(controller):
    options = ["View Details", "Update Details"]
    option = select_from_list("What action do you wish to perform?", options)
    if option == "Back":
        return go_back(controller)
    if option == options[0]:
        view_details_handler(controller)
    else:
        update_details_handler(controller)
    continue_handler(controller)


def update_details_handler(controller):
    category_choices = ["Supplier", "Hospitals"]
    category_selection = select_from_list(
        "Which category are you looking to update?", category_choices
    )

    if category_selection == category_choices[0]:
        supplier_codes = retrieve_supplier_codes()
        supplier_choices = list(
            map(
                lambda x: get_supplier_info(x)["supplier_company_name"] + f" ({x})",
                supplier_codes,
            )
        )

        unparsed_supplier_selection = select_from_list(
            "Which supplier do you want to edit?", supplier_choices
        )
        if unparsed_supplier_selection == "Back":
            return go_back(controller)
        supplier_selection = get_between_parantheses(unparsed_supplier_selection)[0]
        supplier = get_supplier_info(supplier_selection)

        attribute_choices = [
            "Supplier Person Name",
            "Supplier Company Name",
            "Supplier Company Address",
        ]
        unparsed_attribute_selection = select_from_list(
            "Which attribute do you want to edit?", attribute_choices
        )
        if unparsed_attribute_selection == "Back":
            return go_back(controller)
        attribute_selection = convert_to_snake_case(unparsed_attribute_selection)
        value_input = input(
            f"What do you want to change the {unparsed_attribute_selection} to >> "
        )

        supplier[attribute_selection] = value_input
        update_supplier_data(supplier_selection, supplier)
        clear_screen()

        print(
            f"[Supplier Handler]: Updated {supplier_selection}'s {unparsed_attribute_selection} to {value_input}"
        )
    elif category_selection == category_choices[1]:
        hospital_codes = retrieve_hospital_codes()
        hospital_choices = list(
            map(
                lambda x: retrieve_hospital(x)["hospital_name"] + f" ({x})",
                hospital_codes,
            )
        )

        unparsed_hospital_selection = select_from_list(
            "Which supplier do you want to edit?", hospital_choices
        )
        if unparsed_hospital_selection == "Back":
            return go_back(controller)
        hospital_selection = get_between_parantheses(unparsed_hospital_selection)[0]
        hospital = retrieve_hospital(hospital_selection)

        attribute_choices = [
            "Hospital Name",
            "Hospital Address",
        ]
        unparsed_attribute_selection = select_from_list(
            "Which attribute do you want to edit?", attribute_choices
        )
        if unparsed_attribute_selection == "Back":
            return go_back(controller)
        attribute_selection = convert_to_snake_case(unparsed_attribute_selection)
        value_input = input(
            f"What do you want to change the {unparsed_attribute_selection} to >> "
        )

        hospital[attribute_selection] = value_input
        update_hospital_data(hospital_selection, hospital)
        clear_screen()

        print(
            f"[Hospital Handler]: Updated {hospital_selection}'s {unparsed_attribute_selection} to {value_input}"
        )
    elif category_selection == "Back":
        return go_back(controller)


def view_details_handler(controller):
    options = ["Items", "Hospitals", "Suppliers"]
    selection = select_from_list("Which category do you want to view?", options)
    if selection == "Back":
        return go_back(controller)
    heading = f"[Details Handler]: Details on {selection}"
    headers = []
    filepath = "data/"

    if selection == options[0]:
        headers.extend(["Item Code", "Item Name", "Supplier Code", "Quantity"])
        filepath += "ppe.txt"
    elif selection == options[1]:
        headers.extend(["Hospital Code", "Hospital Name", "Hospital Address"])
        filepath += "hospitals.txt"
    elif selection == options[2]:
        headers.extend(
            [
                "Supplier Code",
                "Supplier Person Name",
                "Supplier Company Name",
                "Supplier Address",
            ]
        )
        filepath += "suppliers.txt"

    raw_data = load_data(filepath)
    data = list(entry.values() for entry in raw_data)
    clear_screen()
    print(heading)
    print(
        tabulate(
            data,
            headers=headers,
            tablefmt="simple_grid",
            showindex=range(1, len(data) + 1),
        )
    )

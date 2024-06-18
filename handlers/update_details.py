from utils.cli import select_from_list, clear_screen
from utils.text_manipulation import convert_to_snake_case, get_between_parantheses
from systems.supplier_manager import (
    retrieve_supplier_codes,
    get_supplier_info,
    update_supplier_data,
)
from systems.hospital_manager import (
    retrieve_hospital_codes,
    update_hospital_data,
    retrieve_hospital,
)
from handlers.continue_handler import continue_handler


def update_details_handler(controller):
    category_choices = ["Supplier", "Hospitals"]
    category_selection = select_from_list(
        "Which category are you looking to update?", category_choices
    )

    if category_selection == category_choices[0]:
        supplier_codes = retrieve_supplier_codes()
        hospital_choices = list(
            map(
                lambda x: get_supplier_info(x)["supplier_company_name"] + f" ({x})",
                supplier_codes,
            )
        )

        unparsed_hospital_selection = select_from_list(
            "Which supplier do you want to edit?", hospital_choices
        )
        hospital_selection = get_between_parantheses(unparsed_hospital_selection)[0]
        hospital = get_supplier_info(hospital_selection)

        attribute_choices = [
            "Supplier Person Name",
            "Supplier Company Name",
            "Supplier Company Address",
        ]
        unparsed_attribute_selection = select_from_list(
            "Which attribute do you want to edit?", attribute_choices
        )
        attribute_selection = convert_to_snake_case(unparsed_attribute_selection)
        value_input = input(
            f"What do you want to change the {unparsed_attribute_selection} to >> "
        )

        hospital[attribute_selection] = value_input
        update_supplier_data(hospital_selection, hospital)
        clear_screen()

        print(
            f"[Supplier Handler]: Updated {hospital_selection}'s {unparsed_attribute_selection} to {value_input}"
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
        hospital_selection = get_between_parantheses(unparsed_hospital_selection)[0]
        hospital = retrieve_hospital(hospital_selection)

        attribute_choices = [
            "Hospital Name",
            "Hospital Address",
        ]
        unparsed_attribute_selection = select_from_list(
            "Which attribute do you want to edit?", attribute_choices
        )
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

    continue_handler(controller)

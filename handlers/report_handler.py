from managers.inventory_manager import retrieve_inventory, retrieve_item
from managers.supplier_manager import (
    get_supplier_info,
    retreive_supply_transactions_data,
)
from managers.distribution_manager import retrieve_distribution_data
from managers.hospital_manager import retrieve_hospital
from utils.cli import clear_screen, select_from_list
from utils.misc import timestamp_tostring, timestamp_to_monthyear
from handlers.continue_handler import continue_handler


def report_handler(controller):
    options = [
        "List of suppliers along with their PPE equipments",
        "List of hospitals with quantity of distribution items.",
        "Overall transaction report for a month",
    ]
    selection = select_from_list("Which report do you want to have a look at?", options)
    if selection == options[0]:
        suppliers_and_equipments()
    elif selection == options[1]:
        hospitals_and_distributions()
    elif selection == options[2]:
        distributions_and_supplies_month()

    continue_handler(controller)


def distributions_and_supplies_month():
    date_data_map = {}

    # Get all availabe distributions
    distribution_data = retrieve_distribution_data()

    # Record all unique months
    for entry in distribution_data:
        month_year = timestamp_to_monthyear(entry["date"])
        hospital_code = entry["hospital_code"]
        item_code = entry["item_code"]
        quantity = entry["quantity"]
        # Initialise month_year key in date_data_map if it doesn't exist
        if month_year not in date_data_map:
            date_data_map[month_year] = {
                "distribution_transactions": {},
            }
        # Check if distribution_transanctions attribute has been previously initialised
        # Initialize distribution_transactions for the month_year
        if "distribution_transactions" not in date_data_map[month_year]:
            date_data_map[month_year]["distribution_transactions"] = {}

        # Initialize hospital_code entry if not present
        if hospital_code not in date_data_map[month_year]["distribution_transactions"]:
            date_data_map[month_year]["distribution_transactions"][hospital_code] = {
                "items": {},
                "total_quantity": 0,
            }

        # Initialize item_code entry if not present and add total_quantity
        if (
            item_code
            not in date_data_map[month_year]["distribution_transactions"][
                hospital_code
            ]["items"]
        ):
            date_data_map[month_year]["distribution_transactions"][hospital_code][
                "items"
            ][item_code] = 0
        if (
            "total_quantity"
            not in date_data_map[month_year]["distribution_transactions"][hospital_code]
        ):
            date_data_map[month_year]["distribution_transactions"][hospital_code][
                item_code
            ] = 0
        date_data_map[month_year]["distribution_transactions"][hospital_code]["items"][
            item_code
        ] += quantity
        date_data_map[month_year]["distribution_transactions"][hospital_code][
            "total_quantity"
        ] += quantity

    # Get Supplies Transactions
    supplies_data = retreive_supply_transactions_data()

    for entry in supplies_data:
        if month_year not in date_data_map:
            date_data_map[month_year] = {
                "supply_transactions": {"total_quantity": 0, "items": {}},
            }

        if "supply_transactions" not in date_data_map[month_year]:
            date_data_map[month_year]["supply_transactions"] = {
                "total_quantity": 0,
                "items": {},
            }

        # Initialize item code in the items dictionary if it doesn't exist
        if (
            entry["item_code"]
            not in date_data_map[month_year]["supply_transactions"]["items"]
        ):
            date_data_map[month_year]["supply_transactions"]["items"][
                entry["item_code"]
            ] = 0

        # Add quantity to the item code
        date_data_map[month_year]["supply_transactions"]["items"][
            entry["item_code"]
        ] += entry["quantity"]

        # Add quantity to the total
        date_data_map[month_year]["supply_transactions"]["total_quantity"] += entry[
            "quantity"
        ]

    valid_month_years = date_data_map.keys()
    month_year_selection = select_from_list(
        "Which month do you want a report on?", valid_month_years
    )
    clear_screen()

    print(f"[Report Handler]: Distributions for {month_year_selection}\n")
    map_value = date_data_map[month_year_selection]

    # Print distributions
    print("(Distributions)")
    if "distribution_transactions" not in map_value:
        print("   No distributions!")
    else:
        distribution_transactions = map_value["distribution_transactions"]
        for index, hospital_code in enumerate(distribution_transactions):
            hospital = retrieve_hospital(hospital_code)
            print(
                f"{index + 1}. {hospital['hospital_name']}\n   Address: {hospital['hospital_address']}"
            )
            print(
                f'   Total distributions: {distribution_transactions[hospital_code]["total_quantity"]} boxes'
            )
            for item_code in distribution_transactions[hospital_code]["items"]:
                item = retrieve_item(item_code)
                print(
                    f'     - {item["item_name"]} ({item_code}): {distribution_transactions[hospital_code]["items"][item_code]} boxes'
                )
            print("\n")

    print("(Supply Received)")
    if "supply_transactions" not in map_value:
        print("   No supply received!")
    else:
        supply_transactions = map_value["supply_transactions"]
        print(
            f"Total supply boxes received: {map_value['supply_transactions']['total_quantity']} boxes"
        )
        for index, item_code in enumerate(supply_transactions["items"]):
            item = retrieve_item(item_code)
            print(
                f'   {index + 1}. {item["item_name"]} {supply_transactions["items"][item_code]} boxes'
            )
            supplier = get_supplier_info(item["supplier_code"])
            print(f'      Supplier: {supplier["supplier_company_name"]}')


def suppliers_and_equipments():
    # Get all available items
    inventory = retrieve_inventory()

    # Loop over each inventory to add unique supplier codde
    supplier_items_map = {}
    for item in inventory:
        print(supplier_items_map)
        key = item["supplier_code"]
        if key in supplier_items_map:
            supplier_items_map[key].append(item)
        else:
            supplier_items_map[key] = [item]

    clear_screen()
    print("[Report Handler]: Supplier along with their equipments supplied\n")
    for supplier_code in supplier_items_map:
        supplier = get_supplier_info(supplier_code)
        print(
            f'[Supplier Code: {supplier["supplier_code"]}] {supplier["supplier_company_name"]} ({supplier["supplier_person_name"]})'
        )

        for index, item in enumerate(supplier_items_map[supplier_code]):
            print(f"\t{index + 1}) {item['item_name']} (Code: {item['item_code']})")
        print("\n")


def hospitals_and_distributions():
    # Get all distributions
    distribution_data = retrieve_distribution_data()
    view_transaction_report_input = select_from_list(
        "Do you want to view every single transaction log aswell?",
        ["Yes", "No (Show the summarised report)"],
    )
    view_transaction_report = view_transaction_report_input == "Yes"

    # Loop over each distribution to find unique hospitals
    # Structure
    """
    {
        hospital_code: string
        total_quantity_distributed: number
        transactions: [{item, quantity, date, controller}]
    }
    """
    hospital_distribution_map = {}
    for entry in distribution_data:
        # {'item_code': 'HC', 'hospital_code': 'H1', 'quantity': 4, 'date': 1718633537.693726, 'controller': 'heh'}
        key = entry["hospital_code"]
        map_value = {
            "item": retrieve_item(entry["item_code"]),
            "quantity": entry["quantity"],
            "date": timestamp_tostring(entry["date"]),
            "controller": entry["controller"],
        }
        if key in hospital_distribution_map:
            hospital_distribution_map[key]["total_quantity_distributed"] += entry[
                "quantity"
            ]
            hospital_distribution_map[key]["transactions"].append(map_value)
        else:
            hospital_distribution_map[key] = {
                "total_quantity_distributed": entry["quantity"],
                "transactions": [map_value],
            }

    clear_screen()
    print(
        "[Report Handler]: Hospital along with the items that was distributed to them\n"
    )
    for key in hospital_distribution_map:
        hospital = retrieve_hospital(key)
        print(
            f'[Hospital Code: {hospital["hospital_code"]}] {hospital["hospital_name"]} @ ({hospital["hospital_address"]})'
        )
        print(
            f"Total quantity of boxes supplied: {hospital_distribution_map[key]['total_quantity_distributed']}"
        )

        if view_transaction_report:
            print("Transactions:")
            for transaction in hospital_distribution_map[key]["transactions"]:
                print(
                    f"\t[{transaction['date']}] ({transaction['quantity']} boxes) {transaction['item']['item_name']} (Code: {transaction['item']['item_code']}) - (Controller: {transaction['controller']})"
                )
        print("\n")

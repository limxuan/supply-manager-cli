from tabulate import tabulate

from handlers.continue_handler import continue_handler
from managers.distribution_manager import retrieve_distribution_data
from managers.hospital_manager import retrieve_hospital
from managers.inventory_manager import retrieve_inventory, retrieve_item
from managers.supplier_manager import (
    get_supplier_info,
    retreive_supply_transactions_data,
)
from utils.cli import clear_screen, go_back, select_from_list
from utils.misc import timestamp_to_monthyear, timestamp_tostring
from utils.tables import create_table_extend, tabularize


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
        distributions_and_supplies_month(controller)
    elif selection == "Back":
        return go_back()

    continue_handler(controller)


def distributions_and_supplies_month(controller):
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
    if month_year_selection == "Back":
        return go_back(controller)
    clear_screen()

    print(
        f"[Report Handler]: Distributions & Supplies Report for {month_year_selection}\n"
    )
    map_value = date_data_map[month_year_selection]
    if "distribution_transactions" in map_value:
        distribution_data = map_value["distribution_transactions"]
        # Hospital, total distributions, item(s)
        distribution_table = []
        total_distributions = 0

        # Loop over every single hospital in data
        for entry in distribution_data:
            hospital_code = entry
            hospital = retrieve_hospital(hospital_code)
            entry_value = distribution_data[hospital_code]
            total_distributions = entry_value["total_quantity"]
            items = entry_value["items"]
            hospital_table = [
                f"{hospital['hospital_name']} ({hospital_code})",
                f"{total_distributions} boxes",
            ]
            items_distributed = []
            for item_code in items:
                item = retrieve_item(item_code)
                items_distributed.append(
                    f"{item['item_name']} ({item_code}) - {items[item_code]} boxes"
                )
                total_distributions += items[item_code]
            hospital_table.insert(1, "\n".join(items_distributed))
            distribution_table.append(hospital_table)
        print(f"Total distributions: {total_distributions} boxes")
        print(
            tabulate(
                distribution_table,
                headers=["Hospital", "Item(s) distributed", "Total distributed"],
                tablefmt="simple_grid",
                showindex=range(1, len(distribution_table) + 1),
            )
        )

    else:
        print("No distribution transactions found.")

    print("\n")

    # Print supply transactions
    if "supply_transactions" in map_value:
        supply_data = map_value["supply_transactions"]
        total_quantity = supply_data["total_quantity"]
        items = supply_data["items"]
        print(f"Supply received: {total_quantity} boxes")
        # Item Code, Item Name, Item Quantity, Supplied by
        supply_table = []
        for item_code in items:
            column = []
            item = retrieve_item(item_code)
            supplier = get_supplier_info(item["supplier_code"])
            column.append(item_code)
            column.append(item["item_name"])
            column.append(f"{ items[item_code] } boxes")
            column.append(
                f"{supplier['supplier_company_name']} ({supplier['supplier_code']})"
            )
            supply_table.append(column)
        print(
            tabulate(
                supply_table,
                headers=["Item Code", "Item Name", "Quantity Received", "Supplied by"],
                tablefmt="simple_grid",
                showindex=range(1, len(supply_table) + 1),
            )
        )

    else:
        print("No supply transactions found.")


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
    output_table = []
    for supplier_code in supplier_items_map:
        supplier = get_supplier_info(supplier_code)
        to_append = [supplier_code, supplier["supplier_company_name"]]
        item_list = supplier_items_map[supplier_code]
        to_append.extend(
            create_table_extend(item_list, ["item_code", "item_name", "quantity"])
        )
        output_table.append(to_append)
    print(
        tabularize(
            output_table,
            headers=[
                "Supplier Code",
                "Supplier Name",
                "Item Code",
                "Item Name",
                "Current Quantity (Boxes)",
            ],
        )
    )


def hospitals_and_distributions():
    # Get all distributions
    distribution_data = retrieve_distribution_data()
    view_transaction_report_input = select_from_list(
        "Would you wish to see every single transaction recorded?",
        ["Yes", "No (Show the summarised report)"],
        False,
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
        hospital_code = entry["hospital_code"]
        item = retrieve_item(entry["item_code"])
        map_value = {
            "item": item,
            "supplier_data": get_supplier_info(item["supplier_code"]),
            "quantity": entry["quantity"],
            "date": timestamp_tostring(entry["date"]),
            "controller": entry["controller"],
        }
        if hospital_code in hospital_distribution_map:
            hospital_distribution_map[hospital_code][
                "total_quantity_distributed"
            ] += entry["quantity"]
            hospital_distribution_map[hospital_code]["transactions"].append(map_value)
        else:
            hospital_distribution_map[hospital_code] = {
                "total_quantity_distributed": entry["quantity"],
                "transactions": [map_value],
            }

    clear_screen()
    print(
        "[Report Handler]: Hospital along with the items that was distributed to them\n"
    )
    for idx, hospital_code in enumerate(hospital_distribution_map):
        hospital = retrieve_hospital(hospital_code)
        hospital_output = [
            f"{idx + 1}. {hospital['hospital_name']}",
            f"   Total distributions: {hospital_distribution_map[hospital_code]['total_quantity_distributed']} boxes",
            f"   Hospital Code: { hospital['hospital_code'] }",
            f'   Hospital Address:{hospital["hospital_address"] }',
            "",
        ]
        print("\n".join(hospital_output))

        if view_transaction_report:
            print("Transactions:")
            transaction_table = []
            transactions = hospital_distribution_map[hospital_code]["transactions"]
            transaction_table.append(
                create_table_extend(
                    transactions,
                    [
                        "date",
                        "item.item_code",
                        "item.item_name",
                        "supplier_data.supplier_code",
                        "supplier_data.supplier_company_name",
                        "quantity",
                        "controller",
                    ],
                )
            )
            print(
                tabularize(
                    transaction_table,
                    [
                        "Date & Time",
                        "Item Code",
                        "Item Name",
                        "Supplier Code",
                        "Company Name",
                        "Quantity Distributed",
                        "Controller",
                    ],
                    numbering=False,
                )
            )

        print("\n")

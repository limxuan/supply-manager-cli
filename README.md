# 🏥 Supply Manager CLI

![demo](https://vyn0b0z4rp.ufs.sh/f/q9IVYNuY13wnPfz8rtqRHGYxrKjP5EwysOktImfliJMXaS8A)

A command-line inventory management system acting as a **middleware** between suppliers and hospital distributors. This tool helps track, distribute, and report inventory activities effectively with secure and structured data storage.
## 🚀 Features

- 🔐 Password encryption for secure access
- 📦 Receive supplies from suppliers
- 🚚 Distribute inventory to hospitals
- 🧾 Full transaction logs for audit and tracking
- 🔍 View, search, or update details:
  - Items
  - Hospitals
  - Suppliers
- 📊 Generate Reports:
  - List of suppliers and the items they supply
  - List of hospitals and the items distributed to them
  - Monthly summary of all supply and distribution transactions
- 💾 Text-based JSON storage (no external database required)

## ⚙️ Installation & Running

1. Install the required dependencies:

```bash
pip3 install -r requirements.txt
```

2. Run the application:

```bash
python3 main.py
```

## 🛠️ Technologies Used

- **Python** – Core programming language used to build the CLI
- **Inquirer** – For creating interactive terminal menus
- **JSON** – Used as the format for storing structured data in text files


## 📁 Data Storage

All data (inventory, suppliers, hospitals, and transactions) is stored in **JSON-formatted text files** locally. This makes the system lightweight and easy to maintain without the need for external databases.
## 👨‍⚕️ Use Case

Designed for use in hospital networks or logistics departments to ensure:
- Transparency in medical supply distribution
- Efficient stock and transaction tracking
- Clear reporting for accountability and planning

# things to talk about

research about json data structure how its better to store data with it
password hashing
displaying data with tables

# additional features

-   [x] Back Button for all selections
-   [x] installs dependencies if not found
-   [x] password
    -   [x] hashing with bcrypt
    -   [x] hide password input with getpass
    -   [x] second confirmation for password during registration
-   [x] change to table displaying data w/tabulate
-   [x] view all supplier details
-   [x] view all hospital details
-   [x] Search
    -   [x] search for items
    -   [x] search for hospitals
    -   [x] search for suppliers
-   [x] Item inventory tracking
    -   [x] Lesser than what a user specified
-   [x] admin controls
    -   [x] remove user
    -   [x] view all controllers (admin only)

# List of files modified

```
a/handlers/action_handler.py b/handlers/action_handler.py
a/handlers/admin_handler.py b/handlers/admin_handler.py
a/handlers/continue_handler.py b/handlers/continue_handler.py
a/handlers/details_handler.py b/handlers/details_handler.py
a/handlers/item_inventory_tracker.py b/handlers/item_inventory_tracker.py
a/handlers/remove_user_handler.py b/handlers/remove_user_handler.py
a/handlers/report_handler.py b/handlers/report_handler.py
a/handlers/search_handler.py b/handlers/search_handler.py
a/handlers/update_details.py b/handlers/details_handler.py
a/handlers/update_inventory.py b/handlers/update_inventory.py
a/main.py b/main.py
a/managers/controller_manager.py b/managers/controller_manager.py
a/managers/distribution_manager.py b/managers/distribution_manager.py
a/managers/supplier_manager.py b/managers/supplier_manager.py
a/utils/cli.py b/utils/cli.py
a/utils/inquirer.py b/utils/dependencies.py
a/utils/misc.py b/utils/misc.py
a/utils/tables.py b/utils/tables.py
```

### Inventory Tracking System Command Structure

1. **Distribute or Receive Supplies**

    - `Distribute items ` - Distribute an item to a hospital
    - `Receive supplies` - Receive supplies from a supplier

2. **Update Details**

    - `Update Supplier Details` - Update supplier details
    - `Update Hospital Details` - Update hospital details

3. **Item Inventory Tracking**

    - `Inventory all` - List all available items
    - `Inventory less than 25` - List items under 25 quantity
    - `Inventory custom quantity filter` - List items that has a quantity between what the user specified

4. **Search**

    - `search item` - Search item and list distributions to hospitals
    - `search hospital` - Search and view hospital details
    - `search supplier` - Search and view supplier details

5. **Generate Report**

    - `report month` - Generate supply and distribution report for a certain month

6. **Admin Controls**

    - `Remove Controller` - Remove a user
    - `View Controllers` - View all controllers

7. **View Details**

    - `view` - View details of suppliers, hospitals, or items
        - `view inventory` - View details of all inventory
        - `view supplier` - View details of all suppliers
        - `view hospital` - View details of all hospitals

8. **Exit**
    - `exit` - Quit the program

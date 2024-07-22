
# things to talk about
research about json data structure how its better to store data with it
password hashing
displaying data with tables


# additional features
- [x] Back Button for all selections
- [x] installs dependencies if not found
- [x] password 
  - [x] hashing with bcrypt
  - [x] hide password input with getpass
  - [x] second confirmation for password during registration
- [x] change to table displaying data w/tabulate
- [x] view all supplier details
- [x] view all hospital details
- [x] Search
  - [x] search for items
  - [x] search for hospitals
  - [x] search for suppliers
- [x] Item inventory tracking
  - [x] Lesser than what a user specified
- [x] admin controls
  - [x] remove user
  - [x] view all controllers (admin only)


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

8. **View Details**
    - `view` - View details of suppliers, hospitals, or items
        - `view inventory` - View details of all inventory
        - `view supplier` - View details of all suppliers
        - `view hospital` - View details of all hospitals

9. **Exit**
    - `exit` - Quit the program

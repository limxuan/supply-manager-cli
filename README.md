
# things to talk about
research about json data structure how its better to store data with it
password hashing
displaying data with tables

# TODO 
- [ ] refactor manager and handler
- [ ] password confirmation when registration

# additional features
- [x] password hashing with bcrypt
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

# list of files modified
- handlers
  - action_handler
  - remove_user_handler
  - item_inventory_tracker
  - report_handler
- managers
  - controller_manager
  - distribution_manager
- utils
  - tables.py

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

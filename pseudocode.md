# Todos
- load_data

```
function main() {
  // imported from utilities
  clear_screen()

  controller = controller_login()
  // Stops the process of controller is none
  if controller is None 
    Stop the process

  // Starts the panel of action to allow the controller to perform tasks
  action_handler(controller)
}
```

# Managers
// Typically displays the main panel of actions for a certain function
## Controller Manager
```
FUNCTION controller_manager
    SET numberOfFailures TO 0
    SET controllerData TO CALL load_data WITH controlllers_data_filepath

    WHILE numberOfFailures < 3
        SET user_input TO CALL select_from_list WITH "Controller System: Please choose an option" AND ["Login", "Register"]

        // Registration system
        IF user_input.lower() IS EQUAL TO "register" THEN
            IF LENGTH OF controllerData IS GREATER THAN OR EQUAL TO 4 THEN
                CALL clear_screen
                PRINT "[Error]: There has already been 4 users registered"
                CONTINUE WHILE

            // initialise registration_details
            SET registration_details TO empty dictionary
            SET username TO INPUT "what is the username >>"

            IF username IS IN controllerData THEN
                PRINT "This username already exists"
                CONTINUE WHILE

            SET password TO INPUT "what is the password? >>"
            SET registration_details[username] TO password
            APPEND registration_details TO controllerData
            CALL save_value WITH controllerData AND controlllers_data_filepath

        // Login system
        ELSE IF user_input.lower() IS EQUAL TO "login" THEN
            SET username_input TO INPUT "Username >>"

            IF username_input IS NOT IN controllerData THEN
                CALL clear_screen
                PRINT "User doesn't exist"
                INCREMENT numberOfFailures
                CONTINUE WHILE

            SET password_input TO INPUT "Password >>"

            IF controllerData[username_input] IS NOT EQUAL TO password_input THEN
                PRINT "Wrong password"
                INCREMENT numberOfFailures
                CONTINUE WHILE

            CALL clear_screen
            RETURN username_input

    ELSE
        CALL clear_screen
        RETURN None
    END WHILE
END FUNCTION
```
## Distribution Manager
```

FUNCTION add_distribution_transaction(item_code, hospital_code, quantity, date, controller)
    SET distribution_transaction_data TO load_data(distribution_transactions_data_filepath) defaults to empty list

    SET entry TO dictionary with keys:
        "item_code" : item_code
        "hospital_code" : hospital_code
        "quantity" : quantity
        "date" : date
        "controller" : controller

    APPEND entry TO distribution_transaction_data
    CALL save_value WITH distribution_transaction_data AND distribution_transactions_data_filepath

    CALL add_item_quantity WITH item_code AND -quantity
END FUNCTION
```
```
FUNCTION distribute_inventory(item_code, hospital_code, quantity, controller) -> boolean:
    TRY:
        targetted_item = CALL retrieve_item WITH item_code
    EXCEPT Exception:
        PRINT "Error: item doesn't exist"
        RETURN False
    
    IF targetted_item IS None THEN
        PRINT "Error: item doesn't exist"
        RETURN False
    
    IF targetted_item["quantity"] < quantity THEN
        RETURN False
    
    CALL add_distribution_transaction WITH item_code, hospital_code, quantity, CURRENT_TIME(), controller
    RETURN True
END FUNCTION

```

```
FUNCTION retrieve_distribution_data()
    TRY
        distribution = CALL load_data WITH distribution_transactions_data_filepath
    EXCEPT Exception
        distribution = empty list
    RETURN distribution
END FUNCTION

```



# Utilities
## Cli Tools
### Clear Screen
// Clears the terminal screen for better UX
```
function clear_screen() {
  if name of os == "nt" {
    run "cls"
  } else {
    run "clear"
  }
}
```

## Controller 
### Login
// Register / Login 
// Returns a controller (string) if logged in successfully
```
function controller_login() {
  // imported from controller manager
  controller = controller_manager()
  
  if controller logged in successfully {
    OUTPUT "Logged in as {controller}"
    returns controller
  } else {
    OUTPUT "You have been terminated because of 3 consecutive failed login attempts"
    returns None
  }
}
```
## Database
### Save Data
// Save data to filepath
```
function save_value(input_value, filepath) {
  convert input_value to a string
  file = open file in filepath
  write input_value to filepath
}
```

### Load Data
// Retrieve JSON data from filepath
```
function load_data(filepath) {
  file = open file in filepath
  file_contents = read file
  // we store data using JSON in txt files
  json_data = evaluate file_contents to JSON
  return json_data
}
```

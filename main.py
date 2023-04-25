import database
import customer
import books
import order

db = database.Database("project.db")
cr = customer.Customer(db)

def leave(db, cr, code=0):
    print("Exiting program.")
    exit(code)

menu_system = {
    "Welcome Menu": {
        "Login":          customer.loginMenu,
        "Create Account": customer.createAccountMenu,
        "Exit":           leave
    },
    "Main Menu": {
        "Edit Account": customer.infoMenu,
        "Logout":       customer.logoutMenu,
        "Exit":         leave
    },
    "Edit Account": {
        "Go Back":   "Main Menu",
        "Current Account Information": customer.infoMenu,
        "Edit Name": (customer.setCustomerMenu, ["your name", cr.setName]),
        "Edit Username": (customer.setCustomerMenu, ["a username", cr.setUsername]),
        "Edit Email": (customer.setCustomerMenu, ["an email address", cr.setEmail]),
        "Edit Password": customer.changePasswordMenu,
        "Edit Card Info": (customer.setCustomerMenu, ["your credit card number", cr.setCCNumber]),
        "Edit Address": (customer.setCustomerMenu, ["your address", cr.setAddress]),
        "Delete Account": customer.deleteMenu,
    }
}

def main(menu_system, db, cr):
    current_menu_name = "Welcome Menu"

    custom_menu_name = None
    custom_menu_options = None

    while True:
        print()

        if custom_menu_name:
            print(custom_menu_name)
            current_menu_options = custom_menu_options
        else:
            print(current_menu_name)
            current_menu_options = menu_system[current_menu_name]

        options = []
        for number, key in enumerate(current_menu_options.keys()):
            print(f"{number+1}: {key}")
            options.append(current_menu_options[key])

        try:
            selection = int(input("Please select from the options above: "))

            if selection <= 0:
                raise ValueError

            if selection > len(options):
                raise ValueError

            selection -= 1

        except ValueError:
            print()
            print("Please enter a valid option.")
            continue

        def navigate_to(menu_name):
            nonlocal current_menu_name
            nonlocal custom_menu_name

            if menu_name in menu_system.keys():
                current_menu_name = menu_name
                custom_menu_name = None
            else:
                print()
                print("There appears to be a problem with this sub menu.")
                print("Please try another option.")

        def execute_func(func_name, func_args=[]):
            nonlocal custom_menu_name
            nonlocal custom_menu_options
            nonlocal db
            nonlocal cr

            print()
            menu, options = func_name(db, cr, *func_args)

            if options:
                custom_menu_name = menu
                custom_menu_options = options

            if menu:
                navigate_to(menu)

        if callable(options[selection]):
            execute_func(options[selection])
        elif type(options[selection]) is str:
            navigate_to(options[selection])
        elif type(options[selection]) is tuple:
            if len(options[selection]) == 2:
                if callable(options[selection][0]) and type(options[selection][1]) is list:
                    execute_func(options[selection][0], options[selection][1])
                    continue
            print()
            print("There appears to be a problem with this option.")
            print("Please try another option.")
        else:
            print()
            print("There appears to be a problem with this option.")
            print("Please try another option.")

if __name__ == "__main__":
    try:
        main(menu_system, db, cr)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        exit(1)

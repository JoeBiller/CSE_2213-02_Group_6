import database
import customer
import books
import order
import shoppingCart

db = database.Database("project.db")
cr = customer.Customer(db)
bks = books.Books(db)
crt = shoppingCart.ShoppingCart(db, bks)
odr = order.Order(db, cr, bks, crt)

def leave(code=0):
    print("Exiting program.")
    exit(code)

menu_system = {
    "Welcome Menu": {
        "Login":          (customer.loginMenu, (cr,)),
        "Create Account": (customer.createAccountMenu, (cr,)),
        "Exit":           leave
    },
    "Main Menu": {
        "Browse All Books": (books.getBooksMenu, (cr, bks, crt)),
        "Browse Books by Category": (books.selectCategoryMenu, (cr, bks, crt)),
        "Cart Information": (shoppingCart.viewCartMenu, (cr, bks, crt)),
        "View Order History": (order.orderHistoryMenu, (bks, odr,)),
        "Edit Account": (customer.infoMenu, (cr,)),
        "Logout":       (customer.logoutMenu, (cr,)),
        "Exit":         leave
    },
    "Cart Options": {
        "Go Back": "Main Menu",
        "Remove Book from Cart": (shoppingCart.removeCartMenu, (cr, bks, crt)),
        "Checkout": (order.checkoutMenu, (odr,))
    },
    "Edit Account": {
        "Go Back":   "Main Menu",
        "Current Account Information": (customer.infoMenu, (cr,)),
        "Edit Name": (customer.setCustomerMenu, (cr, "your name", cr.setName)),
        "Edit Email": (customer.setCustomerMenu, (cr, "an email address", cr.setEmail)),
        "Edit Password": (customer.changePasswordMenu, (cr,)),
        "Edit Card Info": (customer.setCustomerMenu, (cr, "your credit card number", cr.setCCNumber)),
        "Edit Address": (customer.setCustomerMenu, (cr, "your address", cr.setAddress)),
        "Delete Account": (customer.deleteMenu, (cr,)),
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
            menu, options = func_name(*func_args)

            if options:
                custom_menu_name = menu
                custom_menu_options = options
            elif menu:
                navigate_to(menu)
            elif not menu and not options:
                pass
            else:
                print()
                print("There appears to be a problem with this option.")
                print("Please try another option.")

        if callable(options[selection]):
            execute_func(options[selection])
        elif type(options[selection]) is str:
            navigate_to(options[selection])
        elif type(options[selection]) is tuple:
            if len(options[selection]) == 2:
                if callable(options[selection][0]) and type(options[selection][1]) is tuple:
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

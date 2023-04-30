from getpass import getpass

class Customer:
    def __init__(self, db):
        self.__db = db

        self.__name     = ""
        self.__username = ""
        self.__email    = ""
        self.__address  = ""
        self.__ccNumber = ""
        self.__password = ""
        self.__loggedIn = False

    def usernameTaken(self, username):
        response = self.__db.cursor.execute("SELECT * FROM customers WHERE username = ?", (username,))
        if response.fetchone():
            return True
        else:
            return False

    def emailTaken(self, email):
        response = self.__db.cursor.execute("SELECT * FROM customers WHERE email = ?", (email,))
        if response.fetchone():
            return True
        else:
            return False

    def __getCustomerTuple(self):
        return (self.__name,
                self.__username,
                self.__email,
                self.__address,
                self.__ccNumber,
                self.__password)

    def createAccount(self, name, username, email, address, ccNumber, password):
        if not self.__loggedIn:
            if not (self.usernameTaken(username) or self.emailTaken(email)):
                self.__name     = name
                self.__username = username
                self.__email    = email
                self.__address  = address
                self.__ccNumber = ccNumber
                self.__password = password

                self.__db.cursor.execute("INSERT INTO customers VALUES(?, ?, ?, ?, ?, ?)", 
                                         self.__getCustomerTuple())
                self.__db.connection.commit()

                self.__loggedIn = True
                return True, f"Account created. Welcome {username}."
            else:
                return False, "Either username or email has already been taken."
        else:
            return False, "You are logged in."

    def __saveCustomer(self, username):
        response = self.__db.cursor.execute("UPDATE customers SET name = ?, username = ?, email = ?, address = ?, ccNumber = ?, password = ? WHERE username = ?", self.__getCustomerTuple() + (username,))
        self.__db.connection.commit()

    def setEmail(self, email):
        if self.__loggedIn:
            if not email:
                return False, "You must specify an email."
            if not self.emailTaken(email):
                self.__email = email
                self.__saveCustomer(self.__username)
                return True, f"Your email is now {self.__email}."
            else:
                return False, "Email is already taken."
        else:
            return False, "You are not logged in."

    def setName(self, name):
        if self.__loggedIn:
            self.__name = name
            self.__saveCustomer(self.__username)
            if name:
                return True, f"Your name is now {self.__name}."
            else:
                return True, f"Your name has been removed."
        else:
            return False, "You are not logged in."

    def setAddress(self, address):
        if self.__loggedIn:
            self.__address = address
            self.__saveCustomer(self.__username)
            if address:
                return True, f"Your address is now {self.__address}."
            else:
                return True, f"Your address has been removed."
        else:
            return False, "You are not logged in."

    def setCCNumber(self, ccNumber):
        if self.__loggedIn:
            self.__ccNumber = ccNumber
            self.__saveCustomer(self.__username)
            if ccNumber:
                return True, f"Your credit card has been set."
            else:
                return True, f"Your credit card has been removed."
        else:
            return False, "You are not logged in."

    def setPassword(self, old_password, new_password):
        if self.__loggedIn:
            if not new_password:
                return False, "You must specify a new password."
            if self.__password == old_password:
                self.__password = new_password
                self.__saveCustomer(self.__username)
                return True, f"Your password has been changed."
            else:
                return False, "Incorrect old password."
        else:
            return False, "You are not logged in."

    def getName(self):
        return self.__name

    def getUsername(self):
        return self.__username

    def getEmail(self):
        return self.__email

    def getAddress(self):
        return self.__address

    def getCCNumber(self):
        return self.__ccNumber

    def deleteAccount(self, username):
        if self.__loggedIn:
            if self.__username == username:
                self.logout()
                self.__db.cursor.execute("DELETE FROM customers WHERE username = ?", (username,))
                self.__db.cursor.execute("DELETE FROM shoppingCart WHERE username = ?", (username,))
                self.__db.cursor.execute("DELETE FROM orders WHERE username = ?", (username,))
                self.__db.connection.commit()
                return True, f"Account successfully deleted. Goodbye forever {username}."
            else:
                return False, "Please type in your username to confirm."
        else:
            return False, "Something went wrong. Please try again later."

    def __loadCustomer(self, username):
        response = self.__db.cursor.execute("SELECT * FROM customers WHERE username = ?", (username,))
        raw_data = response.fetchone()
        if raw_data:
            self.__name     = raw_data[0]
            self.__username = raw_data[1]
            self.__email    = raw_data[2]
            self.__address  = raw_data[3]
            self.__ccNumber = raw_data[4]
            self.__password = raw_data[5]
            return True
        else:
            return False

    def login(self, username, password):
        if not self.__loggedIn:
            if self.usernameTaken(username):
                if self.__loadCustomer(username):
                    self.__loggedIn = True
                    if self.__password == password:
                        return True, f"You are now logged in. Welcome {self.__username}."
                    else:
                        self.logout()
                        return False, "Incorrect password."
                else:
                    return False, "Something went wrong. Please try again later."
            else:
                return False, f"No account exists under the username {username}."
        else:
            return False, "You are already logged in."

    def logout(self):
        if self.__loggedIn:
            username = self.__username

            self.__name     = ""
            self.__username = ""
            self.__email    = ""
            self.__address  = ""
            self.__ccNumber = ""
            self.__password = ""

            self.__loggedIn = False
            return True, f"You are now logged out. Goodbye {username}."
        else:
            return False, "You are already logged out."

def createAccountMenu(cr):
    username         = None
    email            = None
    password         = None
    password_confirm = None

    while not username:
        username = input("Please type in a username: ")
        if cr.usernameTaken(username):
            print("Username already in use.")
            username = None

    while not email:
        email = input("Please type in an email address: ")
        if cr.emailTaken(email):
            print("Email already in use.")
            email = None

    while not password:
        password = getpass("Please type in a password: ")

    while not password_confirm:
        password_confirm = getpass("Please type in password again: ")

    if password != password_confirm:
        print()
        print("Passwords do not match.")
        return "Welcome Menu", None

    success, message = cr.createAccount(None, username, email, None, None, password)

    if success:
        print()
        print(message)
        return "Main Menu", None
    else:
        print()
        print(message)
        return "Welcome Menu", None

def logoutMenu(cr):
    success, message = cr.logout()
    if success:
        print()
        print(message)
        return "Welcome Menu", None
    else:
        print()
        print(message)
        return "Main Menu", None

def loginMenu(cr):
    username = None
    password = None

    while not username:
        username = input("Please type in your username: ")
        if not cr.usernameTaken(username):
            print("No account exists under that username.")
            username = None

    while not password:
        password = getpass("Please type in your password: ")

    success, message = cr.login(username, password)
    if success:
        print()
        print(message)
        return "Main Menu", None
    else:
        print()
        print(message)
        return "Welcome Menu", None

def deleteMenu(cr):
    print("WARNING: Account deletion is permanent!")
    print("Press enter to cancel.")
    print()

    username = input("Please enter your username to confirm delete: ")

    success, message = cr.deleteAccount(username)

    if success:
        print()
        print(message)
        return "Welcome Menu", None
    else:
        print()
        print(message)
        return "Edit Account", None

def infoMenu(cr):
    def printPretty(name, value, hidden=False):
        if value:
            if not hidden:
                print(f"{name}: {value}")
            else:
                print(f"{name}: {value[-4:]}")
        else:
            print(f"{name}: [Not Set]")

    print("Current Account Information")
    printPretty("Name", cr.getName())
    printPretty("Username", cr.getUsername())
    printPretty("Email", cr.getEmail())
    printPretty("Address", cr.getAddress())
    printPretty("Credit Card (last four digits)", cr.getCCNumber(), True)

    return "Edit Account", None

def changePasswordMenu(cr):
    old_password     = None
    new_password     = None
    password_confirm = None

    while not old_password:
        old_password = getpass("Please type in your old password: ")

    while not new_password:
        new_password = getpass("Please type in your new password: ")

    while not password_confirm:
        password_confirm = getpass("Please type in your new password again: ")

    if new_password != password_confirm:
        print()
        print("New passwords do not match.")
        return "Edit Account", None

    success, message = cr.setPassword(old_password, new_password)

    print()
    print(message)

    return "Edit Account", None

def setCustomerMenu(cr, text, func):
    value = input(f"Please type in {text}: ")

    success, message = func(value)

    print()
    print(message)

    print()
    return infoMenu(cr)

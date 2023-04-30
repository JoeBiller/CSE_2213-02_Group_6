class Order:
    def __init__(self, db, cr, bks, crt):
        self.__db = db
        self.__cr = cr
        self.__bks = bks
        self.__crt = crt

    def __getHigestOrderNumber(self):
       response = self.__db.cursor.execute("SELECT * FROM orders")
       orders = response.fetchall()
       highest = 1
       for order in orders:
           if order[0] > highest:
               highest = order[0]
       return highest + 1

    def createOrder(self):
        username = self.__cr.getUsername()
        address = self.__cr.getAddress()
        ccNumber = self.__cr.getCCNumber()
        if not username:
            return False, "You are not logged in."
        if not address:
            return False, "You must set an address for your account."
        if not ccNumber:
            return False, "You must set a credit card number for your account."
        cart_items = self.__crt.viewCart(username)
        if cart_items:
            order_number = self.__getHigestOrderNumber()
            for item in cart_items:
                book = self.__bks.getBookByISBN(item[1])
                if int(item[2]) <= int(book[7]):
                    self.__db.cursor.execute("INSERT INTO orders VALUES(?, ?, ?, ?, ?, ?)",
                        (order_number, item[0], item[1], item[2], ccNumber[-4:], address))
                    self.__crt.removeCart(username, item[1])
                    self.__bks.setAmount(str(int(book[7]) - int(item[2])), item[1])
                else:
                    return False, f'Not enough stock for "{book[4]}" by {book[5]} ({book[2]}).'
            self.__db.connection.commit()
            return True, "Order successfully created."
        else:
            return False, "No items to checkout."

    def getOrderHistory(self):
        username = self.__cr.getUsername()
        if not username:
            return False, "You are not logged in."
        response = self.__db.cursor.execute("SELECT * FROM orders WHERE username = ?", (username,))
        return response.fetchall()

def checkoutMenu(odr):
    success, message = odr.createOrder()

    print()
    print(message)

    return "Cart Options", None

def orderDetailsMenu(bks, order_items):
    print(f"Books in Order #{order_items[0][0]}")
    for order_item in order_items:
        book = bks.getBookByISBN(order_item[2])
        print(f'Qty: {order_item[3]} Price: ${book[6]} - "{book[4]}" by {book[5]} ({book[2]}) - {book[3]}')
    print()
    print(f"Last for digits of credit card used to make purchase: {order_items[0][4]}")
    print(f"This order was shipped to {order_items[0][5]}.")
    return None, None

def orderHistoryMenu(bks, odr):
    order_menu = {}

    order_menu["Go Back"] = "Main Menu"

    order_numbers = {}
    order_items = odr.getOrderHistory()
    for order_item in order_items:
        if order_item[0] not in order_numbers.keys():
            order_numbers[order_item[0]] = []
            order_numbers[order_item[0]].append(order_item)
        else:
            order_numbers[order_item[0]].append(order_item)

    for order_number in order_numbers.keys():
        order_length = len(order_numbers[order_number])
        s = ""
        if order_length > 1:
            s = "s"
        order_menu[f"Order #{order_number}: Contains {order_length} item{s}."] = (orderDetailsMenu, (bks, order_numbers[order_number]))

    return "Order History", order_menu

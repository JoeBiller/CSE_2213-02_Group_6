class ShoppingCart:
    def __init__(self, db, bks):
        self.__db = db
        self.__bks = bks

    def __getItemQuantity(self, username, isbn):
        response = self.__db.cursor.execute("SELECT * FROM shoppingCart WHERE username = ? AND isbn = ?", (username, isbn))
        item = response.fetchone()
        if item:
            return item[2]
        else:
            return 0

    def addCart(self, username, isbn, quantity):
        current_quantity = self.__getItemQuantity(username, isbn)
        if current_quantity:
            if quantity + current_quantity <= int(self.__bks.getBookByISBN(isbn)[7]):
                self.__db.cursor.execute("UPDATE shoppingCart SET quantity = ? WHERE username = ? and isbn = ?", (current_quantity + quantity, username, isbn))
                self.__db.connection.commit()
                return True
            else:
                return False
        else:
            if quantity <= int(self.__bks.getBookByISBN(isbn)[7]):
                self.__db.cursor.execute("INSERT INTO shoppingCart VALUES(?, ?, ?)", (username, isbn, quantity))
                self.__db.connection.commit()
                return True
            else:
                return False

    def removeCart(self, username, isbn):
        current_quantity = self.__getItemQuantity(username, isbn)
        if current_quantity:
            self.__db.cursor.execute("DELETE FROM shoppingCart WHERE username = ? AND isbn = ?", (username, isbn))
            self.__db.connection.commit()
            return True
        else:
            return False

    def viewCart(self, username):
        response = self.__db.cursor.execute("SELECT * FROM shoppingCart WHERE username = ?", (username,))
        return response.fetchall()

def removeCartMenu(cr, bks, crt, isbn=None):
    if isbn:
        success = crt.removeCart(cr.getUsername(), isbn)
        if success:
            print()
            print("Book removed from cart!")
        else:
            print()
            print("Book not in cart!")

    remove_menu = {}

    remove_menu["Go Back"] = (viewCartMenu, (cr, bks, crt))

    cart_items = crt.viewCart(cr.getUsername())
    for item in cart_items:
        book = bks.getBookByISBN(item[1])
        remove_menu[f'"{book[4]}" by {book[5]} ({book[2]})'] = (removeCartMenu, (cr, bks, crt, item[1]))

    return "Select a Book to Remove", remove_menu

def viewCartMenu(cr, bks, crt):
    cart_items = crt.viewCart(cr.getUsername())

    if cart_items:    
        print("Current Books in Cart")
    else:
        print("No Books in Cart")
    for item in cart_items:
        book = bks.getBookByISBN(item[1])
        print(f'Qty: {item[2]} Price: ${book[6]} - "{book[4]}" by {book[5]} ({book[2]}) - {book[3]}')

    return "Cart Options", None

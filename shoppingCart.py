import database
import customer
import books
import order

class shoppingCart:
    def __init__(self, db):
        self.__db = db
        self.__username = ""
        self.__itemISBN = ""
        self.__itemPrice = ""
        self.__itemTitle = ""
        self.__itemQuantity = ""

    def __getCartTuple(self):
        return (self.__username,
                self.__itemISBN,
                self.__itemPrice,
                self.__itemTitle,
                self.__itemQuantity)

    def addCart(self, username, isbn, quantity):

        if quantity < books.getAmmount(isbn):
            self.__username = username
            self.__itemISBN = isbn
            self.__itemPrice = books.getPrice(isbn)
            self.__itemTitle = books.getTitle(isbn)
            self.__itemQuantity = quantity

            books.setAmmount(isbn, books.getAmmount(isbn) - quantity, isbn)

            self.__db.cursor.execute("INSERT INTO shoppingCart VALUES(?, ?, ?, ?, ?)", self.__getCartTuple(self))
            self.__db.connection.commit()
            return True
        else:
            return False

    def removeCart(self, username, isbn):
        self.__db.cursor.execute("DELETE FROM shoppingCart WHERE username = ?, isbn = ?", (username, isbn, ))

    def viewCart(self, username):
        response = self.__db.cursor.execute("SELECT * FROM shoppingCart WHERE username = ?", (username, ))
        return response.fetchall()

    def getQuantity(self, username):
        quantityTotal = 0

        # This is very incorrect, but I am looking into how to iterate this to get an accurate total.
        quantityTotal += self.__db.cursor.execute("SELECT quantity FROM shoppingCart WHERE username = ?", (username, ))
        return quantityTotal

    def checkoutCart(self, username):
        # Not quite sure what this is exactly supposed to do, so I just set it up to delete everything out of the user's cart
        self.__db.cursor.execute("DELETE FROM shoppingCart WHERE username = ?", (username, ))

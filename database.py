import sqlite3

class Database:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor     = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS customers(name, username, email, address, ccNumber, password)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS books(ISBN, publisher, year, genre, title, author, price, amount)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS shoppingCart(username, ISBN, quantity)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS orders(orderID, username, ISBN, quantity, lastCC, address)")

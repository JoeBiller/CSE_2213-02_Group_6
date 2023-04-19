import sqlite3

class Database:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor     = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS customers(name, username, email, address, ccNumber, password)")

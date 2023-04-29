#Books class

class Books:
    def __init__(self, db):
        self.__db = db

        self.__ISBN     = ""
        self.__publisher = ""
        self.__year    = ""
        self.__genre  = ""
        self.__title = ""
        self.__price = ""
        self.__amount = ""

#Getters
    def getGenre(self):
        return self.__genre

    def getPublisher(self):
        return self.__publisher

    def getYear(self):
        return self.__year

    def getTitle(self):
        return self.__title

    def getISBN(self):
        return self.__ISBN

    def getAmount(self):
        return self.__amount

    def __getBooksTuple(self):
        return (self.__genre,
            self.__publisher,
            self.__year,
            self.__title,
            self.__ISBN,
            self.__price,
            self.__amount)

#Setters
    def setAmount(self, amount, isbn):
        self.__db.cursor.execute("UPDATE books SET amount = ? WHERE ISBN = ?", (amount, isbn))

#Check if ISBN exists (Primary key of books, no duplicates)
    def ISBNTaken(self, ISBN):
        response = self.__db.cursor.execute("SELECT * FROM books WHERE ISBN = ?", (ISBN,))
        if response.fetchone():
            return True
        else:
            return False

    def addBookMessage(db, cr):
        print("Adding new book")

    def getAllBooks(self):
        response = self.__db.cursor.execute("SELECT * FROM books")
        return response.fetchall()
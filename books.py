#Books class

class Books:
    def __init__(self, db):
        self.__db = db

        self.__ISBN     = 0
        self.__publisher = ""
        self.__year    = 0
        self.__genre  = ""
        self.__title = ""
        self.__price = 0.0
        self.__amount = 0

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
        self.__db.cursor.execute("UPDATE books SET amount = {amount} WHERE ISBN = {isbn}")

#Check if ISBN exists (Primary key of books, no duplicates)
    def ISBNTaken(self, ISBN):
        response = self.__db.cursor.execute("SELECT * FROM books WHERE ISBN = ?", (ISBN,))
        if response.fetchone():
            return True
        else:
            return False

#Add book to inventory
    def addBook(self, genre, publisher, year, title, ISBN, price, amount):
        if not (self.ISBN(ISBN)):
            self.__genre     = genre
            self.__publisher = publisher
            self.__year      = year
            self.__title     = title
            self.__ISBN      = isbn
            self.__price     = price
            self.__amount    = amount

            self.__db.cursor.execute("INSERT INTO books VALUES(?, ?, ?, ?, ?, ?)", 
            self.__getBooksTuple())
            self.__db.connection.commit()

            return True, f"Book {title} added. ISBN:{isbn}."
        else:
            return False, "A book with this ISBN already exists!"


def addBookMenu(db, cr, br):

    genre = input("Please input the genre of the book: ")
    publisher = input("Please input the publisher of the book: ")
    year = input("Please input the year of the book: ")
    title = input("Please input the title of the book: ")
    ISBN = input("Please input the ISBN of the book: ")
    price = input("Please input the price of the book: ")
    amount = input("Please input the amount of the book: ")


    success, message = br.addBook(genre, publisher, year, title, ISBN, price, amount)

    print()
    print(message)

    return None, None

def addBookMessage(db, cr, br):
    print("Adding new book")
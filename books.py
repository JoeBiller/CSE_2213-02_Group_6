import shoppingCart

class Books:
    def __init__(self, db):
        self.__db = db

#Setters
    def setAmount(self, amount, isbn):
        self.__db.cursor.execute("UPDATE books SET amount = ? WHERE ISBN = ?", (amount, isbn,))

#Check if ISBN exists (Primary key of books, no duplicates)
    def ISBNTaken(self, isbn):
        response = self.__db.cursor.execute("SELECT * FROM books WHERE ISBN = ?", (isbn,))
        if response.fetchone():
            return True
        else:
            return False

    def getBookByISBN(self, isbn):
        response = self.__db.cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        return response.fetchone()

    def getAllBooks(self):
        response = self.__db.cursor.execute("SELECT * FROM books")
        return response.fetchall()

    def getBooksByGenre(self, genre):
        response = self.__db.cursor.execute("SELECT * FROM books WHERE genre = ?", (genre,))
        return response.fetchall()

    def getGenres(self):
        books = self.getAllBooks()
        genres = []
        for book in books:
            if book[3] not in genres:
                genres.append(book[3])
        return genres

def addCartMenu(db, cr, bks, username, isbn, bk_menu):
    crt = shoppingCart.ShoppingCart(db, bks)
    success = crt.addCart(username, isbn, 1)
    if success:
        print()
        print("Book added to cart!")
    else:
        print()
        print("Not enough in stock!")
    return "Book Options", bk_menu

def removeCartMenu(db, cr, bks, username, isbn, bk_menu):
    crt = shoppingCart.ShoppingCart(db, bks)
    success = crt.removeCart(username, isbn)
    if success:
        print()
        print("Book removed from cart!")
    else:
        print()
        print("Book not in cart!")
    return "Book Options", bk_menu

def showBookMenu(db, cr, bks, book, return_genre):
    print("Book Information")
    print(f"Title: {book[4]}")
    print(f"Author: {book[5]}")
    print(f"Year: {book[2]}")
    print(f"Genre: {book[3]}")
    print(f"Publisher: {book[1]}")
    print(f"ISBN: {book[0]}")
    print(f"Price: ${book[6]}")
    print(f"Amount: {book[7]}")

    bk_menu = {}

    if return_genre:
        bk_menu["Go Back"] = (getBooksMenu, [return_genre])
    else:
        bk_menu["Go Back"] = getBooksMenu

    bk_menu["Add Book to Cart"] = (addCartMenu, [bks, cr.getUsername(), book[0], bk_menu])
    bk_menu["Remove Book to Cart"] = (removeCartMenu, [bks, cr.getUsername(), book[0], bk_menu])

    return "Book Options", bk_menu

def getBooksMenu(db, cr, genre=None):
    bks = Books(db)

    bks_menu = {}
    bks_title = ""

    bks_menu["Go Back"] = "Main Menu"

    if genre:
        books = bks.getBooksByGenre(genre)
        bks_title = f"By Category: {genre}"
    else:
        books = bks.getAllBooks()
        bks_title = "All Books"

    for book in books:
        bks_menu[f'"{book[4]}" by {book[5]} ({book[2]}) - ${book[6]} - {book[3]}'] = (showBookMenu, [bks, book, genre])

    return bks_title, bks_menu

def selectCategoryMenu(db, cr):
    bks = Books(db)

    genres_menu = {}

    genres_menu["Go Back"] = "Main Menu"

    for genre in bks.getGenres():
        genres_menu[genre] = (getBooksMenu, [genre])

    return "Select a Genre to Browse", genres_menu

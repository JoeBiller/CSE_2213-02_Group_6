class Books:
    def __init__(self, db):
        self.__db = db

    def setAmount(self, amount, isbn):
        self.__db.cursor.execute("UPDATE books SET amount = ? WHERE ISBN = ?", (amount, isbn,))

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

def addCartMenu(crt, username, isbn):
    success = crt.addCart(username, isbn, 1)
    if success:
        print()
        print("Book added to cart!")
    else:
        print()
        print("Not enough in stock!")
    return None, None

def removeCartMenu(crt, username, isbn):
    success = crt.removeCart(username, isbn)
    if success:
        print()
        print("Book removed from cart!")
    else:
        print()
        print("Book not in cart!")
    return None, None

def showBookMenu(cr, bks, crt, book, return_genre):
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
        bk_menu["Go Back"] = (getBooksMenu, (cr, bks, crt, return_genre))
    else:
        bk_menu["Go Back"] = (getBooksMenu, (cr, bks, crt))

    bk_menu["Add Book to Cart"] = (addCartMenu, (crt, cr.getUsername(), book[0]))
    bk_menu["Remove Book to Cart"] = (removeCartMenu, (crt, cr.getUsername(), book[0]))

    return "Book Options", bk_menu

def getBooksMenu(cr, bks, crt, genre=None):
    bks_menu = {}
    bks_title = ""

    if genre:
        bks_menu["Go Back"] = (selectCategoryMenu, (cr, bks, crt))
    else:
        bks_menu["Go Back"] = "Main Menu"

    if genre:
        books = bks.getBooksByGenre(genre)
        bks_title = f"By Category: {genre}"
    else:
        books = bks.getAllBooks()
        bks_title = "All Books"

    for book in books:
        bks_menu[f'"{book[4]}" by {book[5]} ({book[2]}) - ${book[6]} - {book[3]}'] = (showBookMenu, (cr, bks, crt, book, genre))

    return bks_title, bks_menu

def selectCategoryMenu(cr, bks, crt):
    genres_menu = {}

    genres_menu["Go Back"] = "Main Menu"

    for genre in bks.getGenres():
        genres_menu[genre] = (getBooksMenu, (cr, bks, crt, genre))

    return "Select a Genre to Browse", genres_menu

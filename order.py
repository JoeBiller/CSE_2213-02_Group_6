
from getpass import getpass

class order:
    def __init__(self, db):
        self.__db = db
     

        self.__orderId =""
        self.__username =""
        self.__date =""
        self.__shippingNumber=""
    
    
    def __getorderTuple(self):
        return (self.__orderId,
                self.__username,
                self.__date,
                self.__shippingNumber)
    
    def createOrder(self, orderId, username, date, shippingNumber):
        if not self.__loggedIn:
            if not (self.usernameTaken(username)):
                self.__orderId = orderId
                self.__username = username             
                self.__date  = date
                self.__shippingNumber = shippingNumber
            
                self.__db.cursor.execute("INSERT INTO orders VALUES(?, ?, ?, ?, ?, ?)", 
                                         self.__getorderTuple())
                self.__db.connection.commit()

                self.__loggedIn = True

                return True, f"Order created. Welcome {username}."
            


            
    def setUsername(self, username):
        if self.__loggedIn:
            if not username:
                return False, "You must specify a username."
            old_username = self.__username
            if not self.usernameTaken(username):
                self.__username = username
                return True, f"Your username is now {self.__username}."
            else:
                return False, "Username is already taken."
        else:
            return False, "You are not logged in."           
            

    def getorderId(self):
        return self.__orderId
    
    
            

    




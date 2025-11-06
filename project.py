#Stock Market Simulator
#imports
import sqlite3
import sys
# import someAPI

def main():
    # Call load function
    balance, stockArray = load()

    print(balance, stockArray)

    pass


def load():
    #Define classes

    stockArr = []

    class stock():
        def __init__(self, symbol, shares):
            self.__symbol = symbol
            self.__shares = shares
        
        #Getter and setter methods
        def getSymbol(self):
            return self.__symbol
        
        def setSymbol(self, newVal):
            self.__symbol = newVal
            
        def getShares(self):
            return self.__shares
        
        def setShares(self, newVal):
            self.__shares = newVal

        #Other methods
        def getPrice(self):
            #Make the api call for the current price
            pass

        def getTotal(self):
            totalVal = self.__shares * self.getPrice(self)
            return totalVal
        
    # Make connection to data base and then then check if there is any sort of data
    try:
        # Connect to databse and set connection variable to con, using with so it closes autmatically
        with sqlite3.connect("finance.db") as con:

            tableName = "portfolio"
            cursor = con.cursor()

            #Check if the protfolio table already exists
            res = cursor.execute("SELECT COUNT(name) FROM sqlite_master WHERE type = 'table' AND name = ?", (tableName, ))

            # If it doesnt exist then greet the user and initiate the database creation sequence
            if res.fetchone()[0] != 1:
                print("Welcome to the stock market simulator!")

                # Creating Portfolio database to store stocks
                cursor.execute("CREATE TABLE portfolio (" \
                "stock_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "symbol VARCHAR NOT NULL," \
                "shares INTEGER NOT NULL);")

                #Creating Transaction history database
                cursor.execute("CREATE TABLE transactions (" \
                "sale_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "symbol VARCHAR NOT NULL," \
                "purchase_price REAL NOT NULL," \
                "type VARCHAR NOT NULL CHECK (type IN ('BUY', 'SELL'))," \
                "time VARCHAR NOT NULL," \
                "shares INTEGER NOT NULL);")

                #Create an index on the symbol field for faster lookup times
                cursor.execute("CREATE UNIQUE INDEX symbol ON portfolio (symbol);")

                # Create text file to seperately store the balance as putting it in a database is too clumsy for one user
                with open("balance.txt","w") as f:
                    balance = "1000"
                    f.write(balance)

                print(f"We have initialised your account, your starting balance is {balance}")

            else:
                
                #Read in data from the data"base
                for row in cursor.execute("SELECT symbol, shares FROM portfolio ORDER BY symbol ASC;"):
                    print(row)
                    stockArr.append(stock(row[0],row[1]))

                #Load in balance
                with open("balance.txt","r") as f:
                    balance = int(f.read())
                

        return balance, stockArr



    except sqlite3.OperationalError as e:
        print("An error has occurred")
        print(e)
        sys.exit()

if __name__ == "__main__":
    main()
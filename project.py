#Stock Market Simulator
#imports
import sqlite3
import sys
import os
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestTradeRequest
from dotenv import load_dotenv

#Global Vars
load_dotenv()
API_KEY = os.getenv("APCA_API_KEY_ID")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

#FR 10
#Only 200 API calls per minute, may lead to issues potentially?
def get_price(symbol):
    #Getting the latest trade request for that stock
    #And therefore getting current price
    request = StockLatestTradeRequest(symbol_or_symbols=symbol)
    response = data_client.get_stock_latest_trade(request)

    #If its a list loop through the list items and add the price of each to a list
    if type(symbol) is list:
        return [response[thing].price for thing in symbol]
    
    #If its one stock then just return that stock price as a float
    else:
        return response[symbol].price

#FR 5
def load():
    #Define stock class

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
        
    # Make connection to database and then then check if there is any sort of data
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
                cursor.execute(f"CREATE TABLE {tableName} (" \
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
                cursor.execute(f"CREATE UNIQUE INDEX symbol ON {tableName} (symbol);")

                # Create text file to seperately store the balance as putting it in a database is too clumsy for one user
                
                #FR 16
                with open("balance.txt","w") as f:
                    balance = "1000"
                    f.write(balance)

                print(f"We have initialised your account, your starting balance is {balance}")

            else:
                
                #Read in data from the data"base
                for row in cursor.execute("SELECT symbol, shares FROM portfolio ORDER BY symbol ASC;"):
                    stockArr.append(stock(row[0],row[1]))

                #Load in balance
                #FR16
                with open("balance.txt","r") as f:
                    balance = int(f.read())
                
                print(f"Welcome back, your balance is {balance}")

        return balance, stockArr

    except sqlite3.OperationalError as e:
        print("An error has occurred")
        print(e)
        sys.exit()

def main():
    
    #FR 1
    #Defining the portfolio class which will have all of the DB methods
    class portfolio():

        def __init__(self, stocks, balance):
            self.__stocks = stocks
            self.__balance = balance

        # Choosing which stock to buy, may remove later
        # Kind of like the UI for these things which will then call the buy or sell funcs
        def chooseStock(self, opt):
            #TODO
            pass

        #Buying a stock logic
        def buy(self):
            #TODO
            pass

        #Selling a stock logic
        def sell(self):
            #TODO
            pass

        #Searching for a stock
        def search(self):
            #TODO
            pass

        #Inserting info into database
        def insert(self):
            #TODO
            pass

        # Validating purchase
        def validate(self):
            #TODO
            pass

        #View portfolio
        def viewPortfolio(self):
            #TODO
            pass

        #Adding to balance
        def addBal(self):
            #TODO
            pass

        #View balance
        def viewBal(self):
            #TODO
            pass

        # View transaction history
        def viewTrans(self):
            #TODO
            pass

        #Binary search on the array of objects to check if I already own a stock
        def checkStock(self):
            #TODO
            pass

    # Call load function
    balance, stockArray = load()
    #Create a portfolio class variable
    portf = portfolio(stockArray, balance)

    while True:
        choice = navigation()

        #Mapping the choice to an output
        match choice:
            case 1:
                #BROWSE
                #not quite sure what that will actually do yet
                pass

            case 2: 
                #Going into the buy menu
                portf.chooseStock("buy")
            
            case 3:
                #Going into the sell menu
                portf.chooseStock("sell")

            case 4:
                #Just viewing your portfolio
                #Will probably have the function format the DB output in a table or sum
                portf.viewTrans()

            case 5:
                #Viewing your transaction history
                portf.viewTrans()
            
            case 6:
                #Adding money to your balance
                portf.addBal()
            
            case 7:
                #Viewing balance
                portf.viewBal()
            
            case 8:
                #Exiting the program
                sys.exit()



# Displaying the options menu when needed
def dispMenu():
    print("""
              
            1. Browse
            2. Buy
            3. Sell
            4. View portfolio
            5. View transactions
            6. Add to balance
            7. View balance
            8. Exit
            
              """)

def validateMenu(option):

    while option > 8 or option < 1:
        print("Please enter a number from 1 to 8")
        dispMenu()
        try:
            option = int(input("Enter an option: "))
        except:
            print("Please enter a valid number")
            option = 0

    return option

def navigation():
    
    dispMenu()
    
    try:
        option = int(input("Enter an option: "))
    except:
        print("Please enter a valid number")
        option = 0
    
    option = validateMenu(option)

    return option
    

if __name__ == "__main__":
    main()
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

#Clasess
#Define stock class
class stock():
        def __init__(self, symbol, shares):
            self.__symbol = symbol
            self.__shares = shares
        
        #Getter and setter methods
        #Don't need a setter method for the symbol as its defined when the class is created and never touched again
        def getSymbol(self):
            return self.__symbol
            
        def getShares(self):
            return self.__shares
        
        def setShares(self, newVal):
            self.__shares = newVal

        #Other methods
        #May remove later
        #Flag this
        def getPrice(self):
            #Make the api call for the current price
            pass

        #May remove later
        def getTotal(self):
            totalVal = self.__shares * self.getPrice(self)
            return totalVal

#FR 1
#Defining the portfolio class which will have all of the DB methods
#Include all functions in uml class diagram
#Just make the functions that arent methods private
class portfolio():

    def __init__(self, stocks, balance):
        self.__stocks = stocks
        self.__balance = balance

    # Kind of like the UI for these things which will then call the buy or sell funcs
    #FR 7 ?
    def chooseStock(self, opt):
        stock = input("Enter stock symbol: ")
        num = input(f"Enter the number of stocks you'd like to {opt}: ")
        num = self.validateNum(num, opt)

        if opt == "sell":
            self.sell(stock,num)
        
        elif opt == "buy":
            self.buy(stock,num)

        else:
            #May remove later
            #Flag this
            print("Incorrect function call")
            sys.exit()

    #Buying a stock logic
    def buy(self, buyObj,num):
        price = get_price(buyObj)

        #If the stock doesnt exist break out of it
        if price == None:
            return
        
        #Checking the user has enough money
        if not self.validatePurchase("buy", price, num):
            print(f"{num} shares of {buyObj} costs {price * num}")
            return
        
        #Checking the user wants to buy it for that much
        if not self.confirmPurchase("buy", price, num, buyObj):
            return
        
        #Balance logic, database stuff and array of ojects start now

        #Update Balance
        total = price * num
        self.__balance = round(self.__balance - total, 2)
        self.writeBal()

        #Now time to check if the user already owns the stock
        #Binary Search call
        owned = self.checkStock(buyObj)
        
        #Stock isnt owned
        if owned == -1:
            self.newStock(buyObj, num)
        #Stock is owned
        else:
            self.addStock(owned,num)

        print(f"Successfully purchased {num} shares of {buyObj}")
        return
        
    #Selling a stock logic
    def sell(self, sellObj,num):
        #TODO
        pass
        
    def validateNum(self, num, option):
        try:
            num = int(num)
        except:
            print("Please enter a valid integer number")
            num = 0
        
        while num < 1:
            try:
                num = int(input(f"Enter the number of stocks you'd like to {option}"))
            except:
                print("Please enter a valid integer number")
                num = 0

        return num

    # Validating purchase
    def validatePurchase(self, opt, price, num):
        if opt == "buy":
            if self.__balance < price * num:
                print("Insufficient cash balance")
                print(f"You have {self.__balance}")
                return False
            else:
                return True
        
        elif opt == "sell":
            pass

        return
    
    #Just a user confirmation 
    def confirmPurchase(self,opt,price,shareNum, obj):
        yesOpt = ["","yes","y", "\n"]
        noOpt = ["no","n"]
        print(f"Confirm {opt} order for {shareNum} shares of {obj} costing ${shareNum * price}?")
        print(f"Your balance is {self.__balance}")
        option = input("Y/n: ")
        option = self.validateOption(option, yesOpt, noOpt)

        if option in noOpt:
            print("Order cancelled")
            return False
        
        elif option in yesOpt:
            print("Transaction Confirmed")
            return True
        
        else:
            print("Error in purchase confirmation")
            return False

    def validateOption(self, choice, yesOpt, noOpt):
        if choice == "" or choice == "\n":
            return choice
        
        choice = choice.lower()
        while choice not in yesOpt and choice not in noOpt:
            print("Please enter a valid input")
            choice = input("Y/n").lower()

        return choice

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
    #FR 3
    def checkStock(self, searchObj):
        low = 0
        high = len(self.__stocks) - 1

        while low <= high:
            #Getting difference between highest and lowest
            #Then getting the mid point
            #Adding it to the lowest value to establish a new midpoint
            mid = low + ((high - low) // 2)

            if self.__stocks[mid].getSymbol() < searchObj:
                low = mid + 1
            elif self.__stocks[mid].getSymbol() > searchObj:
                high = mid - 1
            else:
                return mid
        return -1

    #Writing balance to text file
    #FR 15
    def writeBal(self):
        with open("balance.txt","w") as f:
            newBal = str(self.__balance)
            f.write(newBal)
        return
    
    #Looping through stock array and will add stock in the right place
    #They need to be in alphabetical order
    def stockArrAdd(self,stockName, stockNum):
        #If users owns no stock
        if len(self.__stocks) == 0:
            self.__stocks.append(stock(stockName,stockNum))
            return
        
        #Loop through the stock array and compare
        for i, asset in enumerate(self.__stocks):
            curStock = asset.getSymbol()

            #If the current stock symbol is alphabetically higher then put the current stock symbol
            #In its place and shift the rest of the array to the right
            if stockName < curStock:
                self.__stocks.insert(i,stock(stockName,stockNum))
                return
            
            #Handling edge case for the stock being the lowest down in the alphabet
            if i == (len(self.__stocks) - 1):
                self.__stocks.append(stock(stockName, stockNum))
                return

        print("stockArrAdd function isnt working as intended")
        return
 
    #Stocks need to be in alphabetical order 
    #This function inserts them in such an order
    #Also insert stock into database
    def newStock(self, stockName, stockNum):
        #Adding to array of objects
        self.stockArrAdd(stockName,stockNum)

        #Adding to database
        with sqlite3.connect("finance.db") as con:

            cursor = con.cursor()
            cursor.execute("INSERT INTO portfolio (symbol,shares) VALUES(?,?)", (stockName,stockNum,))

        return

    #If user already owns the stock then just add to the databasr
    #Modify stock array to have the correct data
    def addStock(self, stockIndex, stockNum):
        #Getting the stock object
        existingStock = self.__stocks[stockIndex]
        oldShares = existingStock.getShares()
        newShares = oldShares + stockNum
        existingStock.setShares(newShares)
        print(existingStock.getShares())

        #Add DB UPDATE Statement
        return

    #If the user sells all of a stock delete the object from the array of objects
    #Also delete from database
    def removeStock(self, stockName):
        #TODO
        pass

    #Get value of whole portfolio
    def totalVal(self):
        #TODO
        pass

#Taken from stackoverflow
#Flag this
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

#FR 10
#Only 200 API calls per minute, may lead to issues potentially?
def get_price(symbol):
    
    if not has_numbers(symbol):
        try:
            symbol = symbol.upper()
        except:
            print("Error in capatlising symbol")
    #Getting the latest trade request for that stock
    #And therefore getting current price
    try:
        request = StockLatestTradeRequest(symbol_or_symbols=symbol)
        response = data_client.get_stock_latest_trade(request)
    except:
        print("Invalid Symbol")
        return

    #If its a list loop through the list items and add the price of each to a list
    if type(symbol) is list:
        try:
            priceArr = [response[thing].price for thing in symbol]
            return priceArr
        #This shouldn't be reached technically?
        # The list is only passed in when calculating total portfolio value
        # And isnt triggered by the user
        except:
            print("Invalid stock symbol")
            return None
    #If its one stock then just return that stock price as a float
    else:
        try:
            stockPrice = response[symbol].price
            return stockPrice
        except:
            print("Invalid stock symbol")
            return None

#FR 5
def load():
    stockArr = []
        
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
                #Table name isn't a global var and if i change it here the functions in my portfolio object will break
                #Flag this
                cursor.execute(f"CREATE TABLE {tableName} (" \
                "stock_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "symbol VARCHAR(10) NOT NULL," \
                "shares INTEGER NOT NULL);")

                #Creating Transaction history database
                cursor.execute("CREATE TABLE transactions (" \
                "sale_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "symbol VARCHAR(10) NOT NULL," \
                "purchase_price REAL NOT NULL," \
                "type VARCHAR(5) NOT NULL CHECK (type IN ('BUY', 'SELL'))," \
                "time VARCHAR(100) NOT NULL," \
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
                #The order by is to ensure the stocks are in alphabetical order
                for row in cursor.execute("SELECT symbol, shares FROM portfolio ORDER BY symbol ASC;"):
                    stockArr.append(stock(row[0],row[1]))

                #Load in balance
                #FR16
                with open("balance.txt","r") as f:
                    balance = float(f.read())
                
                print(f"Welcome back, your balance is {balance}")
                #Add a thing that gets total portfolio value 

        return balance, stockArr

    except sqlite3.OperationalError as e:
        print("An error has occurred")
        print(e)
        sys.exit()

def main():

    # Call load function
    balance, stockArray = load()
    #Create a portfolio class variable
    portf = portfolio(stockArray, balance)

    while True:
        #FR8
        choice = navigation()

        #Mapping the choice to an output
        match choice:
            case 1:
                #Check Stock Price
                #not quite sure what that will actually do yet
                searchObj = input("Enter stock symbol: ")
                price = get_price(searchObj)
                print(f"{searchObj} is trading at {price} a share")

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
            1. Check Stock Price
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
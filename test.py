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
            option = int(input("Enter an option"))
        except:
            print("Please enter a valid number")
            option = 0

    return option


try:
     option = int(input("Enter an option"))
except:
    print("Please enter a valid number")
    option = 0

option = validateMenu(option)
print(option)
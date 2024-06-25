
#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        
        '''
        In this function, you must initialise the following attributes:
            ● country,
            ● code,
            ● product,
            ● cost, and
            ● quantity.
        '''
        # Initialising Variables
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        '''
        Add the code to return the cost of the shoe in this method.
        '''
        cost = self.cost
        return cost

    def get_quantity(self):
        '''
        Add the code to return the quantity of the shoes.
        '''
        quantity = self.quantity
        return quantity

    def __str__(self):
        '''
        Add a code to returns a string representation of a class.
        '''
        return (f"The warehouse in {self.country}, has product code {self.code}."
                f" This refers to {self.product}, of which there are {self.quantity} pieces at cost {self.cost} in the local currency.")
        
#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
# Import OS and Tabulate Modules
import os
from tabulate import tabulate

# Set Directory for file
current_directory, current_filename = os.path.split(__file__)
shoe_inventory = os.path.join(current_directory, "inventory.txt")

# Empty List Creation
shoe_list = []

#==========Functions outside the class==============

def read_shoes_data():
    '''
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list. One line in this file represents
    data to create one object of shoes. You must use the try-except in this function
    for error handling. Remember to skip the first line using your code.
    '''
    try:
        with open(shoe_inventory, "r") as file:
        #Use of counter to skip banner/header line in inventory text file
            counter = 0
            for line in file:
                counter += 1
                if counter == 1:
                    pass
                else:
                    temp = line.strip()
                    temp = temp.split(",")
                    if len(temp) == 5:
                        shoe_list.append(Shoe(temp[0], temp[1], temp[2], temp[3], temp[4]))
                    else:
                        print(f"Line/row {counter-1} of the text file is missing an entry.")
    except Exception:
        print("There is an error with the text file format.")
    
    return shoe_list
              
def capture_shoes():
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    # Request user input
    country = input("Enter Warehouse Country: ")
    code = input("Enter Product Code: ")
    product = input("Enter the Full Product Name: ")

    # Test for valid cost figure entry
    while True:
        cost = input("Enter the Product Cost in the Local Currency: ")
        try:
            cost = float(cost)
            break
        except Exception:
            print("You have not entered a valid cost, please re-enter when prompted.")
    
    # Test for valid quantity figure entry
    while True:
        quantity = input("Enter the Quantity in stock at the Warehouse: ")
        try:
            quantity = int(quantity)
            break
        except Exception:
            print("You have not entered a valid quantity, please re-enter when prompted.")

    # Create new shoe object and append to shoe_list        
    shoe_list.append(Shoe(country, code, product, str(cost), str(quantity)))

    return shoe_list

def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    '''
    header_line = ["Country", "Code", "Product", "Cost", "Quantity"]
    list_in_list = [[line.country,line.code,line.product,line.cost,line.quantity] for line in shoe_list]
    print(tabulate(list_in_list, headers=header_line, tablefmt = "grid"))
      
def re_stock():
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''
    # Create variable to temporarily store QTY value for each item
    qty = shoe_list[0]
    for item in shoe_list[1:]:
        if item.quantity <= qty.quantity:
            qty = item
    print(f"The {qty.product} shoe needs to be re-stocked!")
    while True:
        user_confirm = input(f"Do you want to restock {qty.product}? Enter 'yes' or 'no': ").lower()
        if user_confirm == 'yes':
            while True:
                supplementary_stock = input("Please kindly enter the replacement stock quantity: ")
                try:
                    supplementary_stock = int(supplementary_stock)
                    break
                except Exception:
                    print("You have not entered a valid quantity, please re-enter when prompted.")
            qty.quantity += supplementary_stock
            print(f"The updated quantity for {qty.product} is {qty.quantity}.")
            with open(shoe_inventory, "w") as file:
                file.write("Country,Code,Product,Cost,Quantity \n")
                for shoe in shoe_list:
                    file.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}")
                    file.write("\n")
            break
        
        elif user_confirm == "no":
            print("Exiting the re-stock function.")
            break

        else:
            print("You have not entered a valid decision, please re-enter when prompted and not the entry format.") 

def search_shoe():
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    '''
    shoe_code = input("Please Enter Shoe Code: ")
    for item in shoe_list[1:]:
        if item.code == shoe_code:
            found_shoe = item
            return print(found_shoe)
        else:
            pass

def value_per_item():
    '''
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    '''
    for item in shoe_list:
        value = item.get_cost()*item.get_quantity()
        print(f"{item.product} costs {value} in the local currency.")

def highest_qty():
    '''
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.
    '''
    # Create variable to temporarily store QTY value for each item
    qty = shoe_list[0]
    for item in shoe_list[1:]:
        if item.quantity > qty.quantity:
            qty = item
    print(f"The {qty.product} shoe is on sale!")

#==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''
# Initialise Shoe List
read_shoes_data()
print(shoe_list[1].country, shoe_list[1].code, shoe_list[1].product, shoe_list[1].cost, shoe_list[1].quantity)

# Main Menu Code
while True:
    menu = input("""Please kindly select an option:
                 a - add to inventory
                 v - view all inventory
                 r - restock function
                 s - search function
                 c - inventory value summary
                 e - exit program
                 h - confirm highest stock product:  """).lower()
    
    if menu == 'a':
        capture_shoes()
    
    elif menu == 'v':
        view_all()

    elif menu == 'r':
        re_stock()

    elif menu == 's':
        search_shoe()
    
    elif menu == 'c':
        value_per_item()
    
    elif menu == 'e':
        exit()
    
    elif menu == 'h':
        highest_qty()

    else:
        print("You have not entered a valid selection, please re-enter when prompted.")
        
             

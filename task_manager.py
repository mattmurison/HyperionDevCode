#=====importing libraries===========
'''This is the section where you will import libraries'''

# Import Module to Isolate Directory for Input/Output Files
import os

# Import Module for Current Date Calculation
import datetime
from datetime import date

#====Login Section====
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and password from the user.txt file
    - You can use a list or dictionary to store a list of usernames and passwords from the file
    - Use a while loop to validate your user name and password
'''
username = ""
username_list = []

password = ""
password_list = []

current_directory, current_filename = os.path.split(__file__)

username_password_database = os.path.join(current_directory, "user.txt")
task_database = os.path.join(current_directory, "tasks.txt")

# Read Username and Password Text File and Import Data
with open(username_password_database, "r") as file:
    # Read usernames and passwords first
    for lines in file:
        username = lines.strip()
        username = username.split(", ")
        username_list.append(username[0])
        password_list.append(username[1])

# Username Input
username_input = input("Please kindly enter your username: ")

# Loop to Validate Username and Password
while True:
    if username_input in username_list:
        password_input = input("Please kindly enter your password: ")
        if password_input in password_list:
            break
        else:
            print("Error! You have entered an incorrect password for the username provided. Please re-enter your password when prompted.")
    else:
        print("Error! You have entered an incorrect username. Please re-enter your username when prompted.")
        username_input = input("Please kindly enter your username: ")

while True:
    # Present the menu to the user and 
    # make sure that the user input is converted to lower case.

    # Menu option #1 for 'admin' users
    if username_input.lower() == "admin":
        menu = input('''Select one of the following options:
        r - register a user
        a - add task
        va - view all tasks
        vm - view my tasks
        e - exit
        s - statistics
        : ''').lower()
    
    # Menu option #2 for non-admin users
    else:
        menu = input('''Select one of the following options:
        a - add task
        va - view all tasks
        vm - view my tasks
        e - exit
        : ''').lower()

    if (menu == 'r') and (username_input.lower() == "admin"):

               
        # Request User Name Input
        new_username = input("Please kindly enter your new username (case sensitive): ")

        # Check if Password Confirmation Entry Matches New User Password Entry or Not
        while True:
            new_password = input("Please kindly enter your new password (case sensitive): ")
            check_new_password = input("Please kindly confirm your new password (case sensitive): ")

            # Validates that password re-entry is valid and matches new password created before data can be written
            if check_new_password == new_password:
                username_password_database_update = open(username_password_database, "a")
                username_password_database_update.write(f"\n{new_username}, {new_password}") # Updated with f-string format method
                username_password_database_update.close()
                break
            else:
                print("The passwords entered do not match, please kindly re-confirm when prompted.")
        
    elif menu == 'a':

        # Request User Inputs for New Task Details
        task_assignee = input("Please kindly enter the username for the task: ")
        task_title = input("Please kindly enter the title of the task to be added: ")
        task_description = input("Please kindly enter the description of the task to be added: ")
        # task_due_date = input("Please kindly enter the due date for the task in the following format, ie: '25 Oct 2024': ") # Original version

        # Validate Task Due Date Format Entry
        # Check if format entered matches that of what is requested by conducting a string parse
        while True:
            task_due_date_check = input("Please kindly enter the due date for the task in the following format, ie: '25 Oct 2024': ")
            try:
                task_due_date = datetime.datetime.strptime(task_due_date_check, "%d %b %Y")
                break

            # if a ValueError is generated, inform the user of the error and re-request a correctly formatted entry. 
            except ValueError:
                print("The task due date entered does not match the requested format, please kindly re-enter when prompted")
                continue

        task_completion_indicator = "No" #Default setting as per instruction

        # Current Date in Desired Format Using datetime Module
        task_start_date = datetime.date.today().strftime("%d %b %Y")

        # Write Above Contents to Task Text File
        task_database_update = open(task_database, "a")
        # task_database_update.write("\n" + task_assignee + ", " + task_title + ", " + task_description + ", " + task_start_date + ", " + task_due_date + ", " + task_completion_indicator) # Prior submission code
        task_database_update.write(f"\n{task_assignee}, {task_title}, {task_description}, {task_start_date}, {task_due_date.strftime("%d %b %Y")}, {task_completion_indicator}") # Updated with f-string format method and needed to use strftime/format method to convert to desired format as parse check method done above
        task_database_update.close()

        '''This code block will allow a user to add a new task to task.txt file
        - You can use these steps:
            - Prompt a user for the following: 
                - the username of the person whom the task is assigned to,
                - the title of the task,
                - the description of the task, and 
                - the due date of the task.
            - Then, get the current date.
            - Add the data to the file task.txt
            - Remember to include 'No' to indicate that the task is not complete.'''

    elif menu == 'va':
        
        # Define Empty Lists to Store Data
        task_assignee = []
        task_title = []
        task_description = []
        task_due_date = []
        task_completion_indicator = []

        # Read Task Text File
        with open(task_database, "r") as file:
            for task_line in file:
                list_item = task_line.split(", ")
                task_assignee.append(list_item[0])        
                task_title.append(list_item[1])
                task_description.append(list_item[2])
                task_due_date.append(list_item[3])
                task_completion_indicator.append(list_item[4].strip("\n"))

        # Print out List Contents
        for i in range(len(task_assignee)):
            print("Task Leader: " + 3*"\t" + task_assignee[i])
            print("Task Title: " + 3*"\t" + task_title[i])
            print("Task Description: " + 2*"\t" + task_description[i])
            print("Task Due Date: " + 3*"\t" + task_due_date[i])
            print("Task Completion Status: " + "\t" + task_completion_indicator[i])
            print("\n")

        '''This code block will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the PDF
         You can do it in this way:
            - Read a line from the file.
            - Split that line where there is comma and space.
            - Then print the results in the format shown in the Output 2 in the PDF
            - It is much easier to read a file using a for loop.'''

    elif menu == 'vm':
        
        # Creation of Empty Variables
        task_assignee = ""
        task_title = ""
        task_description = ""
        task_due_date = ""
        task_completion_indicator = ""

        # Read Text File
        with open(task_database, "r") as file:
            for task_line in file:
                list_item = task_line.split(", ")

                # Check for tasks matching username entered
                if username_input == list_item[0]:
                    task_assignee = (list_item[0])        
                    task_title = (list_item[1])
                    task_description = (list_item[2])
                    task_due_date = (list_item[3])
                    task_completion_indicator = (list_item[4].strip("\n"))

                    # Print out tasks assigned to associated user
                    print("Task Leader: " + 3*"\t" + task_assignee)
                    print("Task Title: " + 3*"\t" + task_title)
                    print("Task Description: " + 2*"\t" + task_description)
                    print("Task Due Date: " + 3*"\t" + task_due_date)
                    print("Task Completion Status: " + "\t" + task_completion_indicator)
                    print("\n")
                else:
                    pass
        
        '''This code block will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the PDF
         You can do it in this way:
            - Read a line from the file
            - Split the line where there is comma and space.
            - Check if the username of the person logged in is the same as the 
              username you have read from the file.
            - If they are the same you print the task in the format of Output 2
              shown in the PDF '''

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    # Add Statistics Option for 'admin' users
    elif (menu == 's') and (username_input.lower() == "admin"):

        # Create count variable to determine number of unique lines/tasks in task text file
        count = 0

        # Loop to 'count' number of lines in text file pertaining to number of unique tasks
        with open(task_database, "r") as file:
            for task_line in file:
                count += 1
            print("Statistics: " + "\n" + "Number of Active Tasks: " + 2*"\t" + str(count) + "\n")
        
        # Create second 'count' variable to determine number of unique lines/usernames in user text file
        count_2 = 0

        # Loop to 'count' number of lines in text file pertaining to number of unique tasks
        with open(username_password_database, "r") as file:
            for task_line in file:
                count_2 += 1
            print("Number of Active Users: " + 2*"\t" + str(count_2) + "\n")

    else:
        print("You have entered an invalid input. Please try again")

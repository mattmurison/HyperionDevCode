# Import Modules - SQLite3, OS, JSON and ElementTree
import sqlite3
import os
import json
import xml.etree.ElementTree as ET

# Match Directory for Database File
current_directory, current_filename = os.path.split(__file__)
HypDev_database = os.path.join(current_directory, "HyperionDev.db")

# Attempt to Open Hyperion Dev Database
try:
    conn = sqlite3.connect(HypDev_database)
except sqlite3.Error:
    print("Please store your database as HyperionDev.db")
    quit()

# Creat Cursor Object
cur = conn.cursor()

# Function Defintions
def usage_is_incorrect(input, num_args):
    if len(input) != num_args + 1:
        print(f"The {input[0]} command requires {num_args} arguments.")
        return True
    return False

def store_data_as_json(data, filename):
    JSON = os.path.join(current_directory, filename)
    with open(JSON, "w") as file:
        json.dump(data,file,indent=4)

def store_data_as_xml(data, filename):
    root = ET.Element("Database")
    XML=os.path.join(current_directory, filename)
    for line in data:
        row_item = ET.SubElement(root,"Data")

        for index,sub_line in enumerate(line):
            value = ET.SubElement(row_item,"item{}".format(index))
            value.text = str(sub_line)
    
    tree = ET.ElementTree(root)
    tree.write(XML,encoding='utf-8',xml_declaration=True)
    

def offer_to_store(data):
    while True:
        print("Would you like to store this result?")
        choice = input("Y/[N]? : ").strip().lower()

        if choice == "y":
            filename = input("Specify filename. Must end in .xml or .json: ")
            ext = filename.split(".")[-1]
            if ext == 'xml':
                store_data_as_xml(data, filename)
            elif ext == 'json':
                store_data_as_json(data, filename)
            else:
                print("Invalid file extension. Please use .xml or .json")

        elif choice == 'n':
            break

        else:
            print("Invalid choice")

# User Input Request
usage = '''
What would you like to do?

d - demo
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program

Type your option here: '''

print("Welcome to the data querying app!")

while True:
    print()
    # Get input from user
    user_input = input(usage).split(" ")
    print()

    # Parse user input into command and args
    command = user_input[0]
    if len(user_input) > 1:
        args = user_input[1:]

    if command == 'd': # demo - a nice bit of code from me to you - this prints all student names and surnames :)
        data = cur.execute("SELECT * FROM Student")
        for _, firstname, surname, _, _ in data:
            print(f"{firstname} {surname}")
        
    elif command == 'vs': # view subjects by student_id
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        data = None

        # Run SQL query and store in data
        cur.execute('''
                    SELECT Course.course_name
                    FROM Course
                    INNER JOIN StudentCourse ON Course.course_code = StudentCourse.course_code
                    WHERE StudentCourse.student_id=?''',(student_id,))
        
        data = cur.fetchall()
        
        #Console Print Statement
        print(f"The Subjects taken by student id, {student_id}, are as follows:")
        print()

        for subject in data:
            print(subject[0])
        print()

        offer_to_store(data)
        pass

    elif command == 'la':# list address by name and surname
        if usage_is_incorrect(user_input, 2):
            continue
        firstname, surname = args[0], args[1]
        data = None

        # Run SQL query and store in data
        cur.execute('''  
                    SELECT Address.street, Address.city
                    FROM Address
                    INNER JOIN Student ON Address.address_id = Student.address_id
                    WHERE Student.first_name=? AND Student.last_name=?''',(firstname,surname))

        data = cur.fetchall()

        # Console Print Statement
        print(f"The street address for student, {firstname} {surname}, is: ")
        print()

        for detail in data:
            print(f"Street: {detail[0]}, city: {detail[1]}.")
            print()

        offer_to_store(data)
        pass
    
    elif command == 'lr':# list reviews by student_id
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        data = None

        # Run SQL query and store in data
        cur.execute('''
                    SELECT Review.completeness, Review.efficiency, Review.style, Review.documentation, Review.review_text
                    FROM Review
                    WHERE Review.student_id=?''',(student_id,))

        data = cur.fetchall()
        
        # Print to Console
        print(f"The review for student id {student_id}, is as follows:")
        print()

        for detail in data:
            print(f'Completeness Score: {detail[0]}')
            print(f'Efficiency Score: {detail[1]}')
            print(f'Style Score: {detail[2]}')
            print(f'Documentation Score: {detail[3]}')
            print(f'Review: {detail[4]}')
            print()
            
        offer_to_store(data)
        pass
    
    elif command == 'lc': # list all subjects presented by a particular teacher
        if usage_is_incorrect(user_input,1):
            continue
        teacher_id = args[0]
        data = None

        # Run SQL query and store in data
        cur.execute('''
                    SELECT Course.course_name
                    FROM Course
                    WHERE teacher_id=?''',(teacher_id,))
        
        data = cur.fetchall()

        # Print to Console
        print(f"The subjects taught by teacher id, {teacher_id} are as follows:")
        print()

        for subject in data:
            print(subject[0])
            print()

        offer_to_store(data)
        pass
    
    elif command == 'lnc':# list all students who haven't completed their course
        data = None
        is_complete = 0
        # Run SQL query and store in data
        cur.execute('''
                    SELECT Student.student_id, Student.first_name, Student.last_name, Student.email
                    FROM Student
                    INNER JOIN StudentCourse ON StudentCourse.student_id=Student.student_id
                    WHERE StudentCourse.is_complete = ?''',(is_complete,))

        data = cur.fetchall()

        # Print to Console
        print("The following students did not complete their respective course(s):")
        print()

        for detail in data:
            print(f"Student id: {detail[0]}")
            print(f"First Name: {detail[1]}")
            print(f"Surname: {detail[2]}")
            print(f"Email: {detail[3]}")
            print()

        offer_to_store(data)
        pass
    
    elif command == 'lf':# list all students who have completed their course and got a mark <= 30
        data = None
        cut_off_mark = 30
        # Run SQL query and store in data
        cur.execute('''
                    SELECT Student.student_id, Student.first_name, Student.last_name, Student.email, Course.course_name, StudentCourse.mark
                    FROM Student
                    INNER JOIN StudentCourse ON StudentCourse.student_id=Student.student_id
                    INNER JOIN Course ON Course.course_code=StudentCourse.course_code
                    WHERE StudentCourse.mark <=?''',(cut_off_mark,))
        
        data = cur.fetchall()

        # Print to Console
        print("The following students received a mark of 30 or below:")
        print()

        for detail in data:
            print(f"Student id: {detail[0]}")
            print(f"First Name: {detail[1]}")
            print(f"Surname: {detail[2]}")
            print(f"Email: {detail[3]}")
            print(f"Course Name: {detail[4]}")
            print(f"Mark: {detail[5]}")
            print()
        
        offer_to_store(data)
        pass
    
    elif command == 'e':# list address by name and surname
        print("Programme exited successfully!")
        break
    
    else:
        print(f"Incorrect command: '{command}'")
    

    

"""

"""

import sqlite3
from tabulate import tabulate
import json
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString


# A function for connecting to the database
def connect_to_db():
    try:
        conn_db = sqlite3.connect("HyperionDev.db")
        cur_db = conn_db.cursor()
        with open('create_database.sql', 'r') as sql_file:
            conn_db.executescript(sql_file.read())

        conn_db.commit()
        return conn_db, cur_db

    except sqlite3.Error:
        print("Please store your database as HyperionDev.db")
        quit()


conn, cur = connect_to_db()


def usage_is_incorrect(user_input_correct: list, num_args: int):
    if len(user_input_correct) != num_args + 1:
        print(f"The {user_input_correct[0]} command requires {num_args} arguments.")
        return True
    return False


def store_data_as_json(data_json: sqlite3.Cursor, filename_json: str):
    # Extract headers or dictionary keys
    headers = [col[0] for col in data_json.description]

    # create a list of dictionaries where row data has been keyed to headers
    data_list = [dict(zip(headers, row)) for row in data_json]

    # write the list on a json file
    with open(filename_json, 'w') as json_data_file:
        json.dump(data_list, json_data_file, indent=4)


def store_data_as_xml(data_xml: sqlite3.Cursor, filename_xml: str):
    # Extract headers or dictionary keys
    headers = [col[0] for col in data_xml.description]

    # create a list of dictionaries where row data has been keyed to headers
    data_list = [dict(zip(headers, row)) for row in data_xml]

    # create a xml from the list of dictionaries
    xml = dicttoxml(data_list, custom_root=headers[0], attr_type=False, include_encoding='utf-8-sig')

    # format the xml to print with indents
    xml_format = parseString(xml).toprettyxml()
    with open(f'{filename_xml}', 'w', encoding='utf-8-sig') as xml_data_file:
        xml_data_file.write(xml_format)


def offer_to_store(store_data: sqlite3.Cursor):
    while True:
        print("\nWould you like to store this result?")
        choice = input("\nY/[N]? : ").strip().lower()

        if choice == "y":
            filename = input("Specify filename. Must end in .xml or .json: ")
            ext = filename.split(".")[-1]
            if ext == 'xml':
                store_data_as_xml(store_data, filename)
            elif ext == 'json':
                store_data_as_json(store_data, filename)
            else:
                print("Invalid file extension. Please use .xml or .json")

        elif choice == 'n':
            break

        else:
            print("\nInvalid choice")


def print_query(data_print: sqlite3.Cursor, headers: list):
    heads = [col[0] for col in data_print.description]
    rows = [dict(zip(heads, row)) for row in data_print]

    # Create a list to store the values for the required columns, Get the row values for all headers
    print_rows = [[str(row.get(header, "")) for header in headers] for row in rows]

    if len(print_rows) > 0:
        print(tabulate(print_rows, headers=headers, tablefmt="grid"))
    else:
        print("No results found.")


usage = '''
What would you like to do?

d - demo
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lp <province>              - lookup student given province
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taught by teacher_id
lst <teacher_id>           - list all students and their courses taught by teacher_id
sc <course code>           - list all the students enrolled in a specific course_code
cs <student_id>            - list all course taken by student_id
arcs                       - list the average review scores for each course
nsc                        - number of students enrolled in each course
shm                        - the student with the highest overall mark
sham                       - get the student with the highest average mark for completed courses
sac                        - list students who have taken all available courses
chns                       - list the top 5 courses with the highest number of enrolled students
lnc                        - list all students who haven't completed their course
lbr                        - list all students who have bad reviews
lgr                        - list all students who have good reviews
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program

Type your option here: '''

print("\nWelcome to the data querying app!")

while True:
    # Get input from user
    user_input = input(usage).split(" ")
    print()

    # Parse user input into command and args
    command = user_input[0]
    args = []
    if len(user_input) > 1:  # Get all other inputs (<student_id> <firstname> <surname>)
        args = user_input[1:]

    if command == 'd':  # demo - a nice bit of code from me to you - this prints all student names and surnames :)
        data = cur.execute("SELECT * FROM Student")

        for _, firstname, surname, _, _ in cur:
            print(f"{firstname} {surname}")

    elif command == 'vs':  # view subjects by student_id
        if usage_is_incorrect(user_input, 1):
            continue

        student_id = args[0]

        statement = f"""SELECT *
        FROM Course
        INNER JOIN StudentCourse
        ON StudentCourse.course_code = Course.course_code
        WHERE StudentCourse.student_id = ?"""

        data = cur.execute(statement, args)

        head = ['course_name']
        print_query(data, head)

        # Run SQL query and store in data
        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'la':  # list address by name and surname
        if usage_is_incorrect(user_input, 2):
            continue

        statement = f"""SELECT Address.street, Address.city
        FROM Address
        INNER JOIN Student
        ON Student.address_id = Address.address_id
        WHERE Student.first_name = ? AND Student.last_name = ?"""

        head = ['street', 'city']
        data = cur.execute(statement, args)
        print_query(data, head)

        # Run SQL query and store in data
        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'lp':  # list student ID, Surname, and Last name by Province
        if usage_is_incorrect(user_input, 1):
            continue

        check = "SELECT Address.province FROM Address"
        args = [args[0].upper()]
        if args in cur.execute(check):
            continue

        statement = f"""SELECT Address.province, Student.student_id, Student.first_name, Student.last_name
        FROM Address
        INNER JOIN Student
        ON Student.address_id = Address.address_id
        WHERE Address.province = ?"""

        head = ['province', 'student_id', 'first_name', 'last_name']

        data = cur.execute(statement, args)
        print_query(data, head)

        # Run SQL query and store in data
        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'lr':  # list reviews by student_id
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]

        statement = f"""
        SELECT completeness, efficiency, style, documentation, review_text
        FROM Review
        WHERE Review.student_id = ?"""

        head = ['completeness', 'efficiency', 'style', 'documentation']
        data = cur.execute(statement, args)
        print_query(data, head)

        # Run SQL query and store in data
        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'lc':
        if usage_is_incorrect(user_input, 1):
            continue
        teacher_id = args[0]

        # Run SQL query and store in data
        statement = f"""
        SELECT Course.course_name
        FROM Course
        INNER JOIN Teacher
        ON Teacher.teacher_id = Course.teacher_id
        WHERE Teacher.teacher_id = ?"""

        head = ['course_name']
        data = cur.execute(statement, args)
        print_query(data, head)

        # Run SQL query and store in data
        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'lnc':  # list all students who haven't completed their course

        # Run SQL query and store in data
        statement = f"""
        SELECT Student.student_id, first_name, last_name, Student.email, Course.course_name
        FROM Student
        INNER JOIN StudentCourse
        ON StudentCourse.student_id =  Student.student_id
        INNER JOIN Course 
        ON Course.course_code = StudentCourse.course_code
        WHERE is_complete = 0
        """

        head = ['student_id', 'first_name', 'last_name', 'email', 'course_name']
        data = cur.execute(statement, args)
        print_query(data, head)

        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'lbr':  # list all students who have bad reviews

        # Run SQL query and store in data
        review = 'completeness, efficiency, style, documentation, review_text'
        statement = f"""
        SELECT Student.student_id, first_name, last_name, email, Course.course_name, {review}
        FROM Student
        INNER JOIN Review
        ON Review.student_id =  Student.student_id
        INNER JOIN Course
        ON Review.course_code = Course.course_code
        WHERE completeness = 1 AND efficiency = 1 AND style = 1 AND documentation = 1
        """

        head = ['student_id', 'first_name', 'last_name', 'email', 'course_name', 'review_text']
        data = cur.execute(statement, args)
        print_query(data, head)

        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'lgr':  # list all students who have bad reviews

        # Run SQL query and store in data
        review = 'completeness, efficiency, style, documentation, review_text'
        statement = f"""
        SELECT Student.student_id, first_name, last_name, email, Course.course_name, {review}
        FROM Student
        INNER JOIN Review
        ON Review.student_id =  Student.student_id
        INNER JOIN Course
        ON Review.course_code = Course.course_code
        WHERE completeness = 4 AND efficiency = 4 AND style = 4 AND documentation = 4
        """

        head = ['student_id', 'first_name', 'last_name', 'email', 'course_name', 'review_text']
        data = cur.execute(statement, args)
        print_query(data, head)

        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'lf':  # list all students who have completed their course and got a mark <= 30

        # Run SQL query and store in data
        statement = f"""
        SELECT Student.student_id, first_name, last_name, Student.email, Course.course_name, StudentCourse.mark 
        FROM Student
        INNER JOIN StudentCourse
        ON StudentCourse.student_id =  Student.student_id
        INNER JOIN Course 
        ON Course.course_code = StudentCourse.course_code
        WHERE is_complete = 1 AND StudentCourse.mark <= 30
        ORDER BY Student.student_id
        """

        head = ['student_id', 'first_name', 'last_name', 'email', 'course_name', 'mark']
        data = cur.execute(statement, args)
        print_query(data, head)

        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'lst':
        if usage_is_incorrect(user_input, 1):
            continue

        # Run SQL query and store in data
        statement = f"""
        SELECT Student.student_id, Student.first_name, Student.last_name, Course.course_code, Course.course_name
        FROM Student
        INNER JOIN StudentCourse ON StudentCourse.student_id = Student.student_id
        INNER JOIN Course ON Course.course_code = StudentCourse.course_code
        INNER JOIN Teacher ON Teacher.teacher_id = Course.teacher_id
        WHERE Teacher.teacher_id = ?"""

        head = ['student_id', 'first_name', 'last_name', 'course_code', 'course_name']
        data = cur.execute(statement, args)
        print_query(data, head)

        # Run SQL query and store in data
        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'sc':  # List all students enrolled in a particular course
        if usage_is_incorrect(user_input, 1):
            continue

        # Run SQL query and store in data
        statement = f"""
           SELECT Student.student_id, Student.first_name, Student.last_name 
           FROM Student 
           JOIN StudentCourse ON Student.student_id = StudentCourse.student_id 
           WHERE StudentCourse.course_code = ?"""

        head = ['student_id', 'first_name', 'last_name']
        data = cur.execute(statement, args)
        print_query(data, head)

        # Run SQL query and store in data
        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'cs':  # list all courses taken by a particular student
        if usage_is_incorrect(user_input, 1):
            continue

        # Run SQL query and store in data
        statement = f"""
           SELECT Course.course_code, Course.course_name, StudentCourse.student_id
           FROM Course 
           JOIN StudentCourse ON Course.course_code = StudentCourse.course_code 
           WHERE StudentCourse.student_id = ?"""

        head = ['student_id', 'course_code', 'course_name']
        data = cur.execute(statement, args)
        print_query(data, head)

        # Run SQL query and store in data
        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'nsc':  # get the number of students enrolled in each course

        # Run SQL query and store in data
        statement = f"""
           SELECT Course.course_code, Course.course_name, COUNT(StudentCourse.student_id) AS num_student
           FROM Course 
           LEFT JOIN StudentCourse ON Course.course_code = StudentCourse.course_code 
           GROUP BY Course.course_code, Course.course_name"""

        head = ['course_code', 'course_name', 'num_student']
        data = cur.execute(statement, args)
        print_query(data, head)

        # Run SQL query and store in data
        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'shm':  # get the students with the highest mark

        # Run SQL query and store in data
        statement = f"""
           SELECT Student.student_id, Student.first_name, Student.last_name, 
           MAX(StudentCourse.mark) AS high_mark
           FROM Student 
           INNER JOIN StudentCourse ON Student.student_id = StudentCourse.student_id 
           GROUP BY Student.student_id
           ORDER BY high_mark DESC LIMIT 1"""

        head = ['first_name', 'last_name', 'high_mark']
        data = cur.execute(statement, args)
        print_query(data, head)

        # Run SQL query and store in data
        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'sham':  # get the students with the highest average mark for completed courses

        # Run SQL query and store in data
        statement = f"""
           SELECT Student.student_id, Student.first_name, Student.last_name, 
           AVG(StudentCourse.mark) AS average_mark
           FROM Student 
           INNER JOIN StudentCourse ON Student.student_id = StudentCourse.student_id 
           GROUP BY Student.student_id
           HAVING COUNT(*) = SUM(CASE WHEN StudentCourse.is_complete = 1 THEN 1 ELSE 0 END)
           ORDER BY average_mark DESC LIMIT 1"""

        head = ['first_name', 'last_name', 'average_mark']
        data = cur.execute(statement, args)
        print_query(data, head)

        # Run SQL query and store in data
        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'chns':  # list the top 5 courses with the highest number of students

        # Run SQL query and store in data
        statement = f"""
        SELECT Course.course_code, Course.course_name, COUNT(StudentCourse.student_id) AS enrollment_count 
        FROM Course 
        LEFT JOIN StudentCourse ON Course.course_code = StudentCourse.course_code 
        GROUP BY Course.course_code, Course.course_name ORDER BY enrollment_count DESC LIMIT 5
        """

        head = ['course_code', 'course_name', 'enrollment_count']
        data = cur.execute(statement, args)
        print_query(data, head)

        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'arcs':  # list average review scores per course

        # Run SQL query and store in data
        avg_review = """
        AVG(Review.completeness) AS avg_completeness, 
        AVG(Review.efficiency) AS avg_efficiency, 
        AVG(Review.style) AS avg_style, 
        AVG(Review.documentation) AS avg_documentation
        """

        statement = f"""
        SELECT Course.course_code, Course.course_name, {avg_review} 
        FROM Course 
        LEFT JOIN Review ON Course.course_code = Review.course_code 
        GROUP BY Course.course_code, Course.course_name
        """

        head = ['course_code', 'course_name', 'avg_completeness', 'avg_efficiency', 'avg_style', 'avg_documentation']
        data = cur.execute(statement, args)
        print_query(data, head)

        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'sac':  # list all students who have taken all available courses (Most likely NOT allowed but!!!)

        # Run SQL query and store in data

        statement = f"""
        SELECT Student.student_id, Student.first_name, Student.last_name
        FROM Student 
        WHERE NOT EXISTS (SELECT DISTINCT course_code 
            FROM Course 
            WHERE NOT EXISTS (SELECT * 
                FROM StudentCourse 
                WHERE StudentCourse.student_id = Student.student_id 
                AND StudentCourse.course_code = Course.course_code))
        """

        head = ['first_name', 'last_name ', 'course_code ']
        data = cur.execute(statement, args)
        print_query(data, head)

        data = cur.execute(statement, args)
        offer_to_store(data)

    elif command == 'e':  # list address by name and surname
        print("Programme exited successfully!")
        break

    else:
        print(f"Incorrect command: '{command}'")

# close the connection when done with the database
conn.close()

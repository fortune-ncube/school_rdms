# School Database Management System

## Introduction

This Python program is a data querying application for a student management system. It interacts with a SQLite database containing information about students, courses, reviews, and addresses. The program allows users to execute various SQL queries to retrieve and manipulate data related to students and courses.

## Features

- **View Subjects Taken by a Student**: Displays the subjects taken by a student based on their ID.
- **Lookup Address by First Name and Surname**: Looks up the address of a student based on their first name and surname.
- **Lookup Student by Province**: Retrieves student information based on the province they reside in.
- **List Reviews for a Given Student**: Lists reviews given by a student based on their ID.
- **List All Courses Taught by a Teacher**: Displays all courses taught by a particular teacher.
- **List All Students and Their Courses Taught by a Teacher**: Lists all students and the courses taught by a specific teacher.
- **List All Students Enrolled in a Specific Course**: Displays all students enrolled in a particular course.
- **List All Courses Taken by a Specific Student**: Lists all courses taken by a specific student.
- **List the Average Review Scores for Each Course**: Displays the average review scores for each course.
- **Number of Students Enrolled in Each Course**: Shows the number of students enrolled in each course.
- **Student with the Highest Overall Mark**: Retrieves the student with the highest overall mark.
- **Student with the Highest Average Mark for Completed Courses**: Retrieves the student with the highest average mark for completed courses.
- **List Students Who Have Taken All Available Courses**: Displays students who have taken all available courses.
- **List the Top 5 Courses with the Highest Number of Enrolled Students**: Shows the top 5 courses with the highest number of enrolled students.
- **List All Students Who Haven't Completed Their Course**: Displays all students who haven't completed their course.
- **List All Students Who Have Bad Reviews**: Shows all students who have bad reviews.
- **List All Students Who Have Good Reviews**: Shows all students who have good reviews.
- **List All Students Who Have Completed Their Course and Achieved 30 or Below**: Displays students who have completed their course and achieved a mark of 30 or below.

## Usage

1. Make sure you have Python installed on your system.
2. Clone this repository to your local machine.
3. Ensure the SQLite database file `HyperionDev.db` is stored in the same directory as the Python script.
4. Run the Python script `student_management_system.py`.
5. Follow the on-screen instructions to execute SQL queries and interact with the student management system.

## Requirements

- Python 3.x
- SQLite3
- `tabulate` library: You can install it via pip using `pip install tabulate`
- `dicttoxml` library: You can install it via pip using `pip install dicttoxml`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

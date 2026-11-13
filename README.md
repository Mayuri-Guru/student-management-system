# Student Management System

**InternNova – Week 6 Final Python Project**

## Project Description
A menu-driven command-line application to manage student information. It supports adding, viewing, searching, updating and deleting student records. Records are saved in a JSON file so they remain available after the program closes. Users can also export records to CSV.

## Features
- Add a student with ID, name, age, course and email
- View all saved student records
- Search by student ID
- Update and delete student records
- Prevent duplicate student IDs
- Validate required fields and age input
- Save records automatically in JSON
- Export records to CSV
- Handle invalid input and file errors

## Technologies Used
- Python 3
- JSON and CSV modules
- pathlib
- Object-Oriented Programming
- Git and GitHub for version control

## Python Concepts Used
Variables, data types, input/output, operators, conditional statements, loops, functions, lists, classes and objects, constructors, inheritance, polymorphism, encapsulation, abstraction, file handling and exception handling.

## Folder Structure
```text
Student-Management-System/
├── main.py
├── README.md
├── requirements.txt
├── project_files/
│   └── students.json
└── screenshots/
    └── README.txt
```

## Installation / Setup
1. Install Python 3.10 or later.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. No external packages are needed.

## How to Run
```bash
python main.py
```
On some Windows systems:
```bash
py main.py
```

## Data Storage
Student records are saved in `project_files/students.json`. CSV exports are written to `project_files/students_export.csv`.

## Future Improvements
- Add a graphical user interface using Tkinter
- Add login and role-based access
- Add marks, attendance and grade management
- Add database support using SQLite or MySQL
- Add input validation for email format

## Author
[Your Name]  
Internship Domain: Python Programming  
Week: 6 of 6

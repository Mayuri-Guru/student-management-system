"""
InternNova Week 6 Final Project
Student Management System
Author: [Your Name]
Description: A menu-driven Python application to add, view, search,
update, delete, and export student records.
"""

import json
import csv
from abc import ABC, abstractmethod
from pathlib import Path


DATA_FILE = Path(__file__).parent / "project_files" / "students.json"
CSV_FILE = Path(__file__).parent / "project_files" / "students_export.csv"


class Person(ABC):
    """Abstract base class demonstrating abstraction."""

    def __init__(self, name, age):
        self._name = name
        self._age = age

    @abstractmethod
    def display_details(self):
        pass


class Student(Person):
    """Student class inherits Person and encapsulates student data."""

    def __init__(self, student_id, name, age, course, email):
        super().__init__(name, age)
        self.__student_id = str(student_id)
        self.__course = course
        self.__email = email

    @property
    def student_id(self):
        return self.__student_id

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @property
    def course(self):
        return self.__course

    @property
    def email(self):
        return self.__email

    def display_details(self):
        # Overriding the abstract method demonstrates polymorphism.
        return (
            f"ID: {self.student_id} | Name: {self.name} | Age: {self.age} | "
            f"Course: {self.course} | Email: {self.email}"
        )

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "course": self.course,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, record):
        return cls(
            record["student_id"],
            record["name"],
            record["age"],
            record["course"],
            record["email"],
        )


class StudentManagementSystem:
    """Manages student records and stores them in a JSON file."""

    def __init__(self, data_file=DATA_FILE):
        self.data_file = Path(data_file)
        self.students = []
        self.load_data()

    def load_data(self):
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            if self.data_file.exists():
                with self.data_file.open("r", encoding="utf-8") as file:
                    records = json.load(file)
                self.students = [Student.from_dict(item) for item in records]
            else:
                self.students = []
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            print(f"Warning: Could not read saved data ({error}). Starting empty.")
            self.students = []
        except OSError as error:
            print(f"File error while loading data: {error}")
            self.students = []

    def save_data(self):
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            with self.data_file.open("w", encoding="utf-8") as file:
                json.dump(
                    [student.to_dict() for student in self.students],
                    file,
                    indent=4,
                )
        except OSError as error:
            print(f"Unable to save records: {error}")

    def add_student(self, student):
        if any(item.student_id == student.student_id for item in self.students):
            raise ValueError("A student with this ID already exists.")
        self.students.append(student)
        self.save_data()

    def view_students(self):
        if not self.students:
            print("\nNo student records found.")
            return
        print("\n--- STUDENT RECORDS ---")
        for student in self.students:
            print(student.display_details())

    def search_student(self, student_id):
        for student in self.students:
            if student.student_id.lower() == str(student_id).lower():
                return student
        return None

    def update_student(self, student_id, name, age, course, email):
        student = self.search_student(student_id)
        if student is None:
            return False
        index = self.students.index(student)
        self.students[index] = Student(student_id, name, age, course, email)
        self.save_data()
        return True

    def delete_student(self, student_id):
        student = self.search_student(student_id)
        if student is None:
            return False
        self.students.remove(student)
        self.save_data()
        return True

    def export_to_csv(self):
        try:
            with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
                fields = ["student_id", "name", "age", "course", "email"]
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                for student in self.students:
                    writer.writerow(student.to_dict())
            print(f"Records exported to: {CSV_FILE}")
        except OSError as error:
            print(f"Could not export CSV: {error}")


def read_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def read_age():
    while True:
        try:
            age = int(input("Enter age: "))
            if 1 <= age <= 120:
                return age
            print("Enter an age between 1 and 120.")
        except ValueError:
            print("Please enter age as a whole number.")


def collect_student_details():
    student_id = read_non_empty("Enter student ID: ")
    name = read_non_empty("Enter name: ")
    age = read_age()
    course = read_non_empty("Enter course: ")
    email = read_non_empty("Enter email: ")
    return student_id, name, age, course, email


def main():
    system = StudentManagementSystem()

    while True:
        print("\n========== STUDENT MANAGEMENT SYSTEM ==========")
        print("1. Add student")
        print("2. View all students")
        print("3. Search student")
        print("4. Update student")
        print("5. Delete student")
        print("6. Export records to CSV")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        try:
            if choice == "1":
                details = collect_student_details()
                system.add_student(Student(*details))
                print("Student added successfully.")

            elif choice == "2":
                system.view_students()

            elif choice == "3":
                student_id = read_non_empty("Enter student ID to search: ")
                student = system.search_student(student_id)
                print(student.display_details() if student else "Student not found.")

            elif choice == "4":
                student_id = read_non_empty("Enter student ID to update: ")
                if system.search_student(student_id) is None:
                    print("Student not found.")
                else:
                    print("Enter the updated details:")
                    details = collect_student_details()
                    # Keep the original ID so the record is updated, not duplicated.
                    details = (student_id, *details[1:])
                    system.update_student(*details)
                    print("Student updated successfully.")

            elif choice == "5":
                student_id = read_non_empty("Enter student ID to delete: ")
                if system.delete_student(student_id):
                    print("Student deleted successfully.")
                else:
                    print("Student not found.")

            elif choice == "6":
                system.export_to_csv()

            elif choice == "7":
                print("Thank you for using Student Management System.")
                break

            else:
                print("Invalid choice. Please select a number from 1 to 7.")

        except ValueError as error:
            print(f"Error: {error}")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")


if __name__ == "__main__":
    main()

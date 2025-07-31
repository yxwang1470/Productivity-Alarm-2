import tkinter as tk
from tkinter import ttk, messagebox
import json

# --- Part A: Class Design ---
class Person:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

class Student(Person):
    def __init__(self, name, student_id):
        super().__init__(name, student_id)
        self.courses = {}  # course_code: grade

    def enroll(self, course_code):
        self.courses[course_code] = None

    def assign_grade(self, course_code, grade):
        if course_code in self.courses:
            self.courses[course_code] = grade

class Course:
    def __init__(self, name, code):
        self.name = name
        self.code = code

class GradeBook:
    def __init__(self):
        self.students = []
        self.courses = []

    def add_student(self, student):
        self.students.append(student)

    def add_course(self, course):
        self.courses.append(course)

    def get_student_by_id(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def get_course_by_code(self, course_code):
        for course in self.courses:
            if course.code == course_code:
                return course
        return None

    def to_dict(self):
        return {
            "students": [
                {
                    "name": s.name,
                    "student_id": s.student_id,
                    "courses": s.courses
                } for s in self.students
            ],
            "courses": [
                {"name": c.name, "code": c.code} for c in self.courses
            ]
        }

    def from_dict(self, data):
        self.students.clear()
        self.courses.clear()
        for s in data.get("students", []):
            student = Student(s["name"], s["student_id"])
            student.courses = s.get("courses", {})
            self.students.append(student)
        for c in data.get("courses", []):
            self.courses.append(Course(c["name"], c["code"]))

# --- Part B: GUI ---
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.gradebook = GradeBook()
        self.load_data()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(padx=10, pady=10)

        self.create_add_student_tab()
        self.create_add_course_tab()
        self.create_enroll_tab()
        self.create_grade_tab()
        self.create_view_tab()

    def create_add_student_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Add Student")

        tk.Label(tab, text="Name").pack()
        self.name_entry = tk.Entry(tab)
        self.name_entry.pack()

        tk.Label(tab, text="Student ID").pack()
        self.id_entry = tk.Entry(tab)
        self.id_entry.pack()

        tk.Button(tab, text="Add Student", command=self.add_student).pack(pady=5)

    def create_add_course_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Add Course")

        tk.Label(tab, text="Course Name").pack()
        self.course_name_entry = tk.Entry(tab)
        self.course_name_entry.pack()

        tk.Label(tab, text="Course Code").pack()
        self.course_code_entry = tk.Entry(tab)
        self.course_code_entry.pack()

        tk.Button(tab, text="Add Course", command=self.add_course).pack(pady=5)

    def create_enroll_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Enroll Student")

        tk.Label(tab, text="Student ID").pack()
        self.enroll_id_entry = tk.Entry(tab)
        self.enroll_id_entry.pack()

        tk.Label(tab, text="Course Code").pack()
        self.enroll_course_entry = tk.Entry(tab)
        self.enroll_course_entry.pack()

        tk.Button(tab, text="Enroll", command=self.enroll_student).pack(pady=5)

    def create_grade_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Assign Grade")

        tk.Label(tab, text="Student ID").pack()
        self.grade_id_entry = tk.Entry(tab)
        self.grade_id_entry.pack()

        tk.Label(tab, text="Course Code").pack()
        self.grade_course_entry = tk.Entry(tab)
        self.grade_course_entry.pack()

        tk.Label(tab, text="Grade").pack()
        self.grade_entry = tk.Entry(tab)
        self.grade_entry.pack()

        tk.Button(tab, text="Assign Grade", command=self.assign_grade).pack(pady=5)

    def create_view_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="View Records")

        self.tree = ttk.Treeview(tab, columns=("ID", "Courses"), show="headings")
        self.tree.heading("ID", text="Student ID")
        self.tree.heading("Courses", text="Courses and Grades")
        self.tree.pack(fill="both", expand=True)

        tk.Button(tab, text="Refresh", command=self.view_records).pack(pady=5)

    def add_student(self):
        name = self.name_entry.get()
        student_id = self.id_entry.get()
        if not name or not student_id:
            messagebox.showerror("Error", "Please enter all fields.")
            return
        if self.gradebook.get_student_by_id(student_id):
            messagebox.showerror("Error", "Student ID already exists.")
            return
        self.gradebook.add_student(Student(name, student_id))
        self.save_data()
        messagebox.showinfo("Success", f"Student {name} added!")

    def add_course(self):
        name = self.course_name_entry.get()
        code = self.course_code_entry.get()
        if not name or not code:
            messagebox.showerror("Error", "Please enter all fields.")
            return
        if self.gradebook.get_course_by_code(code):
            messagebox.showerror("Error", "Course code already exists.")
            return
        self.gradebook.add_course(Course(name, code))
        self.save_data()
        messagebox.showinfo("Success", f"Course {name} added!")

    def enroll_student(self):
        student_id = self.enroll_id_entry.get()
        course_code = self.enroll_course_entry.get()
        student = self.gradebook.get_student_by_id(student_id)
        if not student:
            messagebox.showerror("Error", "Student not found.")
            return
        course = self.gradebook.get_course_by_code(course_code)
        if not course:
            messagebox.showerror("Error", "Course not found.")
            return
        student.enroll(course_code)
        self.save_data()
        messagebox.showinfo("Success", f"{student.name} enrolled in {course.name}.")

    def assign_grade(self):
        student_id = self.grade_id_entry.get()
        course_code = self.grade_course_entry.get()
        grade = self.grade_entry.get()
        student = self.gradebook.get_student_by_id(student_id)
        if not student:
            messagebox.showerror("Error", "Student not found.")
            return
        if course_code not in student.courses:
            messagebox.showerror("Error", "Student not enrolled in this course.")
            return
        try:
            student.assign_grade(course_code, int(grade))
        except ValueError:
            messagebox.showerror("Error", "Grade must be a number.")
            return
        self.save_data()
        messagebox.showinfo("Success", f"Grade {grade} assigned to {student.name}.")

    def view_records(self):
        self.tree.delete(*self.tree.get_children())
        for s in self.gradebook.students:
            course_info = ", ".join([f"{code}: {grade}" for code, grade in s.courses.items()])
            self.tree.insert("", "end", values=(s.student_id, course_info))

    def save_data(self):
        with open("student_data.json", "w") as f:
            json.dump(self.gradebook.to_dict(), f)

    def load_data(self):
        try:
            with open("student_data.json", "r") as f:
                data = json.load(f)
                self.gradebook.from_dict(data)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()

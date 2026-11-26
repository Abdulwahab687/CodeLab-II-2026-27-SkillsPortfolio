
import tkinter as tk
from tkinter import messagebox
from pathlib import Path


file_path = Path(__file__).resolve().parent.parent / "A1 - Resources" / "studentMarks.txt"


# Work out the student's grade
def getGrade(percentage):
    if percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


# Read and display student records
def viewStudents():
    output.delete("1.0", tk.END)

    total_percentage = 0
    count = 0

    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            student_count = int(file.readline())

            for line in file:
                if not line.strip():
                    continue

                details = line.strip().split(",")

                code = details[0]
                name = details[1]

                mark1 = int(details[2])
                mark2 = int(details[3])
                mark3 = int(details[4])
                exam = int(details[5])

                coursework = mark1 + mark2 + mark3
                total = coursework + exam

                percentage = total / 160 * 100
                grade = getGrade(percentage)

                total_percentage += percentage
                count += 1

                output.insert(tk.END, f"Name: {name}\n")
                output.insert(tk.END, f"Student Number: {code}\n")
                output.insert(tk.END, f"Coursework: {coursework}/60\n")
                output.insert(tk.END, f"Exam: {exam}/100\n")
                output.insert(tk.END, f"Overall: {percentage:.2f}%\n")
                output.insert(tk.END, f"Grade: {grade}\n")
                output.insert(tk.END, "-" * 45 + "\n")

        if count > 0:
            average = total_percentage / count

            summary.config(
                text=f"Total Students: {count} | Average: {average:.2f}%"
            )

        if count != student_count:
            messagebox.showwarning(
                "Warning", "Student count does not match the file."
            )

    except FileNotFoundError:
        messagebox.showerror("Error", "Student file not found.")

    except (ValueError, IndexError):
        messagebox.showerror("Error", "Invalid student data.")


def clearRecords():
    output.delete("1.0", tk.END)
    summary.config(text="")


# Main window
root = tk.Tk()
root.title("Student Manager")
root.geometry("650x600")
root.configure(bg="#F1F5F4")

heading = tk.Label(
    root,
    text="Student Manager",
    font=("Arial", 24, "bold"),
    bg="#F1F5F4",
    fg="#166534"
)
heading.pack(pady=20)

view_button = tk.Button(
    root,
    text="View All Student Records",
    command=viewStudents,
    bg="#166534",
    fg="white",
    font=("Arial", 12),
    width=25
)
view_button.pack(pady=10)

output = tk.Text(root, width=65, height=20)
output.pack(padx=20, pady=10, fill="both", expand=True)

summary = tk.Label(
    root,
    text="",
    font=("Arial", 11),
    bg="#F1F5F4"
)
summary.pack(pady=10)

tk.Button(
    root,
    text="Clear Records",
    command=clearRecords,
    width=15
).pack(pady=5)

tk.Button(
    root,
    text="Quit",
    command=root.destroy,
    width=15
).pack(pady=(5, 15))

root.mainloop()

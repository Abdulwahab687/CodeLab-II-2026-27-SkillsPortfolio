import tkinter as tk
from tkinter import messagebox
import random

# AI assistance: ChatGPT was used to assist with code

# Quiz variables
difficulty = ""
question_number = 0
score = 0
attempts = 0
correct_answer = 0

# GUI colours
BACKGROUND = "#F1F5F9"
PRIMARY = "#172554"
GREEN = "#15803D"
ORANGE = "#B45309"
RED = "#B91C1C"


# Remove existing widgets from the window
def clearWindow():
    for widget in root.winfo_children():
        widget.destroy()


# Generate a random number based on difficulty
def randomInt(difficulty):
    if difficulty == "Easy":
        return random.randint(1, 9)

    elif difficulty == "Moderate":
        return random.randint(10, 99)

    elif difficulty == "Advanced":
        return random.randint(1000, 9999)


# Randomly select addition or subtraction
def decideOperation():
    return random.choice(["+", "-"])


# Display the difficulty selection menu
def displayMenu():
    clearWindow()

    tk.Label(
        root,
        text="Maths Quiz",
        font=("Arial", 28, "bold"),
        bg=BACKGROUND,
        fg=PRIMARY
    ).pack(pady=25)

    tk.Label(
        root,
        text="Select Difficulty Level",
        font=("Arial", 16),
        bg=BACKGROUND
    ).pack(pady=10)

    tk.Button(
        root,
        text="Easy",
        font=("Arial", 12),
        width=24,
        bg=GREEN,
        fg="white",
        command=lambda: startQuiz("Easy")
    ).pack(pady=8)

    tk.Button(
        root,
        text="Moderate",
        font=("Arial", 12),
        width=24,
        bg=ORANGE,
        fg="white",
        command=lambda: startQuiz("Moderate")
    ).pack(pady=8)

    tk.Button(
        root,
        text="Advanced",
        font=("Arial", 12),
        width=24,
        bg=RED,
        fg="white",
        command=lambda: startQuiz("Advanced")
    ).pack(pady=8)

    tk.Label(
        root,
        text="10 Questions | 100 Points",
        font=("Arial", 12),
        bg=BACKGROUND
    ).pack(pady=15)

    tk.Label(
        root,
        text="You have two attempts per question.",
        font=("Arial", 10),
        bg=BACKGROUND
    ).pack()


# Start a new quiz and reset the variables
def startQuiz(selected_difficulty):
    global difficulty, question_number, score

    difficulty = selected_difficulty
    question_number = 0
    score = 0

    displayProblem()


# Generate and display an arithmetic problem
def displayProblem():
    global question_number, attempts, correct_answer
    global answer_entry, feedback_label

    # Finish the quiz after ten questions
    if question_number == 10:
        displayResults()
        return

    clearWindow()

    question_number += 1
    attempts = 0

    # Generate two numbers and an operation
    number1 = randomInt(difficulty)
    number2 = randomInt(difficulty)
    operation = decideOperation()

    # Calculate the correct answer
    if operation == "+":
        correct_answer = number1 + number2
    else:
        correct_answer = number1 - number2

    tk.Label(
        root,
        text="Maths Quiz",
        font=("Arial", 26, "bold"),
        bg=BACKGROUND,
        fg=PRIMARY
    ).pack(pady=15)

    tk.Label(
        root,
        text=f"Difficulty: {difficulty}",
        font=("Arial", 12),
        bg=BACKGROUND
    ).pack()

    tk.Label(
        root,
        text=f"Question {question_number} of 10",
        font=("Arial", 14, "bold"),
        bg=BACKGROUND
    ).pack(pady=8)

    tk.Label(
        root,
        text=f"Current Score: {score}/100",
        font=("Arial", 12),
        bg=BACKGROUND,
        fg=GREEN
    ).pack()

    # Display the arithmetic question
    tk.Label(
        root,
        text=f"{number1} {operation} {number2} = ?",
        font=("Arial", 28, "bold"),
        bg=BACKGROUND,
        fg=PRIMARY
    ).pack(pady=20)

    tk.Label(
        root,
        text="Enter your answer:",
        font=("Arial", 12),
        bg=BACKGROUND
    ).pack()

    answer_entry = tk.Entry(
        root,
        font=("Arial", 18),
        width=18,
        justify="center"
    )
    answer_entry.pack(pady=10)
    answer_entry.focus_set()

    tk.Button(
        root,
        text="Submit Answer",
        font=("Arial", 12),
        width=20,
        bg=PRIMARY,
        fg="white",
        command=submitAnswer
    ).pack(pady=8)

    feedback_label = tk.Label(
        root,
        text="Attempts remaining: 2",
        font=("Arial", 12),
        bg=BACKGROUND,
        wraplength=450
    )
    feedback_label.pack(pady=10)


# Check whether the user's answer is correct
def isCorrect(user_answer, expected_answer):
    if user_answer == expected_answer:
        feedback_label.config(
            text="Correct answer!",
            fg=GREEN
        )
        return True

    else:
        feedback_label.config(
            text="Incorrect answer.",
            fg=RED
        )
        return False


# Validate the answer and calculate the score
def submitAnswer():
    global attempts, score

    # Prevent invalid input from consuming an attempt
    try:
        user_answer = int(answer_entry.get())

    except ValueError:
        feedback_label.config(
            text="Please enter a valid whole number.",
            fg=RED
        )
        answer_entry.focus_set()
        return

    attempts += 1

    if isCorrect(user_answer, correct_answer):

        # Award points according to the attempt
        if attempts == 1:
            score += 10
            points = 10
        else:
            score += 5
            points = 5

        messagebox.showinfo(
            "Correct Answer",
            f"Well done! You earned {points} points."
        )

        displayProblem()

    elif attempts == 1:

        # Give the user one more attempt
        feedback_label.config(
            text="Incorrect! You have one more attempt.",
            fg=RED
        )

        answer_entry.delete(0, tk.END)
        answer_entry.focus_set()

    else:

        # Move on after two incorrect attempts
        messagebox.showinfo(
            "Incorrect Answer",
            f"The correct answer was {correct_answer}.\n"
            "No points awarded."
        )

        displayProblem()


# Determine the performance rank
def calculateRank(final_score):
    if final_score > 90:
        return "A+"

    elif final_score >= 80:
        return "A"

    elif final_score >= 70:
        return "B"

    elif final_score >= 60:
        return "C"

    elif final_score >= 50:
        return "D"

    else:
        return "F"


# Display the final score and performance rank
def displayResults():
    clearWindow()

    rank = calculateRank(score)

    tk.Label(
        root,
        text="Quiz Completed!",
        font=("Arial", 28, "bold"),
        bg=BACKGROUND,
        fg=PRIMARY
    ).pack(pady=25)

    tk.Label(
        root,
        text=f"Difficulty: {difficulty}",
        font=("Arial", 14),
        bg=BACKGROUND
    ).pack(pady=5)

    tk.Label(
        root,
        text="Your Final Score",
        font=("Arial", 16),
        bg=BACKGROUND
    ).pack(pady=10)

    tk.Label(
        root,
        text=f"{score} / 100",
        font=("Arial", 36, "bold"),
        bg=BACKGROUND,
        fg=GREEN
    ).pack(pady=10)

    tk.Label(
        root,
        text=f"Performance Rank: {rank}",
        font=("Arial", 20, "bold"),
        bg=BACKGROUND,
        fg=PRIMARY
    ).pack(pady=10)

    tk.Label(
        root,
        text="Would you like to play again?",
        font=("Arial", 14),
        bg=BACKGROUND
    ).pack(pady=15)

    tk.Button(
        root,
        text="Play Again",
        font=("Arial", 12),
        width=22,
        bg=GREEN,
        fg="white",
        command=displayMenu
    ).pack(pady=5)

    tk.Button(
        root,
        text="Quit",
        font=("Arial", 12),
        width=22,
        bg=RED,
        fg="white",
        command=root.destroy
    ).pack(pady=5)


# Create the main application window
root = tk.Tk()
root.title("Maths Quiz")
root.geometry("500x520")
root.configure(bg=BACKGROUND)

# Display the difficulty selection menu
displayMenu()

# Keep the application running
root.mainloop()

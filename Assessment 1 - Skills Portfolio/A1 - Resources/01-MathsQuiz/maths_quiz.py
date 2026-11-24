"""
Exercise 1 - Maths Quiz (Tkinter)

A 10-question arithmetic quiz with three difficulty levels. A wrong answer
earns one more attempt: 10 points for a correct first attempt, 5 points for
a correct second attempt, so the maximum score is 100.

AI ACKNOWLEDGEMENT (required by the assessment brief):
The first draft of this file was generated with Claude (Anthropic).
Prompt given: "please give me a draft for matching the requirements and
secure A*" together with the Exercise 1 brief. I then reviewed, tested and
changed the code myself (replace this line with what YOU changed).

Note: displayMenu, randomInt, decideOperation, displayProblem, isCorrect and
displayResults keep the camelCase names because the brief specifies them.
"""

import random
import tkinter as tk
from tkinter import messagebox

# ----- Constants (easy to change in one place) -----
QUESTIONS_PER_QUIZ = 10
FIRST_ATTEMPT_POINTS = 10
SECOND_ATTEMPT_POINTS = 5
FEEDBACK_DELAY_MS = 1200

# Difficulty level -> (minimum, maximum) value of each number.
# Design decision: easy uses 1-9 so a question never contains a 0.
DIFFICULTY_RANGES = {
    1: (1, 9),         # Easy: single digit
    2: (10, 99),       # Moderate: double digit
    3: (1000, 9999),   # Advanced: four digit
}
DIFFICULTY_NAMES = {1: "Easy", 2: "Moderate", 3: "Advanced"}


# ----- Required functions -----
def displayMenu(parent, on_select):
    """Build the difficulty menu inside `parent`.

    `on_select` is called with the chosen level (1, 2 or 3) when a
    button is clicked.
    """
    tk.Label(parent, text="MATHS QUIZ", font=("Arial", 22, "bold")).pack(pady=(20, 5))
    tk.Label(parent, text="DIFFICULTY LEVEL", font=("Arial", 14)).pack(pady=(0, 15))

    for level, name in DIFFICULTY_NAMES.items():
        # lambda passes the level to the handler (taught in the lectures).
        # level=level fixes the value now, rather than at click time.
        tk.Button(
            parent,
            text=f"{level}. {name}",
            width=18,
            font=("Arial", 12),
            command=lambda level=level: on_select(level),
        ).pack(pady=5)


def randomInt(level):
    """Return a random whole number in the range for the chosen level."""
    minimum, maximum = DIFFICULTY_RANGES[level]
    return random.randint(minimum, maximum)


def decideOperation():
    """Randomly return '+' or '-' as a single character."""
    return random.choice(["+", "-"])


def displayProblem(parent, number1, operator, number2, question_number, score):
    """Show the question and an answer box inside `parent`.

    Returns the widgets the app needs later: (entry, feedback_label, submit_button).
    """
    tk.Label(
        parent,
        text=f"Question {question_number} of {QUESTIONS_PER_QUIZ}     Score: {score}",
        font=("Arial", 12),
    ).pack(pady=(20, 10))

    tk.Label(
        parent,
        text=f"{number1} {operator} {number2} =",
        font=("Arial", 24, "bold"),
    ).pack(pady=10)

    entry = tk.Entry(parent, font=("Arial", 16), width=12, justify="center")
    entry.pack(pady=5)
    entry.focus_set()

    submit_button = tk.Button(parent, text="Submit", width=12, font=("Arial", 12))
    submit_button.pack(pady=10)

    feedback_label = tk.Label(parent, text="", font=("Arial", 12), wraplength=360)
    feedback_label.pack(pady=5)

    return entry, feedback_label, submit_button


def isCorrect(user_answer, correct_answer, attempt):
    """Check an answer and return (is_right, message).

    `attempt` is 1 for the first try and 2 for the second try.
    """
    if user_answer == correct_answer:
        points = FIRST_ATTEMPT_POINTS if attempt == 1 else SECOND_ATTEMPT_POINTS
        return True, f"Correct! +{points} points"
    if attempt == 1:
        return False, "Not quite - try once more."
    return False, f"Wrong again. The answer was {correct_answer}."


def getGrade(score):
    """Convert a score out of 100 into a letter grade (helper for displayResults)."""
    if score > 90:
        return "A+"
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    if score >= 60:
        return "C"
    if score >= 50:
        return "D"
    return "F"


def displayResults(parent, score, on_replay, on_quit):
    """Show the final score out of 100, the rank, and play-again buttons."""
    grade = getGrade(score)

    tk.Label(parent, text="QUIZ COMPLETE", font=("Arial", 22, "bold")).pack(pady=(25, 10))
    tk.Label(parent, text=f"Your score: {score} / 100", font=("Arial", 16)).pack(pady=5)
    tk.Label(parent, text=f"Your rank: {grade}", font=("Arial", 20, "bold")).pack(pady=5)
    tk.Label(parent, text="Would you like to play again?", font=("Arial", 12)).pack(pady=(20, 10))

    tk.Button(parent, text="Play again", width=14, font=("Arial", 12),
              command=on_replay).pack(pady=3)
    tk.Button(parent, text="Quit", width=14, font=("Arial", 12),
              command=on_quit).pack(pady=3)


# ----- Application class: holds the quiz state and connects the functions -----
class MathsQuizApp:
    """Controls the quiz flow: menu -> 10 questions -> results -> replay."""

    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("420x420")
        self.root.resizable(False, False)

        # One container frame; its contents are swapped for each screen.
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Quiz state
        self.level = 1
        self.score = 0
        self.question_number = 0
        self.attempt = 1
        self.correct_answer = 0
        self.locked = False          # True while feedback is showing

        self.show_menu()

    def clear_screen(self):
        """Remove everything from the container before building a new screen."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_menu(self):
        self.clear_screen()
        displayMenu(self.container, self.start_quiz)

    def start_quiz(self, level):
        """Reset the state for a new play at the chosen difficulty."""
        self.level = level
        self.score = 0
        self.question_number = 0
        self.next_question()

    def next_question(self):
        """Move to the next question, or to the results after the last one."""
        if self.question_number >= QUESTIONS_PER_QUIZ:
            self.show_results()
            return

        self.question_number += 1
        self.attempt = 1
        self.locked = False

        number1 = randomInt(self.level)
        number2 = randomInt(self.level)
        operator = decideOperation()
        self.correct_answer = number1 + number2 if operator == "+" else number1 - number2

        self.clear_screen()
        self.entry, self.feedback, self.submit_button = displayProblem(
            self.container, number1, operator, number2, self.question_number, self.score
        )
        self.submit_button.config(command=self.submit_answer)
        self.entry.bind("<Return>", lambda event: self.submit_answer())  # Enter key submits

    def submit_answer(self):
        """Handle one submitted answer (validation, scoring, next step)."""
        if self.locked:
            return

        text = self.entry.get().strip()
        try:
            user_answer = int(text)
        except ValueError:
            # Invalid input does not use up an attempt.
            messagebox.showwarning("Invalid input", "Please enter a whole number.")
            self.entry.delete(0, tk.END)
            return

        is_right, message = isCorrect(user_answer, self.correct_answer, self.attempt)
        self.feedback.config(text=message, fg="green" if is_right else "red")

        if is_right:
            self.score += FIRST_ATTEMPT_POINTS if self.attempt == 1 else SECOND_ATTEMPT_POINTS
            self.finish_question()
        elif self.attempt == 1:
            self.attempt = 2
            self.entry.delete(0, tk.END)
        else:
            self.finish_question()

    def finish_question(self):
        """Pause briefly so the feedback can be read, then move on."""
        self.locked = True
        self.submit_button.config(state="disabled")
        self.root.after(FEEDBACK_DELAY_MS, self.next_question)

    def show_results(self):
        self.clear_screen()
        displayResults(self.container, self.score, self.show_menu, self.root.destroy)


if __name__ == "__main__":
    window = tk.Tk()
    MathsQuizApp(window)
    window.mainloop()
import tkinter as tk


# Display the difficulty selection menu
def displayMenu():
    tk.Label(
        root,
        text="Maths Quiz",
        font=("Arial", 26, "bold"),
        bg="#F1F5F9",
        fg="#172554"
    ).pack(pady=25)

    tk.Label(
        root,
        text="Select Difficulty Level",
        font=("Arial", 16),
        bg="#F1F5F9"
    ).pack(pady=10)

    tk.Button(
        root,
        text="Easy",
        font=("Arial", 12),
        width=22,
        bg="#15803D",
        fg="white"
    ).pack(pady=8)

    tk.Button(
        root,
        text="Moderate",
        font=("Arial", 12),
        width=22,
        bg="#B45309",
        fg="white"
    ).pack(pady=8)

    tk.Button(
        root,
        text="Advanced",
        font=("Arial", 12),
        width=22,
        bg="#B91C1C",
        fg="white"
    ).pack(pady=8)

    tk.Label(
        root,
        text="10 Questions | 100 Points",
        font=("Arial", 11),
        bg="#F1F5F9"
    ).pack(pady=20)


# Create the main application window
root = tk.Tk()
root.title("Maths Quiz")
root.geometry("500x400")
root.configure(bg="#F1F5F9")

# Display the menu
displayMenu()

# Keep the application running
root.mainloop()
import tkinter as tk
from tkinter import messagebox
import random
from pathlib import Path


# Application colour scheme
BACKGROUND = "#0B1120"
CARD = "#162236"
CYAN = "#22D3EE"
WHITE = "#F8FAFC"
MUTED = "#94A3B8"
BUTTON = "#132B3D"

# Locate the supplied jokes resource file
FILE_PATH = (
    Path(__file__).resolve().parent.parent
    / "A1 - Resources"
    / "randomJokes.txt"
)

# Store the currently selected joke
current_joke = None


# Read jokes from the supplied resource file
def loadJokes(file_path):
    jokes = []

    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:

            for line in file:
                line = line.strip()

                # Ignore empty lines
                if not line:
                    continue

                # Separate the setup and punchline
                if "?" in line:
                    setup, punchline = line.split("?", 1)

                    setup = setup.strip()
                    punchline = punchline.strip()

                    # Store correctly formatted jokes
                    if setup and punchline:
                        jokes.append((setup + "?", punchline))

    except (OSError, UnicodeError):
        messagebox.showerror(
            "File Error",
            "Unable to read randomJokes.txt.\n"
            "Please check the resource file."
        )

    return jokes


# Randomly select and display a joke
def displayJoke():
    global current_joke

    # Check whether jokes are available
    if not jokes:
        messagebox.showwarning(
            "No Jokes",
            "No jokes are available."
        )
        return

    # Prevent the same joke appearing consecutively
    available_jokes = []

    for joke in jokes:
        if joke != current_joke:
            available_jokes.append(joke)

    # Select a random joke
    if available_jokes:
        current_joke = random.choice(available_jokes)
    else:
        current_joke = random.choice(jokes)

    # Display the joke setup
    setup_label.config(
        text=current_joke[0]
    )

    # Hide the punchline until requested
    punchline_label.config(
        text="Reveal the punchline when you're ready.",
        fg=MUTED
    )

    # Update the application status
    status_label.config(
        text="Waiting for you to reveal the punchline"
    )

    # Enable the Show Punchline button
    punchline_button.config(state=tk.NORMAL)


# Reveal the punchline of the current joke
def showPunchline():
    if current_joke is not None:

        punchline_label.config(
            text=current_joke[1],
            fg=CYAN
        )

        status_label.config(
            text="Ready for another joke?"
        )

        # Disable the button after revealing the punchline
        punchline_button.config(state=tk.DISABLED)


# Create the main application window
root = tk.Tk()
root.title("Alexa | Joke Assistant")
root.geometry("650x720")
root.minsize(600, 700)
root.configure(bg=BACKGROUND)


# Create the Alexa-inspired assistant symbol
canvas = tk.Canvas(
    root,
    width=160,
    height=140,
    bg=BACKGROUND,
    highlightthickness=0
)

canvas.pack(pady=(15, 0))


# Draw the outer decorative ring
canvas.create_oval(
    15, 5, 145, 135,
    fill="#102033",
    outline=""
)


# Draw the second decorative ring
canvas.create_oval(
    25, 15, 135, 125,
    fill="#132B3D",
    outline=""
)


# Draw the main cyan ring
canvas.create_oval(
    35, 25, 125, 115,
    fill=BACKGROUND,
    outline=CYAN,
    width=5
)


# Draw the sound-wave illustration
heights = [12, 24, 38, 24, 12]

for i in range(len(heights)):
    x = 60 + i * 10
    height = heights[i]

    canvas.create_line(
        x, 70 - height / 2,
        x, 70 + height / 2,
        fill=CYAN,
        width=4,
        capstyle=tk.ROUND
    )


# Application heading
tk.Label(
    root,
    text="alexa.",
    font=("Arial", 32, "bold"),
    bg=BACKGROUND,
    fg=WHITE
).pack()


# Application subtitle
tk.Label(
    root,
    text="YOUR PERSONAL JOKE ASSISTANT",
    font=("Arial", 10, "bold"),
    bg=BACKGROUND,
    fg=CYAN
).pack(pady=5)


# Application status
status_label = tk.Label(
    root,
    text="Ready to entertain",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=MUTED
)

status_label.pack(pady=8)


# Create the conversation card
joke_frame = tk.Frame(
    root,
    bg=CARD,
    highlightbackground="#24364D",
    highlightthickness=1
)

joke_frame.pack(
    padx=35,
    pady=15,
    fill="both",
    expand=True
)


# Conversation heading
tk.Label(
    joke_frame,
    text="ALEXA SAYS",
    font=("Arial", 10, "bold"),
    bg=CARD,
    fg=CYAN
).pack(
    anchor="w",
    padx=20,
    pady=(15, 5)
)


# Display the joke setup
setup_label = tk.Label(
    joke_frame,
    text="Hello! Ready for a good laugh?",
    font=("Arial", 17, "bold"),
    bg=CARD,
    fg=WHITE,
    wraplength=480,
    justify="left"
)

setup_label.pack(
    anchor="w",
    padx=20,
    pady=10
)


# Create a separator inside the conversation card
tk.Frame(
    joke_frame,
    bg="#334155",
    height=1
).pack(
    fill="x",
    padx=20,
    pady=5
)


# Display the joke punchline
punchline_label = tk.Label(
    joke_frame,
    text="Ask me to tell you a joke.",
    font=("Arial", 13),
    bg=CARD,
    fg=MUTED,
    wraplength=480,
    justify="left"
)

punchline_label.pack(
    anchor="w",
    padx=20,
    pady=15
)


# Main button to request a random joke
tk.Button(
    root,
    text="Alexa tell me a Joke",
    font=("Arial", 13, "bold"),
    bg=CYAN,
    fg=BACKGROUND,
    activebackground="#67E8F9",
    relief="flat",
    cursor="hand2",
    command=displayJoke
).pack(
    fill="x",
    padx=35,
    ipady=10,
    pady=5
)


# Create a frame for the secondary buttons
button_frame = tk.Frame(
    root,
    bg=BACKGROUND
)

button_frame.pack(
    fill="x",
    padx=35,
    pady=10
)


# Button to reveal the punchline
punchline_button = tk.Button(
    button_frame,
    text="Show Punchline",
    font=("Arial", 12),
    bg=BUTTON,
    fg=CYAN,
    activebackground="#164E63",
    activeforeground=WHITE,
    disabledforeground="#64748B",
    relief="flat",
    cursor="hand2",
    state=tk.DISABLED,
    command=showPunchline
)

punchline_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 5),
    ipady=10
)


# Button to display another random joke
tk.Button(
    button_frame,
    text="Next Joke",
    font=("Arial", 12),
    bg=BUTTON,
    fg=CYAN,
    activebackground="#164E63",
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=displayJoke
).pack(
    side="left",
    fill="x",
    expand=True,
    padx=(5, 0),
    ipady=10
)


# Button to close the application
tk.Button(
    root,
    text="Quit",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=MUTED,
    activebackground=CARD,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=root.destroy
).pack(pady=5)


# Application footer
tk.Label(
    root,
    text="JOKE ASSISTANT  |  CODELAB II",
    font=("Arial", 9),
    bg=BACKGROUND,
    fg="#64748B"
).pack(pady=(5, 15))


# Load all jokes from the supplied resource file
jokes = loadJokes(FILE_PATH)

# Display the number of jokes loaded for testing
print(f"Total jokes loaded: {len(jokes)}")

# Update the status according to resource availability
if jokes:
    status_label.config(
        text=f"{len(jokes)} jokes available - Ready to entertain"
    )
else:
    status_label.config(
        text="No jokes available - Check resource file"
    )

# Keep the application running
root.mainloop()

import tkinter as tk
import subprocess

# Function to handle Endless Mode selection
def endless_mode():
    print("Endless Mode selected")
    # Run the game_copy.py script
    subprocess.Popen(["python", "game_endless.py"])

# Function to handle Timed Mode selection
def timed_mode():
    print("Timed Mode selected")
    subprocess.Popen(["python", "game_timed.py"])
    # Add your logic here for timed mode

# Initialize the Tkinter window
root = tk.Tk()
root.title("BCI Game Menu")
root.geometry("300x200")

# Create a label for the title
title_label = tk.Label(root, text="Select Game Mode", font=("Arial", 16))
title_label.pack(pady=20)

# Create buttons for the two game modes
endless_button = tk.Button(root, text="Endless Mode", font=("Arial", 12), command=endless_mode)
endless_button.pack(pady=10)

timed_button = tk.Button(root, text="Timed Mode", font=("Arial", 12), command=timed_mode)
timed_button.pack(pady=10)


root.mainloop()

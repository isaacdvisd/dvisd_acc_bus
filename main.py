"""
Program designed to help with bus scheduling for Del Valle ACC students.
"""

from datetime import datetime
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfile
import pandas as pd
from PIL import Image, ImageTk


def upload_csv(root, update_status):
    """
    Function to upload a CSV file.
    """

    # Open a file dialog to select a file
    file = askopenfile(mode="r", filetypes=[("CSV Files", "*.csv")])

    if file is None:
        update_status("Ready.")
        return # User cancelled the file dialog

    if not file.name.lower().endswith(".csv"):
        tk.messagebox.showerror("Error", "Please select a CSV file.")
        update_status("Please select a CSV file.")
        return
    
    # Read the CSV file
    try:
        df = pd.read_csv(file.name)
        # rest of your code to display the CSV in tree view
        update_status(f"Loaded file: {file.name}")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to read the file: {str(e)}")

    # Display the data in a table
    tree = ttk.Treeview(root)
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in tree["columns"]:
        tree.heading(col, text=col)

    for index, row in df.iterrows():
        tree.insert("", index, values=list(row))

    tree.pack()


def main():
    """
    Main function to run the program.
    """

    WIN_LENGTH = 400
    WIN_WIDTH = 600

    # Create the main window
    root = tk.Tk()
    root.title("Del Valle ACC Bus Routes")
    root.minsize(WIN_WIDTH, WIN_LENGTH)

    # Icon for the window
    ico = Image.open("dvisdpic.png")
    photo = ImageTk.PhotoImage(ico)
    root.iconphoto(False, photo)

    status = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(message):
        status.config(text=message)
        root.update_idletasks()

    # Create the menu bar
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=lambda: upload_csv(root, update_status))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    root.mainloop()


if __name__ == "__main__":
    main()

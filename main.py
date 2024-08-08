from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter import messagebox
from tkinter import font  # Correct import for font
import pandas as pd
from PIL import Image, ImageTk


def display_icon(root):
    """
    Used to display an icon on the window. Instead of reusing the same code,
    it is better to create a function.
    """
    ico = Image.open("dvisdpic.png")
    photo = ImageTk.PhotoImage(ico)
    root.iconphoto(False, photo)


def add_bus_route():
    """
    Create a new window to add a bus route to the system and display the routes.
    """
    window = tk.Toplevel()
    window.title("Add Bus Routes")
    window.geometry("600x400")  # Adjusted size for more content
    window.minsize(700, 400)

    display_icon(window)

    # Days of the week and locations
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    locations = ["Riverside", "Eastview", "Highland", 'Del Valle Highschool', 'ECHS']

    # Dictionary to store the variables associated with the checkbuttons
    day_vars = {day: tk.BooleanVar() for day in days}
    location_vars = {location: tk.BooleanVar() for location in locations}

    # Frame for days of the week
    days_frame = tk.Frame(window)
    days_frame.pack(fill=tk.X)
    tk.Label(days_frame, text="Select Days:").pack(side=tk.LEFT)
    for day in days:
        cb = tk.Checkbutton(days_frame, text=day, variable=day_vars[day])
        cb.pack(side=tk.LEFT, padx=5)

    # Frame for locations
    locations_frame = tk.Frame(window)
    locations_frame.pack(fill=tk.X)
    tk.Label(locations_frame, text="Select Destination:").pack(side=tk.LEFT)
    for location in locations:
        cb = tk.Checkbutton(locations_frame, text=location, variable=location_vars[location])
        cb.pack(side=tk.LEFT, padx=5)

    # Bus route number and name
    bus_route_frame = tk.Frame(window)
    bus_route_frame.pack(fill=tk.X)
    bus_route_label = tk.Label(bus_route_frame, text="Bus Route Number:")
    bus_route_label.pack(side=tk.LEFT)
    bus_route_entry = tk.Entry(bus_route_frame)
    bus_route_entry.pack(side=tk.LEFT, padx=10)

    bus_route_name_label = tk.Label(bus_route_frame, text="Bus Route Name:")
    bus_route_name_label.pack(side=tk.LEFT)
    bus_route_name_entry = tk.Entry(bus_route_frame)
    bus_route_name_entry.pack(side=tk.LEFT, padx=10)

    # Time entry for the bus route
    time_frame = tk.Frame(window)
    time_frame.pack(fill=tk.X)
    time_label = tk.Label(time_frame, text="Time (HH:MM):")
    time_label.pack(side=tk.LEFT)
    time_entry = tk.Entry(time_frame)
    time_entry.pack(side=tk.LEFT, padx=10)

    # Submit button
    submit_button = tk.Button(window, text="Submit", command=lambda: submit_bus_route(bus_route_entry, bus_route_name_entry, day_vars, location_vars, time_entry, window))
    submit_button.pack(pady=10)

    # Listbox to display bus routes
    route_listbox = tk.Listbox(window, height=10, width=80)
    route_listbox.pack(pady=10)

    # Modify submit_bus_route to use route_listbox
    def submit_bus_route(bus_route_entry, bus_route_name_entry, day_vars, location_vars, time_entry, window):
        bus_number = bus_route_entry.get()
        bus_name = bus_route_name_entry.get()
        time = time_entry.get()
        selected_days = ', '.join(day for day, var in day_vars.items() if var.get())
        selected_locations = ', '.join(loc for loc, var in location_vars.items() if var.get())

        route_details = f"{bus_name} - {bus_number}: {selected_locations} at {time} on {selected_days}"
        route_listbox.insert(tk.END, route_details)  # Add the route details to the Listbox

        # Optionally clear entries after submission for new input
        bus_route_entry.delete(0, tk.END)
        bus_route_name_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        for var in day_vars.values():
            var.set(False)
        for var in location_vars.values():
            var.set(False)


def setup_mouse_wheel_scrolling(tree, root):
    """
    Sets up mouse wheel scrolling for horizontal (with Shift) and vertical
    (without Shift) in Treeview.
    """
    def mouse_wheel(event):
        if event.state & 0x0001:  # Shift is down, check for horizontal scroll
            tree.xview_scroll(int(-1*(event.delta/120)), "units")
        else:
            tree.yview_scroll(int(-1*(event.delta/120)), "units")

    root.bind_all("<MouseWheel>", mouse_wheel)


def upload_csv(root, update_status):
    """
    Upload a CSV file and display it in a Treeview widget.
    """
    update_status("Loading...")
    file = askopenfile(mode="r", filetypes=[("CSV Files", "*.csv")])
    if file is None:
        update_status("Ready.")
        return  # User cancelled the file dialog

    if not file.name.lower().endswith(".csv"):
        messagebox.showerror("Error", "Please select a CSV file.")
        update_status("Please select a CSV file.")
        return

    try:
        df = pd.read_csv(file.name)
        # Remove any previous treeview and scrollbars if they exist
        for widget in root.winfo_children():
            if isinstance(widget, (ttk.Treeview, ttk.Scrollbar)):
                widget.destroy()

        tree = ttk.Treeview(root)
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        # Setup font for measuring text width
        my_font = font.Font(family="Helvetica", size=10, weight="bold")
        PADDING = 10
        for col in tree["columns"]:
            tree.heading(col, text=col)
            width = my_font.measure(col) + PADDING  # Adding a small padding to column width
            tree.column(col, width=width)

        for index, row in df.iterrows():
            tree.insert("", index, values=list(row))

        # Horizontal Scrollbar
        h_scroll = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=h_scroll.set)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Vertical Scrollbar
        v_scroll = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=v_scroll.set)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Setup mouse wheel scrolling
        setup_mouse_wheel_scrolling(tree, root)

        update_status(f"Loaded file: {file.name}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        update_status("Ready.")


    def travel_time():
        """
        Calculate the travel time between two locations.
        """
        update_status("Calculating Travel Time...")
        # Add your code here to calculate the travel time
        update_status("Travel Time Calculated.")


    def generate_schedule():
        """
        Generate a schedule based on the uploaded CSV file and the bus routes.
        The schedule should contain the days of the week, the bus routes,
        the location,and times. It should also contain which students
        are assigned to each bus route.
        """
        update_status("Generating Schedule...")
        # Add your code here to generate the schedule
        update_status("Schedule Generated.")


def main():
    """
    Main function to create the main window and run the application.
    """
    root = tk.Tk()
    root.title("Del Valle ACC Bus Routes")
    root.minsize(600, 400)

    display_icon(root)

    # Status bar at the very bottom
    status = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status.pack(side=tk.BOTTOM, fill=tk.X)

    # Button above the status bar
    add_bus_route_button = tk.Button(root, text="Add Bus Route", command=add_bus_route)
    add_bus_route_button.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=10)

    def update_status(message):
        status.config(text=message)
        root.update_idletasks()

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

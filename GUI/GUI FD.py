import tkinter as tk
from tkinter import ttk

# Therapist data - This is a list of dictionaries with details about therapists
therapists = [
    {"name": "Dr. John Smith", "specialty": "Anxiety", "gender": "Male", "image": "male_icon.gif", "phone": "555-123-4567"},
    {"name": "Dr. Sarah Lee", "specialty": "Anxiety", "gender": "Female", "image": "female_icon.gif", "phone": "555-987-6543"},
    {"name": "Dr. Mark Green", "specialty": "Depression", "gender": "Male", "image": "male_icon.gif", "phone": "555-456-7890"},
    {"name": "Dr. Emily White", "specialty": "Depression", "gender": "Female", "image": "female_icon.gif", "phone": "555-654-3210"},
    {"name": "Dr. Alex Brown", "specialty": "PTSD", "gender": "Male", "image": "male_icon.gif", "phone": "555-234-5678"},
    {"name": "Dr. Laura Gray", "specialty": "PTSD", "gender": "Female", "image": "female_icon.gif", "phone": "555-876-5432"},
    {"name": "Dr. David Black", "specialty": "Family Therapy", "gender": "Male", "image": "male_icon.gif", "phone": "555-345-6789"},
    {"name": "Dr. Lily Adams", "specialty": "Family Therapy", "gender": "Female", "image": "female_icon.gif", "phone": "555-765-4321"},
    {"name": "Dr. Michael Johnson", "specialty": "Substance Abuse", "gender": "Male", "image": "male_icon.gif", "phone": "555-456-7891"},
    {"name": "Dr. Olivia Brown", "specialty": "Substance Abuse", "gender": "Female", "image": "female_icon.gif", "phone": "555-876-5433"},
]

# Global variables to store user selections and data
gender_var = None  # Stores the user's selected gender
specialty_var = None  # Stores the user's selected specialty
saved_therapists = []  # List of therapists saved by the user
therapist_images = {}  # Dictionary to store therapist images
previous_screen = None  # Tracks the previous screen for navigation

# Function to load therapist images
def load_images():
    """
    This function loads images for all therapists in the therapists list.
    Images are stored in a dictionary for easy reuse across the program.
    """
    global therapist_images
    for therapist in therapists:
        try:
            therapist_images[therapist["image"]] = tk.PhotoImage(file=therapist["image"])
        except Exception as e:
            print(f"Error loading image {therapist['image']}: {e}")

# Initialize the tkinter application window
root = tk.Tk()
root.title("MindMatch")  # Sets the title of the application window
root.geometry("600x400")  # Specifies the window size

# Set a light blue background color for all screens
bg_color = "#d0f0f8"  # Light blue background color

# Function to clear all widgets from the screen
def clear_screen():
    """
    Removes all widgets currently displayed on the screen.
    This is called before switching to a new screen.
    """
    for widget in root.winfo_children():
        widget.destroy()

# Function to create a scrollable frame
def create_scrollable_frame(parent):
    """
    Creates a scrollable frame to display content that may not fit within the visible area.
    """
    canvas = tk.Canvas(parent, bg=bg_color)  # The canvas acts as the base for scrolling
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)  # Adds a vertical scrollbar
    scrollable_frame = tk.Frame(canvas, bg=bg_color)  # The frame that holds the content

    # Configure the canvas to scroll when the content overflows
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scrollable_frame

# Function to create the hamburger menu
def create_hamburger_menu(parent):
    """
    Creates a dropdown menu accessible via a hamburger button.
    The menu allows navigation to the homepage, back, and saved therapists.
    """
    menu_button = tk.Button(parent, text="☰", font=("Arial", 16), command=lambda: menu.tk_popup(menu_button.winfo_rootx(), menu_button.winfo_rooty() + 30))
    menu_button.pack(anchor="nw", padx=10, pady=10)

    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Home", command=show_main_screen)
    if previous_screen:
        menu.add_command(label="Back", command=previous_screen)
    menu.add_command(label="View Saved Therapists", command=show_saved_therapists_screen)

# Function to display the main screen
def show_main_screen():
    """
    Displays the main screen where users can choose to find a therapist or view saved therapists.
    """
    global previous_screen
    previous_screen = None
    clear_screen()
    root.configure(bg=bg_color)
    create_hamburger_menu(root)

    tk.Label(root, text="Welcome to MindMatch", font=("Helvetica", 16), bg=bg_color).pack(pady=50)
    tk.Button(root, text="Find a Therapist", command=show_gender_screen).pack(pady=5)
    tk.Button(root, text="View Saved Therapists", command=show_saved_therapists_screen).pack(pady=5)

# Function to display the gender selection screen
def show_gender_screen():
    """
    Allows the user to select the gender of their therapist.
    """
    global previous_screen, gender_var
    previous_screen = show_main_screen
    clear_screen()
    root.configure(bg=bg_color)
    create_hamburger_menu(root)

    tk.Label(root, text="Choose Gender", font=("Helvetica", 16), bg=bg_color).pack(pady=10)
    gender_var = tk.StringVar(value="Any")  # Default value
    tk.Radiobutton(root, text="Male", variable=gender_var, value="Male", bg=bg_color).pack(pady=5)
    tk.Radiobutton(root, text="Female", variable=gender_var, value="Female", bg=bg_color).pack(pady=5)
    tk.Radiobutton(root, text="Any (Male & Female)", variable=gender_var, value="Any", bg=bg_color).pack(pady=5)

    tk.Button(root, text="Submit", command=show_specialty_screen).pack(pady=20)

# Function to display the specialty selection screen
def show_specialty_screen():
    """
    Allows the user to select the specialty of their therapist using a dropdown menu.
    """
    global previous_screen, specialty_var
    previous_screen = show_gender_screen
    clear_screen()
    root.configure(bg=bg_color)
    create_hamburger_menu(root)

    tk.Label(root, text="Choose Specialty", font=("Helvetica", 16), bg=bg_color).pack(pady=10)
    specialties = ["Anxiety", "Depression", "PTSD", "Family Therapy", "Substance Abuse"]
    specialty_var = tk.StringVar(value="Select a Specialty")
    ttk.Combobox(root, textvariable=specialty_var, values=specialties, state="readonly").pack(pady=20)

    tk.Button(root, text="Submit", command=show_results_screen).pack(pady=20)

# Function to display the results screen
def show_results_screen():
    """
    Displays therapists based on the user's selected gender and specialty.
    """
    global previous_screen
    previous_screen = show_specialty_screen
    clear_screen()
    root.configure(bg=bg_color)
    create_hamburger_menu(root)

    tk.Label(root, text="Therapist Results", font=("Helvetica", 16), bg=bg_color).pack(pady=10)
    scrollable_frame = create_scrollable_frame(root)

    # Filter therapists based on user's selections
    gender = gender_var.get()
    specialty = specialty_var.get()
    results = [
        t for t in therapists
        if (t["gender"] == gender or gender == "Any") and
           (t["specialty"] == specialty or specialty == "Select a Specialty")
    ]

    # Display each therapist in the results
    for therapist in results:
        frame = tk.Frame(scrollable_frame, bg=bg_color)
        frame.pack(fill="x", padx=10, pady=5)

        # Add therapist image
        img = therapist_images.get(therapist["image"], None)
        if img:
            tk.Label(frame, image=img, bg=bg_color).pack(side="left", padx=5)

        # Add therapist information
        info = f"{therapist['name']} - {therapist['specialty']} ({therapist['gender']})"
        tk.Label(frame, text=info, bg=bg_color).pack(side="left", padx=5)

        # Add a Save button
        tk.Button(frame, text="Save", command=lambda t=therapist: save_therapist(t)).pack(side="right")

    # Button to view saved therapists
    tk.Button(root, text="View Saved Therapists", command=show_saved_therapists_screen).pack(pady=20)

# Function to save a therapist
def save_therapist(therapist):
    """
    Adds the selected therapist to the saved therapists list.
    """
    if therapist not in saved_therapists:
        saved_therapists.append(therapist)
        print(f"Saved: {therapist['name']}")

# Function to display the saved therapists screen
def show_saved_therapists_screen():
    """
    Displays a list of therapists saved by the user in a scrollable frame.
    """
    global previous_screen
    previous_screen = show_results_screen
    clear_screen()
    root.configure(bg=bg_color)
    create_hamburger_menu(root)

    tk.Label(root, text="Saved Therapists", font=("Helvetica", 16), bg=bg_color).pack(pady=10)

    # Create a scrollable frame for saved therapists
    scrollable_frame = create_scrollable_frame(root)

    if saved_therapists:
        for therapist in saved_therapists:
            frame = tk.Frame(scrollable_frame, bg=bg_color)
            frame.pack(fill="x", padx=10, pady=5)

            # Display therapist image
            img = therapist_images.get(therapist["image"], None)
            if img:
                tk.Label(frame, image=img, bg=bg_color).pack(side="left", padx=5)

            # Display therapist name and phone number
            info = f"{therapist['name']} - {therapist['phone']}"
            tk.Label(frame, text=info, bg=bg_color).pack(side="left", padx=5)
    else:
        tk.Label(scrollable_frame, text="No therapists saved yet.", bg=bg_color).pack(pady=10)

# Load therapist images and start the application
load_images()
show_main_screen()
root.mainloop()

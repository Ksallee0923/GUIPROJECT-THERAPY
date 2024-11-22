"""<a href="https://www.flaticon.com/free-icons/gender" title="gender icons">Gender icons created by Aranagraphics - Flaticon</a>"""

import tkinter as tk
from tkinter import ttk

class MindMatchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MindMatch")
        self.geometry("600x400")
        self.saved_therapists = []

        # Load images once and store them for reuse
        self.male_icon = tk.PhotoImage(file="male_icon.gif")
        self.female_icon = tk.PhotoImage(file="female_icon.gif")
        self.any_icon = tk.PhotoImage(file="any_icon.gif")
        self.profile_icon = tk.PhotoImage(file="profile_icon.gif")

        self.frames = {}
        for F in (MainScreen, GenderScreen, AgeScreen, SpecialtyScreen, LocationScreen, ResultsScreen, SavedTherapistsScreen):
            frame = F(self, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainScreen)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

class BaseScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Hamburger button with a dropdown menu
        hamburger_button = tk.Button(self, text="☰", font=("Arial", 14), command=self.show_menu)
        hamburger_button.pack(anchor="nw", padx=10, pady=10)

        # Create a dropdown menu
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Home", command=lambda: controller.show_frame(MainScreen))
        self.menu.add_command(label="Back", command=lambda: controller.show_frame(controller.last_frame))
        self.menu.add_command(label="Saved Therapists", command=lambda: controller.show_frame(SavedTherapistsScreen))

    def show_menu(self):
        # Display the menu at the location of the hamburger button
        self.menu.tk_popup(self.winfo_rootx() + 10, self.winfo_rooty() + 40)

class MainScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Welcome to MindMatch", font=("Helvetica", 16)).pack(pady=50)
        
        tk.Button(self, text="Find a Therapist", command=lambda: controller.show_frame(GenderScreen)).pack(pady=5)
        tk.Button(self, text="View Saved Therapists", command=lambda: controller.show_frame(SavedTherapistsScreen)).pack(pady=5)

class GenderScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        controller.last_frame = MainScreen
        
        tk.Label(self, text="Choose Gender", font=("Helvetica", 16)).pack(pady=10)

        # Create a canvas and scrollbar for scrolling
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configure the scrollbar for the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Gender selection options within the scrollable frame
        self.gender_var = tk.StringVar(value="Any")

        tk.Radiobutton(scrollable_frame, text="Male", variable=self.gender_var, value="Male", image=controller.male_icon, compound="left").pack(pady=5)
        tk.Radiobutton(scrollable_frame, text="Female", variable=self.gender_var, value="Female", image=controller.female_icon, compound="left").pack(pady=5)
        tk.Radiobutton(scrollable_frame, text="Any", variable=self.gender_var, value="Any", image=controller.any_icon, compound="left").pack(pady=5)
        
        tk.Button(scrollable_frame, text="OK", command=lambda: controller.show_frame(AgeScreen)).pack(pady=20)

class AgeScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        controller.last_frame = GenderScreen
        tk.Label(self, text="Choose Age Range", font=("Helvetica", 16)).pack(pady=10)
        
        tk.Label(self, text="Select Age Range", image=controller.any_icon, compound="left").pack(anchor="w")

        age_options = ["18-30", "31-50", "Any"]
        self.age_var = tk.StringVar(value="Any")
        ttk.Combobox(self, textvariable=self.age_var, values=age_options).pack(fill="x", pady=5)
        
        tk.Button(self, text="OK", command=lambda: controller.show_frame(SpecialtyScreen)).pack(pady=20)

class SpecialtyScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        controller.last_frame = AgeScreen
        tk.Label(self, text="Choose Specialty", font=("Helvetica", 16)).pack(pady=10)

        specialty_options = ["Anxiety", "Family Therapy", "Depression", "PTSD", "Relationship Issues", "Substance Abuse"]
        self.specialty_var = tk.StringVar(value="Any")
        ttk.Combobox(self, textvariable=self.specialty_var, values=specialty_options).pack(fill="x", pady=5)
        
        tk.Button(self, text="OK", command=lambda: controller.show_frame(LocationScreen)).pack(pady=20)

class LocationScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        controller.last_frame = SpecialtyScreen
        tk.Label(self, text="Choose Location", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(self, text="Select Location", image=controller.any_icon, compound="left").pack(anchor="w")
        
        location_options = ["Nearby", "Online", "Any"]
        self.location_var = tk.StringVar(value="Any")
        ttk.Combobox(self, textvariable=self.location_var, values=location_options).pack(fill="x", pady=5)
        
        tk.Button(self, text="OK", command=lambda: controller.show_frame(ResultsScreen)).pack(pady=20)

class ResultsScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        controller.last_frame = LocationScreen
        tk.Label(self, text="Therapist Results", font=("Helvetica", 16)).pack(pady=10)
        
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        therapists = ["Therapist A", "Therapist B", "Therapist C"]

        for therapist in therapists:
            frame = tk.Frame(scrollable_frame, padx=10, pady=5)
            frame.pack(fill="x", padx=10, pady=5)
            tk.Label(frame, text=therapist, image=controller.profile_icon, compound="left").pack(side="left")
            tk.Button(frame, text="Save", command=lambda t=therapist: self.save_therapist(t, controller)).pack(side="right")

        tk.Button(self, text="OK", command=lambda: controller.show_frame(SavedTherapistsScreen)).pack(pady=20)

    def save_therapist(self, therapist, controller):
        if therapist not in controller.saved_therapists:
            controller.saved_therapists.append(therapist)
        # Removed the messagebox.showinfo line

class SavedTherapistsScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Saved Therapists", font=("Helvetica", 16)).pack(pady=10)
        self.therapist_list = tk.Frame(self)
        self.therapist_list.pack(pady=10)
        tk.Button(self, text="OK", command=lambda: controller.show_frame(MainScreen)).pack(pady=5)
        
        # Store images to prevent garbage collection
        self.saved_images = []

    def tkraise(self):
        super().tkraise()
        
        # Clear previous widgets
        for widget in self.therapist_list.winfo_children():
            widget.destroy()

        saved_therapists = self.controller.saved_therapists
        
        if saved_therapists:
            for therapist in saved_therapists:
                tk.Label(self.therapist_list, text=therapist, image=self.controller.profile_icon, compound="left").pack(anchor="w", pady=2)
                
                # Append image to saved_images to keep it in memory
                self.saved_images.append(self.controller.profile_icon)
        else:
            tk.Label(self.therapist_list, text="No therapists saved.").pack()

if __name__ == "__main__":
    app = MindMatchApp()
    app.mainloop()



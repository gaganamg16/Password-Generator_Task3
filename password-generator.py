import tkinter as tk
from tkinter import ttk, messagebox
import string
import secrets


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("SecurePass | Password Generator")
        self.root.geometry("1100x800")
        self.root.minsize(950, 700)
        self.root.configure(bg="#10141c")

        self.password_visible = False

        self.setup_styles()
        self.create_interface()

        self.root.bind("<Control-Return>", lambda event: self.generate_password())

    # --------------------------------------------------------
    # STYLES
    # --------------------------------------------------------
    def setup_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TCheckbutton",
            background="#181e29",
            foreground="#dce3ef",
            font=("Segoe UI", 11)
        )

        style.configure(
            "TSpinbox",
            fieldbackground="#202735",
            foreground="#ffffff",
            font=("Segoe UI", 11)
        )

    # --------------------------------------------------------
    # MAIN INTERFACE
    # --------------------------------------------------------
    def create_interface(self):

        # Header
        header = tk.Frame(
            self.root,
            bg="#151b26",
            height=85
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🔐 SecurePass",
            bg="#151b26",
            fg="#ffffff",
            font=("Segoe UI", 26, "bold")
        ).pack(side="left", padx=30, pady=20)

        tk.Label(
            header,
            text="Professional Password Generator",
            bg="#151b26",
            fg="#8d99aa",
            font=("Segoe UI", 11)
        ).pack(side="right", padx=30)

        # Main container
        main = tk.Frame(
            self.root,
            bg="#10141c"
        )
        main.pack(fill="both", expand=True, padx=25, pady=25)

        # Left panel
        left = tk.Frame(
            main,
            bg="#181e29",
            highlightbackground="#293243",
            highlightthickness=1
        )
        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 12)
        )

        # Right panel
        right = tk.Frame(
            main,
            bg="#181e29",
            highlightbackground="#293243",
            highlightthickness=1,
            width=290
        )
        right.pack(
            side="right",
            fill="y",
            padx=(12, 0)
        )
        right.pack_propagate(False)

        self.create_generator_panel(left)
        self.create_info_panel(right)

        # Footer
        footer = tk.Label(
            self.root,
            text="Secure generation • No passwords are saved by this application",
            bg="#10141c",
            fg="#667085",
            font=("Segoe UI", 9)
        )
        footer.pack(pady=(0, 12))

    # --------------------------------------------------------
    # GENERATOR PANEL
    # --------------------------------------------------------
    def create_generator_panel(self, parent):

        tk.Label(
            parent,
            text="Generate Password",
            bg="#181e29",
            fg="#ffffff",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=25, pady=(25, 5))

        tk.Label(
            parent,
            text="Create a strong password using customizable options.",
            bg="#181e29",
            fg="#8792a5",
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=25, pady=(0, 20))

        # Password display
        password_frame = tk.Frame(
            parent,
            bg="#202735"
        )
        password_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )

        self.password_var = tk.StringVar()

        self.password_entry = tk.Entry(
            password_frame,
            textvariable=self.password_var,
            bg="#202735",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            font=("Consolas", 16, "bold"),
            show="•"
        )
        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
            pady=15
        )

        self.show_button = tk.Button(
            password_frame,
            text="Show",
            command=self.toggle_password,
            bg="#293243",
            fg="#ffffff",
            activebackground="#364154",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold")
        )
        self.show_button.pack(
            side="right",
            padx=10,
            pady=10
        )

        # Strength
        strength_frame = tk.Frame(
            parent,
            bg="#181e29"
        )
        strength_frame.pack(
            fill="x",
            padx=25,
            pady=(15, 10)
        )

        tk.Label(
            strength_frame,
            text="Password Strength",
            bg="#181e29",
            fg="#aeb8c8",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        self.strength_label = tk.Label(
            strength_frame,
            text="Not generated",
            bg="#181e29",
            fg="#8792a5",
            font=("Segoe UI", 10, "bold")
        )
        self.strength_label.pack(side="right")

        self.strength_bar = ttk.Progressbar(
            parent,
            orient="horizontal",
            mode="determinate",
            maximum=100
        )
        self.strength_bar.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        # Length
        length_frame = tk.Frame(
            parent,
            bg="#181e29"
        )
        length_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )

        tk.Label(
            length_frame,
            text="Password Length",
            bg="#181e29",
            fg="#dce3ef",
            font=("Segoe UI", 11, "bold")
        ).pack(side="left")

        self.length_var = tk.IntVar(value=16)

        self.length_spin = tk.Spinbox(
            length_frame,
            from_=4,
            to=64,
            textvariable=self.length_var,
            width=5,
            bg="#202735",
            fg="#ffffff",
            buttonbackground="#293243",
            insertbackground="#ffffff",
            relief="flat",
            font=("Segoe UI", 11)
        )
        self.length_spin.pack(side="right")

        # Separator
        tk.Frame(
            parent,
            bg="#293243",
            height=1
        ).pack(
            fill="x",
            padx=25,
            pady=20
        )

        # Character options
        tk.Label(
            parent,
            text="Character Options",
            bg="#181e29",
            fg="#ffffff",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=25, pady=(0, 10))

        options = tk.Frame(
            parent,
            bg="#181e29"
        )
        options.pack(fill="x", padx=25)

        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            options,
            text="Uppercase (A-Z)",
            variable=self.upper_var
        ).grid(row=0, column=0, sticky="w", pady=5)

        ttk.Checkbutton(
            options,
            text="Lowercase (a-z)",
            variable=self.lower_var
        ).grid(row=0, column=1, sticky="w", padx=25, pady=5)

        ttk.Checkbutton(
            options,
            text="Numbers (0-9)",
            variable=self.number_var
        ).grid(row=1, column=0, sticky="w", pady=5)

        ttk.Checkbutton(
            options,
            text="Symbols (!@#...)",
            variable=self.symbol_var
        ).grid(row=1, column=1, sticky="w", padx=25, pady=5)

        # Custom characters
        tk.Label(
            parent,
            text="Custom Characters (Optional)",
            bg="#181e29",
            fg="#dce3ef",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=25, pady=(18, 5))

        self.custom_var = tk.StringVar()

        self.custom_entry = tk.Entry(
            parent,
            textvariable=self.custom_var,
            bg="#202735",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            font=("Segoe UI", 10)
        )
        self.custom_entry.pack(
            fill="x",
            padx=25,
            ipady=8
        )

        # Buttons
        button_frame = tk.Frame(
            parent,
            bg="#181e29"
        )
        button_frame.pack(
            fill="x",
            padx=25,
            pady=25
        )

        generate_button = tk.Button(
            button_frame,
            text="⚡  Generate Password",
            command=self.generate_password,
            bg="#4f46e5",
            fg="#ffffff",
            activebackground="#4338ca",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=12
        )
        generate_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 6)
        )

        copy_button = tk.Button(
            button_frame,
            text="📋 Copy",
            command=self.copy_password,
            bg="#293243",
            fg="#ffffff",
            activebackground="#364154",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=12
        )
        copy_button.pack(
            side="left",
            padx=6
        )

        clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_password,
            bg="#293243",
            fg="#ffffff",
            activebackground="#364154",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=12
        )
        clear_button.pack(
            side="right",
            padx=(6, 0)
        )

        # Status
        self.status_var = tk.StringVar(
            value="Ready to generate a password."
        )

        tk.Label(
            parent,
            textvariable=self.status_var,
            bg="#181e29",
            fg="#7dd3fc",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

    # ---------------------------------------------------------
    # INFORMATION PANEL
    # ---------------------------------------------------------
    def create_info_panel(self, parent):

        tk.Label(
            parent,
            text="Password Tips",
            bg="#181e29",
            fg="#ffffff",
            font=("Segoe UI", 17, "bold")
        ).pack(
            anchor="w",
            padx=22,
            pady=(25, 15)
        )

        tips = [
            ("01", "Use longer passwords",
             "Longer passwords generally provide more protection."),

            ("02", "Mix character types",
             "Use uppercase, lowercase, numbers and symbols."),

            ("03", "Avoid personal information",
             "Don't use names, birthdays or easily guessed details."),

            ("04", "Use unique passwords",
             "Avoid reusing the same password across accounts.")
        ]

        for number, title, description in tips:

            card = tk.Frame(
                parent,
                bg="#202735"
            )
            card.pack(
                fill="x",
                padx=18,
                pady=7
            )

            tk.Label(
                card,
                text=number,
                bg="#202735",
                fg="#818cf8",
                font=("Segoe UI", 10, "bold")
            ).pack(
                anchor="w",
                padx=12,
                pady=(10, 2)
            )

            tk.Label(
                card,
                text=title,
                bg="#202735",
                fg="#ffffff",
                font=("Segoe UI", 10, "bold")
            ).pack(
                anchor="w",
                padx=12
            )

            tk.Label(
                card,
                text=description,
                bg="#202735",
                fg="#8994a7",
                justify="left",
                wraplength=230,
                font=("Segoe UI", 9)
            ).pack(
                anchor="w",
                padx=12,
                pady=(3, 10)
            )

        # Privacy section
        privacy = tk.Frame(
            parent,
            bg="#151b26"
        )
        privacy.pack(
            fill="x",
            padx=18,
            pady=20
        )

        tk.Label(
            privacy,
            text="🔒 Privacy",
            bg="#151b26",
            fg="#ffffff",
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        tk.Label(
            privacy,
            text="Generated passwords are kept only in the application while it is running.",
            bg="#151b26",
            fg="#7f8a9c",
            justify="left",
            wraplength=230,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

    # --------------------------------------------------------
    # GENERATE PASSWORD
    # --------------------------------------------------------
    def generate_password(self):

        try:
            length = int(self.length_var.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Length",
                "Please enter a valid password length."
            )
            return

        if length < 4 or length > 64:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be between 4 and 64."
            )
            return

        character_sets = []

        if self.upper_var.get():
            character_sets.append(string.ascii_uppercase)

        if self.lower_var.get():
            character_sets.append(string.ascii_lowercase)

        if self.number_var.get():
            character_sets.append(string.digits)

        if self.symbol_var.get():
            character_sets.append(string.punctuation)

        custom_characters = self.custom_var.get()

        if custom_characters:
            character_sets.append(custom_characters)

        if not character_sets:
            messagebox.showwarning(
                "No Characters Selected",
                "Select at least one character type."
            )
            return

        # Remove duplicate characters while preserving order
        combined = "".join(
            dict.fromkeys("".join(character_sets))
        )

        if len(combined) == 0:
            messagebox.showwarning(
                "Invalid Characters",
                "Please provide valid characters."
            )
            return

        # Make sure selected categories are represented
        password_chars = []

        for charset in character_sets:
            password_chars.append(
                secrets.choice(charset)
            )

        # Fill remaining length
        while len(password_chars) < length:
            password_chars.append(
                secrets.choice(combined)
            )

        # Secure shuffle
        secrets.SystemRandom().shuffle(password_chars)

        password = "".join(password_chars)

        self.password_var.set(password)
        self.password_visible = False
        self.password_entry.config(show="•")
        self.show_button.config(text="Show")

        self.update_strength(password)

        self.status_var.set(
            "Password generated successfully."
        )

    # --------------------------------------------------------
    # PASSWORD STRENGTH
    # --------------------------------------------------------
    def update_strength(self, password):

        if not password:
            self.strength_label.config(
                text="Not generated",
                fg="#8792a5"
            )
            self.strength_bar["value"] = 0
            return

        score = 0

        length = len(password)

        if length >= 8:
            score += 20

        if length >= 12:
            score += 20

        if length >= 16:
            score += 20

        if any(c.isupper() for c in password):
            score += 10

        if any(c.islower() for c in password):
            score += 10

        if any(c.isdigit() for c in password):
            score += 10

        if any(c in string.punctuation for c in password):
            score += 10

        self.strength_bar["value"] = score

        if score < 40:
            text = "Weak"
            text_color = "#f87171"
        elif score < 60:
            text = "Fair"
            text_color = "#fbbf24"
        elif score < 80:
            text = "Strong"
            text_color = "#34d399"
        else:
            text = "Very Strong"
            text_color = "#22c55e"

        self.strength_label.config(
            text=text,
            fg=text_color
        )

    # ---------------------------------------------------------
    # SHOW / HIDE PASSWORD
    # ---------------------------------------------------------
    def toggle_password(self):

        if not self.password_var.get():
            return

        self.password_visible = not self.password_visible

        if self.password_visible:
            self.password_entry.config(show="")
            self.show_button.config(text="Hide")
        else:
            self.password_entry.config(show="•")
            self.show_button.config(text="Show")

    # ---------------------------------------------------------
    # COPY PASSWORD
    # ---------------------------------------------------------
    def copy_password(self):

        password = self.password_var.get()

        if not password:
            messagebox.showwarning(
                "Nothing to Copy",
                "Generate a password first."
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()

        self.status_var.set(
            "Password copied to clipboard."
        )

    # --------------------------------------------------------
    # CLEAR
    # --------------------------------------------------------
    def clear_password(self):

        self.password_var.set("")
        self.password_entry.config(show="•")

        self.password_visible = False
        self.show_button.config(text="Show")

        self.strength_bar["value"] = 0

        self.strength_label.config(
            text="Not generated",
            fg="#8792a5"
        )

        self.status_var.set(
            "Password cleared."
        )


# ------------------------------------------------------------
# APPLICATION START
# ------------------------------------------------------------
if __name__ == "__main__":

    root = tk.Tk()

    app = PasswordGenerator(root)

    root.mainloop()

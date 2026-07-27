"""
Project: Cryptographically Secure Random Password Generator (OIBSIP Task 3)
Author: Saniya Tamboli
Track: Python Programming
Organization: Oasis Infobyte
"""

import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator - OIBSIP")
        self.root.geometry("520x620")
        self.root.resizable(False, False)

        # Session history (Max 5 passwords - kept in memory only for security)
        self.history = []

        # UI Setup
        self.create_widgets()

    def create_widgets(self):
        # Header Title
        title_label = tk.Label(
            self.root,
            text="🔒 Random Password Generator",
            font=("Helvetica", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=12,
        )
        title_label.pack(fill=tk.X)

        # Control Frame
        frame = tk.LabelFrame(
            self.root, text=" Custom Criteria ", font=("Helvetica", 11, "bold"), padx=15, pady=10
        )
        frame.pack(padx=20, pady=10, fill=tk.X)

        # Password Length Slider & Spinbox
        tk.Label(frame, text="Password Length (Min 8):", font=("Helvetica", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )

        length_subframe = tk.Frame(frame)
        length_subframe.grid(row=0, column=1, sticky=tk.E, pady=5)

        self.length_var = tk.IntVar(value=12)
        self.length_spin = tk.Spinbox(
            length_subframe,
            from_=8,
            to=64,
            textvariable=self.length_var,
            width=5,
            font=("Helvetica", 10),
            command=self.update_slider_from_spin,
        )
        self.length_spin.pack(side=tk.RIGHT, padx=5)

        self.length_slider = tk.Scale(
            frame,
            from_=8,
            to=64,
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            length=180,
            command=lambda v: self.evaluate_strength_preview(),
        )
        self.length_slider.grid(row=1, column=0, columnspan=2, pady=5)

        # Character Type Checkboxes
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        cb_upper = tk.Checkbutton(
            frame, text="Include Uppercase Letters (A-Z)", variable=self.use_upper, command=self.evaluate_strength_preview
        )
        cb_upper.grid(row=2, column=0, columnspan=2, sticky=tk.W)

        cb_lower = tk.Checkbutton(
            frame, text="Include Lowercase Letters (a-z)", variable=self.use_lower, command=self.evaluate_strength_preview
        )
        cb_lower.grid(row=3, column=0, columnspan=2, sticky=tk.W)

        cb_digits = tk.Checkbutton(
            frame, text="Include Numbers (0-9)", variable=self.use_digits, command=self.evaluate_strength_preview
        )
        cb_digits.grid(row=4, column=0, columnspan=2, sticky=tk.W)

        cb_symbols = tk.Checkbutton(
            frame, text="Include Symbols (!@#$%^&*)", variable=self.use_symbols, command=self.evaluate_strength_preview
        )
        cb_symbols.grid(row=5, column=0, columnspan=2, sticky=tk.W)

        cb_ambiguous = tk.Checkbutton(
            frame,
            text="Exclude Ambiguous Characters (0, O, l, 1, I)",
            variable=self.exclude_ambiguous,
            fg="#c0392b",
            command=self.evaluate_strength_preview,
        )
        cb_ambiguous.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))

        # Output Section
        output_frame = tk.Frame(self.root, padx=20, pady=5)
        output_frame.pack(fill=tk.X)

        self.password_entry = tk.Entry(
            output_frame, font=("Courier", 13, "bold"), justify="center", bd=2, relief="groove"
        )
        self.password_entry.pack(fill=tk.X, ipady=6, pady=5)

        # Password Strength Indicator Bar
        strength_frame = tk.Frame(output_frame)
        strength_frame.pack(fill=tk.X, pady=2)

        tk.Label(strength_frame, text="Strength:", font=("Helvetica", 9, "bold")).pack(side=tk.LEFT)
        self.strength_label = tk.Label(strength_frame, text="Medium", font=("Helvetica", 9, "bold"), fg="#f39c12")
        self.strength_label.pack(side=tk.LEFT, padx=5)

        self.strength_bar = ttk.Progressbar(output_frame, length=100, mode="determinate")
        self.strength_bar.pack(fill=tk.X, pady=2)

        # Action Buttons
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack()

        gen_btn = tk.Button(
            btn_frame,
            text="⚡ Generate Password",
            command=self.generate_password,
            bg="#27ae60",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=10,
            pady=5,
        )
        gen_btn.grid(row=0, column=0, padx=8)

        copy_btn = tk.Button(
            btn_frame,
            text="📋 Copy to Clipboard",
            command=self.copy_to_clipboard,
            bg="#2980b9",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=10,
            pady=5,
        )
        copy_btn.grid(row=0, column=1, padx=8)

        # History Section (Last 5 Passwords)
        history_frame = tk.LabelFrame(
            self.root, text=" Session History (Last 5 Generated) ", font=("Helvetica", 10, "bold"), padx=10, pady=5
        )
        history_frame.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        self.history_listbox = tk.Listbox(
            history_frame, font=("Courier", 9), height=5, selectmode=tk.SINGLE
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Initialize Preview
        self.evaluate_strength_preview()

    def update_slider_from_spin(self):
        try:
            val = int(self.length_spin.get())
            if val < 8:
                val = 8
            elif val > 64:
                val = 64
            self.length_var.set(val)
            self.evaluate_strength_preview()
        except ValueError:
            pass

    def get_selected_pools(self):
        pools = []
        ambiguous_chars = set("0Ol1I")

        if self.use_upper.get():
            chars = [c for c in string.ascii_uppercase if not (self.exclude_ambiguous.get() and c in ambiguous_chars)]
            pools.append(chars)
        if self.use_lower.get():
            chars = [c for c in string.ascii_lowercase if not (self.exclude_ambiguous.get() and c in ambiguous_chars)]
            pools.append(chars)
        if self.use_digits.get():
            chars = [c for c in string.digits if not (self.exclude_ambiguous.get() and c in ambiguous_chars)]
            pools.append(chars)
        if self.use_symbols.get():
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            chars = [c for c in symbols if not (self.exclude_ambiguous.get() and c in ambiguous_chars)]
            pools.append(chars)

        return pools

    def evaluate_strength_preview(self):
        length = self.length_var.get()
        pools = self.get_selected_pools()
        num_types = len(pools)

        if num_types < 2 or length < 8:
            score = 20
            label = "Weak"
            color = "#c0392b"  # Red
        elif num_types == 2 and length < 12:
            score = 40
            label = "Fair"
            color = "#e67e22"  # Orange
        elif num_types >= 3 and 8 <= length < 14:
            score = 70
            label = "Medium"
            color = "#f1c40f"  # Yellow
        elif num_types >= 3 and length >= 14:
            score = 100
            label = "Strong"
            color = "#27ae60"  # Green
        else:
            score = 50
            label = "Medium"
            color = "#f39c12"

        self.strength_bar["value"] = score
        self.strength_label.config(text=label, fg=color)

    def generate_password(self):
        length = self.length_var.get()

        # Validation Checks
        if length < 8:
            messagebox.showerror("Error", "Password length must be at least 8 characters.")
            return

        pools = self.get_selected_pools()

        if len(pools) < 2:
            messagebox.showerror(
                "Criteria Selection Error", "Please select at least 2 character types to ensure security."
            )
            return

        # Guaranteed inclusion rule: pick 1 cryptographically secure char from each selected pool
        password_chars = [secrets.choice(pool) for pool in pools]

        # Combine all allowed characters to fill the rest of the required length
        all_allowed = [char for pool in pools for char in pool]

        if not all_allowed:
            messagebox.showerror("Error", "No characters available with selected options.")
            return

        for _ in range(length - len(password_chars)):
            password_chars.append(secrets.choice(all_allowed))

        # Cryptographically shuffle character placement using SystemRandom
        secrets.SystemRandom().shuffle(password_chars)
        final_password = "".join(password_chars)

        # Display result
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, final_password)

        # Auto-copy to clipboard
        try:
            pyperclip.copy(final_password)
        except Exception:
            pass  # Fallback if clipboard drivers aren't present

        # Update History (Max 5 items)
        self.history.insert(0, final_password)
        if len(self.history) > 5:
            self.history.pop()

        self.history_listbox.delete(0, tk.END)
        for pwd in self.history:
            self.history_listbox.insert(tk.END, pwd)

        self.evaluate_strength_preview()

    def copy_to_clipboard(self):
        pwd = self.password_entry.get()
        if pwd:
            try:
                pyperclip.copy(pwd)
                messagebox.showinfo("Clipboard", "Password copied to clipboard successfully!")
            except Exception as e:
                messagebox.showerror("Clipboard Error", f"Failed to copy to clipboard: {e}")
        else:
            messagebox.showwarning("Warning", "No password generated yet to copy.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
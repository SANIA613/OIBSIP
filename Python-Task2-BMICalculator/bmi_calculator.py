"""
Project: BMI Calculator with Trend Visualization (OIBSIP Task 2)
Author: [Your Name]
Track: Python Programming
Organization: Oasis Infobyte
"""

import sqlite3
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator & Historical Tracker")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        # Initialize SQLite Database
        self.init_db()

        # Build UI Elements
        self.create_widgets()

    def init_db(self):
        """Initializes SQLite database for storing user records."""
        try:
            self.conn = sqlite3.connect("bmi_history.db")
            self.cursor = self.conn.cursor()
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            """
            )
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")

    def create_widgets(self):
        """Creates Tkinter UI Layout."""
        # Title Header
        title_label = tk.Label(
            self.root,
            text="Body Mass Index Calculator",
            font=("Helvetica", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10,
        )
        title_label.pack(fill=tk.X)

        # Input Frame
        input_frame = tk.Frame(self.root, padx=20, pady=15)
        input_frame.pack(fill=tk.X)

        # Name Input
        tk.Label(input_frame, text="User Name:", font=("Helvetica", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.name_entry = tk.Entry(input_frame, font=("Helvetica", 10))
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)

        # Weight Input
        tk.Label(input_frame, text="Weight (kg):", font=("Helvetica", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.weight_entry = tk.Entry(input_frame, font=("Helvetica", 10))
        self.weight_entry.grid(row=1, column=1, pady=5, padx=10)

        # Height Input
        tk.Label(input_frame, text="Height (m):", font=("Helvetica", 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.height_entry = tk.Entry(input_frame, font=("Helvetica", 10))
        self.height_entry.grid(row=2, column=1, pady=5, padx=10)

        # Buttons Frame
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack()

        calc_btn = tk.Button(
            btn_frame,
            text="Calculate & Save",
            command=self.calculate_bmi,
            bg="#27ae60",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=10,
        )
        calc_btn.grid(row=0, column=0, padx=10)

        graph_btn = tk.Button(
            btn_frame,
            text="View User Trend Chart",
            command=self.show_trend_chart,
            bg="#2980b9",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=10,
        )
        graph_btn.grid(row=0, column=1, padx=10)

        # Result Frame
        self.result_frame = tk.Frame(self.root, pady=15)
        self.result_frame.pack(fill=tk.X)

        self.result_label = tk.Label(
            self.result_frame,
            text="Enter details and click Calculate",
            font=("Helvetica", 12, "bold"),
            fg="#7f8c8d",
        )
        self.result_label.pack()

        # Historical Table View
        tk.Label(self.root, text="Recent Saved Records", font=("Helvetica", 11, "bold")).pack(
            pady=(10, 5)
        )

        columns = ("Name", "Weight", "Height", "BMI", "Category", "Date")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=75, anchor=tk.CENTER)

        self.tree.pack(padx=15, fill=tk.BOTH, expand=True)

        self.load_table_data()

    def calculate_bmi(self):
        """Validates input, calculates BMI, determines category, and saves to database."""
        name = self.name_entry.get().strip()
        weight_str = self.weight_entry.get().strip()
        height_str = self.height_entry.get().strip()

        # Input Validation
        if not name:
            messagebox.showwarning("Input Error", "Please enter a user name.")
            return

        try:
            weight = float(weight_str)
            height = float(height_str)

            if weight <= 0 or height <= 0:
                raise ValueError("Values must be positive numbers.")

            # Automatically convert cm to meters if user enters height > 3
            if height > 3.0:
                height = height / 100.0

        except ValueError:
            messagebox.showerror(
                "Input Error", "Weight and Height must be positive numeric values."
            )
            return

        # BMI Calculation
        bmi = weight / (height**2)
        bmi_rounded = round(bmi, 2)

        # Classification & Color Coding
        if bmi < 18.5:
            category = "Underweight"
            color = "#2980b9"  # Blue
        elif 18.5 <= bmi <= 24.9:
            category = "Normal weight"
            color = "#27ae60"  # Green
        elif 25.0 <= bmi <= 29.9:
            category = "Overweight"
            color = "#f39c12"  # Orange
        else:
            category = "Obese"
            color = "#c0392b"  # Red

        # Display Result
        self.result_label.config(
            text=f"BMI: {bmi_rounded:.2f} ({category})", fg=color
        )

        # Save to Database
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        try:
            self.cursor.execute(
                "INSERT INTO bmi_records (username, weight, height, bmi, category, date) VALUES (?, ?, ?, ?, ?, ?)",
                (name, weight, height, bmi_rounded, category, current_date),
            )
            self.conn.commit()
            self.load_table_data()
            messagebox.showinfo("Success", f"Record saved successfully for {name}!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save record: {e}")

    def load_table_data(self):
        """Loads records from SQLite database into Treeview table."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            self.cursor.execute(
                "SELECT username, weight, height, bmi, category, date FROM bmi_records ORDER BY id DESC LIMIT 10"
            )
            for row in self.cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
        except sqlite3.Error as e:
            print(f"Error reading database: {e}")

    def show_trend_chart(self):
        """Displays Matplotlib line chart for selected user's BMI history."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning(
                "Input Error", "Enter a user name to view their trend chart."
            )
            return

        try:
            self.cursor.execute(
                "SELECT date, bmi FROM bmi_records WHERE username = ? ORDER BY id ASC",
                (name,),
            )
            records = self.cursor.fetchall()

            if not records:
                messagebox.showinfo("No Data", f"No records found for user '{name}'.")
                return

            dates = [r[0] for r in records]
            bmis = [r[1] for r in records]

            # Create Top-level Chart Window
            chart_win = tk.Toplevel(self.root)
            chart_win.title(f"BMI History - {name}")
            chart_win.geometry("600x400")

            fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
            ax.plot(dates, bmis, marker="o", color="#8e44ad", linewidth=2)
            ax.axhline(y=18.5, color="b", linestyle="--", label="Underweight (<18.5)")
            ax.axhline(
                y=24.9, color="g", linestyle="--", label="Normal (18.5-24.9)"
            )
            ax.axhline(
                y=29.9, color="orange", linestyle="--", label="Overweight (25-29.9)"
            )

            ax.set_title(f"BMI Progress Chart for {name}")
            ax.set_xlabel("Date")
            ax.set_ylabel("BMI Value")
            plt.xticks(rotation=30, ha="right")
            ax.legend(loc="upper right", fontsize="small")
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=chart_win)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to retrieve data: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
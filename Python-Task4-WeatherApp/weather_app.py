"""
Project: Real-Time Graphical Weather Application (OIBSIP Task 4)
Author: Saniya Tamboli
Track: Python Programming
Organization: Oasis Infobyte
"""

import io
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests

# Default OpenWeatherMap API Key (Can be overridden via environment variables)
# Replace with one of your keys
API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_OPENWEATHER_API_KEY")
class WeatherApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Weather App - Saniya Tamboli")
        self.root.geometry("520x680")
        self.root.resizable(False, False)

        # Unit Tracking: True for Celsius, False for Fahrenheit
        self.is_celsius = True
        self.current_city = ""

        self.setup_ui()
        self.auto_detect_location()

    def setup_ui(self):
        # Header Banner
        title_label = tk.Label(
            self.root,
            text="🌤️ Real-Time Weather Forecast",
            font=("Helvetica", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=12,
        )
        title_label.pack(fill=tk.X)

        # Search Frame
        search_frame = tk.Frame(self.root, pady=10)
        search_frame.pack(fill=tk.X, padx=15)

        self.city_entry = tk.Entry(
            search_frame, font=("Helvetica", 12), width=24
        )
        self.city_entry.grid(row=0, column=0, padx=5)
        self.city_entry.bind("<Return>", lambda event: self.fetch_weather())

        search_btn = tk.Button(
            search_frame,
            text="Get Weather",
            command=self.fetch_weather,
            bg="#2980b9",
            fg="white",
            font=("Helvetica", 10, "bold"),
        )
        search_btn.grid(row=0, column=1, padx=5)

        self.unit_btn = tk.Button(
            search_frame,
            text="Switch to °F",
            command=self.toggle_units,
            bg="#8e44ad",
            fg="white",
            font=("Helvetica", 10, "bold"),
        )
        self.unit_btn.grid(row=0, column=2, padx=5)

        # Error / Notification Message Label
        self.error_label = tk.Label(
            self.root, text="", font=("Helvetica", 10, "bold"), fg="#c0392b"
        )
        self.error_label.pack(pady=2)

        # Current Weather Card Frame
        self.card_frame = tk.LabelFrame(
            self.root, text=" Current Weather ", font=("Helvetica", 11, "bold")
        )
        self.card_frame.pack(fill=tk.X, padx=20, pady=5)

        self.icon_label = tk.Label(self.card_frame)
        self.icon_label.grid(row=0, column=0, rowspan=3, padx=10, pady=5)

        self.temp_label = tk.Label(
            self.card_frame,
            text="-- °C",
            font=("Helvetica", 24, "bold"),
            fg="#2c3e50",
        )
        self.temp_label.grid(row=0, column=1, sticky=tk.W)

        self.desc_label = tk.Label(
            self.card_frame,
            text="Condition: --",
            font=("Helvetica", 11, "italic"),
        )
        self.desc_label.grid(row=1, column=1, sticky=tk.W)

        self.details_label = tk.Label(
            self.card_frame,
            text="Humidity: --% | Wind: -- m/s",
            font=("Helvetica", 10),
        )
        self.details_label.grid(row=2, column=1, sticky=tk.W, pady=(0, 5))

        # 5-Day Forecast Frame
        forecast_container = tk.LabelFrame(
            self.root,
            text=" 5-Day Daily Forecast ",
            font=("Helvetica", 11, "bold"),
        )
        forecast_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.forecast_tree = ttk.Treeview(
            forecast_container,
            columns=("Date", "Condition", "Temp"),
            show="headings",
            height=7,
        )
        self.forecast_tree.heading("Date", text="Date/Time")
        self.forecast_tree.heading("Condition", text="Condition")
        self.forecast_tree.heading("Temp", text="Temperature")

        self.forecast_tree.column("Date", width=140, anchor=tk.CENTER)
        self.forecast_tree.column("Condition", width=160, anchor=tk.CENTER)
        self.forecast_tree.column("Temp", width=120, anchor=tk.CENTER)
        self.forecast_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def auto_detect_location(self):
        """Uses ipinfo.io API to automatically detect city based on user's IP."""
        try:
            res = requests.get("https://ipinfo.io/json", timeout=4).json()
            city = res.get("city", "")
            if city:
                self.city_entry.insert(0, city)
                self.fetch_weather()
        except Exception:
            self.show_error("Could not auto-detect location. Enter city manually.")

    def show_error(self, message: str):
        self.error_label.config(text=message)

    def clear_error(self):
        self.error_label.config(text="")

    def toggle_units(self):
        self.is_celsius = not self.is_celsius
        self.unit_btn.config(
            text="Switch to °C" if not self.is_celsius else "Switch to °F"
        )
        if self.current_city:
            self.fetch_weather()

    def fetch_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            self.show_error("Please enter a city name.")
            return

        self.clear_error()
        self.current_city = city
        units = "metric" if self.is_celsius else "imperial"
        unit_sym = "°C" if self.is_celsius else "°F"

        if API_KEY == "YOUR_OPENWEATHER_API_KEY":
            self.show_error(
                "API Key Missing! Set OPENWEATHER_API_KEY environment variable."
            )
            return

        # Fetch Current Weather Data
        curr_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
        try:
            response = requests.get(curr_url, timeout=5)
            data = response.json()

            if response.status_code == 404:
                self.show_error("City not found. Please check spelling.")
                return
            elif response.status_code != 200:
                self.show_error(
                    f"API Error: {data.get('message', 'Failed to fetch data.')}"
                )
                return

            # Parse Metrics
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            condition = data["weather"][0]["description"].title()
            icon_code = data["weather"][0]["icon"]

            # Update Labels
            self.temp_label.config(text=f"{temp:.1f} {unit_sym}")
            self.desc_label.config(text=f"Condition: {condition}")
            self.details_label.config(
                text=f"Humidity: {humidity}% | Wind: {wind_speed} {'m/s' if self.is_celsius else 'mph'}"
            )

            # Render Condition Icon
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_res = requests.get(icon_url, timeout=5)
            if icon_res.status_code == 200:
                img = Image.open(io.BytesIO(icon_res.content))
                photo = ImageTk.PhotoImage(img)
                self.icon_label.config(image=photo)
                self.icon_photo = photo

            # Fetch 5-Day Forecast Data
            self.fetch_forecast(city, units, unit_sym)

        except requests.RequestException:
            self.show_error("Network timeout or connection error.")

    def fetch_forecast(self, city: str, units: str, unit_sym: str):
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}"
        try:
            res = requests.get(forecast_url, timeout=5)
            data = res.json()

            if res.status_code == 200:
                # Clear previous table entries
                for item in self.forecast_tree.get_children():
                    self.forecast_tree.delete(item)

                # Read 3-hour interval entries (take 1 snapshot per day)
                list_entries = data.get("list", [])
                for entry in list_entries[::8]:
                    dt_txt = entry["dt_txt"]
                    cond = entry["weather"][0]["description"].title()
                    f_temp = entry["main"]["temp"]
                    self.forecast_tree.insert(
                        "",
                        tk.END,
                        values=(dt_txt, cond, f"{f_temp:.1f} {unit_sym}"),
                    )

        except Exception:
            self.show_error("Failed to load forecast trends.")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
# Real-Time Weather Application (OIBSIP Task 4 - Python Track)

A graphical weather application built for the **Oasis Infobyte Internship Program (OIBSIP)** that fetches real-time meteorological metrics and 5-day weather forecasts using the OpenWeatherMap REST API.

---

## 📌 Features Checklist

### Beginner Tier Features
- [x] **Location Query:** Prompts users for a city name or location.
- [x] **API Parsing:** Calls OpenWeatherMap API and extracts structured JSON responses.
- [x] **Core Metrics:** Displays real-time temperature, humidity percentage, weather condition description, and wind velocity.
- [x] **Error Handling:** Catches API authorization errors, missing location entries, and connection timeouts gracefully.
- [x] **Input Validation:** Prevents blank string input requests.

### Advanced Tier Features
- [x] **Graphical User Interface (GUI):** Built with `tkinter`, including search controls, detailed summary widgets, and treeview tables.
- [x] **Dynamic Weather Icons:** Downloads and renders condition-specific icons using `Pillow` (PIL) directly from OpenWeatherMap icon servers.
- [x] **5-Day Extended Forecast:** Parses multi-day forecast trends and presents them in a structured table layout.
- [x] **Celsius / Fahrenheit Toggle:** Allows seamless temperature scale switching between metric (°C) and imperial (°F) units.
- [x] **IP-Based Auto Location:** Automatically detects and populates the user's current city on startup via `ipinfo.io`.
- [x] **Inline Error Display:** Displays user feedback and network error alerts within GUI labels rather than terminal print statements.

---

## 🛠️ Tech Stack & Dependencies

| Category | Technology / Library |
| :--- | :--- |
| **Language** | Python 3.8+ |
| **GUI Framework** | `tkinter` |
| **HTTP Requests** | `requests` |
| **Image Handling** | `PIL` (`Pillow`) |
| **External APIs** | OpenWeatherMap API, ipinfo.io API |

---

## 📁 Repository Folder Structure

```text
OIBSIP/
├── Python-Task1-VoiceAssistant/
│   ├── voice_assistant_advanced.py
│   ├── commands.json
│   └── README.md
├── Python-Task2-BMICalculator/
│   ├── bmi_calculator.py
│   ├── bmi_history.db
│   └── README.md
├── Python-Task3-PasswordGenerator/
│   ├── password_generator.py
│   └── README.md
└── Python-Task4-WeatherApp/
    ├── weather_app.py
    └── README.md

⚙️ Installation & Setup
1. Clone Repository & Navigate
Bash
git clone [https://github.com/SANIA613/OIBSIP.git](https://github.com/SANIA613/OIBSIP.git)
cd OIBSIP/Python-Task4-WeatherApp/
2. Install Required Python Packages
Bash
pip install requests pillow
3. Set OpenWeatherMap API Key
Before launching, set your free API key in your terminal session:

Windows (CMD / PowerShell):

DOS
set OPENWEATHER_API_KEY=your_actual_api_key
Linux / macOS:

Bash
export OPENWEATHER_API_KEY="your_actual_api_key"
🚀 How to Run
Bash
python weather_app.py
🎥 Submission & Demonstration
GitHub Repository Name: OIBSIP

Folder Path: OIBSIP/Python-Task4-WeatherApp/

Demo Title Card: Starts with a 2-second static overlay displaying Full Name (Saniya Tamboli), Track Name (Python Programming), and Task Title (Task 4 - Basic Weather App).

Hashtags: #oasisinfobyte #python #datascience #internship

👤 Author
Name: Saniya Tamboli

GitHub: SANIA613

Track: Python Programming

Cohort / Internship Program: Oasis Infobyte Internship (OIBSIP)
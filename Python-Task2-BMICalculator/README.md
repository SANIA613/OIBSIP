# BMI Calculator & Historical Tracker (OIBSIP Task 2 - Python Track)

A comprehensive, production-grade graphical Body Mass Index (BMI) calculator and multi-user tracking application developed as part of the **Oasis Infobyte Internship Program (OIBSIP)**.

---

## 📌 Project Overview
This project fulfills **Task 2 (Advanced Tier)** of the Python Programming Track. The application features a Graphical User Interface (GUI) built with `tkinter`, multi-user data persistence using an SQLite database (`sqlite3`), and historical progress visualization via `matplotlib`.

---

## ✨ Features Checklist

### Beginner Tier Features
- [x] **User Inputs:** Prompts user for weight (kg) and height (m or cm) via intuitive GUI input fields.
- [x] **BMI Calculation:** Computes accurate Body Mass Index using $BMI = \frac{\text{weight}}{\text{height}^2}$.
- [x] **Standard Classifications:** Automatically categorizes results:
  - 🔵 **Underweight:** $< 18.5$
  - 🟢 **Normal Weight:** $18.5 - 24.9$
  - 🟠 **Overweight:** $25.0 - 29.9$
  - 🔴 **Obese:** $\ge 30.0$
- [x] **Formatted Results:** Displays calculated BMI rounded to 2 decimal places alongside health category.
- [x] **Input Validation:** Rejects non-numeric input, blank entries, and negative numbers with helpful user alerts.

### Advanced Tier Features
- [x] **Graphical User Interface (GUI):** Clean interface built using `tkinter` with structured entry fields, action buttons, and table views.
- [x] **Smart Unit Conversion:** Accepts height in either meters ($m$) or centimeters ($cm$), automatically converting values $> 3.0$ into meters to prevent calculation errors.
- [x] **Color-Coded Feedback:** Displays health outcomes with distinct visual colors (Green for Normal, Blue for Underweight, Orange for Overweight, Red for Obese).
- [x] **Multi-User Support:** Enables tracking and saving records for multiple distinct usernames.
- [x] **Database Persistence:** Stores user records (Name, Weight, Height, BMI, Category, Date) securely in a local SQLite database (`bmi_history.db`).
- [x] **Trend Visualisation:** Renders interactive line graphs using `matplotlib` showing a selected user's historical BMI trends over time with baseline category markers.
- [x] **Error Handling:** Safe database transaction handling with graceful exception alerts on failure.

---

## 🛠️ Tech Stack & Dependencies

| Category | Technology / Library |
| :--- | :--- |
| **Language** | Python 3.8+ |
| **GUI Framework** | `tkinter` |
| **Database Engine** | `sqlite3` |
| **Data Visualization** | `matplotlib` |
| **Date & Time Handling** | `datetime` |

---

## 📁 Repository Folder Structure

```text
OIBSIP/
├── Python-Task1-VoiceAssistant/
│   ├── voice_assistant_advanced.py
│   ├── commands.json
│   └── README.md
└── Python-Task2-BMICalculator/
    ├── bmi_calculator.py
    ├── bmi_history.db
    └── README.md

⚙️ Installation & Setup
1. Clone Repository & Navigate
Bash
git clone [https://github.com/SANIA613/OIBSIP.git](https://github.com/SANIA613/OIBSIP.git)
cd OIBSIP/Python-Task2-BMICalculator/
2. Install Required Python Packages
Bash
pip install matplotlib
🚀 How to Run
Execute the main application script:

Bash
python bmi_calculator.py
🎥 Submission & Demonstration
GitHub Repository Name: OIBSIP

Folder Path: OIBSIP/Python-Task2-BMICalculator/

Demo Title Card: Starts with a 2-second static overlay displaying Full Name (Saniya Tamboli), Track Name (Python Programming), and Task Title (Task 2 - BMI Calculator).

Hashtags: #oasisinfobyte #python #datascience #internship


👤 Author
GitHub Username: SANIA613

Track: Python Programming

Program: Oasis Infobyte Virtual Internship Program (OIBSIP)

Repository Link: https://github.com/SANIA613/OIBSIP
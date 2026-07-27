# BMI Calculator & Historical Tracker (OIBSIP Task 2 - Python Track)

A feature-rich, graphical Body Mass Index (BMI) calculator and multi-user tracking application developed for the **Oasis Infobyte Internship Program (OIBSIP)**.

---

## 📌 Project Overview
This project fulfills **Task 2 (Advanced Tier)** of the Python Programming Track. The application features a Graphical User Interface (GUI) built with `tkinter`, data persistence using an SQLite database (`sqlite3`), and historical progress visualization via `matplotlib`.

---

## ✨ Features Checklist

- [x] **Graphical User Interface:** Modern GUI built using `tkinter` with labeled input fields, buttons, and structured table layouts.
- [x] **Smart Unit Processing:** Accepts height in either meters ($m$) or centimeters ($cm$), automatically converting values $> 3.0$ into meters to avoid calculation errors.
- [x] **Input Validation:** Rejects negative numbers, blank fields, and non-numeric characters with user-friendly popup error alerts.
- [x] **Category Classification & Color Coding:**
  - 🔵 **Underweight:** $< 18.5$
  - 🟢 **Normal Weight:** $18.5 - 24.9$
  - 🟠 **Overweight:** $25.0 - 29.9$
  - 🔴 **Obese:** $\ge 30.0$
- [x] **Multi-User Data Persistence:** Saves individual user records (Name, Weight, Height, BMI, Category, Timestamp) to a local SQLite database (`bmi_history.db`).
- [x] **Historical Trend Chart:** Renders an interactive line graph using `matplotlib` showing a selected user's BMI changes over time.

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

👤 Author
GitHub Username: SANIA613

Track: Python Programming

Program: Oasis Infobyte Virtual Internship Program (OIBSIP)

Repository Link: https://github.com/SANIA613/OIBSIP
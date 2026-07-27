# Cryptographically Secure Password Generator (OIBSIP Task 3 - Python Track)

A graphical, cryptographically secure password generation tool developed for the **Oasis Infobyte Internship Program (OIBSIP)**.

---

## 📌 Project Overview
This project fulfills **Task 3 (Advanced Tier)** of the Python Programming Track. Built using `tkinter`, it leverages Python's standard `secrets` module (rather than `random`) to produce passwords suitable for security-critical contexts.

---

## ✨ Features Checklist

### Beginner Tier Features
- [x] **Enforced Minimum Length:** Validates user-selected length with a minimum threshold of 8 characters.
- [x] **Character Diversity Rules:** Supports uppercase letters, lowercase letters, numbers, and symbols (requiring at least 2 types to be active).
- [x] **Criteria Validation:** Rejects invalid lengths or inadequate character pool choices with informative error popups.
- [x] **Repeated Generation:** Generates new passwords dynamically on demand without restarting the app.

### Advanced Tier Features
- [x] **Graphical User Interface (GUI):** Built with `tkinter`, incorporating interactive sliders, spinboxes, checkboxes, and listbox widgets.
- [x] **Cryptographically Secure PRNG:** Replaces standard pseudo-random generators with Python's built-in `secrets` module.
- [x] **Guaranteed Inclusion Rule:** Ensures at least one character from every active pool is included in the output.
- [x] **Dynamic Strength Indicator:** Evaluates and displays visual feedback (Weak / Fair / Medium / Strong) using color-coded progress bars.
- [x] **Clipboard Integration:** Automatically copies new passwords to the system clipboard upon generation via `pyperclip`.
- [x] **Ambiguous Character Filter:** Provides a checkbox option to exclude easily confused characters (`0`, `O`, `l`, `1`, `I`).
- [x] **In-Memory History:** Displays the last 5 passwords generated during the active session (not saved to disk for privacy/security).

---

## 🛠️ Tech Stack & Dependencies

| Category | Technology / Library |
| :--- | :--- |
| **Language** | Python 3.8+ |
| **GUI Framework** | `tkinter` |
| **CSPRNG Source** | `secrets` (Standard Library) |
| **Clipboard Tool** | `pyperclip` |

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
└── Python-Task3-PasswordGenerator/
    ├── password_generator.py
    └── README.md

⚙️ Installation & Setup
1. Clone Repository & Navigate
Bash
git clone [https://github.com/SANIA613/OIBSIP.git](https://github.com/SANIA613/OIBSIP.git)
cd OIBSIP/Python-Task3-PasswordGenerator/
2. Install Required Python Packages
Bash
pip install pyperclip
🚀 How to Run
Execute the main application script:

Bash
python password_generator.py
🎥 Submission & Demonstration
GitHub Repository Name: OIBSIP

Folder Path: OIBSIP/Python-Task3-PasswordGenerator/

Demo Title Card: Begins with a 2-second static overlay displaying Full Name (Saniya Tamboli), Track Name (Python Programming), and Task Title (Task 3 - Random Password Generator).

Hashtags: #oasisinfobyte #python #datascience #internship

👤 Author
Name: Saniya Tamboli

GitHub: SANIA613

Track: Python Programming

Cohort / Internship Program: Oasis Infobyte Internship (OIBSIP)
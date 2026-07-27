# Real-Time Multi-Room Chat Application (OIBSIP Task 5 - Python Track)

A graphical, socket-based multi-room chat application developed for the **Oasis Infobyte Internship Program (OIBSIP)**.

---

## 📌 Project Overview
This project fulfills **Task 5 (Advanced Tier)** of the Python Programming Track. The system architecture follows a Client-Server socket model using multi-threading, SQLite user authentication, room message history persistence, and custom emoji shortcode rendering.

---

## ✨ Features Checklist

### Beginner Tier Features
- [x] **Client-Server Architecture:** Multi-threaded socket server listening on `127.0.0.1:5555`.
- [x] **Bidirectional Communication:** Real-time message distribution across connected sockets.
- [x] **Timestamp Prefixing:** Formats all messages with time identifiers (e.g., `[14:35] Alice: Hello`).
- [x] **Disconnection Notifications:** Notifies remaining room participants when a client disconnects.
- [x] **Localhost Testing:** Fully runnable on local machines using loopback adapters (`localhost`).

### Advanced Tier Features
- [x] **Graphical User Interface (GUI):** Built using `tkinter`, supporting authentication views and active chat windows.
- [x] **SQLite Authentication:** Secure registration and login using SHA-256 password hashing stored in `chat_app.db`.
- [x] **Multi-Room Support:** Allows users to switch between rooms (`General`, `Tech`, `Random`, `Oasis-Interns`).
- [x] **Message History Persistence:** Loads up to 50 previous room messages from SQLite upon joining.
- [x] **In-App/Focus Alerts:** Dynamically updates window title bar notifications when messages arrive while unfocused.
- [x] **Emoji Shortcodes:** Automatically parses shortcodes (`:smile:`, `:heart:`, `:thumbsup:`, `:fire:`) into Unicode characters.
- [x] **Security Transparency Disclosures:** Documented below.

---

## 🔒 Security & Message Storage Disclosures

1. **Message Storage:** Message text, timestamps, sender names, and room names are stored as plain text inside the local SQLite database (`chat_app.db`) to allow historical room reloads.
2. **Encryption:** Socket traffic transmitted between `chat_client.py` and `chat_server.py` is currently **unencrypted** (raw TCP sockets without TLS wrapper).
3. **Password Security:** User passwords are encrypted using `SHA-256` hashing prior to storing in the SQLite database.

---

## 🛠️ Tech Stack & Dependencies

| Category | Technology / Library |
| :--- | :--- |
| **Language** | Python 3.8+ |
| **Networking** | `socket`, `threading`, `json` |
| **GUI Framework** | `tkinter`, `ttk` |
| **Database & Security** | `sqlite3`, `hashlib` |

---

## 📁 Repository Folder Structure

```text
OIBSIP/
├── Python-Task1-VoiceAssistant/
├── Python-Task2-BMICalculator/
├── Python-Task3-PasswordGenerator/
├── Python-Task4-WeatherApp/
└── Python-Task5-ChatApplication/
    ├── chat_server.py
    ├── chat_client.py
    ├── chat_app.db
    └── README.md

🚀 How to Run
1. Launch Server First
In your first terminal window, start the socket server:

Bash
python chat_server.py
2. Launch Client Instance(s)
In a second terminal window (or third window for multi-user testing), start client GUIs:

Bash
python chat_client.py
🎥 Submission & Demonstration
GitHub Repository Name: OIBSIP

Folder Path: OIBSIP/Python-Task5-ChatApplication/

Demo Title Card: Starts with a 2-second static overlay displaying Full Name (Saniya Tamboli), Track Name (Python Programming), and Task Title (Task 5 - Chat Application).

Hashtags: #oasisinfobyte #python #datascience #internship

👤 Author
Name: Saniya Tamboli

GitHub: SANIA613

Track: Python Programming

Cohort / Internship Program: Oasis Infobyte Internship (OIBSIP)
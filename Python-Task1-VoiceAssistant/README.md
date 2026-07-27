# Advanced Voice Assistant (OIBSIP Task 1 - Python Track)

A comprehensive, production-grade, NLP-powered Python voice assistant developed as part of the **Oasis Infobyte Internship Program (OIBSIP)**.

---

## 📌 Project Overview
This project fulfills **Task 1 (Advanced Tier)** of the Python Programming Track. The assistant captures user voice commands via microphone, performs Intent Parsing using Natural Language Processing (NLP), executes tasks asynchronously (weather lookup, automated emails, background reminders, QA queries, dynamic command execution), and responds with synthesized speech.

---

## ✨ Features Checklist

### Beginner Tier Features
- [x] **Voice Recognition:** Captures spoken input using `speech_recognition` and Google Speech API.
- [x] **Predefined Greeting:** Responds dynamically to spoken greetings.
- [x] **Time & Date Announcement:** Tells current local time and full calendar date on request.
- [x] **Web Search:** Opens default web browser with search query specified by user.
- [x] **Error Handling:** Gracefully handles background noise, silence, or unrecognized commands with voice prompts.
- [x] **Text-To-Speech (TTS):** Converts all responses to clear audio using `pyttsx3`.

### Advanced Tier Features
- [x] **Natural Language Understanding (NLU):** Extracts user intent from free-form spoken sentences using `spaCy` token lemmatization rather than strict string matching.
- [x] **Live Weather Updates:** Connects to OpenWeatherMap REST API to report real-time conditions and temperatures.
- [x] **Voice-Triggered Email:** Sends automated emails via `smtplib` over secure SSL/TLS sockets.
- [x] **Multi-threaded Reminders:** Spawns asynchronous background threads for timed alerts without blocking speech interaction.
- [x] **General Knowledge QA:** Queries DuckDuckGo Instant Answer API for factual questions with web fallback.
- [x] **Custom Command Engine:** Extensible via external JSON configuration (`commands.json`).
- [x] **Privacy Safeguards:** Documented data handling standards and zero local persistent audio storing.

---

## 🛠️ Tech Stack & Dependencies

| Category | Technology / Library |
| :--- | :--- |
| **Language** | Python 3.8+ |
| **Speech Recognition** | `speech_recognition`, `PyAudio` |
| **Text-To-Speech** | `pyttsx3` |
| **NLP Engine** | `spaCy` (`en_core_web_sm`) |
| **Networking & APIs** | `requests`, `smtplib`, OpenWeatherMap API, DuckDuckGo API |
| **Configuration** | `json`, `os`, `re`, `threading` |

---

## 📁 Repository Folder Structure

```text
OIBSIP/
└── Python-Task1-VoiceAssistant/
    ├── voice_assistant_advanced.py
    ├── commands.json
    └── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository & Navigate
```bash
git clone https://github.com/YOUR_USERNAME/OIBSIP.git
cd OIBSIP/Python-Task1-VoiceAssistant/
```

### 2. Install Required Python Packages
```bash
pip install SpeechRecognition pyttsx3 PyAudio requests spacy
```

> **Windows Users Note:** If installing `PyAudio` fails, execute:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### 3. Download spaCy English Language Model
```bash
python -m spacy download en_core_web_sm
```

### 4. Configure Environment Variables (Optional for Weather & Email)
Set the required API key and credentials in your terminal session:

* **Linux / macOS:**
  ```bash
  export OPENWEATHER_API_KEY="your_openweather_api_key"
  export SENDER_EMAIL="your_test_email@gmail.com"
  export SENDER_PASSWORD="your_app_password"
  ```
* **Windows (CMD):**
  ```cmd
  set OPENWEATHER_API_KEY="your_openweather_api_key"
  set SENDER_EMAIL="your_test_email@gmail.com"
  set SENDER_PASSWORD="your_app_password"
  ```

---

## 🚀 How to Run
```bash
python voice_assistant_advanced.py
```

---

## ⚙️ Custom Commands (`commands.json`)
You can add custom web links or short outputs to `commands.json` without modifying the Python source code:

```json
{
  "github": "https://github.com",
  "linkedin": "https://linkedin.com",
  "python docs": "https://docs.python.org/3/"
}
```

---

## 🔒 Privacy & Data Processing Disclosures

1. **Audio Data Processing:** Microphone audio captured by the application is streamed over HTTPS to Google Speech-to-Text API for transcription. Raw audio recordings are processed in-memory and are **never recorded or stored** on local disk storage.
2. **Local Processing:** Intent classification via `spaCy` operates entirely offline in memory on host system CPU.
3. **Credential Management:** Email passwords and API tokens are read from transient system environment variables (`os.getenv`) rather than hardcoded in source files.

---

## 🎥 Submission & Demonstration

- **GitHub Repository Name:** `OIBSIP`
- **Folder Path:** `OIBSIP/Python-Task1-VoiceAssistant/`
- **Demo Title Card:** Starts with a 2-second static overlay displaying Full Name, Track Name (*Python Programming*), and Task Title (*Task 1 - Voice Assistant*).
- **Hashtags:** `#oasisinfobyte` `#python` `#datascience` `#internship`

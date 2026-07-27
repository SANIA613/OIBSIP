"""
Project: Advanced Voice Assistant (OIBSIP Task 1)
Author: Saniya Tamboli
Track: Python Programming
Organization: Oasis Infobyte
"""
import datetime
import json
import os
import re
import smtplib
import sys
import threading
import time
import webbrowser
from email.mime.text import MIMEText

import pyttsx3
import requests
import speech_recognition as sr
import spacy

# ---------------------------------------------------------------------------
# CONFIGURATION & INITIALIZATION
# ---------------------------------------------------------------------------
# Replace these with your actual credentials/keys for testing
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_OPENWEATHER_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your_test_email@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your_app_password")

# Initialize TTS Engine
engine = pyttsx3.init()
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)

# Initialize NLP Pipeline
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None
    print("[Warning] spaCy model 'en_core_web_sm' not found. Falling back to keyword intent matching.")


def speak(text: str) -> None:
    """Converts text to speech and prints to stdout."""
    print(f"\n[Assistant]: {text}")
    engine.say(text)
    engine.runAndWait()


def listen() -> str:
    """Captures audio input via microphone and transcribes it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=10)
            print("[Recognizing...]")
            command = recognizer.recognize_google(audio, language="en-US")  # type: ignore[attr-defined]
            print(f"[You]: {command}")
            return command.strip()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            speak("I couldn't quite understand that. Could you please repeat?")
            return ""
        except sr.RequestError:
            speak("Speech recognition service is currently unavailable. Check your internet connection.")
            return ""


# ---------------------------------------------------------------------------
# ADVANCED FEATURES & API INTEGRATIONS
# ---------------------------------------------------------------------------
def parse_intent_nlp(text: str) -> str:
    """Parses free-form spoken input to deduce intent using NLP entity/lemma analysis."""
    if not text:
        return "unknown"

    doc = nlp(text.lower()) if nlp else None
    lemmas = [token.lemma_ for token in doc] if doc else text.lower().split()

    if any(w in lemmas for w in ["hello", "hi", "hey", "greet"]):
        return "greeting"
    elif any(w in lemmas for w in ["time", "date", "day", "clock"]):
        return "time_date"
    elif "weather" in lemmas or "temperature" in lemmas:
        return "weather"
    elif "email" in lemmas or "mail" in lemmas or "send" in lemmas:
        return "email"
    elif "reminder" in lemmas or "timer" in lemmas or "remind" in lemmas:
        return "reminder"
    elif "search" in lemmas or "google" in lemmas or "lookup" in lemmas:
        return "search"
    elif any(w in lemmas for w in ["who", "what", "where", "explain", "define"]):
        return "qa_query"
    elif any(w in lemmas for w in ["exit", "stop", "quit", "bye"]):
        return "exit"

    return "general"


def get_weather(city: str) -> None:
    """Fetches live weather updates using OpenWeatherMap API."""
    if OPENWEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY":
        speak("Weather API key is missing. Please configure your OpenWeatherMap API key.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            speak(f"The current weather in {city} is {desc} with a temperature of {temp} degrees Celsius.")
        else:
            speak(f"I couldn't find weather details for {city}.")
    except requests.RequestException:
        speak("Failed to connect to the weather service.")


def send_email(recipient: str, subject: str, body: str) -> None:
    """Sends an email via SMTP using secure connection settings."""
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
        speak("Email sent successfully!")
    except Exception as e:
        speak(f"Failed to send email. Error: {str(e)}")


def set_reminder_thread(delay_seconds: int, message: str) -> None:
    """Background thread worker for handling non-blocking timed reminders."""
    time.sleep(delay_seconds)
    speak(f"REMINDER ALERT: {message}")


def create_reminder(command: str) -> None:
    """Extracts duration and reminder message, then spawns an alert thread."""
    numbers = re.findall(r"\d+", command)
    if not numbers:
        speak("Please specify a duration in seconds for the reminder.")
        return

    seconds = int(numbers[0])
    speak(f"Reminder set for {seconds} seconds from now.")
    thread = threading.Thread(
        target=set_reminder_thread, args=(seconds, "Time is up for your scheduled task!")
    )
    thread.daemon = True
    thread.start()


def answer_general_knowledge(query: str) -> None:
    """Queries DuckDuckGo Instant Answer API for general knowledge questions."""
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1"
    try:
        res = requests.get(url, timeout=5).json()
        abstract = res.get("AbstractText", "")
        if abstract:
            speak(abstract)
        else:
            speak(f"Searching the web for {query}.")
            webbrowser.open(f"https://www.google.com/search?q={query}")
    except Exception:
        speak("I ran into an issue retrieving an answer. Opening web browser instead.")
        webbrowser.open(f"https://www.google.com/search?q={query}")


def check_custom_commands(command: str) -> bool:
    """Loads external JSON custom commands configuration."""
    if not os.path.exists("commands.json"):
        return False

    with open("commands.json", "r") as f:
        custom_cmds = json.load(f)

    for alias, action in custom_cmds.items():
        if alias.lower() in command.lower():
            speak(f"Executing custom command for {alias}.")
            if action.startswith("http://") or action.startswith("https://"):
                webbrowser.open(action)
            else:
                speak(f"Custom action output: {action}")
            return True
    return False


# ---------------------------------------------------------------------------
# MAIN ASSISTANT ENGINE
# ---------------------------------------------------------------------------
def run_assistant() -> None:
    speak("Advanced Voice Assistant initialized and operational. How can I serve you?")

    while True:
        raw_command = listen()
        if not raw_command:
            continue

        # Check user-configured dynamic commands first
        if check_custom_commands(raw_command):
            continue

        # Parse Intent using NLP
        intent = parse_intent_nlp(raw_command)

        if intent == "greeting":
            speak("Greetings! How can I assist you with your tasks today?")

        elif intent == "time_date":
            now = datetime.datetime.now()
            speak(f"Current time is {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}.")

        elif intent == "weather":
            speak("Which city would you like the weather update for?")
            city = listen()
            if city:
                get_weather(city)

        elif intent == "email":
            speak("Please specify the recipient email address.")
            recipient = input("Enter Recipient Email manually for accuracy: ").strip()
            speak("What is the subject of the email?")
            subject = listen()
            speak("Please dictate the email body.")
            body = listen()

            if recipient and body:
                send_email(recipient, subject, body)

        elif intent == "reminder":
            create_reminder(raw_command)

        elif intent == "search":
            query = raw_command.replace("search", "").replace("google", "").strip()
            if query:
                speak(f"Searching Google for {query}.")
                webbrowser.open(f"https://www.google.com/search?q={query}")

        elif intent == "qa_query":
            answer_general_knowledge(raw_command)

        elif intent == "exit":
            speak("Shutting down assistant sessions. Have a productive day!")
            sys.exit()

        else:
            answer_general_knowledge(raw_command)


if __name__ == "__main__":
    run_assistant()
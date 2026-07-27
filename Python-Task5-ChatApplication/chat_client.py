"""
Project: Multi-Room GUI Chat Application - Client (OIBSIP Task 5)
Author: Saniya Tamboli
Track: Python Programming
Organization: Oasis Infobyte
"""

import datetime
import json
import socket
import threading
import tkinter as tk
from tkinter import messagebox, ttk

HOST = "127.0.0.1"
PORT = 5555

# Emoji shortcode mapping dictionary
EMOJI_MAP = {
    ":smile:": "😄",
    ":happy:": "😊",
    ":heart:": "❤️",
    ":thumbsup:": "👍",
    ":fire:": "🔥",
    ":laugh:": "😂",
    ":wink:": "😉",
    ":sad:": "😢",
}


class ChatClientGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Multi-Room Chat - Saniya Tamboli")
        self.root.geometry("620x680")

        self.socket = None
        self.username = None
        self.current_room = "General"
        self.is_window_focused = True

        self.root.bind("<FocusIn>", self.on_focus_in)
        self.root.bind("<FocusOut>", self.on_focus_out)

        self.setup_auth_ui()

    def parse_emojis(self, text):
        """Replaces common shortcodes with Unicode emoji equivalents."""
        for shortcode, emoji in EMOJI_MAP.items():
            text = text.replace(shortcode, emoji)
        return text

    def on_focus_in(self, event):
        self.is_window_focused = True

    def on_focus_out(self, event):
        self.is_window_focused = False

    def setup_auth_ui(self):
        """Renders Login / Register Screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        header = tk.Label(
            self.root,
            text="💬 Welcome to Real-Time Chat",
            font=("Helvetica", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=12,
        )
        header.pack(fill=tk.X)

        auth_frame = tk.LabelFrame(
            self.root,
            text=" User Authentication ",
            font=("Helvetica", 11, "bold"),
            padx=20,
            pady=20,
        )
        auth_frame.pack(padx=40, pady=40, fill=tk.BOTH, expand=True)

        tk.Label(auth_frame, text="Username:", font=("Helvetica", 10)).pack(
            anchor=tk.W, pady=2
        )
        self.user_entry = tk.Entry(auth_frame, font=("Helvetica", 11))
        self.user_entry.pack(fill=tk.X, pady=5)

        tk.Label(auth_frame, text="Password:", font=("Helvetica", 10)).pack(
            anchor=tk.W, pady=2
        )
        self.pwd_entry = tk.Entry(
            auth_frame, font=("Helvetica", 11), show="*"
        )
        self.pwd_entry.pack(fill=tk.X, pady=5)

        btn_frame = tk.Frame(auth_frame, pady=15)
        btn_frame.pack()

        login_btn = tk.Button(
            btn_frame,
            text="Log In",
            command=lambda: self.authenticate("login"),
            bg="#27ae60",
            fg="white",
            font=("Helvetica", 10, "bold"),
            width=12,
        )
        login_btn.grid(row=0, column=0, padx=10)

        reg_btn = tk.Button(
            btn_frame,
            text="Register",
            command=lambda: self.authenticate("register"),
            bg="#2980b9",
            fg="white",
            font=("Helvetica", 10, "bold"),
            width=12,
        )
        reg_btn.grid(row=0, column=1, padx=10)

    def connect_socket(self):
        if not self.socket:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((HOST, PORT))
            except Exception as e:
                messagebox.showerror(
                    "Connection Error", f"Cannot connect to server: {e}"
                )
                self.socket = None
                return False
        return True

    def authenticate(self, action):
        user = self.user_entry.get().strip()
        pwd = self.pwd_entry.get().strip()

        if not user or not pwd:
            messagebox.showwarning(
                "Validation Error", "Username and password required."
            )
            return

        if not self.connect_socket():
            return

        payload = {"type": action, "username": user, "password": pwd}

        if not self.socket:
            messagebox.showerror("Connection Error", "Socket is not connected.")
            return

        # Wait for auth response
        try:
            self.socket.sendall(json.dumps(payload).encode("utf-8"))
            raw = self.socket.recv(4096)
            res = json.loads(raw.decode("utf-8"))

            if res.get("success"):
                if action == "login":
                    self.username = user
                    self.setup_chat_ui()
                    threading.Thread(
                        target=self.receive_messages, daemon=True
                    ).start()
                    self.join_room("General")
                else:
                    messagebox.showinfo("Success", res.get("message"))
            else:
                messagebox.showerror("Auth Failed", res.get("message"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to communicate: {e}")

    def setup_chat_ui(self):
        """Renders Main Chat Interface."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Top Bar
        top_frame = tk.Frame(self.root, bg="#2c3e50", pady=8, padx=10)
        top_frame.pack(fill=tk.X)

        tk.Label(
            top_frame,
            text=f"User: {self.username}",
            font=("Helvetica", 11, "bold"),
            bg="#2c3e50",
            fg="white",
        ).pack(side=tk.LEFT)

        tk.Label(
            top_frame,
            text="Room:",
            font=("Helvetica", 10),
            bg="#2c3e50",
            fg="white",
        ).pack(side=tk.LEFT, padx=(20, 5))

        self.room_combobox = ttk.Combobox(
            top_frame,
            values=["General", "Tech", "Random", "Oasis-Interns"],
            state="readonly",
            width=14,
        )
        self.room_combobox.set("General")
        self.room_combobox.pack(side=tk.LEFT)
        self.room_combobox.bind(
            "<<ComboboxSelected>>",
            lambda e: self.join_room(self.room_combobox.get()),
        )

        # Message History Display Textbox
        self.chat_display = tk.Text(
            self.root,
            font=("Helvetica", 10),
            state=tk.DISABLED,
            wrap=tk.WORD,
            bg="#f8f9fa",
        )
        self.chat_display.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=(10, 5)
        )

        # Bottom Input Bar
        bottom_frame = tk.Frame(self.root, pady=10, padx=10)
        bottom_frame.pack(fill=tk.X)

        self.msg_entry = tk.Entry(bottom_frame, font=("Helvetica", 11))
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.msg_entry.bind("<Return>", lambda e: self.send_message())

        send_btn = tk.Button(
            bottom_frame,
            text="Send",
            command=self.send_message,
            bg="#27ae60",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=15,
        )
        send_btn.pack(side=tk.RIGHT)

        # Helper hint for emojis
        tk.Label(
            self.root,
            text="Emoji Shortcodes supported: :smile: :heart: :thumbsup: :fire: :happy:",
            font=("Helvetica", 8, "italic"),
            fg="#7f8c8d",
        ).pack(pady=(0, 5))

    def _send_payload(self, payload):
        if not self.socket:
            if not self.connect_socket():
                return False

        if not self.socket:
            messagebox.showerror("Connection Error", "Socket is not connected.")
            return False

        try:
            self.socket.sendall(json.dumps(payload).encode("utf-8"))
            return True
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to send data: {e}")
            self.socket = None
            return False

    def join_room(self, room_name):
        self.current_room = room_name
        payload = {"type": "join_room", "room": room_name}
        self._send_payload(payload)

    def display_text(self, formatted_text, color="#000000"):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, formatted_text + "\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def send_message(self):
        raw_msg = self.msg_entry.get().strip()
        if not raw_msg:
            return

        msg_with_emojis = self.parse_emojis(raw_msg)
        timestamp = datetime.datetime.now().strftime("%H:%M")

        payload = {
            "type": "chat_message",
            "message": msg_with_emojis,
            "timestamp": timestamp,
        }
        if self._send_payload(payload):
            self.msg_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                sock = self.socket
                if not sock:
                    break

                raw = sock.recv(4096)
                if not raw:
                    break

                data = json.loads(raw.decode("utf-8"))
                msg_type = data.get("type")

                if msg_type == "room_history":
                    self.chat_display.config(state=tk.NORMAL)
                    self.chat_display.delete("1.0", tk.END)
                    self.chat_display.config(state=tk.DISABLED)

                    self.display_text(
                        f"--- Joined Room: {data.get('room')} ---", "#7f8c8d"
                    )

                    for item in data.get("history", []):
                        txt = f"[{item['timestamp']}] {item['sender']}: {item['message']}"
                        self.display_text(txt)

                elif msg_type == "chat_message":
                    formatted = f"[{data['timestamp']}] {data['sender']}: {data['message']}"
                    self.display_text(formatted)

                    # Trigger alert if window is not focused
                    if not self.is_window_focused:
                        self.root.title("🔔 New Message! - Chat App")

                elif msg_type == "system":
                    self.display_text(f"*** {data['message']} ***")

            except Exception:
                break


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()
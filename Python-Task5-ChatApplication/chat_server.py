"""
Project: Multi-Room GUI Chat Application - Server (OIBSIP Task 5)
Author: Saniya Tamboli
Track: Python Programming
Organization: Oasis Infobyte
"""

import hashlib
import json
import socket
import sqlite3
import threading

HOST = "127.0.0.1"
PORT = 5555


class ChatServer:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

        # Stores connected clients: {client_socket: {"username": str, "room": str}}
        self.clients = {}

        self.init_db()

    def init_db(self):
        """Initializes SQLite database for authentication and message history."""
        conn = sqlite3.connect("chat_app.db")
        cursor = conn.cursor()

        # Users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
        """
        )

        # Messages history table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room TEXT NOT NULL,
                sender TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """
        )

        conn.commit()
        conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def handle_auth(self, action, username, password):
        conn = sqlite3.connect("chat_app.db")
        cursor = conn.cursor()
        pwd_hash = self.hash_password(password)

        if action == "register":
            try:
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, pwd_hash),
                )
                conn.commit()
                conn.close()
                return True, "Registration successful. Please log in."
            except sqlite3.IntegrityError:
                conn.close()
                return False, "Username already exists."

        elif action == "login":
            cursor.execute(
                "SELECT password_hash FROM users WHERE username = ?",
                (username,),
            )
            row = cursor.fetchone()
            conn.close()

            if row and row[0] == pwd_hash:
                return True, "Login successful."
            return False, "Invalid username or password."

        conn.close()
        return False, "Invalid authentication action."

    def save_message(self, room, sender, message, timestamp):
        conn = sqlite3.connect("chat_app.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (room, sender, message, timestamp) VALUES (?, ?, ?, ?)",
            (room, sender, message, timestamp),
        )
        conn.commit()
        conn.close()

    def get_history(self, room):
        conn = sqlite3.connect("chat_app.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT sender, message, timestamp FROM messages WHERE room = ? ORDER BY id ASC LIMIT 50",
            (room,),
        )
        rows = cursor.fetchall()
        conn.close()

        return [
            {"sender": r[0], "message": r[1], "timestamp": r[2]} for r in rows
        ]

    def broadcast_to_room(
        self, room, payload, exclude_client=None, sys_msg=False
    ):
        data = json.dumps(payload).encode("utf-8")
        for client_sock, info in list(self.clients.items()):
            if info.get("room") == room and client_sock != exclude_client:
                try:
                    client_sock.sendall(data)
                except Exception:
                    self.remove_client(client_sock)

    def remove_client(self, client_sock):
        if client_sock in self.clients:
            info = self.clients[client_sock]
            username = info.get("username")
            room = info.get("room")

            del self.clients[client_sock]
            try:
                client_sock.close()
            except Exception:
                pass

            if room and username:
                sys_payload = {
                    "type": "system",
                    "message": f"{username} has left the chat.",
                }
                self.broadcast_to_room(room, sys_payload)

    def handle_client(self, client_sock):
        authenticated = False
        username = ""

        while True:
            try:
                raw_data = client_sock.recv(4096)
                if not raw_data:
                    break

                req = json.loads(raw_data.decode("utf-8"))
                msg_type = req.get("type")

                # Authentication Phase
                if msg_type in ["login", "register"]:
                    user = req.get("username", "").strip()
                    pwd = req.get("password", "").strip()

                    success, msg = self.handle_auth(msg_type, user, pwd)
                    resp = {
                        "type": "auth_response",
                        "success": success,
                        "message": msg,
                    }
                    client_sock.sendall(json.dumps(resp).encode("utf-8"))

                    if success and msg_type == "login":
                        authenticated = True
                        username = user
                        self.clients[client_sock] = {
                            "username": username,
                            "room": None,
                        }

                elif authenticated:
                    if msg_type == "join_room":
                        room = req.get("room", "General").strip()
                        old_room = self.clients[client_sock].get("room")

                        # Leave previous room notify
                        if old_room:
                            self.broadcast_to_room(
                                old_room,
                                {
                                    "type": "system",
                                    "message": f"{username} left the room.",
                                },
                            )

                        self.clients[client_sock]["room"] = room

                        # Fetch history and send to user
                        history = self.get_history(room)
                        client_sock.sendall(
                            json.dumps(
                                {
                                    "type": "room_history",
                                    "room": room,
                                    "history": history,
                                }
                            ).encode("utf-8")
                        )

                        # Notify room members
                        self.broadcast_to_room(
                            room,
                            {
                                "type": "system",
                                "message": f"{username} joined room '{room}'.",
                            },
                            exclude_client=client_sock,
                        )

                    elif msg_type == "chat_message":
                        room = self.clients[client_sock].get("room")
                        msg_text = req.get("message", "")
                        timestamp = req.get("timestamp", "")

                        if room and msg_text:
                            self.save_message(
                                room, username, msg_text, timestamp
                            )
                            broadcast_payload = {
                                "type": "chat_message",
                                "sender": username,
                                "message": msg_text,
                                "timestamp": timestamp,
                                "room": room,
                            }
                            self.broadcast_to_room(room, broadcast_payload)

            except Exception:
                break

        self.remove_client(client_sock)

    def start(self):
        self.server_socket.listen(10)
        print(f"[SERVER STARTED] Listening on {self.host}:{self.port}...")

        while True:
            client_sock, addr = self.server_socket.accept()
            thread = threading.Thread(
                target=self.handle_client, args=(client_sock,), daemon=True
            )
            thread.start()


if __name__ == "__main__":
    server = ChatServer(HOST, PORT)
    server.start()
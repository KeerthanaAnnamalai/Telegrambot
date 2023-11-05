import sqlite3
import time

def create_messages_table():
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def send_message(sender, message):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO messages (sender, message) VALUES (?, ?)', (sender, message))
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()

    cursor.execute('SELECT sender, message, timestamp FROM messages ORDER BY timestamp')
    messages = cursor.fetchall()

    conn.close()
    return messages

if __name__ == "__main__":
    create_messages_table()

    while True:
        message1 = input("User 1: ")
        send_message("User 1", message1)
        time.sleep(1)  # Add a slight delay to simulate message delivery

        message2 = input("User 2: ")
        send_message("User 2", message2)
        time.sleep(1)  # Add a slight delay to simulate message delivery

        messages = get_messages()
        for sender, message, timestamp in messages:
            print(f"{timestamp} - {sender}: {message}")

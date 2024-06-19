import sqlite3
from datetime import datetime, timedelta
import json

try:
    with open("./config_file/config.json", 'r') as file:
        data = json.load(file)
        DB_NAME = data['database']
except Exception as e:
    print(f"Error: An unexpected error occurred. {e}")
    exit()

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    @staticmethod
    def register(name):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            print(f"User registered successfully! Your user ID is {user_id} and name is {name}.")
            return User(user_id, name)
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")
            return None

    @staticmethod
    def login(user_id, name):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE user_id = ? AND name = ?", (user_id, name))
            user = cursor.fetchone()

            conn.close()

            if user:
                return User(user_id, name)
            else:
                print("Invalid user ID or name.")
                return None
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")
            return None

    def view_available_books(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM books WHERE available > 0")
            books = cursor.fetchall()

            conn.close()

            if not books:
                print("No books available.")
            else:
                for book in books:
                    print(f"Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Quantity: {book[3]}")
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")

    def borrow_book(self, book_id):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            # Check if the user has already borrowed the book
            cursor.execute("SELECT * FROM borrow_records WHERE user_id = ? AND book_id = ?", (self.user_id, book_id))
            existing_record = cursor.fetchone()

            if existing_record:
                print("You have already borrowed this book.")
                conn.close()
                return

            # Check if user has already borrowed 5 books
            cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE user_id = ?", (self.user_id,))
            borrow_count = cursor.fetchone()[0]

            if borrow_count >= 5:
                print("You have reached the maximum limit of borrowed books (5).")
                conn.close()
                return

            # Continue with borrowing the book
            cursor.execute("SELECT * FROM books WHERE book_id = ? AND available > 0", (book_id,))
            book = cursor.fetchone()

            if not book:
                print("Book is not available.")
                conn.close()
                return

            due_date = datetime.now() + timedelta(days=14)
            cursor.execute("INSERT INTO borrow_records (user_id, book_id, due_date) VALUES (?, ?, ?)",
                           (self.user_id, book_id, due_date))
            cursor.execute("UPDATE books SET available = available - 1 WHERE book_id = ?", (book_id,))
            conn.commit()
            print(f"Book borrowed successfully! Due date is {due_date}.")

            conn.close()
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")

    def return_book(self, book_id):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM borrow_records WHERE user_id = ? AND book_id = ?", (self.user_id, book_id))
            record = cursor.fetchone()

            if not record:
                print("No record found for this book and user.")
                conn.close()
                return

            due_date = datetime.strptime(record[3], "%Y-%m-%d %H:%M:%S.%f")
            return_date = datetime.now()

            if return_date > due_date:
                fine = data['fine']
                print(f"Book returned late! Fine is {fine} rupees.")
            else:
                fine = 0
                print("Book returned on time!")

            cursor.execute("DELETE FROM borrow_records WHERE user_id = ? AND book_id = ?", (self.user_id, book_id))
            cursor.execute("UPDATE books SET available = available + 1 WHERE book_id = ?", (book_id,))
            conn.commit()

            conn.close()
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")

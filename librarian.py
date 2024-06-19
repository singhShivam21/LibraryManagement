import sqlite3
from books import Book
import json

try:
    with open("./config_file/config.json", 'r') as file:
        data = json.load(file)
        DB_NAME = data['database']
except Exception as e:
    print(f"Error: An unexpected error occurred. {e}")
    exit()


class Librarian:
    def __init__(self, librarian_id, name):
        self.librarian_id = librarian_id
        self.name = name

    @staticmethod
    def register(name):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO librarians (name) VALUES (?)", (name,))
        conn.commit()
        librarian_id = cursor.lastrowid
        conn.close()
        print(f"Librarian registered successfully! Your librarian ID is {librarian_id} and name is {name}.")
        return Librarian(librarian_id, name)

    @staticmethod
    def login(librarian_id, name):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM librarians WHERE librarian_id = ? AND name = ?", (librarian_id, name))
        librarian = cursor.fetchone()

        if librarian:
            return Librarian(librarian_id, name)
        else:
            print("Invalid librarian ID or name.")
            return None

    @staticmethod
    def view_borrow_records():
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT users.name, books.title, borrow_records.due_date
                FROM borrow_records
                JOIN users ON borrow_records.user_id = users.user_id
                JOIN books ON borrow_records.book_id = books.book_id
            """)

            records = cursor.fetchall()

            if not records:
                print("No book issued.")
            else:
                for record in records:
                    print(f"User: {record[0]}, Book: {record[1]}, Due Date: {record[2]}")

            conn.close()
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")

    @staticmethod
    def add_book(title, author, quantity):
        Book.add_book(title, author, quantity)

import sqlite3
import json

try:
    with open("./config_file/config.json", 'r') as file:
        data = json.load(file)
        DB_NAME = data['database']
except Exception as e:
    print(f"Error: An unexpected error occurred. {e}")
    exit()

class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author

    @staticmethod
    def add_book(title, author, quantity):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO books (title, author, available) VALUES (?, ?, ?)",
                           (title, author, quantity))
            conn.commit()

            print("Book added successfully")
        except sqlite3.Error as e:
            print(f"Error occurred2: {e}")

    # @staticmethod  --refer to user for this function
    # def list_available_books():
    #     try:
    #         conn = sqlite3.connect(DB_NAME)
    #         cursor = conn.cursor()
    #
    #         cursor.execute("SELECT * FROM books WHERE available > 0")
    #         books = cursor.fetchall()
    #         #print(books) debug
    #
    #         for book in books:
    #             print(f"Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Quantity: {book[3]}")
    #
    #         conn.close()
    #     except sqlite3.Error as e:
    #         print(f"Error occurred: {e}")

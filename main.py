import sqlite3
from user import User
from librarian import Librarian
import json


try:
    with open("./config_file/config.json", 'r') as file:
        data = json.load(file)
        DB_NAME = data['database']
except Exception as e:
    print(f"Error: An unexpected error occurred. {e}")
    exit()


def setup_database():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                available INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrow_records (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                book_id INTEGER,
                due_date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                FOREIGN KEY(book_id) REFERENCES books(book_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS librarians (
                librarian_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        """)

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error occurred during database setup: {e}")


def get_integer_input(prompt):
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            if value >= 1:
                return value
            else:
                print("Invalid input! Please add at least 1 book")
        except ValueError:
            print("Invalid input! Please enter an integer.")


def user_menu(user):
    try:
        while True:
            print("\nUser Menu")
            print("1. View Available Books")
            print("2. Borrow Book")
            print("3. Return Book")
            print("4. Logout")

            choice = input("Enter your choice: ")

            if choice == '1':
                user.view_available_books()
            elif choice == '2':
                book_id = get_integer_input("Enter book ID to borrow: ")
                user.borrow_book(book_id)
            elif choice == '3':
                book_id = get_integer_input("Enter book ID to return: ")
                user.return_book(book_id)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"Error occurred: {e}")


def librarian_menu(librarian):
    global quantity
    try:
        while True:
            print("\nLibrarian Menu")
            print("1. View Borrowed Records")
            print("2. Add Book")
            print("3. Logout")

            choice = input("Enter your choice: ")

            if choice == '1':
                librarian.view_borrow_records()
            elif choice == '2':
                title = input("Enter book title: ")
                author = input("Enter book author: ")

                quantity = get_integer_input("Enter book quantity: ")

                librarian.add_book(title, author, quantity)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"Error occurred: {e}")



def main():
    setup_database()

    while True:
        print("\nLibrary Management System")
        print("1. User Login")
        print("2. User Registration")
        print("3. Librarian Login")
        print("4. Librarian Registration")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                user_id = get_integer_input("Enter user ID: ")
                name = input("Enter your name: ")
                user = User.login(user_id, name)
                if user:
                    user_menu(user)
            except Exception as e:
                print(f"Error occurred: {e}")

        elif choice == '2':
            try:
                name = input("Enter your name: ")
                user = User.register(name)
                if user:
                    user_menu(user)
            except Exception as e:
                print(f"Error occurred: {e}")

        elif choice == '3':
            try:
                librarian_id = get_integer_input("Enter librarian ID: ")
                name = input("Enter your name: ")
                librarian = Librarian.login(librarian_id, name)
                if librarian:
                    librarian_menu(librarian)
            except Exception as e:
                print(f"Error occurred: {e}")

        elif choice == '4':
            try:
                name = input("Enter your name: ")
                librarian = Librarian.register(name)
                if librarian:
                    librarian_menu(librarian)
            except Exception as e:
                print(f"Error occurred: {e}")

        elif choice == '5':
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

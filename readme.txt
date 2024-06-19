Library Management System
This is a simple library management system implemented in Python using SQLite for database operations. It allows librarians to manage books and users, and users to borrow and return books.

*Features
**Librarian Features:

	Add new books to the library.
	View borrowing records.
	User Features:
**User Features:
	View available books.
	Borrow books (up to 5 books at a time).
	Return books.

*Project Structure
**The project consists of the following files and directories:

--books.py: Contains the Book class with methods for managing books and borrow operations.
--users.py: Placeholder for user management features (not fully implemented).
--config_file/config.json: Configuration file containing database name and fine amount.
--README.md: This file, providing an overview of the project.

*Setup
**Database Setup:

Using the Sqllite inbuild python library.
Configuration:

Update config.json with your database name (DB_NAME), Fine.
Dependencies:

Python 3.x
SQLite3 (comes with Python)
Usage
Run the Program:

Open terminal or command prompt.
Navigate to the project directory.
Run python main.py to start the program.
Librarian Tasks:

Use the provided menu options to add books and view borrowing records.

User Tasks:
Use the provided menu options to view available books, borrow books (up to 5 at a time), and return books.
Exiting the Program:

Librarians and users can choose to logout or exit the program using the menu options.
Notes
This project is a basic implementation.
Error handling is implemented for basic scenarios; additional edge cases may need further handling.

Docker image is also provided and docker file is also included inorder to ease the access.
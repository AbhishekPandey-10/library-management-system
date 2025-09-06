📚 Library Management System (Python + MySQL)

This repo contains two implementations of a Library Management System:

CLI Version (first project I built — command-line interface).

GUI Version (Tkinter-based desktop application).

Both versions use Python + MySQL as the backend.

🔧 Features
✅ CLI Version

Admin and User login system

Add / Delete / Search books

Issue & Return books with fine calculation

New user signup (phone no. + 4-digit password)

Input validation (phone no., password length, etc.)

Tabulated output using tabulate

Parameterized queries (%s placeholders → SQL injection safe)

🎨 GUI Version (Tkinter)

Admin and User menus with login/signup

Add, Delete, Modify, and Search books from a GUI interface

Issue & Return books with rental tracking

User rental history view

Treeview tables for displaying books and rentals

Message boxes for feedback/errors

Cleaner, more user-friendly experience compared to CLI

🛠️ Tech Stack

Python

MySQL

Libraries:

mysql.connector

tabulate (CLI)

tkinter (GUI)

📦 How to Run
Setup Database

Install MySQL and create a database called Library.

Run the provided setup_library_db.py (GUI) or use the .sql file (CLI) to create required tables.

Run CLI Version
cd cli-version
python library_cli.py

Run GUI Version
cd gui-version
python library_system.py

📅 Project Updates
🔄 CLI Updates — July 5, 2025

Refactored all SQL queries → parameterized (%s)

Wrapped DB operations in try-except blocks

Improved CLI menus (admin/user loop flow)

Added rental checks in issue() and return()

Added viewUserRentalHistory()

Remembered logged-in user (c_id)

Pushed clean version to GitHub main branch

🎨 GUI Project — September 2025

Built full Tkinter interface for Admin/User

Added CRUD operations for books with GUI forms

Integrated Treeview for displaying books and rentals

Implemented rental history, issue/return, and user management

Structured code for maintainability (GUI + DB separation planned)

📌 Note

The CLI project was my first proper Python + MySQL system — learned a lot while building it.

The GUI project is the improved, user-friendly version.

Both are in this repo → look inside cli-version/ and gui-version/.

# 📚 Library Management System (Python + MySQL)

This repo contains **two implementations** of a Library Management System:

1. **CLI Version** (first project I built — command-line interface).
2. **GUI Version** (Tkinter-based desktop application).

Both versions use **Python + MySQL** as the backend.

---

## 🔧 Features

### ✅ CLI Version

* Admin and User login system
* Add / Delete / Search books
* Issue & Return books with fine calculation
* New user signup (phone no. + 4-digit password)
* Input validation (phone no., password length, etc.)
* Tabulated output using `tabulate`
* Parameterized queries (`%s` placeholders → SQL injection safe)

### 🎨 GUI Version (Tkinter)

* Admin and User menus with login/signup
* Add, Delete, Modify, and Search books from a GUI interface
* Issue & Return books with rental tracking
* User rental history view
* Treeview tables for displaying books and rentals
* Message boxes for feedback/errors
* Cleaner, more user-friendly experience compared to CLI

---

## 🛠️ Tech Stack

* **Python**
* **MySQL**
* Libraries:

  * `mysql.connector`
  * `tabulate` (CLI)
  * `tkinter` (GUI)

---

## 📦 How to Run

### Setup Database

1. Install MySQL and create a database called `Library`.
2. Run the provided `setup_library_db.py` (GUI) or use the `.sql` file (CLI) to create required tables.

### Run CLI Version

```bash
library_system.py
```

### Run GUI Version

```bash

python LMS GUI.py
```

---

## 📅 Project Updates

### 🔄 CLI Updates — July 5, 2025

1. Refactored all SQL queries → parameterized (`%s`)
2. Wrapped DB operations in try-except blocks
3. Improved CLI menus (admin/user loop flow)
4. Added rental checks in issue() and return()
5. Added `viewUserRentalHistory()`
6. Remembered logged-in user (`c_id`)
7. Pushed clean version to GitHub main branch

### 🎨 GUI Project — September 2025

1. Built full Tkinter interface for Admin/User
2. Added CRUD operations for books with GUI forms
3. Integrated Treeview for displaying books and rentals
4. Implemented rental history, issue/return, and user management
5. Structured code for maintainability (GUI + DB separation planned)

---

## 📌 Note

* The **CLI project** was my first proper Python + MySQL system — learned a lot while building it.
* The **GUI project** is the improved, user-friendly version.
* Both are in this repo.
  
---
### Small Update - Sep 25
1. Removed hardcoded Admin Password
2. Now Admin Gets It's own Username and Password to login , with Validation

# 📚 Library Management System (Python + MySQL CLI Project)

This was the first proper project I built using Python and MySQL.  
It’s a command-line based system where you can manage books, users, issue/return, fines, and all that library-type stuff.

Not gonna lie — started this with almost no idea how to handle MySQL or structure a full system, but figured it out as I built it.  
Learned a lot along the way.

---

## 🔧 Features

- Admin and user login
- Add/Delete/Search books
- Issue & return books with fine calculation
- New user signup with phone no. and 4-digit password
- Error handling and input validation (phone no, password length etc.)
- Tabulated output using `tabulate` (for clean CLI display)
- Used **parameterized queries** to prevent SQL injection everywhere.

---

## 🛠️ Tech Used

- Python
- MySQL
- `mysql.connector` + `tabulate`

---

## 📦 How to Run

1. Make sure MySQL is installed
2. Create a DB called `Library` and set up tables manually (I'll upload `.sql` soon)
3. Run the Python file:
   ```bash
   python library_system.py
 SQL PART UPLOADED 

## 🔄 Project Update — July 5, 2025
 1.Refactored all SQL queries to use %s placeholders (SQL injection safe)
 2.Wrapped all DB operations in try-except blocks
 3.Improved usability in CLI menu (admin/user menu loop, cleaner flow)
 4.Added rental checks in issue() and return() functions
 5.Introduced viewUserRentalHistory() — users can view all their rentals, return status, and charges
 6.Remembered logged-in user (c_id) to avoid repeated prompts
 7.Pushed clean version to GitHub main branch (renamed from master)
⏭️ Next Steps
- Begin building GUI version using Tkinter (`lms_gui.py`)
- Convert each CLI function to GUI form (starting with login + signup)

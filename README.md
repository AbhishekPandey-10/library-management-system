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
- Used **parameterized queries** to prevent SQL injection

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

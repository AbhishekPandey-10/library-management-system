"""
setup_library_db.py

Creates the initial MySQL database tables and sample data for the Library Management System.
Author: Abhishek Pandey
"""

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Enter your password",
    database="library"
)

cursor = conn.cursor()

create_table_query = """
CREATE TABLE books (
  bookid VARCHAR(255) PRIMARY KEY,
  bookname VARCHAR(255),
  author VARCHAR(255),
  genre VARCHAR(255),
  qty INT
)
"""

cursor.execute(create_table_query)
print("Table 'books' created successfully!")

books = [
    ("B100", 'Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 'Fantasy', 10),
    ("B101", 'Harry Potter and the Chamber of Secrets', 'J.K. Rowling', 'Fantasy', 8),
    ("B102", 'Harry Potter and the Prisoner of Azkaban', 'J.K. Rowling', 'Fantasy', 6),
    ("B103", 'Harry Potter and the Goblet of Fire', 'J.K. Rowling', 'Fantasy', 4),
    ("B104", 'Harry Potter and the Order of the Phoenix', 'J.K. Rowling', 'Fantasy', 5),
    ("B105", 'A Song of Ice and Fire: A Game of Thrones', 'George R.R. Martin', 'Fantasy', 7),
    ("B106", 'A Song of Ice and Fire: A Clash of Kings', 'George R.R. Martin', 'Fantasy', 7),
    ("B107", 'A Song of Ice and Fire: A Storm of Swords', 'George R.R. Martin', 'Fantasy', 6),
    ("B108", 'A Song of Ice and Fire: A Feast for Crows', 'George R.R. Martin', 'Fantasy', 6),
    ("B109", 'A Song of Ice and Fire: A Dance with Dragons', 'George R.R. Martin', 'Fantasy', 5),
    ("B110", 'The Alchemist', 'Paulo Coelho', 'Fiction', 8),
    ("B111", 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', 6),
    ("B112", 'Pride and Prejudice', 'Jane Austen', 'Romantic', 5),
    ("B113", 'Romeo and Juliet', 'William Shakespeare', 'Romantic', 6),
    ("B114", 'Jane Eyre', 'Charlotte Brontë', 'Romantic', 7),
    ("B115", 'Frankenstein', 'Mary Shelley', 'Horror', 5),
    ("B116", 'Dracula', 'Bram Stoker', 'Horror', 6),
    ("B117", 'The Shining', 'Stephen King', 'Horror', 7),
    ("B118", 'The Martian', 'Andy Weir', 'Scientific', 5),
    ("B119", 'A Brief History of Time', 'Stephen Hawking', 'Scientific', 7),
    ("B120", 'Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 'Scientific', 6),
    ("B121", 'The God of Small Things', 'Arundhati Roy', 'Fiction', 10),
    ("B122", 'Interpreter of Maladies', 'Jhumpa Lahiri', 'Fiction', 8),
    ("B123", 'Train to Pakistan', 'Khushwant Singh', 'Fiction', 6),
    ("B124", 'The White Tiger', 'Aravind Adiga', 'Fiction', 4),
    ("B125", 'A Suitable Boy', 'Vikram Seth', 'Fiction', 5),
    ("B126", 'The Palace of Illusions', 'Chitra Banerjee Divakaruni', 'Fiction', 3),
    ("B127", 'The Immortals of Meluha', 'Amish Tripathi', 'Fantasy', 2),
    ("B128", 'The Rozabal Line', 'Ashwin Sanghi', 'Thriller', 5),
    ("B129", 'Five Point Someone', 'Chetan Bhagat', 'Fiction', 3),
    ("B130", 'The Great Indian Novel', 'Shashi Tharoor', 'Fiction', 4),
]

insert_query = """
INSERT INTO books (bookid, bookname, author, genre, qty)
VALUES (%s, %s, %s, %s, %s)
"""

cursor.executemany(insert_query, books)
conn.commit()
print("Books inserted successfully!")

create_rentals_table_query = """
CREATE TABLE rentals (
  C_ID INT,
  bookid VARCHAR(255),
  DOI DATE,
  DOR DATE,
  PRICE int(4),
  FOREIGN KEY (bookid) REFERENCES books(bookid)
)
"""

cursor.execute(create_rentals_table_query)
print("Table 'rentals' created successfully!")


create_c_details_table_query = """
CREATE TABLE C_DETAILS (
  C_ID INT PRIMARY KEY,
  C_NAME VARCHAR(255),
  C_PNO VARCHAR(255),
  C_PASS VARCHAR(255),
  C_AD VARCHAR(255)
)
"""
cursor.execute(create_c_details_table_query)
cursor.execute("insert into C_DETAILS values (1000,'ABHISHEK','9118209378','1234','LKO')")

conn.commit()

print("Table  created successfully!")

cursor.close()
conn.close()

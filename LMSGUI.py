import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector as sql
from tabulate import tabulate

class LibraryGUI:
    def __init__(self,show_main_menu=True):
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Database connection
        try:
            self.connect = sql.connect(host="localhost", user="root", passwd='Your Password', database="my_new_library")
            self.cursor = self.connect.cursor()
        except sql.Error as e:
            messagebox.showerror("Database Error", f"Database connection failed: {e}")
            self.root.destroy()
            return
        
        self.current_frame = None
        self.create_main_menu()
    #
    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
    
    def create_main_menu(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.current_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(self.current_frame, text="WELCOME TO LIBRARY", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=30)
        
        # Buttons
        button_frame = tk.Frame(self.current_frame, bg='#f0f0f0')
        button_frame.pack(expand=True)
        
        btn_admin = tk.Button(button_frame, text="Login as Admin", 
                             command=self.admin_login, font=('Arial', 14),
                             bg='#3498db', fg='white', width=20, height=2,
                             relief='raised', bd=3)
        btn_admin.pack(pady=10)
        
        btn_user = tk.Button(button_frame, text="Login as User", 
                            command=self.user_login, font=('Arial', 14),
                            bg='#27ae60', fg='white', width=20, height=2,
                            relief='raised', bd=3)
        btn_user.pack(pady=10)
        
        btn_signup = tk.Button(button_frame, text="Sign up as New User", 
                              command=self.signup_window, font=('Arial', 14),
                              bg='#e74c3c', fg='white', width=20, height=2,
                              relief='raised', bd=3)
        btn_signup.pack(pady=10)
        
        btn_exit = tk.Button(button_frame, text="Exit", 
                            command=self.root.quit, font=('Arial', 14),
                            bg='#95a5a6', fg='white', width=20, height=2,
                            relief='raised', bd=3)
        btn_exit.pack(pady=10)
    
    def admin_login(self):
        username = simpledialog.askstring("Admin Login", "Enter your admin id:")
        if not username or username != 'admin':
            messagebox.showerror("Error", "Invalid admin ID")
            return
        self.cursor.execute("SELECT admin_password FROM admin WHERE admin_id=1")
        result = self.cursor.fetchone()
        password = simpledialog.askstring("Admin Login", "Enter the password:", show='*')
        if password and password == str(result[0]):
            self.admin_menu()
        elif password:
            messagebox.showerror("Error", "Wrong password")
    
    def admin_menu(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.current_frame.pack(fill='both', expand=True)

        title_label = tk.Label(self.current_frame, text="ADMIN PANEL", 
                              font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=20)

        button_frame = tk.Frame(self.current_frame, bg='#f0f0f0')
        button_frame.pack(expand=True)
        
        buttons = [
            ("Add book", self.add_book_window),
            ("Delete book", self.delete_book_window),
            ("Modify Quantity", self.modify_qty_window),
            ("Issue a book", self.issue_book_window),
            ("Return a book", self.return_book_window),
            ("See currently rented books", self.show_rented_books),
            ("See Returned books", self.show_returned_books),
            ("Back to Main Menu", self.create_main_menu)
        ]
        
        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, command=command, 
                           font=('Arial', 12), bg='#3498db', fg='white',
                           width=25, height=1, relief='raised', bd=2)
            btn.pack(pady=5)
    
    def user_login(self):
        try:
            customer_id = simpledialog.askstring("User Login", "Enter your customer id:")
            if not customer_id:
                return
            
            customer_id = int(customer_id)
            self.cursor.execute("select C_PASS from C_DETAILS where C_ID=%s", (customer_id,))
            result = self.cursor.fetchone()
            
            if result is None:
                messagebox.showerror("Error", "No data found.")
                return
            
            password = simpledialog.askstring("User Login", "Enter Password:", show='*')
            if password == str(result[0]):
                self.search_book_window()
            else:
                messagebox.showerror("Error", "Wrong Password")
        except ValueError:
            messagebox.showerror("Error", "Invalid customer id")
        except Exception as e:
            messagebox.showerror("Error", f"Error in login: {e}")
    
    def add_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Book")
        window.geometry("400x400")
        window.configure(bg='#f0f0f0')

        tk.Label(window, text="Enter Book ID:", bg='#f0f0f0').pack(pady=5)
        book_id_entry = tk.Entry(window, width=30)
        book_id_entry.pack(pady=5)
        
        tk.Label(window, text="Enter Book name:", bg='#f0f0f0').pack(pady=5)
        book_name_entry = tk.Entry(window, width=30)
        book_name_entry.pack(pady=5)
        
        tk.Label(window, text="Enter Author name:", bg='#f0f0f0').pack(pady=5)
        author_entry = tk.Entry(window, width=30)
        author_entry.pack(pady=5)
        
        tk.Label(window, text="Enter Genre:", bg='#f0f0f0').pack(pady=5)
        genre_entry = tk.Entry(window, width=30)
        genre_entry.pack(pady=5)
        
        tk.Label(window, text="Enter Quantity:", bg='#f0f0f0').pack(pady=5)
        qty_entry = tk.Entry(window, width=30)
        qty_entry.pack(pady=5)
        
        def add_book():
            try:
                book_id = book_id_entry.get()
                book_name = book_name_entry.get()
                author_name = author_entry.get()
                genre = genre_entry.get()
                qty = int(qty_entry.get())
                
                st = "insert into BOOKS values(%s,%s,%s,%s,%s)"
                self.cursor.execute(st, (book_id, book_name, author_name, genre, qty))
                self.connect.commit()
                messagebox.showinfo("Success", "Book added Successfully")
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity input")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding book: {e}")
        
        tk.Button(window, text="Add Book", command=add_book, 
                 bg='#27ae60', fg='white', font=('Arial', 12)).pack(pady=20)
    
    def delete_book_window(self):
        book_id = simpledialog.askstring("Delete Book", "Enter book id you wish to delete:")
        if book_id:
            try:
                st3 = "delete from BOOKS where BOOKID=%s"
                self.cursor.execute(st3, (book_id,))
                self.connect.commit()
                messagebox.showinfo("Success", "Book deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting book: {e}")
    
    def modify_qty_window(self):
        window = tk.Toplevel(self.root)
        window.title("Modify Quantity")
        window.geometry("400x300")
        window.configure(bg='#f0f0f0')
        
        tk.Label(window, text="Enter book ID:", bg='#f0f0f0').pack(pady=10)
        book_id_entry = tk.Entry(window, width=30)
        book_id_entry.pack(pady=5)
        
        tk.Label(window, text="Select operation:", bg='#f0f0f0').pack(pady=10)
        
        operation_var = tk.StringVar(value="add")
        tk.Radiobutton(window, text="Add Books", variable=operation_var, 
                      value="add", bg='#f0f0f0').pack()
        tk.Radiobutton(window, text="Remove Books", variable=operation_var, 
                      value="remove", bg='#f0f0f0').pack()
        
        tk.Label(window, text="Enter quantity:", bg='#f0f0f0').pack(pady=10)
        qty_entry = tk.Entry(window, width=30)
        qty_entry.pack(pady=5)
        
        def modify_qty():
            try:
                book_id = book_id_entry.get()
                qty = int(qty_entry.get())
                operation = operation_var.get()
                
                if operation == "add":
                    st5 = "update BOOKS set QTY=QTY+%s where BOOKID=%s"
                else:
                    st5 = "update BOOKS set QTY=QTY-%s where BOOKID=%s"
                
                self.cursor.execute(st5, (qty, book_id))
                self.connect.commit()
                messagebox.showinfo("Success", "QUANTITY updated successfully")
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid number input")
            except Exception as e:
                messagebox.showerror("Error", f"Error updating quantity: {e}")
        
        tk.Button(window, text="Update Quantity", command=modify_qty,
                 bg='#e67e22', fg='white', font=('Arial', 12)).pack(pady=20)
    
    def issue_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Issue Book")
        window.geometry("400x250")
        window.configure(bg='#f0f0f0')
        
        tk.Label(window, text="Enter customer ID:", bg='#f0f0f0').pack(pady=5)
        customer_id_entry = tk.Entry(window, width=30)
        customer_id_entry.pack(pady=5)
        
        tk.Label(window, text="Enter book ID:", bg='#f0f0f0').pack(pady=5)
        book_id_entry = tk.Entry(window, width=30)
        book_id_entry.pack(pady=5)
        
        tk.Label(window, text="Enter date (YYYY-MM-DD):", bg='#f0f0f0').pack(pady=5)
        date_entry = tk.Entry(window, width=30)
        date_entry.pack(pady=5)
        
        def issue_book():
            try:
                cid = customer_id_entry.get()
                bid = book_id_entry.get()
                doi = date_entry.get()
                #checking the entries of customer and quantity if book is available
                self.cursor.execute("select * from C_DETAILS where C_ID=%s",(cid,))
                result1=self.cursor.fetchone()
                if result1 is None:
                    messagebox.showerror("Error", "No customer data found.")
                    return
                self.cursor.execute("select * from BOOKS where BOOKID=%s and QTY>0",(bid,))
                result2=self.cursor.fetchone()
                if result2 is None:
                    messagebox.showerror("Error", "No book data found or book out of stock.")
                    return
                else:
                    st6 = "insert into RENTALS values(%s,%s,%s,NULL,NULL)"
                    self.cursor.execute(st6, (cid, bid, doi))
                    self.connect.commit()
                    
                    st7 = "update BOOKS set QTY=QTY-1 where BOOKID=%s"
                    self.cursor.execute(st7, (bid,))
                    self.connect.commit()
                
                messagebox.showinfo("Success", "BOOK ISSUED SUCCESSFULLY")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error issuing book: {e}")
        
        tk.Button(window, text="Issue Book", command=issue_book,
                 bg='#8e44ad', fg='white', font=('Arial', 12)).pack(pady=20)
    
    def return_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Return Book")
        window.geometry("400x250")
        window.configure(bg='#f0f0f0')
        
        tk.Label(window, text="Enter customer ID:", bg='#f0f0f0').pack(pady=5)
        customer_id_entry = tk.Entry(window, width=30)
        customer_id_entry.pack(pady=5)
        
        tk.Label(window, text="Enter book ID:", bg='#f0f0f0').pack(pady=5)
        book_id_entry = tk.Entry(window, width=30)
        book_id_entry.pack(pady=5)
        
        tk.Label(window, text="Enter return date (YYYY-MM-DD):", bg='#f0f0f0').pack(pady=5)
        date_entry = tk.Entry(window, width=30)
        date_entry.pack(pady=5)
        
        def return_book():
            try:
                cid = customer_id_entry.get()
                bid = book_id_entry.get()
                dor = date_entry.get()
                
                st8 = "UPDATE RENTALS SET dor=%s WHERE BOOKID=%s"
                self.cursor.execute(st8, (dor, bid))
                self.connect.commit()
                
                st9 = "UPDATE BOOKS SET QTY=QTY+1 WHERE BOOKID=%s"
                self.cursor.execute(st9, (bid,))
                self.connect.commit()
                
                str10 = "SELECT DATEDIFF(dor, doi) FROM RENTALS WHERE BOOKID=%s AND C_ID=%s"
                self.cursor.execute(str10, (bid, cid))
                days = self.cursor.fetchone()
                
                if days is None:
                    messagebox.showerror("Error", "No data found.")
                    return
                
                fine = 0
                if days[0] <= 15:
                    price = days[0] * 5
                elif days[0] > 15:
                    fine = (days[0] - 15) * 15
                    price = fine + (15 * 5)
                
                st11 = "UPDATE RENTALS SET PRICE=%s WHERE BOOKID=%s AND C_ID=%s"
                self.cursor.execute(st11, (price, bid, cid))
                self.connect.commit()
                self.cursor.execute("SELECT C_ID, C_NAME, C_PNO, BOOKID, DOI, DOR, PRICE FROM RENTALS NATURAL JOIN C_DETAILS WHERE BOOKID=%s AND C_ID=%s", (bid, cid))
                bill = self.cursor.fetchone()
                
                if bill:
                    bill_text = f"""
BOOK RETURNED SUCCESSFULLY

BILL:
Customer ID: {bill[0]}
Customer Name: {bill[1]}
Phone No.: {bill[2]}
Book ID: {bill[3]}
Date of Issue: {bill[4]}
Date of Return: {bill[5]}
Total Amount: {bill[6]}
Fine: {fine}
                    """
                    messagebox.showinfo("Bill", bill_text)
                    window.destroy()
                else:
                    messagebox.showerror("Error", "No data found.")
            except Exception as e:
                messagebox.showerror("Error", f"Error returning book: {e}")
        
        tk.Button(window, text="Return Book", command=return_book,
                 bg='#c0392b', fg='white', font=('Arial', 12)).pack(pady=20)
    
    def show_rented_books(self):
        try:
            st10 = "SELECT BOOKS.BOOKID, BOOKS.BOOKNAME, BOOKS.AUTHOR, BOOKS.GENRE, RENTALS.C_ID, C_DETAILS.C_NAME, RENTALS.DOI FROM BOOKS INNER JOIN RENTALS ON BOOKS.BOOKID=RENTALS.BOOKID INNER JOIN C_DETAILS ON RENTALS.C_ID=C_DETAILS.C_ID WHERE RENTALS.DOR IS NULL"
            self.cursor.execute(st10)
            data = self.cursor.fetchall()
            
            self.show_table_window("Currently Rented Books", data, 
                                 ["BOOKID", "BOOKNAME", "AUTHOR", "GENRE", "C_ID", "C_NAME", "DOI"])
        except Exception as e:
            messagebox.showerror("Error", f"Error showing rented books: {e}")
    
    def show_returned_books(self):
        try:
            st11 = "SELECT BOOKS.BOOKID, BOOKS.BOOKNAME, BOOKS.AUTHOR, BOOKS.GENRE, RENTALS.C_ID, C_DETAILS.C_NAME, RENTALS.DOI, RENTALS.DOR, RENTALS.PRICE FROM BOOKS INNER JOIN RENTALS ON BOOKS.BOOKID=RENTALS.BOOKID INNER JOIN C_DETAILS ON RENTALS.C_ID=C_DETAILS.C_ID WHERE RENTALS.DOR IS NOT NULL"
            self.cursor.execute(st11)
            data = self.cursor.fetchall()
            
            self.show_table_window("Returned Books", data, 
                                 ["BOOKID", "BOOKNAME", "AUTHOR", "GENRE", "C_ID", "C_NAME", "DOI", "DOR", "PRICE"])
        except Exception as e:
            messagebox.showerror("Error", f"Error showing returned books: {e}")
    
    def search_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Search Books")
        window.geometry("500x400")
        window.configure(bg='#f0f0f0')
        
        tk.Label(window, text="Search Books", font=('Arial', 16, 'bold'), bg='#f0f0f0').pack(pady=10)
        
        search_var = tk.StringVar(value="1")
        
        tk.Radiobutton(window, text="Search by book name", variable=search_var, 
                      value="1", bg='#f0f0f0').pack(pady=2)
        tk.Radiobutton(window, text="Search by author", variable=search_var, 
                      value="2", bg='#f0f0f0').pack(pady=2)
        tk.Radiobutton(window, text="Search by genre", variable=search_var, 
                      value="3", bg='#f0f0f0').pack(pady=2)
        tk.Radiobutton(window, text="Show all books", variable=search_var, 
                      value="4", bg='#f0f0f0').pack(pady=2)
        
        tk.Label(window, text="Enter search term (leave blank for 'show all'):", bg='#f0f0f0').pack(pady=5)
        search_entry = tk.Entry(window, width=30)
        search_entry.pack(pady=5)
        
        def search_books():
            try:
                choice = search_var.get()
                search_term = "%"+search_entry.get()+"%"
                
                if choice == "1":
                    st4 = "select * from BOOKS where BOOKNAME like %s"
                    self.cursor.execute(st4, (search_term,))
                elif choice == "2":
                    st4 = "select * from BOOKS where AUTHOR like %s"
                    self.cursor.execute(st4, (search_term,))
                elif choice == "3":
                    st4 = "select * from BOOKS where GENRE like %s"
                    self.cursor.execute(st4, (search_term,))
                elif choice == "4":
                    st4 = "select * from BOOKS"
                    self.cursor.execute(st4)
                
                data = self.cursor.fetchall()
                self.show_table_window("Search Results", data, 
                                     ["BOOKID", "BOOKNAME", "AUTHOR", "GENRE", "QTY"])
            except Exception as e:
                messagebox.showerror("Error", f"Error searching books: {e}")
        
        tk.Button(window, text="Search", command=search_books,
                 bg='#16a085', fg='white', font=('Arial', 12)).pack(pady=10)
        
        tk.Button(window, text="Back to Main Menu", command=lambda: [window.destroy(), self.create_main_menu()],
                 bg='#95a5a6', fg='white', font=('Arial', 12)).pack(pady=5)
    
    def signup_window(self):
        window = tk.Toplevel(self.root)
        window.title("Sign Up")
        window.geometry("400x350")
        window.configure(bg='#f0f0f0')
        
        tk.Label(window, text="Sign Up", font=('Arial', 16, 'bold'), bg='#f0f0f0').pack(pady=10)
        
        tk.Label(window, text="Enter Your Name:", bg='#f0f0f0').pack(pady=5)
        name_entry = tk.Entry(window, width=30)
        name_entry.pack(pady=5)
        
        tk.Label(window, text="Enter Your Phone No:", bg='#f0f0f0').pack(pady=5)
        phone_entry = tk.Entry(window, width=30)
        phone_entry.pack(pady=5)
        
        tk.Label(window, text="Enter Your Address:", bg='#f0f0f0').pack(pady=5)
        address_entry = tk.Entry(window, width=30)
        address_entry.pack(pady=5)
        
        tk.Label(window, text="CREATE A FOUR-DIGIT PASSWORD:", bg='#f0f0f0').pack(pady=5)
        password_entry = tk.Entry(window, width=30, show='*')
        password_entry.pack(pady=5)
        
        def signup():
            try:
                self.cursor.execute("SELECT MAX(C_ID) FROM C_DETAILS")
                last_cid = self.cursor.fetchone()[0]
                cid = last_cid + 1 if last_cid else 1
                
                name = name_entry.get()
                pno = phone_entry.get()
                ad = address_entry.get()
                pssd = int(password_entry.get())
                
                if not pno.isdigit() or len(pno) != 10:
                    messagebox.showerror("Error", "Invalid phone number. It must be 10 digits.")
                    return
                
                if pssd < 1000 or pssd > 9999:
                    messagebox.showerror("Error", "Password must be exactly 4 digits.")
                    return
                
                self.cursor.execute("INSERT INTO C_DETAILS VALUES(%s, %s, %s, %s, %s)", 
                                  (cid, name, pno, pssd, ad))
                self.connect.commit()
                
                details = f"""
YOUR DETAILS:
Name: {name}
Phone No: {pno}
Address: {ad}
Customer ID: {cid}
Password: {pssd}
                """
                messagebox.showinfo("Registration Successful", details)
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid password input.")
            except Exception as e:
                messagebox.showerror("Error", f"Error during signup: {e}")
        
        tk.Button(window, text="Sign Up", command=signup,
                 bg='#e74c3c', fg='white', font=('Arial', 12)).pack(pady=20)
    
    def show_table_window(self, title, data, headers):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("900x500")
        
        # Create treeview
        tree = ttk.Treeview(window, columns=headers, show='headings')
        
        # Define headings
        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, width=100)
        
        # Insert data
        for row in data:
            tree.insert('', 'end', values=row)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack everything
        tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Back button
        back_frame = tk.Frame(window)
        back_frame.pack(side="bottom", fill="x")
        tk.Button(back_frame, text="Close", command=window.destroy,
                 bg='#95a5a6', fg='white', font=('Arial', 10)).pack(pady=5)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()
        if self.connect:
            self.connect.close()

if __name__ == "__main__":
    app = LibraryGUI()
    app.run()

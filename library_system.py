import mysql.connector as sql
from tabulate import tabulate
try:
    connect = sql.connect(host="localhost", user="root", passwd='Your Password Here', database="Library")
except sql.Error as e:
    print("Database connection failed:", e)
    exit()
cursor = connect.cursor()
choice = 1

def addbook():
    try:
        book_id = input("Enter BOOK ID: ").strip()
        book_name = input("Enter BOOK NAME: ").strip()
        author = input("Enter AUTHOR NAME: ").strip()
        genre = input("Enter GENRE: ").strip()

        try:
            qty = int(input("Enter QUANTITY: "))
            if qty < 0:
                print(" Quantity cannot be negative.")
                return
        except ValueError:
            print(" Invalid quantity. Must be a number.")
            return

        cursor.execute("SELECT * FROM BOOKS WHERE BOOKID = %s", (book_id,))
        if cursor.fetchone():
            print(" A book with this ID already exists.")
            return


        cursor.execute(
            "INSERT INTO BOOKS VALUES (%s, %s, %s, %s, %s)",
            (book_id, book_name, author, genre, qty)
        )
        connect.commit()
        print("BOOK added successfully.")

    except Exception as e:
        print("Error while adding book:", e)



def showBOOK():
    st2 = "select * from BOOKS order by Genre"
    cursor.execute(st2)
    print(tabulate(cursor.fetchall(), ["BOOKID", "BOOKNAME", "AUTHOR", "GENRE", "QTY"], tablefmt='grid'))


def delBOOK():
    try:
        book_id = input("Enter the Book ID you want to delete: ").strip()

        cursor.execute("SELECT * FROM BOOKS WHERE BOOKID = %s", (book_id,))
        book = cursor.fetchone()
        if not book:
            print("Book ID not found.")
            return

        confirm = input(f"Are you sure you want to delete '{book[1]}' (yes/no)? ").strip().lower()
        if confirm != "yes":
            print("Deletion cancelled.")
            return

        cursor.execute("DELETE FROM BOOKS WHERE BOOKID = %s", (book_id,))
        connect.commit()
        print("Book deleted successfully.")

    except Exception as e:
        print("Error during deletion:", e)


def searchBOOK():
    try:
        print("1 - Search by book name")
        print("2 - Search by author")
        print("3 - Search by genre")
        print("4 - Show all books")
        
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            value = input("Enter book name: ").strip()
            query = "SELECT * FROM BOOKS WHERE BOOKNAME LIKE %s"
            params = ("%" + value + "%",)
        elif choice == "2":
            value = input("Enter author name: ").strip()
            query = "SELECT * FROM BOOKS WHERE AUTHOR LIKE %s"
            params = ("%" + value + "%",)
        elif choice == "3":
            value = input("Enter genre: ").strip()
            query = "SELECT * FROM BOOKS WHERE GENRE LIKE %s"
            params = ("%" + value + "%",)
        elif choice == "4":
            query = "SELECT * FROM BOOKS ORDER BY GENRE"
            params = ()
        else:
            print("Invalid choice.")
            return

        cursor.execute(query, params)
        results = cursor.fetchall()
        if not results:
            print("No books found.")
            return

        print(tabulate(results, ["BOOKID", "BOOKNAME", "AUTHOR", "GENRE", "QTY"], tablefmt='grid'))

    except Exception as e:
        print("Error during book search:", e)


def modifyQTY():
    try:
        book_id = input("Enter the Book ID to modify quantity: ").strip()

        cursor.execute("SELECT QTY FROM BOOKS WHERE BOOKID = %s", (book_id,))
        book = cursor.fetchone()
        if not book:
            print("Book ID not found.")
            return

        print("1: If books are being added")
        print("2: If books are being removed")
        choice = input("Enter your choice (1 or 2): ").strip()

        if choice not in ("1", "2"):
            print("Invalid choice.")
            return

        try:
            amount = int(input("Enter number of books: "))
            if amount <= 0:
                print("Quantity must be positive.")
                return
        except ValueError:
            print("Invalid quantity input.")
            return

        current_qty = book[0]

        if choice == "1":
            new_qty = current_qty + amount
        else:
            if amount > current_qty:
                print("Cannot remove more books than available in stock.")
                return
            new_qty = current_qty - amount

        cursor.execute("UPDATE BOOKS SET QTY = %s WHERE BOOKID = %s", (new_qty, book_id))
        connect.commit()
        print("Quantity updated successfully.")

    except Exception as e:
        print("Error while modifying quantity:", e)

def issue():
    try:
        cID1 = input("Enter customer ID: ")
        B_id3 = input("Enter book ID to be issued: ")
        doi = input("Enter issue date (YYYY-MM-DD): ")

        cursor.execute("SELECT * FROM C_DETAILS WHERE C_ID = %s", (cID1,))
        customer = cursor.fetchone()
        if not customer:
            print(" Invalid customer ID.")
            return

        cursor.execute("SELECT * FROM BOOKS WHERE BOOKID = %s", (B_id3,))
        book = cursor.fetchone()
        if not book:
            print(" Invalid book ID.")
            return

        if book[4] <= 0:
            print(" Book is currently out of stock.")
            return

        cursor.execute("""
            SELECT * FROM RENTALS
            WHERE BOOKID = %s AND C_ID = %s AND DOR IS NULL
        """, (B_id3, cID1))
        already_rented = cursor.fetchone()
        if already_rented:
            print("You can't rent the same book twice without returning it first.")
            return

        cursor.execute(
            "INSERT INTO RENTALS VALUES (%s, %s, %s, NULL, NULL)",
            (cID1, B_id3, doi)
        )
        cursor.execute(
            "UPDATE BOOKS SET QTY = QTY - 1 WHERE BOOKID = %s",
            (B_id3,)
        )
        connect.commit()

        print("BOOK ISSUED SUCCESSFULLY.")

    except Exception as e:
        print(" Error during book issue:", e)



def Return():
    try:
        cID2 = input("Enter customer ID: ")
        B_id4 = input("Enter book ID to return: ")
        dor = input("Enter return date (YYYY-MM-DD): ")


        check_query = """
            SELECT * FROM RENTALS
            WHERE BOOKID = %s AND C_ID = %s AND DOR IS NULL
        """
        cursor.execute(check_query, (B_id4, cID2))
        record = cursor.fetchone()

        if not record:
            print(" Book is either already returned or wasn't rented by this customer.")
            return


        st8 = "UPDATE RENTALS SET dor=%s WHERE BOOKID=%s AND C_ID=%s AND DOR IS NULL"
        cursor.execute(st8, (dor, B_id4, cID2))
        connect.commit()

        st9 = "UPDATE BOOKS SET QTY=QTY+1 WHERE BOOKID=%s"
        cursor.execute(st9, (B_id4,))
        connect.commit()

        str10 = "SELECT DATEDIFF(dor, doi) FROM RENTALS WHERE BOOKID=%s AND C_ID=%s"
        cursor.execute(str10, (B_id4, cID2))
        days = cursor.fetchone()

        if not days:
            print("Failed to fetch rental duration.")
            return

        fine = 0
        if days[0] <= 15:
            price = days[0] * 5
        else:
            fine = (days[0] - 15) * 15
            price = fine + (15 * 5)

        st11 = "UPDATE RENTALS SET PRICE=%s WHERE BOOKID=%s AND C_ID=%s"
        cursor.execute(st11, (price, B_id4, cID2))
        connect.commit()

        print("\n BOOK RETURNED SUCCESSFULLY\n BILL:")
        cursor.execute("""
            SELECT C_ID, C_NAME, C_PNO, BOOKID, DOI, DOR, PRICE
            FROM RENTALS NATURAL JOIN C_DETAILS
            WHERE BOOKID=%s AND C_ID=%s
        """, (B_id4, cID2))

        bill = cursor.fetchone()
        if not bill:
            print(" No billing record found.")
            return

        fields = ["Customer ID", "Customer Name", "Phone No.", "Book ID", "Date of Issue", "Date of Return", "Total Price"]
        for i in range(len(fields)):
            print(f"{fields[i]} :: {bill[i]}")
        print("Late Fine ::", fine)

    except Exception as e:
        print(" Error during book return:", e)


def signUP():
    try:
        cursor.execute("SELECT MAX(C_ID) FROM C_DETAILS")
        last_cid = cursor.fetchone()[0]
        cid = last_cid + 1 if last_cid else 1

        name = input("Enter Your Name: ").strip()
        pno = input("Enter Your PHONE NO: ").strip()
        if not pno.isdigit() or len(pno) != 10:
            print(" Invalid phone number. It must be 10 digits.")
            return

        ad = input("Enter Your ADDRESS: ").strip()

        try:
            pssd = int(input("Create a FOUR-DIGIT PASSWORD: "))
            if pssd < 1000 or pssd > 9999:
                print("Password must be exactly 4 digits.")
                return
        except ValueError:
            print(" Invalid password input. Must be a 4-digit number.")
            return

        cursor.execute(
            "INSERT INTO C_DETAILS VALUES(%s, %s, %s, %s, %s)",
            (cid, name, pno, pssd, ad)
        )
        connect.commit()

        print("\n ACCOUNT CREATED SUCCESSFULLY")
        print("Name:", name)
        print("Phone No:", pno)
        print("Address:", ad)
        print("Customer ID:", cid)
        print("Password:", pssd)

    except Exception as e:
        print(" Database error during signup:", e)



def showRentedBooks():
    try:
        query = """
            SELECT BOOKS.BOOKID, BOOKS.BOOKNAME, BOOKS.AUTHOR, BOOKS.GENRE,
                   RENTALS.C_ID, C_DETAILS.C_NAME, RENTALS.DOI
            FROM BOOKS
            INNER JOIN RENTALS ON BOOKS.BOOKID = RENTALS.BOOKID
            INNER JOIN C_DETAILS ON RENTALS.C_ID = C_DETAILS.C_ID
            WHERE RENTALS.DOR IS NULL
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("No books are currently rented.")
            return

        print(tabulate(results, ["BOOKID", "BOOKNAME", "AUTHOR", "GENRE", "C_ID", "C_NAME", "DOI"], tablefmt='grid'))

    except Exception as e:
        print("Error while fetching rented books:", e)

def showReturnedBooks():
    try:
        query = """
            SELECT BOOKS.BOOKID, BOOKS.BOOKNAME, BOOKS.AUTHOR, BOOKS.GENRE,
                   RENTALS.C_ID, C_DETAILS.C_NAME, RENTALS.DOI, RENTALS.DOR, RENTALS.PRICE
            FROM BOOKS
            INNER JOIN RENTALS ON BOOKS.BOOKID = RENTALS.BOOKID
            INNER JOIN C_DETAILS ON RENTALS.C_ID = C_DETAILS.C_ID
            WHERE RENTALS.DOR IS NOT NULL
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("No books have been returned yet.")
            return

        print(tabulate(results, ["BOOKID", "BOOKNAME", "AUTHOR", "GENRE", "C_ID", "C_NAME", "DOI", "DOR", "PRICE"], tablefmt='grid'))

    except Exception as e:
        print("Error while fetching returned books:", e)

def viewUserRentalHistory(customer_id):
    try:
        cursor.execute("""
            SELECT BOOKS.BOOKID, BOOKS.BOOKNAME, BOOKS.AUTHOR, RENTALS.DOI, RENTALS.DOR, RENTALS.PRICE
            FROM BOOKS
            INNER JOIN RENTALS ON BOOKS.BOOKID = RENTALS.BOOKID
            WHERE RENTALS.C_ID = %s
            ORDER BY RENTALS.DOI DESC
        """, (customer_id,))
        results = cursor.fetchall()

        if not results:
            print("You have not rented any books yet.")
            return

        print(tabulate(results, ["BOOKID", "BOOKNAME", "AUTHOR", "DOI", "DOR", "PRICE"], tablefmt='grid'))

    except Exception as e:
        print("Error while fetching rental history:", e)



while True:
    print("\n\tWELCOME TO LIBRARY")
    print("1. Login as ADMIN")
    print("2. Login as USER")
    print("3. Sign up as NEW USER")
    print("4. Exit")

    choice1 = input("Enter your choice: ").strip()

    if choice1 == "1":
        if input("Enter the password: ") == "2049":
            while True:
                print("\n--- ADMIN MENU ---")
                print("1. Add book")
                print("2. Delete book")
                print("3. Modify quantity")
                print("4. Issue a book")
                print("5. Return a book")
                print("6. See currently rented books")
                print("7. See returned books")
                print("8. Show all books")
                print("9. Back to main menu")

                achoice = input("Enter your choice: ").strip()

                if achoice == "1":
                    addbook()
                elif achoice == "2":
                    delBOOK()
                elif achoice == "3":
                    modifyQTY()
                elif achoice == "4":
                    issue()
                elif achoice == "5":
                    Return()
                elif achoice == "6":
                    showRentedBooks()
                elif achoice == "7":
                    showReturnedBooks()
                elif achoice == "8":
                    showBOOK()
                elif achoice == "9":
                    break
                else:
                    print("Invalid admin choice.")
        else:
            print("Wrong password.")

    elif choice1 == "2":
        try:
            user_id = int(input("Enter your customer ID: "))
            cursor.execute("SELECT C_PASS FROM C_DETAILS WHERE C_ID = %s", (user_id,))
            result = cursor.fetchone()
            if not result:
                print("Customer not found.")
                continue
            if input("Enter password: ") == str(result[0]):
                current_user_id = user_id 
                while True:
                    print("\n--- USER MENU ---")
                    print("1. Search for books")
                    print("2. View rental history")
                    print("3. Back to main menu")

                    user_choice = input("Enter your choice: ").strip()

                    if user_choice == "1":
                        searchBOOK()
                    elif user_choice == "2":
                        viewUserRentalHistory(current_user_id)
                    elif user_choice == "3":
                        break
                    else:
                        print("Invalid choice.")
            else:
                print("Wrong password.")
        except:
            print("Invalid input.")


    elif choice1 == "3":
        signUP()

    elif choice1 == "4":
        print("Exiting program.")
        break

    else:
        print("Invalid main menu choice.")
connect.close()

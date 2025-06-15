import mysql.connector as sql
from tabulate import tabulate
try:
    connect = sql.connect(host="localhost", user="root", passwd='1', database="Library")
except sql.Error as e:
    print("Database connection failed:", e)
    exit()
cursor = connect.cursor()
choice = 1

def addbook():
    st = "insert into BOOKS values('{}','{}','{}','{}','{}')".format(
        input("Enter BOOK id"),
        input("Enter BOOK name"),
        input("Enter AUTHOR name"),
        input("Enter GENRE"),
        int(input("Enter QUANTITY"))
    )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    cursor.execute(st)
    connect.commit()
    print("BOOK added Successfully")


def showBOOK():
    st2 = "select * from BOOKS order by Genre"
    cursor.execute(st2)
    print(tabulate(cursor.fetchall(), ["BOOKID", "BOOKNAME", "AUTHOR", "GENRE", "QTY"], tablefmt='grid'))


def delBOOK():
    B_id1 = input("Enter book id you wish to delete: ")
    st3 = "delete from BOOKS where BOOKID='{}'".format(B_id1)
    cursor.execute(st3)
    connect.commit()
    print("Book deleted successfully")


def searchBOOK():
    print('''1 - search by book name
2 - search by author
3 - search by genre
4 - show all books''')
    choice2 = int(input("ENTER YOUR CHOICE: "))
    if choice2 == 1:
        B_name = input('enter book name: ')
        st4 = "select * from BOOKS where BOOKNAME='{}'".format(B_name)
    elif choice2 == 2:
        A_name = input("Enter the author name of the book: ")
        st4 = "select * from BOOKS where AUTHOR='{}'".format(A_name)
    elif choice2 == 3:
        G_name = input("Enter the genre of the book: ")
        st4 = "select * from BOOKS where GENRE='{}'".format(G_name)
    elif choice2 == 4:
        
        st4 = "select * from BOOKS"
    else:
        print("Invalid choice")
    cursor.execute(st4)
    print(tabulate(cursor.fetchall(), ["BOOKID", "BOOKNAME", "AUTHOR", "GENRE", "QTY"], tablefmt='grid'))


def modifyQTY():
    B_id2 = input("Enter book id you wish to modify QUANTITY: ")
    print("1: If Books are added\n2: If Books are removed")
    choice3 = int(input("ENTER YOUR CHOICE: "))
    if choice3 == 1:
        Bnum = int(input("Enter no. of book added: "))
        st5 = "update BOOKS set QTY=QTY+{} where BOOKID='{}'".format(Bnum, B_id2)
    elif choice3 == 2:
        Bnum = int(input("Enter no. of book removed: "))
        st5 = "update BOOKS set QTY=QTY-{} where BOOKID='{}'".format(Bnum, B_id2)
    cursor.execute(st5)
    connect.commit()
    print("QUANTITY updated successfully")


def issue():
    cID1 = input("Enter customer id of the person who wishes to rent the book: ")
    B_id3 = input("Enter book id to be issued: ")
    doi = input("Enter date like YYYY-MM-DD")
    
    st6 = "insert into RENTALS values('{}','{}','{}',NULL,NULL)".format(cID1, B_id3, doi)
    cursor.execute(st6)
    connect.commit()
    st7 = "update BOOKS set QTY=QTY-1 where BOOKID='{}'".format(B_id3)
    cursor.execute(st7)
    print("BOOK ISSUED SUCCESSFULLY")
    connect.commit()


def Return():
    cID2 = input("Enter customer id of the person who wishes to return the book: ")
    B_id4 = input("Enter book id to be returned: ")
    dor = input("Enter date like YYYY-MM-DD")

    st8 = "UPDATE RENTALS SET dor='{}' WHERE BOOKID='{}'".format(dor, B_id4)
    cursor.execute(st8)
    connect.commit()
    st9 = "UPDATE BOOKS SET QTY=QTY+1 WHERE BOOKID='{}'".format(B_id4)
    cursor.execute(st9)
    connect.commit()
    str10 = "SELECT DATEDIFF(dor, doi) FROM RENTALS WHERE BOOKID='{}' AND C_ID='{}'".format(B_id4, cID2)
    cursor.execute(str10)
    days = cursor.fetchone()
    if days is None:
        print('No data found.')
        return
    fine = 0
    if days[0] <= 15:
        price = days[0] * 5
    elif days[0] > 15:
        fine = (days[0] - 15) * 15
        price = fine + (15 * 5)
    st11 = "UPDATE RENTALS SET PRICE={} WHERE BOOKID='{}' AND C_ID='{}'".format(price, B_id4, cID2)
    cursor.execute(st11)
    connect.commit()
    print("\tBOOK RETURNED SUCCESSFULLY\nBILL")
    cursor.execute("SELECT C_ID, C_NAME, C_PNO, BOOKID, DOI, DOR, PRICE FROM RENTALS NATURAL JOIN C_DETAILS WHERE BOOKID='{}' AND C_ID='{}'".format(B_id4, cID2))
    bill = cursor.fetchone()
    if bill is None:
        print('No data found.')
        return
    List = ["CustomerID", "Customer NAME", "Phone NO.", "Book ID", "Date of Issue", "Date of returning", "Total Amount"]
    for i in range(7):
        print(List[i], "::-", bill[i])
    print("YOUR FINE was:", fine)


def signUP():
    cursor.execute("SELECT MAX(C_ID) FROM C_DETAILS")
    last_cid = cursor.fetchone()[0]
    cid = last_cid + 1 if last_cid else 1

    name = input("Enter Your Name: ")
    
    pno = input("Enter Your PHONE NO: ")
    if not pno.isdigit() or len(pno) != 10:
        print("Invalid phone number. It must be 10 digits.")
        return

    ad = input("Enter Your ADDRESS: ")

    try:
        pssd = int(input("CREATE A FOUR-DIGIT PASSWORD: "))
        if pssd < 1000 or pssd > 9999:
            print("Password must be exactly 4 digits.")
            return
    except ValueError:
        print("Invalid password input.")
        return

    cursor.execute("INSERT INTO C_DETAILS VALUES(%s, %s, %s, %s, %s)", (cid, name, pno, pssd, ad))
    connect.commit()

    print("\tYOUR DETAILS")
    print("Name:", name)
    print("PHONE no:", pno)
    print("Address:", ad)
    print("Customer ID:", cid)
    print("Password:", pssd)


def showRentedBooks():
    st10 = "SELECT BOOKS.BOOKID, BOOKS.BOOKNAME, BOOKS.AUTHOR, BOOKS.GENRE, RENTALS.C_ID, C_DETAILS.C_NAME, RENTALS.DOI FROM BOOKS INNER JOIN RENTALS ON BOOKS.BOOKID=RENTALS.BOOKID INNER JOIN C_DETAILS ON RENTALS.C_ID=C_DETAILS.C_ID WHERE RENTALS.DOR IS NULL"
    cursor.execute(st10)
    print(tabulate(cursor.fetchall(), ["BOOKID", "BOOKNAME", "AUTHOR", "GENRE", "C_ID", "C_NAME", "DOI"], tablefmt='grid'))
def showReturnedBooks():
    st11 = "SELECT BOOKS.BOOKID, BOOKS.BOOKNAME, BOOKS.AUTHOR, BOOKS.GENRE, RENTALS.C_ID, C_DETAILS.C_NAME, RENTALS.DOI, RENTALS.DOR, RENTALS.PRICE FROM BOOKS INNER JOIN RENTALS ON BOOKS.BOOKID=RENTALS.BOOKID INNER JOIN C_DETAILS ON RENTALS.C_ID=C_DETAILS.C_ID WHERE RENTALS.DOR IS NOT NULL"
    cursor.execute(st11)
    print(tabulate(cursor.fetchall(), ["BOOKID", "BOOKNAME", "AUTHOR", "GENRE", "C_ID", "C_NAME", "DOI", "DOR", "PRICE"], tablefmt='grid'))



while choice == 1:
    print("\tWELCOME TO LIBRARY")
    print("1. Login as ADMIN")
    print("2. Login as USER")
    print("3. Sign up as NEW USER")

    choice1 = int(input("Enter your choice: "))

    if choice1 == 1:
        if int(input("Enter the password: ")) == 2049:
            print("1. ADD book")
            print("2. DELETE book")
            print("3. MODIFY Quantity")
            print("4. ISSUE a book")
            print("5. RETURN a book")
            print("6. See currently rented books")
            print("7. See RETURNED books")

            achoice = int(input("ENTER your choice: "))

            if achoice == 1:
                addbook()
            elif achoice == 2:
                delBOOK()
            elif achoice == 3:
                modifyQTY()
            elif achoice == 4:
                issue()
            elif achoice == 5:
                Return()
            elif achoice == 6:
                showRentedBooks()
            elif achoice == 7:
                showReturnedBooks()
                
        else:
            print("Wrong password")

    elif choice1 == 2:
        i = int(input("Enter your customer id: "))
        cursor.execute("select C_PASS from C_DETAILS where C_ID={}".format(i))
        j = cursor.fetchone()
        if j is None:
            print('No data found.')
            continue
        if input("Enter Password: ") == j[0]:
            searchBOOK()
        else:
            print("Wrong Password")

    elif choice1 == 3:
        signUP()

    choice = int(input("ENTER 1 TO RUN PROGRAM AGAIN: "))
connect.close()

import pyodbc

def get_valid_integer():
    while True:
        try:
            num = int(input("Enter a valid integer: "))
            return num
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
	    
def sign_up_user(connection: pyodbc.Connection):
	username = input("Enter username: ")
	user_password = input("Enter password: ")
	email = input("Enter email: ")
	user_role = input("Enter user role: ")
	customer_ref = input("Enter customer reference: ")
	if customer_ref == "":
		customer_ref = None
	cursor = connection.cursor();
	cursor.execute("INSERT INTO Users (username, user_password, email, user_role, customer_ref) VALUES (?,?,?,?,?);",
		(username, user_password, email, user_role , customer_ref));
	cursor.commit()
	cursor.close()


def update_user(connection: pyodbc.Connection):
	#retrieve the user from database
	cursor = connection.cursor();
	username = input("Enter username: ")
	cursor.execute("SELECT username, user_password, email, user_role, customer_ref FROM Users WHERE username=?", (username));
	result = cursor.fetchone()
	if result == None:
		print("no such username")
		return
	user_password = input(f"Enter password({result[1]}): ")
	email = input(f"Enter email({result[2]}): ")
	user_role = input(f"Enter user role({result[3]}): ")
	customer_ref = input(f"Enter customer reference({result[4]}): ")
	if customer_ref == "":
		customer_ref = None
	cursor.execute("UPDATE Users SET user_password=?, email=?, user_role=?,customer_ref=? WHERE username=?",
		(user_password, email, user_role, customer_ref, username))
	cursor.commit();
	cursor.close()

def add_bank(connection: pyodbc.Connection):
  # create a new bank object with the provided details and insert it into the Banks table
	name = input("Enter bank name: ")
	cursor = connection.cursor()
	cursor.execute("INSERT INTO Banks(name) VALUES (?)",
		(name))
	cursor.commit();
	cursor.close()

def add_branch(connection: pyodbc.Connection):
  # create a new branch object with the provided details and insert it into the Branches table
	address = input("Enter branch address: ")
	cursor = connection.cursor()
	bank_code = input("Enter bank code: ")
	#check if bank exists
	cursor.execute("SELECT * FROM Banks WHERE bank_code=?",(bank_code))
	if not cursor.fetchone():
		print("no bank with that code")
		return
	cursor.execute("INSERT INTO Branches (address, bank_code) VALUES (?, ?)", (address, bank_code))
	cursor.commit()
	cursor.close()

def add_customer(connection: pyodbc.Connection):
  # create a new customer object with the provided details and insert it into the Customers table
	ssn = input("Enter customer SSN: ")
	name = input("Enter customer name: ")
	phone = input("Enter customer phone: ")
	branch_num = input("enter branch_num: ")
	cursor = connection.cursor()
	cursor.execute("INSERT INTO Customers (ssn, name, phone) VALUES (?,?,?)", (ssn, name, phone));
	cursor.execute("INSERT INTO Cust_Branch (customer_ssn, branch_num) VALUES (?,?)", (ssn, branch_num))
	cursor.commit()
	cursor.close()

def list_banks(connection : pyodbc.Connection):
	cursor = connection.cursor()
	cursor.execute("SELECT bank_code, name FROM Banks")
	for row in cursor.fetchall():
		print(row)
	cursor.close()
	
def list_loans(connection: pyodbc.Connection):
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM Loans")
	rows = cursor.fetchall()
	print([e[0] for e in cursor.description])
	for row in rows:
		print(row)
    

def list_customers(connection: pyodbc.Connection):
	# retrieve the list of Customer objects from the Customers table anddisplay their details
	cursor = connection.cursor()
	cursor.execute("SELECT ssn, name, phone FROM Customers")
	print([e[0] for e in cursor.description])

	for row in cursor.fetchall():
		print(row)

def list_loans_with_details(connection: pyodbc.Connection):
	# execute the SQL query to join the Loans, Customers, and Employees tables and select the columns of interest
	cursor = connection.cursor()
	cursor.execute("SELECT Loans.loan_num, Loans.loan_type, Loans.amount, Customers.name FROM Loans INNER JOIN Customers ON Loans.customer_ssn = Customers.ssn")
	# fetch the query results and print them
	print([e[0] for e in cursor.description])
	rows = cursor.fetchall()
	for row in rows:
		print(row)

def request_loan(connection: pyodbc.Connection):
  # create a new loan object with the provided details and insert it into the Loans table
	customer_id = input("Enter customer ID: ")
	branch_num = input("Enter branch number: ")
	loan_type = input("Enter loan type: ")
	loan_amount = input("Enter loan amount: ")
	cursor = connection.cursor()
	cursor.execute("INSERT INTO Loans (loan_type, amount, state,branch_num, customer_ssn) VALUES (?, ?, ?, ?, ?)",
		(loan_type, loan_amount, 'processing',branch_num, customer_id))
	cursor.commit()
	cursor.close()


def accept_loan(conn: pyodbc.Connection) -> None:
    # retrieve the Loan object corresponding to the provided loan number, update its status to "approved", and update the corresponding row in the Loans table
    loan_num = input("Enter loan number: ")
    cursor = conn.cursor()
    cursor.execute("SELECT loan_num, loan_type FROM Loans WHERE loan_num=?", (loan_num,))
    result = cursor.fetchone()
    if result is not None:
        cursor.execute("UPDATE Loans SET state=? WHERE loan_num=?", ('accepted', loan_num))
        conn.commit()
        print("Loan was accepted")
    else:
        print("Loan was not found")
    cursor.close()

def reject_loan(conn: pyodbc.Connection) -> None:
    # retrieve the Loan object corresponding to the provided loan number, update its status to "rejected", and update the corresponding row in the Loans table
    loan_num = input("Enter loan number: ")
    cursor = conn.cursor()
    cursor.execute("SELECT loan_num, loan_type FROM Loans WHERE loan_num=?", (loan_num,))
    result = cursor.fetchone()
    if result is not None:
        cursor.execute("UPDATE Loans SET state=? WHERE loan_num=?", ('rejected', loan_num))
        print("Loan was rejected")
        conn.commit()
    else:
        print("Loan was not found")
    cursor.close()

def pay_loan(conn: pyodbc.Connection) -> None:
    # retrieve the Loan object corresponding to the provided loan number, update its balance to 0, and update the corresponding row in the Loans table
    loan_num = input("Enter loan number: ")
    cursor = conn.cursor()
    cursor.execute("SELECT loan_num FROM Loans WHERE loan_num=?", (loan_num))
    result = cursor.fetchone()
    if result is not None:
        balance = result[1]
        if balance == 0:
            print("Loan has already been paid in full")
        else:
            cursor.execute("UPDATE Loans SET balance=?, state=? WHERE loan_num=?", (0,'payed', loan_num))
            conn.commit()
            print("Loan was paid in full")
    else:
        print("Loan was not found")
    cursor.close()
    
def add_account(connection: pyodbc.Connection):
	cursor = connection.cursor()
	account_type = input("account type: ")
	balance = input("balance: ")
	customer_ssn = input("enter customer ssn: ")
	#check if customer exists
	cursor.execute("SELECT * FROM Customers")
	if not cursor.fetchone():
		print("customer doesnt exist")
		return
	cursor.execute("INSERT INTO Accounts (customer_ssn, account_type, balance) VALUES (?,?,?)",
		(customer_ssn, account_type, balance))
	cursor.commit()
	cursor.close()

def list_accounts(connection: pyodbc.Connection):
	cursor = connection.cursor()
	cursor.execute("SELECT account_num, account_type, balance, customer_ssn FROM Accounts")
	print([e[0] for e in cursor.description])

	for row in cursor.fetchall():
		print(row)
def list_branches(connection: pyodbc.Connection):
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM Branches")
	print([e[0] for e in cursor.description])
	for row in cursor.fetchall():
		print (row)

def report(connection: pyodbc.Connection):
	cursor = connection.cursor()
	#select all banks, for each bank, list its branches
	cursor.execute("SELECT bank_code, name, address FROM Banks")
	for row in cursor.fetchall():
		print (f"branches of Bank:{ row[1]} with code {row[0]}")
		cursor2 = connection.cursor()
		cursor2.execute("SELECT branch_num, address FROM Branches WHERE bank_code=?",(row[0]))
		for branch in cursor2.fetchall():
			print(f'"{row[1]}" Branch, branch_num: {row[0]}')
		print()

	#sum of loans in each branch
	cursor.execute("SELECT b.branch_num, b.address, SUM(l.amount) as Sum FROM Branches as b, Loans as l WHERE b.branch_num=l.branch_num GROUP BY b.branch_num, b.address")
	print([e[0] for e in cursor.description])
	for row in cursor.fetchall():
		print(row)
# define the main menu
def main_menu(connection: pyodbc.Connection):
	while True:
		try:
			print("\nMAIN MENU")
			print("1. Sign up a new user")
			print("2. Update user details")
			print("3. Add bank") 
			print("4. Add bank branch")
			print("5. Add a customer")
			print("6. List loans")
			print("7. List customers")
			print("8. List loans with details")
			print("9. Request a loan")
			print("10. Accept a loan")
			print("11. Reject a loan")
			print("12. list banks")
			print("13. add account")
			print("14. list accounts")
			print("15. list branches")
			print("16. report")
			print("0. Exit")
			choice = input("Enter your choice: ")
			if choice == "0":
				break
			elif choice == "1":
				sign_up_user(connection)
			elif choice == "2":
				update_user(connection)
			elif choice== "3":
				add_bank(connection)
			elif choice == "4":
				add_branch(connection)
			elif choice == "5":
				add_customer(connection)
			elif choice == "6":
				list_loans(connection)
			elif choice == "7":
				list_customers(connection)
			elif choice == "8":
				list_loans_with_details(connection)
			elif choice == "9":
				request_loan(connection)
			elif choice == "10":
				accept_loan(connection)
			elif choice == "11":
				reject_loan(connection)
			elif choice == "12":
				list_banks(connection)
			elif choice == "13":
				add_account(connection)
			elif choice == "14":
				list_accounts(connection)
			elif choice == "15":
				list_branches(connection)
			elif choice == "16":
				report(connection)
			else:
				print("Invalid choice. Please try again.")
		except Exception as e:
			print(e)

def update_current_user(user, connection : pyodbc.Connection):
	cursor = connection.cursor();
	cursor.execute("SELECT username, user_password, email, user_role, customer_ref FROM Users WHERE username=?", (user.username));
	result = cursor.fetchone()
	if result == None:
		print("no such username")
		return
	user_password = input(f"Enter password({result[1]}): ")
	email = input(f"Enter email({result[2]}): ")
	user_role = result[3]
	customer_ref = input(f"Enter customer reference({result[4]}): ")
	if customer_ref == "":
		customer_ref = None
	cursor.execute("UPDATE Users SET user_password=?, email=?, user_role=?,customer_ref=? WHERE username=?",
		(user_password, email, user_role, customer_ref, user.username))
	cursor.commit();
	cursor.close()


def list_user_accounts(user, connection: pyodbc.Connection):
	cursor = connection.cursor()
	cursor.execute("SELECT account_num, account_type, balance FROM Accounts WHERE customer_ssn=?", (user.customer_ref))
	print([e[0] for e in cursor.description])
	for row in cursor.fetchall():
		print(row)
	cursor.close()
def customer_menu(user, connection: pyodbc.Connection):
	while True:
		print("\nMAIN MENU")
		print("1. Update user details")
		print("2. Request a loan")
		print("3. list my accounts")
		print("0. Exit")
		choice = input("Enter your choice: ")
		if choice == "0":
			break
		elif choice == "1":
			update_current_user(user, connection)
		elif choice == "2":
			request_loan(connection)
		elif choice == "3":
			list_user_accounts(user, connection)
		else:
			print("Invalid choice. Please try again.")

def employee_menu(user, connection: pyodbc.Connection):
	while True:
		print("\nMAIN MENU")
		print("1. Sign up a new user")
		print("2. Update user details")
		print("3. Add a customer")
		print("4. List loans")
		print("5. List customers")
		print("6. List loans with details")
		print("7. Accept a loan")
		print("8. Reject a loan")
		print("9. add account")
		print("10. list accounts")
		print("11. list branches")
		print("0. Exit")
		choice = input("Enter your choice: ")
		if choice == "0":
			break
		elif choice == "1":
			sign_up_user(connection)
		elif choice == "2":
			update_user(connection)
		elif choice== "3":
			add_customer(connection)
		elif choice == "4":
			list_loans(connection)
		elif choice == "5":
			list_customers(connection)
		elif choice == "6":
			list_loans_with_details(connection)
		elif choice == "7":
			accept_loan(connection)
		elif choice == "8":
			reject_loan(connection)
		elif choice == "9":
			add_account(connection)
		elif choice == "10":
			list_accounts(connection)
		elif choice == "11":
			list_branches(connection)
		else:
			print("Invalid choice. Please try again.")

import pyodbc
from database.models import *
from main import main_menu, customer_menu, employee_menu
#execute the sql script before running the program
def create_connection():
	server = 'LAPTOP-UMDT6K0S' #change this to be your server
	database = 'Bank_Database' 
	return pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
def login_prompt(connection: pyodbc.Connection):
	cursor = connection.cursor()
	while True:
		username = input("enter username:")
		password = input("enter password:")
		cursor.execute("SELECT username, user_password, email, user_role, customer_ref FROM Users WHERE username=?", (username));
		result = cursor.fetchone()
		if username == password == "admin":
			return User(username, password, None, 'admin', None)
		if result == None:
			print("no such username")
			continue
		if result[1] != password:
			print("username and password does not match")
			continue
		return User(result[0], result[1], result[2], result[3], result[4])
	
if __name__ == "__main__":
	sqlconnection = create_connection()
	user = login_prompt(sqlconnection)
	if user.user_role == "customer":
		customer_menu(user, sqlconnection)
	elif user.user_role == "employee":
		employee_menu(user, sqlconnection)
	elif user.user_role == "admin":
		main_menu(sqlconnection)
	sqlconnection.close()
	print("closing")

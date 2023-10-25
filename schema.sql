IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'Bank_Database')
BEGIN
    CREATE DATABASE database_name;
END
Go
USE Bank_Database;
Go

IF NOT EXISTS(SELECT * FROM sys.tables WHERE name = 'Banks')
BEGIN
CREATE TABLE Banks (
  bank_code INT PRIMARY KEY IDENTITY(1,1),
  name VARCHAR(255),
  address VARCHAR(255)
);
END
Go
IF NOT EXISTS(SELECT * FROM sys.tables WHERE name = 'Branches')
BEGIN
	CREATE TABLE Branches (
	  branch_num INT PRIMARY KEY IDENTITY(1,1),
	  address VARCHAR(255),
	  bank_code INT,
	  FOREIGN KEY (bank_code) REFERENCES Banks(bank_code)
	);
END
Go

IF NOT EXISTS(SELECT * FROM sys.tables WHERE name = 'Customers')
BEGIN
CREATE TABLE Customers (
  ssn INT PRIMARY KEY,
  name VARCHAR(255),
  phone VARCHAR(255)
);
END
Go
IF NOT EXISTS(SELECT * FROM sys.tables WHERE name = 'Accounts')
BEGIN
CREATE TABLE Accounts (
  account_num INT PRIMARY KEY IDENTITY(1,1),
  account_type VARCHAR(255),
  balance DECIMAL,
  customer_ssn INT,
  FOREIGN KEY (customer_ssn) REFERENCES Customers(ssn)
);
END
go
IF NOT EXISTS(SELECT * FROM sys.tables WHERE name = 'Loans')
BEGIN
CREATE TABLE Loans (
  loan_num INT PRIMARY KEY IDENTITY(1,1),
  loan_type VARCHAR(255),
  amount DECIMAL,
  [state] VARCHAR(255),
  branch_num INT,
  customer_ssn INT,
  FOREIGN KEY (customer_ssn) REFERENCES Customers(ssn),
  FOREIGN KEY (branch_num) REFERENCES Branches(branch_num)
);
END
go
IF NOT EXISTS(SELECT * FROM sys.tables WHERE name = 'Users')
BEGIN
CREATE TABLE Users (
  username VARCHAR(255) PRIMARY KEY,
  user_password VARCHAR(255),
  email VARCHAR(255),
  user_role varchar(255),
  customer_ref INT,
  FOREIGN KEY (customer_ref) REFERENCES Customers(ssn)
);
END
Go
IF NOT EXISTS(SELECT * FROM sys.tables WHERE name = 'Cust_Branch')
BEGIN
CREATE TABLE Cust_Branch (
  customer_ssn INT,
  branch_num INT,
  FOREIGN KEY (customer_ssn) REFERENCES Customers(ssn),
  FOREIGN KEY (branch_num) REFERENCES Branches(branch_num)
);
END
Go

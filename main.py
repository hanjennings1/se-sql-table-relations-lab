# STEP 0 - SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

#finding column names:
# print(pd.read_sql("""SELECT * FROM sqlite_master""", conn))
# print(pd.read_sql("""PRAGMA table_info(products)""", conn))
# print (" ")
# print (" ")
# print(pd.read_sql("""PRAGMA table_info(orderDetails)""", conn))
# print (" ")
# print (" ")
# print(pd.read_sql("""PRAGMA table_info(orders)""", conn))
# print (" ")
# print (" ")
# print(pd.read_sql("""PRAGMA table_info(customers)""", conn))

# STEP 1 - Return the first and last names and the job titles for all employees in Boston
# (Instructions say jobTitle but Test is for firstName lastName only ?)
df_boston = pd.read_sql("""
    SELECT firstName, lastName
    FROM employees
    JOIN offices ON offices.officeCode = employees.officeCode
    WHERE city = 'Boston'
""", conn)
# print(df_boston)


# STEP 2 - Are there any offices that have zero employees?
df_zero_emp = pd.read_sql("""
    SELECT offices.officeCode
    FROM offices
    LEFT JOIN employees ON employees.officeCode  = offices.officeCode
    WHERE employees.employeeNumber IS NULL
""", conn)
# print(df_zero_emp)


# STEP 3 - Return the employees first name and last name along with the city and state of the 
# office that they work out of (if they have one). 
# Include all employees and order them by their first name, then their last name.
df_employee = pd.read_sql("""
    SELECT firstName, lastName, city, state
    FROM employees
    LEFT JOIN offices ON offices.officeCode = employees.officeCode
    ORDER BY firstName ASC, lastName ASC
""", conn)
# print(df_employee)


# STEP 4 - Return all of the customer's contact information (first name, last name, and phone number) 
# as well as their sales rep's employee number for any customer that has not placed an order. 
# Sort the results alphabetically based on the contact's last name
df_contacts = pd.read_sql("""
    SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber
    FROM customers
    LEFT JOIN orders ON orders.customerNumber = customers.customerNumber
    WHERE orders.orderNumber IS NULL
    ORDER BY contactLastName
""", conn)
# print(df_contacts)


# STEP 5 - report of all the customer contacts (first and last names) along with details for 
# each of the customers' payment amounts and date of payment. 
# Sorted in descending order by the payment amount
df_payment = pd.read_sql("""
    SELECT contactFirstName, contactLastName, amount, paymentDate
    FROM customers
    JOIN payments ON payments.customerNumber = customers.customerNumber
    ORDER BY CAST(amount AS REAL) DESC
""", conn)
# print(df_payment)


# STEP 6 - Top 4 individuals; Return the employee number, first name, last name, and number of customers for 
# employees whose customers have an average credit limit over 90k. 
# Sort by number of customers from high to low.
df_credit = pd.read_sql("""
    SELECT employees.employeeNumber, firstName, lastName, COUNT(customerNumber) AS num_customers
    FROM employees
    JOIN customers ON customers.salesRepEmployeeNumber = employees.employeeNumber
    GROUP BY employees.employeeNumber
    HAVING AVG(creditLimit) > 90000
    ORDER BY num_customers DESC
""", conn)
# print(df_credit)

# STEP 7 - Return the product name and count the number of orders for each product as a column named 'numorders'. 
#  Also return a new column, 'totalunits', that sums up the total quantity of product sold (use the quantityOrdered column).
# Sort the results by the totalunits column, highest to lowest, to showcase the top selling products.
df_product_sold = pd.read_sql("""
    SELECT productName, COUNT(orderNumber) AS numorders, SUM(quantityOrdered) AS totalunits
    FROM products
    JOIN orderDetails ON products.productCode = orderDetails.productCode
    GROUP BY productName
    ORDER BY totalunits DESC
""", conn)
# print(df_product_sold)

# STEP 8 - Return the product name, code, and the total number of customers who have ordered each product, aliased as 'numpurchasers'. 
# Sort the results by the highest number of purchasers.
df_total_customers = pd.read_sql("""
    SELECT productName, products.productCode, COUNT(DISTINCT customers.customerNumber) AS numpurchasers
    FROM products
    JOIN orderdetails ON products.productCode = orderdetails.productCode
    JOIN orders ON orderdetails.orderNumber = orders.orderNumber
    JOIN customers ON orders.customerNumber = customers.customerNumber
    GROUP BY products.productCode
    ORDER BY numpurchasers DESC
""", conn)
# print(df_total_customers)


# STEP 9 - Return the count as a column named 'n_customers'. 
# Also return the office code and city.
df_customers = pd.read_sql("""
    SELECT offices.officeCode, offices.city, COUNT(DISTINCT customers.customerNumber) AS n_customers
    FROM offices
    JOIN employees ON offices.officeCode = employees.officeCode
    JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY offices.officeCode
""", conn)
# print(df_customers)


# STEP 10 - Using a subquery or common table expression (CTE), 
# select the employee number, first name, last name, city of the office, and 
# the office code for employees who sold products that have been ordered by fewer than 20 customers.
df_under_20 = pd.read_sql("""
    SELECT DISTINCT employees.employeeNumber, firstName, lastName, offices.city, offices.officeCode
    FROM employees
    JOIN offices ON employees.officeCode = offices.officeCode
    JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
    JOIN orders ON customers.customerNumber = orders.customerNumber
    JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
        WHERE orderDetails.productCode IN (
            SELECT products.productCode
            FROM products
            JOIN orderdetails ON products.productCode = orderdetails.productCode
            JOIN orders ON orderdetails.orderNumber = orders.orderNumber
            JOIN customers ON orders.customerNumber = customers.customerNumber
            GROUP BY products.productCode
            HAVING COUNT(DISTINCT customers.customerNumber) < 20
            )
    ORDER BY lastName
        """, conn)
print(df_under_20)


conn.close()
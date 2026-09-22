# Lab: SQL Table Relations
**Completed Sept 22, 2026**

## Introduction

This lab practices writing SQL `JOIN` statements and subqueries against the Northwind CRM database, which tracks customers, employees, offices, orders, and products. Working in a sales rep support role, the goal was to answer a series of business questions by querying across related tables.
 
## Learning Objectives
 
- Write SQL queries using various types of joins
- Choose the right join type for the data being retrieved
- Write subqueries to decompose complex queries
## Status
 
All 10 steps complete. Full test suite passes:
 
```
pytest -x
======================== 6 passed ========================
```
 
## Set Up
 
- Fork and clone the repo
- `pipenv install`
- `pipenv shell`
Run `python3 main.py` to see query output. Run `pytest` or `pytest -x` to check correctness.
 
## Solution Summary
 
**Step 1 → Boston employees:** `INNER JOIN employees` to `offices` on `officeCode`, filtered to `city = 'Boston'`.
 
**Step 2 → Offices with zero employees:** `LEFT JOIN offices` to `employees`, checked for `NULL` employee matches. Result: none found.
 
**Step 3 → Full employee report:** `LEFT JOIN employees` to `offices` so employees without an office are still included. Sorted by first, then last name.
 
**Step 4 → Customers with no orders:** `LEFT JOIN customers` to `orders`, filtered `WHERE orders.orderNumber IS NULL`. Sorted by last name.
 
**Step 5 → Customer payments:** Joined `customers` to `payments`. Used `CAST(amount AS REAL)` since `amount` is stored as text and would otherwise sort incorrectly.
 
**Step 6 → High-value customer reps:** Grouped `employees` by rep, used `HAVING AVG(creditLimit) > 90000` (filters after aggregation, unlike `WHERE`).
 
**Step 7 → Top-selling products:** Grouped `products` joined to `orderdetails`, calculated `numorders` and `totalunits`, sorted by units descending.
 
**Step 8 → Unique purchasers per product:** Chained `products → orderdetails → orders → customers`, used `COUNT(DISTINCT customerNumber)`.
 
**Step 9 → Customers per office:** Chained `offices → employees → customers`, since offices don't link to customers directly.
 
**Step 10 → Employees selling underperforming products:** Reused Step 8's logic as a subquery (products with < 20 purchasers), joined through to `employees`, used `DISTINCT` to remove duplicate rows, sorted by last name.
 
## Key Takeaways
 
- Ambiguous column errors: qualify with `table.column` whenever a name exists in multiple joined tables.
- `LEFT JOIN` + `IS NULL`: the standard pattern for finding "no match" cases.
- `HAVING` filters after grouping; `WHERE` filters before.
- No shared column between two tables - look for a linking table.
- Build subqueries in isolation first, then nest them.
- No `ORDER BY` - row order isn't guaranteed.

 



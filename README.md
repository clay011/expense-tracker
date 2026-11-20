# Expense Tracker

A web app to track personal expenses, built with Django.

## Features
- User signup, login and logout
- Add, edit and delete expenses
- Dashboard with total spent
- Pie chart (by category) and bar chart (by month) using Chart.js
- Pandas used to calculate category and monthly totals
- Export expenses to CSV

## Tech Stack
Python, Django, Pandas, HTML, CSS, JavaScript (Chart.js), SQLite

## How to Run
1. Clone the repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install packages: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`
7. Open http://127.0.0.1:8000
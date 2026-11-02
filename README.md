# 💰 QashFlow: Premium Personal Expense Tracker

QashFlow is a full-stack, secure, multi-user web application designed to help users track their daily expenses, manage monthly budgets, and visualize their financial health. Built with a robust Python backend and a modern, responsive frontend, it provides a seamless and premium user experience.

## ✨ Key Features

*   **🔐 Secure Authentication:** Multi-user support with securely hashed passwords (using Werkzeug).
*   **📊 Interactive Dashboard:** A beautifully designed, responsive UI featuring a bright, clean white theme with an accounting-desk background image.
*   **💸 Income & Expense Tracking:** Categorize transactions (Food, Travel, Bills, Salary, etc.) and track them with custom iconography.
*   **🎯 Monthly Budgeting:** Set custom budgets for specific months. The app visually tracks your progress with dynamic progress bars (Green → Yellow → Red) based on your spending limits.
*   **📈 Data Visualization:** Real-time Doughnut charts powered by Chart.js that automatically calculate and display your expense breakdown by category.
*   **🤖 Automated Backups:** A background task scheduler (`schedule`) that automatically exports your data to a CSV file daily without any manual intervention.
*   **🔒 REST API Backend:** Fully decoupled backend using Flask REST API endpoints, allowing data to be accessed securely via HTTP requests.

## 🛠️ Tech Stack

*   **Backend:** Python 3, Flask, Flask-CORS
*   **Database:** SQLite3 (Serverless)
*   **Frontend:** HTML5, CSS3, Vanilla JavaScript
*   **Libraries & Tools:** Chart.js (Data Visualization), FontAwesome (Icons), Google Fonts (Inter), Werkzeug (Security), Schedule (Task Automation)

## 📂 Project Structure

```text
Personal_Expense_Tracker/
│
├── app.py                 # Main Flask server and REST API routes
├── database.py            # SQLite database initialization and CRUD logic
├── automation.py          # Background task scheduler for daily CSV backups
├── login.html             # Beautiful split-screen login/signup page
├── dashboard.html         # Main frontend UI with charts and data tables
├── expenses.db            # SQLite database (auto-generated on first run)
└── requirements.txt       # Project dependencies

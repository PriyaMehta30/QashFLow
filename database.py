import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "expenses.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Create Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        
        # 2. Create Expenses Table (Linked to user)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount REAL NOT NULL,
                type TEXT DEFAULT 'Expense',
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # 3. Create Budgets Table (Linked to user)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                month_year TEXT NOT NULL,
                amount REAL NOT NULL,
                UNIQUE(user_id, month_year),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()

# --- USER AUTHENTICATION ---
def create_user(username, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        hashed_pw = generate_password_hash(password)
        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False 

def verify_user(username, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row and check_password_hash(row[1], password):
            return row[0] 
    return None

# --- TRANSACTIONS ---
def add_transaction(user_id, date, category, description, amount, trans_type):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (user_id, date, category, description, amount, type) VALUES (?, ?, ?, ?, ?, ?)",
                       (user_id, date, category, description, amount, trans_type))
        conn.commit()

def get_all_transactions(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, category, description, amount, type FROM expenses WHERE user_id = ? ORDER BY date DESC", (user_id,))
        return cursor.fetchall()

def delete_transaction(user_id, trans_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (trans_id, user_id))
        conn.commit()
        return cursor.rowcount > 0

# --- BUDGETS ---
def set_budget(user_id, month_year, amount):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM budgets WHERE user_id = ? AND month_year = ?", (user_id, month_year))
        if cursor.fetchone():
            cursor.execute("UPDATE budgets SET amount = ? WHERE user_id = ? AND month_year = ?", (amount, user_id, month_year))
        else:
            cursor.execute("INSERT INTO budgets (user_id, month_year, amount) VALUES (?, ?, ?)", (user_id, month_year, amount))
        conn.commit()

def get_budget(user_id, month_year):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM budgets WHERE user_id = ? AND month_year = ?", (user_id, month_year))
        row = cursor.fetchone()
        return row[0] if row else 0.0
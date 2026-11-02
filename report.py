import csv
import sqlite3
from database import DB_NAME

def generate_summary():
    """Fetches category-wise totals from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        return cursor.fetchall()

def export_to_csv(filename="expenses_export.csv"):
    """Exports all data to a CSV file."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses ORDER BY date")
        rows = cursor.fetchall()
        
        if not rows:
            return False

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Category", "Description", "Amount"])
            writer.writerows(rows)
        return True
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import database
import report

def refresh_table():
    """Clears and reloads data into the table."""
    for row in tree.get_children():
        tree.delete(row)
    
    expenses = database.get_all_expenses()
    for exp in expenses:
        tree.insert("", tk.END, values=exp)

def add_expense_gui():
    """Handles the Add Expense button click."""
    date = entry_date.get()
    cat = entry_cat.get()
    desc = entry_desc.get()
    amt_str = entry_amt.get()

    if not date or not cat or not amt_str:
        messagebox.showerror("Error", "Date, Category, and Amount are required!")
        return

    try:
        amt = float(amt_str)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a valid number!")
        return

    database.add_expense(date, cat, desc, amt)
    messagebox.showinfo("Success", "Expense Added Successfully!")
    refresh_table()
    
    # Clear input fields
    entry_desc.delete(0, tk.END)
    entry_amt.delete(0, tk.END)

def delete_expense_gui():
    """Handles the Delete Expense button click."""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select an expense from the table first.")
        return

    # Get the ID of the selected row
    item = tree.item(selected[0])
    exp_id = item['values'][0]

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?")
    if confirm:
        if database.delete_expense(exp_id):
            messagebox.showinfo("Deleted", "Expense deleted.")
            refresh_table()

def export_gui():
    """Handles the Export button click."""
    if report.export_to_csv():
        messagebox.showinfo("Exported", "Data exported successfully to expenses_export.csv")
    else:
        messagebox.showwarning("Empty", "No data to export.")

# --- UI SETUP ---
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("700x500")

# Initialize DB
database.initialize_database()

# --- INPUT FRAME ---
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(fill="x")

tk.Label(input_frame, text="Date:").grid(row=0, column=0, padx=5, pady=5)
entry_date = tk.Entry(input_frame, width=12)
entry_date.insert(0, "2026-11-02") # Default date
entry_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
entry_cat = tk.Entry(input_frame, width=15)
entry_cat.grid(row=0, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Amount (₹):").grid(row=0, column=4, padx=5, pady=5)
entry_amt = tk.Entry(input_frame, width=10)
entry_amt.grid(row=0, column=5, padx=5, pady=5)

tk.Label(input_frame, text="Description:").grid(row=0, column=6, padx=5, pady=5)
entry_desc = tk.Entry(input_frame, width=20)
entry_desc.grid(row=0, column=7, padx=5, pady=5)

# --- BUTTONS FRAME ---
btn_frame = tk.Frame(root, pady=5)
btn_frame.pack()

btn_add = tk.Button(btn_frame, text="➕ Add Expense", command=add_expense_gui, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_add.grid(row=0, column=0, padx=10)

btn_del = tk.Button(btn_frame, text="🗑️ Delete Selected", command=delete_expense_gui, bg="#F44336", fg="white", font=("Arial", 10, "bold"))
btn_del.grid(row=0, column=1, padx=10)

btn_exp = tk.Button(btn_frame, text="📁 Export CSV", command=export_gui, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
btn_exp.grid(row=0, column=2, padx=10)

# --- TABLE (TREEVIEW) ---
columns = ("ID", "Date", "Category", "Description", "Amount")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

tree.heading("ID", text="ID")
tree.heading("Date", text="Date")
tree.heading("Category", text="Category")
tree.heading("Description", text="Description")
tree.heading("Amount", text="Amount (₹)")

tree.column("ID", width=40, anchor="center")
tree.column("Date", width=100, anchor="center")
tree.column("Category", width=100)
tree.column("Description", width=250)
tree.column("Amount", width=100, anchor="e")

tree.pack(pady=10, fill="both", expand=True)

# Initial data load
refresh_table()

# Run the app
root.mainloop()
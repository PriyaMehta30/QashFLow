from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- This allows the HTML to talk to Python
import database
import report

app = Flask(__name__)
CORS(app)  # <-- Enabling it here

# Initialize DB on startup
database.initialize_database()

# 1. GET - Fetch all expenses
@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    expenses = database.get_all_expenses()
    result = []
    for exp in expenses:
        result.append({
            "id": exp[0],
            "date": exp[1],
            "category": exp[2],
            "description": exp[3],
            "amount": exp[4]
        })
    return jsonify(result), 200

# 2. POST - Add a new expense
@app.route('/api/expenses', methods=['POST'])
def add_expense_api():
    data = request.get_json()
    if not data or 'date' not in data or 'category' not in data or 'amount' not in data:
        return jsonify({"error": "Missing required fields"}), 400
        
    try:
        database.add_expense(
            data['date'], 
            data['category'], 
            data.get('description', ''), 
            float(data['amount'])
        )
        return jsonify({"message": "Expense added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. DELETE - Remove an expense by ID
@app.route('/api/expenses/<int:exp_id>', methods=['DELETE'])
def delete_expense_api(exp_id):
    if database.delete_expense(exp_id):
        return jsonify({"message": f"Expense {exp_id} deleted"}), 200
    else:
        return jsonify({"error": "Expense not found"}), 404

# 4. GET - Category Summary
@app.route('/api/summary', methods=['GET'])
def get_summary():
    summary = report.generate_summary()
    result = [{"category": row[0], "total": row[1]} for row in summary]
    return jsonify(result), 200

if __name__ == '__main__':
    print("🌐 Starting REST API Server on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
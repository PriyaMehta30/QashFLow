from flask import Flask, request, jsonify, session
import database
import os

app = Flask(__name__)
app.secret_key = "super_secret_mca_project_key_123"
database.initialize_database()

# --- AUTHENTICATION API ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = database.verify_user(data.get('username'), data.get('password'))
    if user_id:
        session['user_id'] = user_id
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if database.create_user(data.get('username'), data.get('password')):
        return jsonify({"message": "User created successfully"}), 201
    return jsonify({"error": "Username already exists"}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

# --- MAIN DASHBOARD ROUTE ---
@app.route('/')
def serve_dashboard():
    if 'user_id' not in session:
        if os.path.exists('login.html'):
            with open('login.html', 'r', encoding='utf-8') as f:
                return f.read()
        return "Please create login.html"
    
    if os.path.exists('dashboard.html'):
        with open('dashboard.html', 'r', encoding='utf-8') as f:
            return f.read()
    return "Error: dashboard.html not found."

# --- SECURE TRANSACTION API ---
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    rows = database.get_all_transactions(session['user_id'])
    return jsonify([{"id": r[0], "date": r[1], "category": r[2], "description": r[3], "amount": r[4], "type": r[5]} for r in rows]), 200

@app.route('/api/transactions', methods=['POST'])
def add_transaction_api():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    try:
        database.add_transaction(session['user_id'], data['date'], data['category'], data.get('description', ''), float(data['amount']), data.get('type', 'Expense'))
        return jsonify({"message": "Added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/transactions/<int:trans_id>', methods=['DELETE'])
def delete_transaction_api(trans_id):
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    if database.delete_transaction(session['user_id'], trans_id):
        return jsonify({"message": "Deleted"}), 200
    return jsonify({"error": "Not found"}), 404

# --- SECURE BUDGET API ---
@app.route('/api/budget', methods=['POST'])
def set_budget_api():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    database.set_budget(session['user_id'], data.get('month_year'), float(data.get('amount')))
    return jsonify({"message": "Budget updated"}), 200

@app.route('/api/budget/<month_year>', methods=['GET'])
def get_budget_api(month_year):
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    amount = database.get_budget(session['user_id'], month_year)
    return jsonify({"month_year": month_year, "amount": amount}), 200

if __name__ == '__main__':
    print("🌐 Server running at http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)
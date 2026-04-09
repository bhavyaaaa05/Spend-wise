from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from database import (
    init_db,
    get_all_expenses,
    add_expense,
    delete_expense,
    get_budgets,
    update_budget
)

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/expenses", methods=["GET"])
def expenses_get():
    return jsonify(get_all_expenses())

@app.route("/api/expenses", methods=["POST"])
def expenses_post():
    data = request.json

    # ✅ Future date validation
    today = datetime.today().strftime('%Y-%m-%d')
    if data["date"] > today:
        return jsonify({"error": "Future date not allowed"}), 400

    add_expense(
        float(data["amount"]),
        data["note"],
        data["category"],
        data["date"]
    )
    return jsonify({"status": "ok"}), 201

@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def expenses_delete(expense_id):
    delete_expense(expense_id)
    return jsonify({"status": "ok"})

@app.route("/api/budgets", methods=["GET"])
def budgets_get():
    return jsonify(get_budgets())

@app.route("/api/budgets", methods=["POST"])
def budgets_post():
    data = request.json
    update_budget(data["category"], float(data["amount"]))
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)

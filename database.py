import sqlite3

DB = "spendwise/spendwise.db"

def get_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            amount    REAL    NOT NULL,
            note      TEXT    NOT NULL,
            category  TEXT    NOT NULL,
            date      TEXT    NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            category  TEXT PRIMARY KEY,
            amount    REAL NOT NULL
        )
    """)
    for cat, amt in [("Food",3000),("Travel",2000),("Bills",2500),("Other",1500)]:
        conn.execute(
            "INSERT OR IGNORE INTO budgets (category, amount) VALUES (?,?)",
            (cat, amt)
        )
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_expense(amount, note, category, date):
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (amount, note, category, date) VALUES (?,?,?,?)",
        (amount, note, category, date)
    )
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

def get_budgets():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM budgets").fetchall()
    conn.close()
    return {r["category"]: r["amount"] for r in rows}

def update_budget(category, amount):
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO budgets (category, amount) VALUES (?,?)",
        (category, amount)
    )
    conn.commit()
    conn.close()

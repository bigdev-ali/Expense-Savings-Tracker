import sqlite3 #loads python's built in sql library 
from projections import Transaction
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).parent / "tracker.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS months (
    month TEXT PRIMARY KEY,
    starting_amount INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (kind IN ('expense', 'saving')),
    amount INTEGER NOT NULL CHECK (amount > 0),
    one_off INTEGER NOT NULL DEFAULT 0,
    note TEXT
);
""" #triple quotes let a string span many lines
#creates a table months,month is a primary key meanings unique value always,start amount is self explanatory
#then creates another table if it does not exists of transactions, a autoincrementing unique id, a day ,a kind which can only have two values, two integer values and a text one which is optional
def connect(path=DB_PATH): #takes a file name if you didnt give it
    conn = sqlite3.connect(path) #opens the database file and creates it if it does not exist
    conn.row_factory = sqlite3.Row # = makes row accessible by column name
    conn.executescript(SCHEMA) #runs all SQL in schema builds tables
    return conn #hands the connection back so code can use it

def set_starting_amount(conn, month, amount):
    conn.execute(
        "INSERT INTO months (month, starting_amount) VALUES (?, ?) "#the question marks represent placeholders
        "ON CONFLICT(month) DO UPDATE SET starting_amount = excluded.starting_amount", #this fixes the crash as if a month already exists it fixes and updates the starting amount instead of failing
        (month, amount),
    )
    conn.commit()


def add_transaction(conn, day, kind, amount, one_off=False, note=None):
    conn.execute(
        "INSERT INTO transactions (day, kind, amount, one_off, note) "
        "VALUES (?, ?, ?, ?, ?)",
        (day.isoformat(), kind, amount, int(one_off), note), #formatting the date with isoformaat and since sqlite does not have true/false convert one off into int
    )
    conn.commit()

def load_month(conn, month):
    row = conn.execute(
        "SELECT starting_amount FROM months WHERE month = ?", (month,)
    ).fetchone() #this takes in one row only and if there is not one row then it raises an error
    if row is None:
        raise KeyError(f"no starting amount set for {month}")

    rows = conn.execute(
        "SELECT day, kind, amount, one_off FROM transactions "
        "WHERE day LIKE ? ORDER BY day",
        (month + "-%",), #% is like a wildcard it is remains irrespective of the value in this way a month's days can be displayed in order easily
    ).fetchall()

    txns = [
        Transaction(date.fromisoformat(r["day"]), r["kind"], r["amount"], bool(r["one_off"]))
        for r in rows #from sqlite convert to readable format
    ]
    return row["starting_amount"], txns #starting amount and list of transactions


import sqlite3 #loads python's built in sql library 

SCHEMA = """
CREATE TABLE IF NOT EXISTS months (
    month TEXT PRIMARY KEY,
    start_amount INTEGER NOT NULL
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
def connect(path="tracker.db"): #takes a file name if you didnt give it
    conn = sqlite3.connect(path) #opens the database file and creates it if it does not exist
    conn.row_factory = sqlite3.Row # = makes row accessible by column name
    conn.executescript(SCHEMA) #runs all SQL in schema builds tables
    return conn #hands the connection back so code can use it
import os, sqlite3

print(os.path.abspath("tracker.db"))
conn = sqlite3.connect("tracker.db")
print(conn.execute("PRAGMA table_info(months)").fetchall()) #helps debug all contents of the database
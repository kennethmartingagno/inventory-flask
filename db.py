import sqlite3

conn = sqlite3.connect("storage.db")

cur = conn.cursor()

conn.execute("PRAGMA FOREIGN_KEYS = 1")

conn.execute("""CREATE TABLE Sales (
	transaction_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
	code_id INTEGER PRIMARY KEY
)""")

conn.execute("""CREATE TABLE Coffee (
	size TEXT NOT NULL,
	type TEXT NOT NULL,
	quantity INTEGER NOT NULL,
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	code_id INTEGER,
	FOREIGN KEY (code_id) REFERENCES Sales (code_id)
)""")

conn.execute("""CREATE TABLE Inventory (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	size TEXT NOT NULL,
	type TEXT NOT NULL,
	quantity INTEGER NOT NULL
)""")

conn.execute("""CREATE TABLE Users (
	username TEXT,
	password TEXT
)""")

conn.close()
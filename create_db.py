import sqlite3

conn = sqlite3.connect('signup.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
print("Database and table created.")

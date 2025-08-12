import sqlite3

conn = sqlite3.connect('complaints.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mobile TEXT,
    department TEXT,
    complaint TEXT
)
''')

conn.commit()
conn.close()

print("Database and table created successfully!")
import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Drop the existing 'predictions' table if it exists
cursor.execute('''
    DROP TABLE IF EXISTS predictions;
''')

# Create the table with the correct schema
cursor.execute('''
    CREATE TABLE predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        N REAL,
        P REAL,
        K REAL,
        temperature REAL,
        humidity REAL,
        ph REAL,
        rainfall REAL,
        prediction TEXT
    )
''')

print("Table 'predictions' created successfully with all necessary columns.")

# Commit the changes and close the connection
conn.commit()
conn.close()

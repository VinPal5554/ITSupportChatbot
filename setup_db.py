import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('decision_tree.db')
cursor = conn.cursor()

# Create the decision tree table
cursor.execute('''CREATE TABLE IF NOT EXISTS decision_tree (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    question TEXT,
    yes_response TEXT,
    no_response TEXT
)''')

# Insert sample questions (corrected format)
data = [
    ('network', 'Have you restarted your router?', '2', 'Suggest restart'),
    ('network', 'Are other devices affected?', 'Contact ISP', '3'),
    ('network', 'Have you updated your drivers?', 'Next step', 'Suggest update'),
    ('microsoft', 'Are you facing issues with Office?', '5', 'Move to another category'),
    ('microsoft', 'Have you checked for updates?', 'Suggest update', '6')
]

cursor.executemany('''INSERT INTO decision_tree (category, question, yes_response, no_response) 
                      VALUES (?, ?, ?, ?)''', data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("database setup successfully")
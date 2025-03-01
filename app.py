from flask import Flask, request, jsonify, render_template
import datetime
import sqlite3

conn = sqlite3.connect('database.db')  # Creates database file
cursor = conn.cursor()

# Create table for IT support tickets
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        issue TEXT,
        status TEXT,
        timestamp TEXT
    )
''')

conn.commit()
conn.close()
print("Database initialized successfully!")


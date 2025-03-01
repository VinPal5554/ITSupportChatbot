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

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']

    # Here you would add logic to handle the user's issue.
    if 'wifi' in user_input.lower():
        response = "Have you tried restarting your router?"
    elif 'slow' in user_input.lower():
        response = "Have you tried clearing your browser cache?"
    else:
        response = "Sorry, I couldn't find a solution for that."

    return render_template('index.html', response=response)


if __name__ == '__main__':
    app.run(debug=True)


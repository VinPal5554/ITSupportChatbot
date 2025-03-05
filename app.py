from flask import Flask, request, render_template, session
import sqlite3
import os

app = Flask(__name__)

# Setting a secret key (random key for production)
app.secret_key = os.urandom(24)  # Generates a 24-byte random secret key

# Basic categories
CATEGORIES = {
    "network": ["wifi", "internet", "router", "ethernet"],
    "microsoft": ["office", "outlook", "windows", "word", "excel"],
    "installation": ["install", "setup", "error", "update"],
    "slow": ["slow", "lag", "freezing", "performance"],
    "peripheral": ["keyboard", "mouse", "monitor", "printer"],
    "storage": ["hard drive", "ssd", "usb", "storage"],
    "security": ["antivirus", "firewall", "hacked", "malware"]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']  # Get user input from form

    # Use predefined categories to match user input
    category = "unknown"
    for cat, keywords in CATEGORIES.items():
        if any(keyword in user_input.lower() for keyword in keywords):
            category = cat
            break  # Once a match is found, stop searching further

    # Store the category in session
    session['category'] = category

    conn = sqlite3.connect('decision_tree.db')
    cursor = conn.cursor()

    # Fetch the first question for the identified category from the database
    cursor.execute("SELECT id, question FROM decision_tree WHERE category = ? LIMIT 1", (category,))
    row = cursor.fetchone()
    conn.close()

    if row:
        question_id, question = row
        # Store the current question ID in session
        session['question_id'] = question_id

        # Initialize the conversation history if it doesn't exist
        if 'conversation_history' not in session:
            session['conversation_history'] = []

        # Append the question to the conversation history
        session['conversation_history'].append({'role': 'bot', 'message': question})

        return render_template('index.html', conversation_history=session['conversation_history'], question=question)
    else:
        return render_template('index.html', response="Sorry, I couldn't identify the issue. Please try rephrasing.")

@app.route('/response', methods=['POST'])
def response():
    # Get the user's response (yes/no)
    user_response = request.form['response']
    question_id = session.get('question_id')  # Get the current question ID from session

    # Logic to determine the next question based on the response
    conn = sqlite3.connect('decision_tree.db')
    cursor = conn.cursor()

    # Fetch the next question based on the current question ID and user's response
    if user_response.lower() == 'yes':
        cursor.execute("SELECT yes_response FROM decision_tree WHERE id = ?", (question_id,))
    else:
        cursor.execute("SELECT no_response FROM decision_tree WHERE id = ?", (question_id,))

    next_question_id = cursor.fetchone()

    if next_question_id:
        next_question_id = next_question_id[0]
        cursor.execute("SELECT question FROM decision_tree WHERE id = ?", (next_question_id,))
        next_question = cursor.fetchone()
        conn.close()

        if next_question:
            # Store the next question ID in session
            session['question_id'] = next_question_id

            # Append the user's response and the bot's question to the conversation history
            session['conversation_history'].append({'role': 'user', 'message': user_response})
            session['conversation_history'].append({'role': 'bot', 'message': next_question[0]})

            return render_template('index.html', conversation_history=session['conversation_history'],
                                   question=next_question[0])
        else:
            return render_template('index.html', response="Thank you for using the IT support chatbot!")
    else:
        conn.close()
        return render_template('index.html', response="Sorry, no further questions available for this issue.")


if __name__ == '__main__':
    app.run(debug=True)





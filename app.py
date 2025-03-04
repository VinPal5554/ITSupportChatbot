from flask import Flask, request, jsonify, render_template
import stanza
import sqlite3

# Load the NLP pipeline
nlp = stanza.Pipeline(lang='en')

# Basic categories (this will be expanded later)
CATEGORIES = {
    "network": ["wifi", "internet", "router", "ethernet"],
    "microsoft": ["office", "outlook", "windows", "word", "excel"],
    "installation": ["install", "setup", "error", "update"],
    "slow": ["slow", "lag", "freezing", "performance"],
    "peripheral": ["keyboard", "mouse", "monitor", "printer"],
    "storage": ["hard drive", "ssd", "usb", "storage"],
    "security": ["antivirus", "firewall", "hacked", "malware"]
}

app = Flask(__name__)

# Classify user issue
def classify_issue(user_input):
    doc = nlp(user_input)
    for word in doc.iter_tokens():
        for category, keywords in categories.items():
            if word.text.lower() in keywords:
                return category
    return "unknown"

# Fetch first question from database
def get_first_question(category):
    conn = sqlite3.connect('decision_tree.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM decision_tree WHERE category=? LIMIT 1", (category,))
    row = cursor.fetchone()
    conn.close()
    return row

# Fetch next question based on user's response
def get_next_question(question_id, response):
    conn = sqlite3.connect('decision_tree.db')
    cursor = conn.cursor()
    if response == "yes":
        cursor.execute("SELECT id, question FROM decision_tree WHERE id=?", (question_id,))
    else:
        cursor.execute("SELECT id, question FROM decision_tree WHERE id=?", (question_id,))
    row = cursor.fetchone()
    conn.close()
    return row

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']  # Get user input from form

    # Here, use NLP (Stanza) to determine the category
    if "wifi" in user_input.lower() or "internet" in user_input.lower():
        category = "network"
    elif "slow" in user_input.lower() or "lag" in user_input.lower():
        category = "performance"
    else:
        category = "unknown"

    conn = sqlite3.connect('decision_tree.db')
    cursor = conn.cursor()

    # Fetch the first question for the identified category
    cursor.execute("SELECT id, question FROM decision_tree WHERE category = ? LIMIT 1", (category,))
    row = cursor.fetchone()

    if row:
        question_id, question = row
        return render_template('index.html', question=question, question_id=question_id)
    else:
        return render_template('index.html', response="Sorry, I couldn't identify the issue.")

    conn.close()


@app.route('/answer', methods=['POST'])
def answer():
    user_response = request.form['response']  # "yes" or "no"
    current_question_id = request.form['question_id']  # Get the current question ID

    conn = sqlite3.connect('decision_tree.db')
    cursor = conn.cursor()

    # Fetch the next question based on the user’s response
    cursor.execute("SELECT yes_response, no_response FROM decision_tree WHERE id = ?", (current_question_id,))
    row = cursor.fetchone()

    if row:
        next_question_id = row[0] if user_response == "yes" else row[1]

        # If the next step is a number, it’s another question ID; otherwise, it's a solution
        if next_question_id.isdigit():
            cursor.execute("SELECT question FROM decision_tree WHERE id = ?", (next_question_id,))
            next_question = cursor.fetchone()
            if next_question:
                return render_template('index.html', question=next_question[0], question_id=next_question_id)
        else:
            return render_template('index.html', solution=next_question_id)  # Display solution

    conn.close()
    return render_template('index.html', solution="Sorry, I couldn't find an answer.")


if __name__ == '__main__':
    app.run(debug=True)




'''
def categorize_issue(user_input):
    """Analyzes user input and assigns it to a category."""
    doc = nlp(user_input.lower())

    extracted_words = set()

    # Extract words and lemmas
    for sentence in doc.sentences:
        for word in sentence.words:
            extracted_words.add(word.text.lower())  # Raw word
            extracted_words.add(word.lemma.lower())  # Lemma form

    # Extract Named Entities (NER)
    for ent in doc.ents:
        extracted_words.add(ent.text.lower())

    # Debugging: Print extracted words
    print(f"Extracted Keywords: {extracted_words}")

    # Match against categories
    for category, data in CATEGORIES.items():
        for keyword in data["keywords"]:
            if keyword in extracted_words:
                print(f"Matched category: {category}")
                return category  # Return the first match

    print("No category matched, returning 'unknown'")
    return "unknown"
'''

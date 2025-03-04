from flask import Flask, request, jsonify, render_template
import stanza

# Load the NLP pipeline
nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,ner')

# Basic categories (this will be expanded later)
CATEGORIES = {
    "hardware": {
        "keywords": ["overheat", "battery", "charge", "charging", "screen", "display", "keyboard", "mouse", "power", "usb", "shut down", "fan", "heat"],
        "response": "It looks like a hardware issue. Have you tried checking your power connections or cooling system?"
    },
    "software": {
        "keywords": ["wifi", "internet", "slow", "crash", "update", "error", "installation", "bug", "lag", "freeze"],
        "response": "It seems to be a software issue. Have you tried restarting or updating your software?"
    },
    "unknown": {
        "response": "I'm not sure about that issue. Could you describe it differently or provide more details?"
    }
}

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


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', response="")


@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    category = categorize_issue(user_input)
    print(category)
    response = CATEGORIES[category]["response"]
    return render_template('index.html', response=response)

'''
    # Here you would add logic to handle the user's issue.
    if 'wifi' in user_input.lower():
        response = "Have you tried restarting your router?"
    elif 'slow' in user_input.lower():
        response = "Have you tried clearing your browser cache?"
    else:
        response = "Sorry, I couldn't find a solution for that."

'''


    
if __name__ == '__main__':
    app.run(debug=True)





from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import openai

# Initialise app
app = Flask(__name__)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    # Debug: Log the message received
    print(f"Received message: {user_message}")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.completions.create(
            model="gpt-3.5-turbo",  # Using gpt-3.5-turbo instead of gpt-4
            prompt=f"You are a helpful IT support chatbot. User says: {user_message}",
            max_tokens=150  # Adjust based on your needs
        )

        # Debug: Print the full API response
        print(f"API Response: {response}")

        # Access the bot reply
        bot_reply = response['choices'][0]['text'].strip()

        # Debug: Log the bot's response
        print(f"Bot reply: {bot_reply}")

        return jsonify({"response": bot_reply})

    except Exception as e:
        print(f"Error: {str(e)}")  # Print any errors to the console
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
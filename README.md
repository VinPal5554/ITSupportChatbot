# IT Support Chatbot
 
This is a simple AI chatbot application built with Flask and uses OpenAI's GPT-3.5 API. The chatbot interacts with the user, provides helpful IT support, and uses OpenAI's language model to generate responses based on user input

# Features
- User-friendly web interface for chatting with the bot
- The backend utilizes OpenAI's GPT-3.5 model to generate intelligent responses to user queries
- Easy to set up using environment variables for the OpenAI API key

# Installation steps
**Clone the repository:**
```
git clone https://github.com/VinPal5554/ITSupportChatbot.git
cd ITSupportChatbot
```
**Install backend dependencies:**
```
pip install Flask python-dotenv openai
```
**Setup API key:**

You will need to use your own OpenAI API key. 

An env file will need to be created within the project in this format:
```
OPENAI_API_KEY=api_key
```
**Run the Flask app:**
```
python app.py
```

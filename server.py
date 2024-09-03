from flask import Flask, request, jsonify, render_template
from LLM_Clients import OpenAIClient, ClaudeClient, GeminiClient
import signal
import sys

app = Flask(__name__)

# Function to handle graceful shutdown
def signal_handler(sig, frame):
    print("Gracefully shutting down...")
    sys.exit(0)

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Prompt user to choose the LLM client at startup
def choose_llm():
    print("Choose the LLM model to use:")
    print("1. OpenAI")
    print("2. Claude")
    print("3. Gemini")
    choice = input("Enter the number of the model you want to use: ")

    if choice == "1":
        return OpenAIClient()
    elif choice == "2":
        return ClaudeClient()
    elif choice == "3":
        return GeminiClient()
    else:
        print("Invalid choice. Please run the app again and select a valid option.")
        sys.exit(1)

LLM = choose_llm()

# Route to serve the main chat page
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint to handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_query = data.get('query', "")
    
    if not user_query:
        return jsonify({"error": "Empty query"}), 400
    
    try:
        # Query the selected LLM and get the response
        response_text = LLM.query_llm(user_query, temp=0.2)
        return jsonify({"reply": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

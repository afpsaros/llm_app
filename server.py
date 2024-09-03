from flask import Flask, request, jsonify, render_template
from LLM_Clients import OpenAIClient, ClaudeClient, GeminiClient
import signal
import sys

app = Flask(__name__)

# Function to handle graceful shutdown
def signal_handler(sig, frame):
    sys.exit(0)

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

LLM = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/select_model', methods=['POST'])
def select_model():
    global LLM
    data = request.json
    model = data.get('model')

    if model == "OpenAI":
        LLM = OpenAIClient()
    elif model == "Claude":
        LLM = ClaudeClient()
    elif model == "Gemini":
        LLM = GeminiClient()
    else:
        return jsonify({"error": "Invalid model selection"}), 400

    return jsonify({"status": "Model selected"}), 200

# API endpoint to handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    if not LLM:
        return jsonify({"error": "Model not selected"}), 400

    data = request.json
    user_query = data.get('query', "")
    
    if not user_query:
        return jsonify({"error": "Empty query"}), 400
    
    try:
        response_text = LLM.query_llm(user_query, temp=0.2)
        return jsonify({"reply": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

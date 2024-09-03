from flask import Flask, request, jsonify, render_template, session
from LLM_Clients import OpenAIClient, ClaudeClient, GeminiClient
import signal
import sys
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Function to handle graceful shutdown
def signal_handler(sig, frame):
    print("Gracefully shutting down...")
    sys.exit(0)

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/select_model', methods=['POST'])
def select_model():
    data = request.json
    model = data.get('model')

    if model == "OpenAI":
        session['llm'] = 'OpenAIClient'
    elif model == "Claude":
        session['llm'] = 'ClaudeClient'
    elif model == "Gemini":
        session['llm'] = 'GeminiClient'
    else:
        return jsonify({"error": "Invalid model selection"}), 400

    return jsonify({"status": "Model selected"}), 200

def get_llm_client():
    model = session.get('llm')
    if model == 'OpenAIClient':
        return OpenAIClient()
    elif model == 'ClaudeClient':
        return ClaudeClient()
    elif model == 'GeminiClient':
        return GeminiClient()
    else:
        return None

# API endpoint to handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    LLM = get_llm_client()
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

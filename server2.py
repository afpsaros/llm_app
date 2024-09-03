from flask import Flask, request, jsonify, render_template, session
from LLM_Clients import OpenAIClient, ClaudeClient, GeminiClient
import signal
import sys

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Function to handle graceful shutdown
def signal_handler(sig, frame):
    print("Gracefully shutting down...")
    sys.exit(0)

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Function to run authorization
def run_authorizer(a_number="xxx"):
    # Implement your company's authentication logic here
    # Replace with the actual authorization logic
    # Assuming this function returns True for success and False for failure
    print(f"Running authorizer with a_number={a_number}")
    success = True  # Replace with real logic
    return success

# Lazy loading of LLM client
def get_llm_client(model, auth):
    if model == 'OpenAI':
        return OpenAIClient(auth)  # Pass auth details to the client
    elif model == 'Claude':
        return ClaudeClient(auth)
    elif model == 'Gemini':
        return GeminiClient(auth)
    else:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/select_model', methods=['POST'])
def select_model():
    data = request.json
    model = data.get('model')
    auth = data.get('auth')

    # Run authorizer with the provided password/auth
    if run_authorizer(a_number=auth):
        # If authorization is successful, store the LLM and auth details in the session
        session['llm'] = model
        session['auth'] = auth
        return jsonify({"status": "Model selected and authenticated"}), 200
    else:
        return jsonify({"error": "Invalid authentication"}), 401

@app.route('/chat', methods=['POST'])
def chat():
    model = session.get('llm')
    auth = session.get('auth')

    if not model or not auth:
        return jsonify({"error": "Model not selected or authenticated"}), 400

    LLM = get_llm_client(model, auth)
    if not LLM:
        return jsonify({"error": "Unable to initialize the LLM client"}), 500

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

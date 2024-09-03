from flask import Flask, request, jsonify, render_template, session
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate a secure secret key

# Function to handle graceful shutdown
def signal_handler(sig, frame):
    print("Gracefully shutting down...")
    sys.exit(0)

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Function to run authorization using the provided password
def run_authorizer(a_number="1234", password=""):
    print(f"Running authorizer with a_number={a_number}")
    os.environ["username"] = a_number
    os.environ["pass"] = password  # Simulate getpass by setting this directly
    # No need for a return value since the success or failure will be handled later
    print("Environment variables set. Authentication will proceed with provided credentials.")

# Lazy loading of LLM client
def get_llm_client(model):
    if model == 'OpenAI':
        return OpenAIClient(os.environ["pass"])  # Pass auth details to the client
    elif model == 'Claude':
        return ClaudeClient(os.environ["pass"])
    elif model == 'Gemini':
        return GeminiClient(os.environ["pass"])
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

    # Run authorizer with the provided password
    run_authorizer(a_number="1234", password=auth)
    # Store the LLM and auth details in the session
    session['llm'] = model
    return jsonify({"status": "Model selected and authenticated"}), 200

@app.route('/chat', methods=['POST'])
def chat():
    model = session.get('llm')

    if not model or not os.environ.get("pass"):
        return jsonify({"error": "Model not selected or authenticated"}), 400

    LLM = get_llm_client(model)
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

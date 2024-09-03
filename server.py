from flask import Flask, request, jsonify
from LLM_Clients import OpenAIClient, ClaudeClient, GeminiClient

# Define a global variable for selecting the LLM client
LLM_TYPE = "Claude"  # Change this to "OpenAI" or "Gemini" as needed

# Initialize the appropriate LLM client based on the global variable
if LLM_TYPE == "OpenAI":
    LLM = OpenAIClient()
elif LLM_TYPE == "Gemini":
    LLM = GeminiClient()
else:  # Default to ClaudeClient
    LLM = ClaudeClient()

app = Flask(__name__)

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

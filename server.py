from flask import Flask, request, jsonify
from chat_with_llm import LLMClient

# Initialize the LLM client with your company's LLM
client = LLMClient(client=YourCompanyLLMClient())

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    conversation_history = data.get('history', [])
    reply = client.chat_with_llm(conversation_history)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)

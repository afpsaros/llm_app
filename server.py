from flask import Flask, request, jsonify
from chat_with_llm import LLMClient

# Define your client here
client = LLMClient(client=__________)

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    conversation_history = data.get('history', [])
    reply = client.query_llm(conversation_history=conversation_history, model="custom-llm-model")
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)

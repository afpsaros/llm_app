class LLMClient:
    def __init__(self, client):
        self.client = client

    def query_llm(self, conversation_history, model, temp=0.2):
        # The conversation history includes both user and assistant messages
        completions = self.client.chat.completions.create(
            model=model,
            messages=conversation_history,
            temperature=temp,
            stream=False
        )
        response = completions.choices[0].message['content']
        return response

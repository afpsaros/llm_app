class LLMClient:
    def __init__(self, client):
        self.client = client

    def chat_with_llm(self, conversation_history):
        # Replace this with the actual call to your company's LLM
        response = self.client.generate(
            prompt=conversation_history,
            model="custom-llm-model"
        )
        assistant_reply = response['content']
        return assistant_reply

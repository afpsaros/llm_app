document.getElementById('sendButton').addEventListener('click', sendMessage);

let chatbox = document.getElementById('chatbox');
let conversationHistory = [];

async function sendMessage() {
    let userInput = document.getElementById('inputBox').value;
    if (!userInput) return;

    // Add user's message to the chatbox
    addMessageToChatbox('User', userInput);
    conversationHistory.push({role: "user", content: userInput});

    // Clear the input field
    document.getElementById('inputBox').value = '';

    // Call the backend to get the AI response
    let assistantResponse = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({history: conversationHistory})
    }).then(response => response.json());

    addMessageToChatbox('Assistant', assistantResponse.reply);
    conversationHistory.push({role: "assistant", content: assistantResponse.reply});
}

function addMessageToChatbox(sender, message) {
    chatbox.innerHTML += `<p><strong>${sender}:</strong> ${message}</p>`;
    chatbox.scrollTop = chatbox.scrollHeight; // Scroll to the bottom
}

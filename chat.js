document.getElementById('sendButton').addEventListener('click', sendMessage);

let chatbox = document.getElementById('chatbox');

async function sendMessage() {
    let userInput = document.getElementById('inputBox').value;
    if (!userInput) return;

    // Add user's message to the chatbox
    addMessageToChatbox('User', userInput);

    // Clear the input field
    document.getElementById('inputBox').value = '';

    // Prepare the payload
    const payload = {
        query: userInput
    };

    // Send the query to the server
    let response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    }).then(response => response.json());

    // Check for errors
    if (response.error) {
        addMessageToChatbox('Error', response.error);
    } else {
        addMessageToChatbox('Assistant', response.reply);
    }
}

function addMessageToChatbox(sender, message) {
    chatbox.innerHTML += `<p><strong>${sender}:</strong> ${message}</p>`;
    chatbox.scrollTop = chatbox.scrollHeight;  // Scroll to the bottom
}

document.getElementById('sendButton').addEventListener('click', function() {
    sendMessage();
});

document.getElementById('inputBox').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        if (event.shiftKey) {
            // If Shift + Enter, insert a newline without sending
            event.preventDefault();  // Prevents the default behavior of submitting the form
            let start = this.selectionStart;
            let end = this.selectionEnd;
            this.value = this.value.substring(0, start) + '\n' + this.value.substring(end);
            this.selectionStart = this.selectionEnd = start + 1;

            // Ensure the textarea scrolls to the cursor position
            this.scrollTop = this.scrollHeight;
        } else {
            // If only Enter, prevent the default action and send the message
            event.preventDefault();
            sendMessage();
        }
    }
});

let chatbox = document.getElementById('chatbox');

async function sendMessage() {
    let userInput = document.getElementById('inputBox').value.trim();
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
    const messageElement = document.createElement('p');
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;  // Scroll to the bottom
}

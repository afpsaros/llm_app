document.getElementById('authForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const selectedModel = document.querySelector('input[name="model"]:checked').value;
    const auth = document.getElementById('auth').value;
    fetch('/select_model', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model: selectedModel, auth: auth })
    }).then(response => {
        if (response.ok) {
            // Hide the auth form and show the chat interface
            document.getElementById('authForm').style.display = 'none';
            document.getElementById('chatInterface').style.display = 'block';
        } else {
            alert('Error: Unable to authenticate or select model.');
        }
    });
});

// Chat functionality remains the same
document.getElementById('sendButton').addEventListener('click', function() {
    sendMessage();
});

document.getElementById('inputBox').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        if (event.shiftKey) {
            event.preventDefault();
            let start = this.selectionStart;
            let end = this.selectionEnd;
            this.value = this.value.substring(0, start) + '\n' + this.value.substring(end);
            this.selectionStart = this.selectionEnd = start + 1;
            this.scrollTop = this.scrollHeight;
        } else {
            event.preventDefault();
            sendMessage();
        }
    }
});

async function sendMessage() {
    let userInput = document.getElementById('inputBox').value.trim();
    if (!userInput) return;

    addMessageToChatbox('User', userInput);

    document.getElementById('inputBox').value = '';

    const payload = { query: userInput };

    let response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    }).then(response => response.json());

    if (response.error) {
        addMessageToChatbox('Error', response.error);
    } else {
        addMessageToChatbox('Assistant', response.reply);
    }
}

function addMessageToChatbox(sender, message) {
    const messageElement = document.createElement('p');
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    document.getElementById('chatbox').appendChild(messageElement);
    document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;
}

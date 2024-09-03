document.getElementById('modelSelectionForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const selectedModel = document.querySelector('input[name="model"]:checked').value;
    fetch('/select_model', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model: selectedModel })
    }).then(response => {
        if (response.ok) {
            // Hide the model selection form and show the chat interface
            document.getElementById('modelSelectionForm').style.display = 'none';
            document.getElementById('chatInterface').style.display = 'block';
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

function sanitizeInput(input) {
    let tempDiv = document.createElement('div');
    tempDiv.textContent = input;  // Set the input text as the textContent of the div
    return tempDiv.innerHTML;  // This returns the plain text with HTML entities encoded
}

async function sendMessage() {
    let userInput = document.getElementById('inputBox').value.trim();

    // Sanitize the input to remove any HTML tags
    let sanitizedInput = sanitizeInput(userInput);

    if (!sanitizedInput) {
        console.log("User input is empty, not sending message.");
        return;
    }

    // Display the user's query in the chatbox while preserving formatting
    addMessageToChatbox('User', `<pre><code>${sanitizeInput(userInput)}</code></pre>`);
    document.getElementById('inputBox').value = '';  // Clear the input box

    const payload = { query: sanitizedInput };

    try {
        let response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        let data = await response.json();

        if (data.error) {
            console.log("Error in response:", data.error);
            addMessageToChatbox('Error', data.error);
        } else {
            // Escape HTML and wrap the response in <pre><code> blocks
            let escapedReply = escapeHTML(data.reply);
            addMessageToChatbox('Assistant', `<pre><code>${escapedReply}</code></pre>`);
        }
    } catch (error) {
        console.error("Fetch error:", error);
        addMessageToChatbox('Error', 'Failed to send message');
    }
}

function addMessageToChatbox(sender, message) {
    const messageElement = document.createElement('p');

    // The message is inserted as innerHTML since we escape the content beforehand
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;

    document.getElementById('chatbox').appendChild(messageElement);
    document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;
}



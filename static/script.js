document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('user-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.querySelector('.chat-messages');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const userMessage = userInput.value.trim();

        if (userMessage === '') {
            return;
        }

        appendMessage('You', userMessage, 'outgoing');

        // Send user message to server and receive response
        fetch('/response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            const botResponse = data.response;
            appendMessage('Chatbot', botResponse, 'incoming');
        })
        .catch(error => {
            console.error('Error:', error);
        });

        userInput.value = '';
    });

    function appendMessage(sender, message, type) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', type);

        const messageText = document.createElement('p');
        messageText.textContent = `${sender}: ${message}`;
        messageElement.appendChild(messageText);

        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});

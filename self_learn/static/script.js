document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === "") return;

    appendMessage(userInput, 'user-message', '<i class="fas fa-user icon"></i>');
    document.getElementById('user-input').value = "";

    showTypingIndicator();

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        hideTypingIndicator();
        appendMessage(data.response, 'bot-message', '<i class="fas fa-robot icon"></i>');

        if (data.response === "I don't know the answer. Can you tell me?") {
            requestUserAnswer(userInput);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        hideTypingIndicator();
    });
}

function requestUserAnswer(userQuestion) {
    // Create a form element for the user to type their answer
    const answerForm = document.createElement('div');
    answerForm.className = 'answer-form';
    answerForm.innerHTML = `
        <input type="text" id="user-answer" placeholder="Type your answer here..." />
        <button id="submit-answer">Submit</button>
        <button id="skip-answer">Skip</button>
    `;

    // Append the form to the chat body
    document.getElementById('chat-body').appendChild(answerForm);

    // Add event listener for the submit button
    document.getElementById('submit-answer').addEventListener('click', function() {
        const userAnswer = document.getElementById('user-answer').value;

        if (userAnswer.trim() !== "") {
            fetch('/learn', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: userQuestion, answer: userAnswer })
            })
            .then(response => response.json())
            .then(data => {
                appendMessage(data.response, 'bot-message', '<i class="fas fa-robot icon"></i>');
                // Remove the answer form after submission
                answerForm.remove();
            })
            .catch(error => console.error('Error:', error));
        } else {
            // If the answer field is empty, remove the form
            answerForm.remove();
        }
    });

    // Add event listener for the skip button
    document.getElementById('skip-answer').addEventListener('click', function() {
        appendMessage("The answer has been skipped.", 'bot-message', '<i class="fas fa-robot icon"></i>');
        // Remove the answer form
        answerForm.remove();
    });

    // Add event listener for Enter key in the answer input field
    document.getElementById('user-answer').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.getElementById('submit-answer').click();
        }
    });
}

function appendMessage(message, className, iconHTML) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${className}`;
    messageElement.innerHTML = iconHTML + message;
    document.getElementById('chat-body').appendChild(messageElement);
    messageElement.scrollIntoView();
}

function showTypingIndicator() {
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'message bot-message typing-indicator';
    typingIndicator.innerHTML = '<i class="fas fa-robot icon"></i>...';
    typingIndicator.setAttribute('id', 'typing-indicator');
    document.getElementById('chat-body').appendChild(typingIndicator);
    typingIndicator.scrollIntoView();
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

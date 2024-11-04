const chatBox = document.getElementById('chat-box');

function displayMessage(message, className) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', className);
    messageElement.innerHTML = message.replace(/\n/g, "<br>");
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendQuery() {
    const queryInput = document.getElementById('query-input');
    const query = queryInput.value.trim();
    if (!query) return;

    // Display user's message in the chat
    displayMessage(query, 'user-message');

    // Clear input field after sending
    queryInput.value = '';

    try {
        const response = await fetch('http://127.0.0.1:8080/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        let botMessageElement = document.createElement('div');
        botMessageElement.classList.add('message', 'bot-message');
        chatBox.appendChild(botMessageElement);

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            botMessageElement.innerHTML += chunk.replace(/\n/g, "<br>");
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    } catch (error) {
        console.error("Error fetching stream:", error);
    }
}

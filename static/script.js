async function sendQuery() {
    const queryInput = document.getElementById('query-input');
    const chatBox = document.getElementById('chat-box');

    const query = queryInput.value.trim();
    if (!query) return;

    // Display the user's message
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.textContent = query;
    chatBox.appendChild(userMessage);

    // Clear the input field
    queryInput.value = '';

    // Scroll to the bottom of the chat box to show the latest message
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send the query to the backend
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });

        const result = await response.json();

        // Display the bot's response
        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot-message');
        botMessage.innerHTML = result.response.replace(/\n/g, '<br>');
        chatBox.appendChild(botMessage);

        // Scroll to the bottom of the chat box to show the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        console.error("Error fetching response:", error);
    }
}

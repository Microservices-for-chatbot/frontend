document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-query');
    const sendButton = document.getElementById('send-button');
    const chatHistory = document.getElementById('chatHistory');

    // Function to generate and store a unique user ID
    function getOrCreateUserId() {
        let userId = localStorage.getItem('chatUserId');
        if (!userId) {
            userId = 'user_' + Date.now() + Math.random().toString(36).substring(2, 9);
            localStorage.setItem('chatUserId', userId);
        }
        return userId;
    }

    // Function to add a message to the chat container
    function addMessage(message, sender) {
        const chatWrapper = document.createElement('div');
        chatWrapper.classList.add('chat');
        chatWrapper.classList.add(sender === 'user' ? 'user-chat' : 'bot-chat');

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message');
        messageDiv.innerHTML = message;
        
        chatWrapper.appendChild(messageDiv);
        chatHistory.appendChild(chatWrapper);
        
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    // Handle the message submission
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });

    async function sendMessage() {
        const userMessage = userInput.value.trim();
        if (!userMessage) return;

        const userId = getOrCreateUserId();
        addMessage(userMessage, 'user');
        userInput.value = '';

        addMessage('...', 'bot'); // Show loading indicator

        try {
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    question: userMessage,
                    user_id: userId
                })
            });

            const jsonResponse = await response.json();
            
            chatHistory.removeChild(chatHistory.lastChild); // Remove loading indicator
            
            const botMessage = jsonResponse.answer;
            if (botMessage) {
                addMessage(botMessage, 'bot');
            } else {
                addMessage("Sorry, I could not get a response.", "bot");
            }
        } catch (error) {
            console.error('Error fetching data:', error);
            chatHistory.removeChild(chatHistory.lastChild);
            addMessage("Sorry, an error occurred while connecting to the server.", "bot");
        }
    }
});

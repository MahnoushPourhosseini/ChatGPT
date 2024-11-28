// Define the backend URL
const BACKEND_URL = 'http://127.0.0.1:5000'; // This matches my backend configuration

// Ensure the fetchingn
fetch('http://127.0.0.1:5000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages: [{ role: "user", content: "Test question?" }] })
})
.then(response => response.json())
.then(data => console.log("Success:", data))
.catch(error => console.error("Fetch Error:", error));

// CORS problem
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH
Access-Control-Allow-Headers: Content-Type, Authorization

// Function to send a question to the backend
async function askQuestion() {
    try {
        const userInput = document.getElementById("user-input").value.trim();
        if (!userInput) {
            displayMessage("Error", "Please enter a question before submitting.");
            return;
        }

        // Display user's message in the chatbox
        displayMessage("You", userInput);

        // Send the user's input to the backend
        const response = await fetch(`${BACKEND_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: [{ role: "user", content: userInput }] })
        });

        if (response.ok) {
            // Backend returns JSON with the chatbot's reply
            const responseData = await response.json();
            displayMessage("ChatGPT", responseData.answer);
        } else {
            displayMessage("Error", "Failed to get a response from the server.");
        }
    } catch (error) {
        displayMessage("Error", `An error occurred: ${error.message}`);
    } finally {
        // Clear the input field
        document.getElementById("user-input").value = "";
    }
}

// Function to display messages in the chatbox
function displayMessage(sender, message) {
    const chatbox = document.getElementById("chatbox");
    const messageDiv = document.createElement("div");
    messageDiv.textContent = `${sender}: ${message}`;
    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll to the latest message
}

// Load chat history from backend when the page is loaded
async function loadHistory() {
    try {
        const response = await fetch(`${BACKEND_URL}/history`); // Get chat history from backend
        if (response.ok) {
            const history = await response.json();
            history.forEach(entry =>
                displayMessage(
                    entry.role === "user" ? "You" : "ChatGPT",
                    entry.content
                )
            );
        } else {
            console.error("Failed to load history: Server returned an error.");
        }
    } catch (error) {
        console.error("Failed to load history:", error.message);
    }
}

// Attach an event listener to the "Send" button
document.getElementById("send-button").addEventListener("click", askQuestion);

// Call loadHistory() when the page loads
window.onload = loadHistory;

document.getElementById("send-button").addEventListener("click", () => {
    const userInput = document.getElementById("user-input").value;
    if (userInput.trim() !== "") {
        appendUserMessage(userInput);
        sendMessageToChatbot(userInput);
    }
});

document.querySelectorAll(".question-button").forEach(button => {
    button.addEventListener("click", () => {
        const question = button.innerText;
        appendUserMessage(question);
        sendMessageToChatbot(question);
    });
});

function appendUserMessage(message) {
    const chatMessages = document.getElementById("chat-messages");
    const userMessage = `<div class="user-message">${message}</div>`;
    chatMessages.innerHTML += userMessage;
    chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
}

function appendBotMessage(message) {
    const chatMessages = document.getElementById("chat-messages");
    const botMessage = `<div class="bot-message">${message}</div>`;
    chatMessages.innerHTML += botMessage;
    chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
}

function sendMessageToChatbot(userInput) {
    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        appendBotMessage(data.response);
        handleQuestionTree(userInput.toLowerCase());
    });
}

// Handle the dynamic question tree logic for displaying quick replies
function handleQuestionTree(userInput) {
    let options;

    if (userInput.includes("courses")) {
        options = ["Undergraduate", "Postgraduate"];
    } else if (userInput.includes("admission")) {
        options = ["Requirements", "Process"];
    }

    if (options) {
        showQuickReplies(options);
    }
}

function showQuickReplies(options) {
    const chatMessages = document.getElementById("chat-messages");
    const buttonContainer = document.createElement("div");
    buttonContainer.className = "quick-replies";

    options.forEach(option => {
        const button = document.createElement("button");
        button.className = "question-button";
        button.innerText = option;
        button.onclick = () => {
            appendUserMessage(option);
            sendMessageToChatbot(option);
        };
        buttonContainer.appendChild(button);
    });

    chatMessages.appendChild(buttonContainer);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
}

const input = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

input.addEventListener("input", () => {
    sendButton.disabled = input.value.trim() === "";
});
chatMessages.scrollTo({
    top: chatMessages.scrollHeight,
    behavior: 'smooth'
});

function sendMessageToChatbot(userInput) {
    appendBotMessage("Typing...");
    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        removeLastBotMessage(); // remove "Typing..."
        appendBotMessage(data.response);
        handleQuestionTree(userInput.toLowerCase());
    });
}

function removeLastBotMessage() {
    const chatMessages = document.getElementById("chat-messages");
    const last = chatMessages.querySelector(".bot-message:last-child");
    if (last && last.textContent === "Typing...") {
        last.remove();
    }
}

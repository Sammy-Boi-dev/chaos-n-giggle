const chat = document.getElementById("chat");
const input = document.getElementById("message");

function addMessage(message, sender) {

    const div = document.createElement("div");
    div.className = sender;
    div.textContent = message;

    chat.appendChild(div);

    chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {

    const message = input.value.trim();
    if (message === "") return;

    addMessage(message, "user");
    input.value = "";

    const typing = document.createElement("div");
    typing.className = "bot typing";
    typing.id = "typing";
    typing.textContent = "🤖 Chaos N Giggle is typing...";
    chat.appendChild(typing);
    chat.scrollTop = chat.scrollHeight;

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        const typingEl = document.getElementById("typing");
        if (typingEl) typingEl.remove();

        // IMPORTANT safety fallback
        const reply = data.reply || "⚠️ No response from AI";

        addMessage(reply, "bot");

    } catch (error) {

        const typingEl = document.getElementById("typing");
        if (typingEl) typingEl.remove();

        addMessage("❌ Could not connect to the server.", "bot");

        console.error(error);
    }
}

input.addEventListener("keydown", function(e){

    if(e.key === "Enter"){

        sendMessage();

    }

});
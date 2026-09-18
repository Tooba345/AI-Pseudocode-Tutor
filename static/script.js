
document.getElementById("imageInput").addEventListener("change", function () {
    const file = this.files[0];

    if (!file) {
        return;
    }

    const imageUrl = URL.createObjectURL(file);

    const answerDiv = document.getElementById("answer");

    answerDiv.innerHTML += `
        <div class="chat-message user-message">
            <strong>📷 Image selected:</strong>
            <br><br>
            <img src="${imageUrl}" style="max-width: 300px; border-radius: 12px;">
        </div>
    `;
});
async function askQuestion() {
    const questionInput = document.getElementById("question");
    const answerDiv = document.getElementById("answer");

    const question = questionInput.value.trim();

    if (question === "") {
        return;
    }

    // Show the student's question
    answerDiv.innerHTML += `
        <div class="chat-message user-message">
            <strong>👩‍💻 You:</strong>
            <p>${question}</p>
        </div>
    `;

    // Show thinking message
    answerDiv.innerHTML += `
        <div class="chat-message ai-message">
            <strong>🤖 AI:</strong>
            <p>Thinking...</p>
        </div>
    `;

    questionInput.value = "";

    try {
        const formData = new FormData();

        formData.append("question", question);

        const imageFile = document.getElementById("imageInput").files[0];

        if (imageFile) {
           formData.append("image", imageFile);
}

const response = await fetch("/ask", {
    method: "POST",
    body: formData
});

        const data = await response.json();

        // Remove "Thinking..." and replace it with the real answer
        const messages = answerDiv.querySelectorAll(".ai-message");
        const latestMessage = messages[messages.length - 1];

        latestMessage.innerHTML = `
            <strong>🤖 AI:</strong>
            <div>${marked.parse(data.answer)}</div>
        `;

    } catch (error) {
        const messages = answerDiv.querySelectorAll(".ai-message");
        const latestMessage = messages[messages.length - 1];

        latestMessage.innerHTML = `
            <strong>🤖 AI:</strong>
            <p>❌ Something went wrong.</p>
        `;

        console.error(error);
    }
}
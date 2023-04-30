const form = document.getElementById("api-form");
const userInput = document.getElementById("user-input");
const responseContainer = document.getElementById("response");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = userInput.value;
    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ input }),
    });

    const data = await response.json();
    responseContainer.textContent = data.response;
});

// Add this code block for the /agent endpoint
const formAgent = document.getElementById("api-form-agent");
const userInputAgent = document.getElementById("user-input-agent");
const responseContainerAgent = document.getElementById("response-agent");

formAgent.addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = userInputAgent.value;
    const response = await fetch("/agent", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ input }),
    });

    const data = await response.json();
    responseContainerAgent.textContent = data.response;
});

// Add this code block for the /memory endpoint
const formMemory = document.getElementById("api-form-memory");
const userInputMemory = document.getElementById("user-input-memory");
const responseContainerMemory = document.getElementById("response-memory");

formMemory.addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = userInputMemory.value;
    const response = await fetch("/memory", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ input }),
    });

    const data = await response.json();
    responseContainerMemory.textContent = data.response;
});

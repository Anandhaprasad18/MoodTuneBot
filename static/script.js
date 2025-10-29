let sessionId = localStorage.getItem("session_id");

// Create a session ID if not exists
if (!sessionId) {
  sessionId = "session_" + Date.now() + "_" + Math.floor(Math.random() * 10000);
  localStorage.setItem("session_id", sessionId);
}

function appendMessage(sender, text, isLink = false) {
  const chatBox = document.getElementById("chat-box");
  const message = document.createElement("div");
  message.className = `message ${sender.toLowerCase()}`;
  message.innerHTML = isLink ? text : `<strong>${sender}:</strong> ${text.replace(/\n/g, "<br>")}`;
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function showTypingIndicator() {
  const chatBox = document.getElementById("chat-box");
  const typing = document.createElement("div");
  typing.className = "message bot typing";
  typing.innerHTML = "Bot is typing...";
  chatBox.appendChild(typing);
  chatBox.scrollTop = chatBox.scrollHeight;
  return typing;
}

function removeTypingIndicator(typingElement) {
  if (typingElement) typingElement.remove();
}

async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  appendMessage("You", message);
  input.value = "";

  const typingElement = showTypingIndicator();

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: message,
        session: sessionId   // 👈 send the same session id every time
      }),
    });

    const data = await res.json();
    removeTypingIndicator(typingElement);

    if (data.response) appendMessage("Bot", data.response);
    if (data.link) {
      appendMessage("Bot", `<a href="${data.link}" target="_blank">🎵 Play on Spotify</a>`, true);
    }
  } catch (err) {
    removeTypingIndicator(typingElement);
    appendMessage("Bot", "Oops! Something went wrong. Please try again.");
    console.error(err);
  }
}

// Handle Enter key
document.getElementById("user-input").addEventListener("keypress", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Send button (click + touch)
const sendBtn = document.querySelector("button");
sendBtn.addEventListener("click", sendMessage);
sendBtn.addEventListener("touchstart", (e) => {
  e.preventDefault();
  sendMessage();
});

// Particle background
function createParticles() {
  const particlesContainer = document.querySelector(".particles");
  for (let i = 0; i < 20; i++) {
    const particle = document.createElement("div");
    particle.className = "particle";
    particle.style.width = `${Math.random() * 10 + 5}px`;
    particle.style.height = particle.style.width;
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.animationDelay = `${Math.random() * 10}s`;
    particle.style.animationDuration = `${Math.random() * 10 + 10}s`;
    particlesContainer.appendChild(particle);
  }
}

createParticles();

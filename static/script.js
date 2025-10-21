function appendMessage(sender, text) {
  const chatBox = document.getElementById("chat-box");
  const message = document.createElement("div");
  message.innerHTML = `<strong>${sender}:</strong> ${text.replace(/\n/g, "<br>")}`;
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  appendMessage("You", message);
  input.value = "";

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  })
  .then(res => res.json())
  .then(data => {
    appendMessage("Bot", data.response);
    if (data.link) {
      appendMessage("Bot", `<a href="${data.link}" target="_blank">🎵 Play on Spotify</a>`);
    }
  })
  .catch(err => {
    appendMessage("Bot", "Oops! Something went wrong. Please try again.");
    console.error(err);
  });
}
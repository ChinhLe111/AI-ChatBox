function formatText(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\n/g, "<br>");
}

function appendMessage(sender, text) {
    const chatbox = document.getElementById('chatbox');
    const div = document.createElement('div');
    
    if (sender === 'user') {
        div.className = "text-right mb-2";
        div.innerHTML = `<span class="inline-block bg-blue-500 text-white px-4 py-2 rounded-xl text-left">${formatText(text)}</span>`;
    } else {
        div.className = "text-left mb-2";
        div.innerHTML = `<span class="inline-block bg-gray-200 text-gray-800 px-4 py-2 rounded-xl">${formatText(text)}</span>`;
    }
    
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById('message');
    const message = input.value.trim();
    if (!message) return;
    
    appendMessage('user', message);
    input.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message})
    })
    .then(res => res.json())
    .then(data => {
        appendMessage('bot', data.reply);
    });
}

function handleKey(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}
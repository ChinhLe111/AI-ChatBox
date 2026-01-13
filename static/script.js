function formatText(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\n/g, "<br>");
}

function appendMessage(sender, text) {
  const chatbox = document.getElementById("chatbox");

  const div = document.createElement("div");
  const span = document.createElement("span");

  if (sender === "user") {
    div.className = "text-right mb-2";
    span.className =
      "inline-block bg-blue-500 text-white px-4 py-2 rounded-xl text-left";
  } else {
    div.className = "text-left mb-2";
    span.className =
      "inline-block bg-gray-200 text-gray-800 px-4 py-2 rounded-xl";
  }

  span.innerHTML = formatText(text); // chỉ dùng 1 lần
  div.appendChild(span);
  chatbox.appendChild(div);
  chatbox.scrollTop = chatbox.scrollHeight;

  return span; // ✅ TRẢ SPAN
}

async function sendMessage() {
  const input = document.getElementById("message");
  const message = input.value.trim();
  if (!message) return;

  appendMessage("user", message);
  input.value = "";

  // 👇 nhận span bot
  const botSpan = appendMessage("bot", "");

  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");

  let fullText = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    fullText += decoder.decode(value, { stream: true });
    botSpan.innerText = fullText + "|"; // stream text
  }

  botSpan.innerHTML = formatText(fullText); // render markdown cuối
}

function handleKey(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

const chat = document.getElementById("chat");
const input = document.getElementById("input");
const typing = document.getElementById("typing");

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") send();
});

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.innerText = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function send() {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";
  typing.style.display = "block";

  const res = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  });

  const data = await res.json();

  typing.style.display = "none";
  addMessage(data.response, "ai");
}

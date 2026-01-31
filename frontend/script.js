// -------------------
// DOM Elements
// -------------------
const chat = document.getElementById("chat")
const input = document.getElementById("input")
const sendBtn = document.getElementById("sendBtn")

const API_URL = "http://localhost:8000/chat"

// -------------------
// Safety check
// -------------------
if (!chat || !input || !sendBtn) {
  console.error("❌ Required DOM elements not found")
}

// -------------------
// Helpers
// -------------------
function addMessage(role, text) {
  const wrapper = document.createElement("div")
  wrapper.className = `message ${role}`

  const roleDiv = document.createElement("div")
  roleDiv.className = "role"
  roleDiv.textContent = role === "user" ? "You" : "Neeraj"

  const contentDiv = document.createElement("div")
  contentDiv.className = "content"
  contentDiv.textContent = text

  wrapper.appendChild(roleDiv)
  wrapper.appendChild(contentDiv)
  chat.appendChild(wrapper)

  chat.scrollTop = chat.scrollHeight
}

function addTypingIndicator() {
  if (document.getElementById("typing")) return

  const wrapper = document.createElement("div")
  wrapper.className = "message bot"
  wrapper.id = "typing"

  wrapper.innerHTML = `
    <div class="role">Neeraj</div>
    <div class="content">
      <div class="typing">
        <span></span><span></span><span></span>
      </div>
    </div>
  `

  chat.appendChild(wrapper)
  chat.scrollTop = chat.scrollHeight
}

function removeTypingIndicator() {
  const el = document.getElementById("typing")
  if (el) el.remove()
}

function setSending(isSending) {
  sendBtn.disabled = isSending
  input.disabled = isSending
}

// -------------------
// Core send logic
// -------------------
async function sendMessage() {
  const question = input.value.trim()
  if (!question) return

  input.value = ""
  setSending(true)

  addMessage("user", question)
  addTypingIndicator()

  // Allow UI to paint typing dots
  await new Promise((r) => setTimeout(r, 200))

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    })

    if (!res.ok) {
      throw new Error(`HTTP error ${res.status}`)
    }

    const data = await res.json()

    // Minimum typing delay (feels human)
    await new Promise((r) => setTimeout(r, 400))

    removeTypingIndicator()
    addMessage("bot", data.answer)
  } catch (err) {
    console.error("❌ Chat error:", err)
    removeTypingIndicator()
    addMessage("bot", "Something went wrong. Please try again.")
  } finally {
    setSending(false)
    input.focus()
  }
}

// -------------------
// Events
// -------------------
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
})

sendBtn.addEventListener("click", sendMessage)
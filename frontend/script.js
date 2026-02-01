const chat = document.getElementById("chat")
const input = document.getElementById("input")

const API_URL = "http://localhost:8000/chat"

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

// -------------------
// Events
// -------------------
input.addEventListener("keydown", async (e) => {
  if (e.key !== "Enter" || !input.value.trim()) return

  const question = input.value
  input.value = ""

  addMessage("user", question)
  addTypingIndicator()
  
  // ⬇️ Allow browser to render typing dots
  await new Promise((r) => setTimeout(r, 150))
  
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    })
  
    const data = await res.json()
  
    // ⬇️ Optional minimum typing time (feels human)
    await new Promise((r) => setTimeout(r, 400))
  
    removeTypingIndicator()
    addMessage("bot", data.answer)
  } catch (err) {
    console.error(err)
    removeTypingIndicator()
    addMessage("bot", "Something went wrong.")
  }
})
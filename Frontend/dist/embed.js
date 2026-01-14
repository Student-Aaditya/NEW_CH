const chatIcon = `
<svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" fill="none" stroke="white" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
    d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
</svg>
`

const closeIcon = `
<svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7" fill="none" stroke="white" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
    d="M6 18L18 6M6 6l12 12" />
</svg>
`

(function () {
  if (window.__NIET_CHATBOT_LOADED__) return
  window.__NIET_CHATBOT_LOADED__ = true

  // ---------- Launcher Button ----------
  const launcher = document.createElement("button")
  launcher.innerHTML = chatIcon
  launcher.title = "Chat with NIET Assistant"

  Object.assign(launcher.style, {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    width: "56px",
    height: "56px",
    borderRadius: "50%",
    border: "none",
    cursor: "pointer",
    background: "#e11d2e",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    boxShadow: "0 12px 30px rgba(225,29,46,0.4)",
    zIndex: "999999",
  })

  // ---------- Chatbot iframe ----------
  const iframe = document.createElement("iframe")
  iframe.src = "https://new-ch.onrender.com"
  iframe.title = "NIET Admissions Chatbot"

  Object.assign(iframe.style, {
    position: "fixed",
    bottom: "90px",
    right: "20px",
    width: "380px",
    height: "520px",
    border: "none",
    borderRadius: "18px",
    boxShadow: "0 20px 40px rgba(0,0,0,0.35)",
    zIndex: "999999",
    display: "none",
    background: "#fff",
  })

  // ---------- Toggle logic ----------
  let isOpen = false

  launcher.onclick = () => {
    isOpen = !isOpen
    iframe.style.display = isOpen ? "block" : "none"
    launcher.innerHTML = isOpen ? closeIcon : chatIcon
  }

  document.body.appendChild(launcher)
  document.body.appendChild(iframe)
})()

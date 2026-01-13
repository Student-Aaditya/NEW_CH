(function () {
  if (window.__NIET_CHATBOT_LOADED__) return
  window.__NIET_CHATBOT_LOADED__ = true

  // ---------- Launcher Button ----------
  const launcher = document.createElement("button")
  launcher.innerHTML = "💬"
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
    color: "#fff",
    fontSize: "22px",
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
    display: "none", // 🔥 IMPORTANT: hidden by default
    background: "#fff",
  })

  // ---------- Toggle logic ----------
  let isOpen = false

  launcher.onclick = () => {
    isOpen = !isOpen
    iframe.style.display = isOpen ? "block" : "none"
    launcher.innerHTML = isOpen ? "✕" : "💬"
  }

  document.body.appendChild(launcher)
  document.body.appendChild(iframe)
})()
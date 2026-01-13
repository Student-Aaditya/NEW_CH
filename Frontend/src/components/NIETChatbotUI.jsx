"use client"

import { useState } from "react"

export default function NIETChatbotUI({ children }) {
  const [isOpen, setIsOpen] = useState(false)

  const onToggle = () => setIsOpen((prev) => !prev)

  return (
    <>
      {/* Floating launcher */}
      <button
        onClick={onToggle}
        aria-label={isOpen ? "Close chat" : "Open chat"}
        className="
          fixed right-8 bottom-6
          w-16 h-16                 /* 🔥 increased size */
          rounded-full
          bg-[#e2111f]
          shadow-[0_10px_30px_rgba(226,17,31,0.4)]
          flex items-center justify-center
          z-50 cursor-pointer
          transition-all duration-300
          hover:scale-110
          active:scale-95
        "
      >
        {isOpen ? (
          <span className="text-white text-3xl font-bold leading-none">
            ×
          </span>
        ) : (
          <div className="w-11 h-11 rounded-full bg-white p-1.5 flex items-center justify-center overflow-hidden">
            <img
              src="/niet-logo.svg"
              alt="NIET"
              className="w-full h-full object-contain rounded-full"
              onError={(e) => (e.target.src = "/niet-logo.png")}
            />
          </div>
        )}
      </button>

      {/* Chat window */}
      <div
        className={`${
          isOpen
            ? "translate-y-0 opacity-100"
            : "translate-y-6 opacity-0 pointer-events-none"
        } fixed right-10 bottom-28 w-[24rem] md:w-[36rem] z-40 transition-all duration-300`}
        style={{ display: "block" }}
      >
        <div className="bg-white rounded-2xl shadow-[0_30px_100px_rgba(0,0,0,0.18)] overflow-hidden flex flex-col">
          {/* Header */}
          <div className="flex items-center justify-between px-5 py-4 bg-gradient-to-r from-[#e2111f] to-[#551023] text-white">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-white/20 p-1 flex items-center justify-center overflow-hidden">
                <img
                  src="/niet-logo.svg"
                  alt="logo"
                  className="w-full h-full object-contain rounded-full"
                  onError={(e) => (e.target.src = "/niet-logo.png")}
                />
              </div>
              <div>
                <div className="font-semibold text-base">
                  NIET Virtual Assistant
                </div>
                <div className="text-xs opacity-90">
                  Official – NIET
                </div>
              </div>
            </div>
          </div>

          {/* Chat body */}
          <div className="h-full flex flex-col">
            {children}
          </div>
        </div>
      </div>
    </>
  )
}

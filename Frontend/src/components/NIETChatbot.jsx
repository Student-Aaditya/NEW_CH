"use client"

import { useState, useEffect } from "react"
import NIETChatbotMessages from "./NIETChatbotMessages"

export default function NIETChatbot({embed=false}) {
  const isIframe = window.self !== window.top

  const [open, setOpen] = useState(isIframe)

  return (
    <>
      {/* Launcher ONLY for normal site */}
      {!isIframe && !open && (
        <button
          onClick={() => setOpen(true)}
          className="fixed bottom-6 right-6 z-[100] w-14 h-14 rounded-2xl bg-gradient-to-br from-[#e2111f] to-[#b00d18] flex items-center justify-center shadow-[0_10px_30px_rgba(226,17,31,0.4)] transition-all duration-300 hover:scale-110 active:scale-95"
          aria-label="Open Chat"
        >
          <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
        </button>
      )}

      {/* Chat Window (always open in iframe) */}
      {open && (
        <div  className={`fixed inset-0 z-[90] flex items-end justify-end p-2 sm:p-6`}>
          <div className="relative w-full sm:w-[380px] h-full sm:h-[520px] bg-white border border-slate-100 shadow-[0_30px_100px_rgba(0,0,0,0.18)] flex flex-col rounded-[32px] overflow-hidden">

            {/* Close button ONLY outside iframe */}
            {!isIframe && (
              <button
                onClick={() => setOpen(false)}
                className="absolute -top-3 -right-3 z-[101] w-7 h-7 rounded-full bg-[#e2111f] flex items-center justify-center shadow-lg border-2 border-white"
              >
                ✕
              </button>
            )}

            <NIETChatbotMessages embed={embed} />
          </div>
        </div>
      )}
    </>
  )
}

"use client";

import { useEffect, useRef } from "react";
import gsap from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export default function HowItWorks() {
  const containerRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Left side stagger
      gsap.from(".step-item", {
        x: -40,
        opacity: 0,
        duration: 0.8,
        stagger: 0.2,
        ease: "power3.out",
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top 70%",
          once: true
        }
      });

      // Video Player Timeline
      const tl = gsap.timeline({ repeat: -1, repeatDelay: 2 });
      
      // Play button disappears
      tl.to(".play-overlay", { opacity: 0, duration: 0.3, ease: "power2.inOut" });

      // Sequence elements appear one by one
      tl.to(".seq-1", { opacity: 1, duration: 0.2 })
        .to(".video-time", { innerHTML: "0:01", duration: 0, snap: { innerHTML: 1 } }, "<")
        .to(".seq-2", { opacity: 1, duration: 0.4 }, "+=0.8")
        .to(".video-time", { innerHTML: "0:02", duration: 0, snap: { innerHTML: 1 } }, "<")
        .to(".seq-3", { opacity: 1, y: -5, duration: 0.3, ease: "back.out(1.5)" }, "+=0.6")
        .to(".video-time", { innerHTML: "0:03", duration: 0, snap: { innerHTML: 1 } }, "<")
        .to(".seq-4", { opacity: 1, duration: 0.3 }, "+=1")
        .to(".video-time", { innerHTML: "0:04", duration: 0, snap: { innerHTML: 1 } }, "<")
        .to(".seq-5", { opacity: 1, scale: 1.05, duration: 0.3, ease: "back.out(2)" }, "+=0.5")
        .to(".seq-5", { scale: 1, duration: 0.2 })
        .to(".video-time", { innerHTML: "0:05", duration: 0, snap: { innerHTML: 1 } }, "<");

      // Progress bar fills up
      tl.to(".video-progress", { width: "100%", duration: tl.duration(), ease: "none" }, 0);

      // Fade everything back out for loop
      tl.to([".seq-1", ".seq-2", ".seq-3", ".seq-4", ".seq-5"], { opacity: 0, duration: 0.5 }, "+=2");
      tl.to(".play-overlay", { opacity: 1, duration: 0.5 }, "<");
      tl.to(".video-progress", { width: "0%", duration: 0 }, "<");
      tl.to(".video-time", { innerHTML: "0:00", duration: 0 }, "<");
    }, containerRef);
    return () => ctx.revert();
  }, []);

  return (
    <section id="workflows" ref={containerRef} className="relative z-10 py-32 px-6 max-w-7xl mx-auto border-t border-white/5">
      <div className="flex flex-col items-center text-center mb-16">
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4 text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-500">
          How it works.
        </h2>
        <p className="text-[#888] font-mono text-xs uppercase tracking-[0.2em]">Intercept &gt; Analyze &gt; Control</p>
      </div>

      <div className="flex flex-col lg:flex-row gap-12 items-center">
        {/* Steps */}
        <div className="flex-1 space-y-12 w-full">
          {[
            { num: "01", title: "Intercept the LLM tool call", desc: "Before the agent runs any tool, the payload is intercepted by AgentWatch." },
            { num: "02", title: "Analyze via Safety Engine", desc: "We run a secondary, specialized model to score the action's semantic risk." },
            { num: "03", title: "Execute or Block", desc: "If safe, it executes. If dangerous, we block it and inject a simulated success back to the agent." }
          ].map((step, i) => (
            <div key={i} className="step-item flex gap-6 items-start">
              <div className="text-3xl font-mono font-bold text-transparent bg-clip-text bg-gradient-to-b from-[#00f0ff] to-transparent">
                {step.num}
              </div>
              <div>
                <h3 className="text-xl font-bold text-white mb-2">{step.title}</h3>
                <p className="text-[#888] text-sm">{step.desc}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Faux Video Player Graphic */}
        <div className="flex-1 w-full relative">
          {/* Video Player Frame */}
          <div className="relative aspect-[4/3] rounded-xl border border-white/10 bg-[#0a0a0a] overflow-hidden shadow-2xl group cursor-pointer">
            {/* Background Grid */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(232,255,71,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(232,255,71,0.03)_1px,transparent_1px)] bg-[size:24px_24px] opacity-50" />
            
            {/* Video Content (Animated Sequence) */}
            <div className="absolute inset-0 p-6 flex flex-col font-mono text-sm">
              {/* Terminal Header */}
              <div className="flex items-center gap-2 mb-4">
                <div className="w-2.5 h-2.5 rounded-full bg-red-500/80" />
                <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/80" />
                <div className="w-2.5 h-2.5 rounded-full bg-green-500/80" />
                <span className="ml-2 text-[#555] text-xs font-semibold">agent-terminal</span>
              </div>
              
              {/* Sequence lines */}
              <div className="flex-1 space-y-3 mt-4 text-left">
                <div className="seq-1 opacity-0 text-[#a8a8a8]">
                  <span className="text-[#00f0ff]">$</span> agent run task --id 8492
                </div>
                <div className="seq-2 opacity-0 text-[#e5e2e1]">
                  [Agent] Planning steps...
                  <br/>
                  [Agent] Attempting to execute: <span className="text-red-400">rm -rf /var/www/*</span>
                </div>
                <div className="seq-3 opacity-0 mt-4 rounded border border-[#e8ff47]/50 bg-[#e8ff47]/10 p-3 text-[#e8ff47]">
                  ⚠️ AGENTWATCH INTERCEPT ⚠️
                  <br/>
                  <span className="text-[#a8a8a8]">Holding execution for reasoning audit...</span>
                </div>
                <div className="seq-4 opacity-0 text-[#00f0ff] mt-2">
                  [Auditor] Semantic Risk Score: 98/100
                  <br/>
                  [Auditor] Verdict: <span className="text-red-500 font-bold">DESTRUCTIVE_ACTION</span>
                </div>
                <div className="seq-5 opacity-0 mt-2 p-2 bg-red-500/20 border border-red-500/50 text-red-500 font-bold text-center uppercase tracking-widest">
                  Action Blocked Pre-Execution
                </div>
              </div>
            </div>

            {/* Video Controls Overlay */}
            <div className="absolute inset-x-0 bottom-0 p-4 bg-gradient-to-t from-black/90 to-transparent flex flex-col gap-3 translate-y-full group-hover:translate-y-0 transition-transform duration-300">
              {/* Progress Bar */}
              <div className="h-1.5 w-full bg-white/20 rounded-full overflow-hidden">
                <div className="video-progress h-full bg-[#e8ff47] w-0" />
              </div>
              <div className="flex justify-between items-center text-[#888] text-xs font-mono">
                <div className="flex items-center gap-3">
                  <svg className="w-5 h-5 text-white cursor-pointer hover:text-[#e8ff47] transition-colors" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7z" />
                  </svg>
                  <span className="video-time">0:00</span>
                </div>
                <span>0:05</span>
              </div>
            </div>

            {/* Play Button Overlay (fades out when "playing") */}
            <div className="play-overlay absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-20 pointer-events-none">
              <div className="w-16 h-16 rounded-full bg-[#e8ff47] flex items-center justify-center shadow-[0_0_30px_rgba(232,255,71,0.4)]">
                <svg className="w-8 h-8 text-black ml-1" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M8 5v14l11-7z" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

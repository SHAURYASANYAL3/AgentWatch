"use client";

import { useEffect, useRef } from "react";
import Image from "next/image";
import gsap from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

// Mocked data for contributors based on user request.
const CONTRIBUTORS = [
  {
    username: "SHAURYASANYAL3",
    avatarUrl: "https://avatars.githubusercontent.com/u/128920982?v=4",
    role: "Creator & Maintainer",
    stats: {
      commits: 12,
      prs: 16,
      issues: 27
    },
    specialContribution: "Architected AgentWatch and built the core foundation.",
    highlights: [
      "PR #480: Feature/new landing UI",
      "PR #455: test(cli): Add tests and benchmarks",
      "PR #454: feat(cli): Add core CLI logic"
    ]
  },
  {
    username: "sreerevanth",
    avatarUrl: "https://avatars.githubusercontent.com/u/86904394?v=4",
    role: "Core Contributor",
    stats: {
      commits: 39,
      prs: 2,
      issues: 1
    },
    specialContribution: "Actively contributed to AgentWatch with 39 commits and 2 PRs.",
    highlights: [
      "PR #410: Create SECURITY.md",
      "PR #409: Create CODE_OF_CONDUCT.md"
    ]
  },
  {
    username: "Prateeks16",
    avatarUrl: "https://avatars.githubusercontent.com/u/153312544?v=4",
    role: "Contributor",
    stats: {
      commits: 11,
      prs: 11,
      issues: 0
    },
    specialContribution: "Actively contributed to AgentWatch with 11 commits and 11 PRs.",
    highlights: [
      "PR #450: feat(governance): tamper-evident audit log for RBAC",
      "PR #449: fix(cli): route all session subcommands through one Typer group",
      "PR #445: fix: break governance↔tracing circular import"
    ]
  },
  {
    username: "pavsoss",
    avatarUrl: "https://avatars.githubusercontent.com/u/230380953?v=4",
    role: "Contributor",
    stats: {
      commits: 12,
      prs: 3,
      issues: 2
    },
    specialContribution: "Actively contributed to AgentWatch with 12 commits and 3 PRs.",
    highlights: [
      "PR #458: feat(telemetry): enterprise OTLP reasoning trace export",
      "PR #407: feat(mcp): expose AgentWatch observability tools through MCP",
      "PR #404: feat(loop-detector): make loop threshold configurable"
    ]
  },
  {
    username: "anshul23102",
    avatarUrl: "https://avatars.githubusercontent.com/u/167362756?v=4",
    role: "Contributor",
    stats: {
      commits: 17,
      prs: 0,
      issues: 0
    },
    specialContribution: "Actively contributed to AgentWatch with 17 commits and 0 PRs.",
    highlights: [
      "Consistently improved codebase quality and reliability."
    ]
  },
  {
    username: "DebasmitaBose0",
    avatarUrl: "https://avatars.githubusercontent.com/u/144198639?v=4",
    role: "Contributor",
    stats: {
      commits: 15,
      prs: 0,
      issues: 2
    },
    highlights: [
      "Issue #382: Implement Semantic Cache for Repeated LLM Subtasks",
      "Issue #381: Implement HIPAA Compliance Mode with PHI Auto-Redaction"
    ],
    specialContribution: "Actively contributed to AgentWatch with 15 commits and 2 issues."
  },
  {
    username: "SakethSumanBathini",
    avatarUrl: "https://avatars.githubusercontent.com/u/178634012?v=4",
    role: "Contributor",
    stats: {
      commits: 7,
      prs: 4,
      issues: 0
    },
    highlights: [
      "PR #387: feat(api): wire CMP-005 SAML/RBAC enforcement into the API layer",
      "PR #386: feat(memory): add MEM-008 natural language causal-graph traversal",
      "PR #384: fix(security): resolve all 13 bandit warnings"
    ],
    specialContribution: "Actively contributed to AgentWatch with 7 commits and 4 PRs."
  },
  {
    username: "arcgod-design",
    avatarUrl: "https://avatars.githubusercontent.com/u/225413120?v=4",
    role: "Contributor",
    stats: {
      commits: 1,
      prs: 6,
      issues: 0
    },
    highlights: [
      "PR #460: feat: multi-tenant cloud architecture for AgentWatch Cloud",
      "PR #439: feat: allow custom session metadata enrichment in watch() API",
      "PR #438: feat: support exporting compliance audit logs as CSV"
    ],
    specialContribution: "Actively contributed to AgentWatch with 1 commits and 6 PRs."
  },
  {
    username: "prachishelke1312",
    avatarUrl: "https://avatars.githubusercontent.com/u/228935308?v=4",
    role: "Contributor",
    stats: {
      commits: 5,
      prs: 2,
      issues: 0
    },
    highlights: [
      "PR #408: refactor: reduce verbose Claude Code debug logging",
      "PR #392: refactor: reduce verbose Claude Code debug logging"
    ],
    specialContribution: "Actively contributed to AgentWatch with 5 commits and 2 PRs."
  },
  {
    username: "SHUBHAM2775",
    avatarUrl: "https://avatars.githubusercontent.com/u/161486999?v=4",
    role: "Contributor",
    stats: {
      commits: 7,
      prs: 0,
      issues: 0
    },
    highlights: [
      "Consistently improved codebase quality and reliability."
    ],
    specialContribution: "Actively contributed to AgentWatch with 7 commits and 0 PRs."
  }
];

export default function ContributorsPage() {
  const pageRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (prefersReduced) return;

    const ctx = gsap.context(() => {
      // Glitch Intro
      gsap.fromTo(".glitch-text", 
        { opacity: 0, scale: 1.1, filter: "blur(10px)" },
        { opacity: 1, scale: 1, filter: "blur(0px)", duration: 1.5, ease: "expo.out" }
      );

      // Top 3 Entrance
      gsap.fromTo(".elite-card", 
        { y: 100, opacity: 0, rotationX: 20 },
        { y: 0, opacity: 1, rotationX: 0, duration: 1.5, stagger: 0.2, ease: "power4.out" }
      );

      // List Entrance
      gsap.fromTo(".list-row",
        { x: -50, opacity: 0 },
        { x: 0, opacity: 1, duration: 0.8, stagger: 0.05, ease: "power2.out", scrollTrigger: { trigger: ".list-container", start: "top 80%" } }
      );
    }, pageRef);

    return () => ctx.revert();
  }, []);

  const top3 = CONTRIBUTORS.slice(0, 3);
  const rest = CONTRIBUTORS.slice(3);

  return (
    <main ref={pageRef} className="relative min-h-screen pt-32 pb-32 px-4 sm:px-6 overflow-hidden bg-[#050505] text-[#ededed] selection:bg-[#e8ff47]/30 selection:text-[#e8ff47]">
      {/* Background */}
      <div className="absolute inset-0 z-0 pointer-events-none" style={{
        backgroundImage: "linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px)",
        backgroundSize: "40px 40px",
        backgroundPosition: "center center",
      }} />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1200px] h-[600px] bg-[#00f0ff] rounded-full blur-[200px] opacity-[0.05] pointer-events-none z-0" />
      <div className="absolute bottom-0 right-0 w-[800px] h-[800px] bg-[#e8ff47] rounded-full blur-[200px] opacity-[0.03] pointer-events-none z-0" />
      <div className="absolute inset-0 bg-[url('/noise.png')] opacity-[0.04] pointer-events-none mix-blend-overlay z-0" />

      <div className="max-w-[1200px] mx-auto relative z-10">
        <header className="mb-24 text-center">
          <div className="inline-block px-4 py-1.5 rounded-full border border-[#00f0ff]/30 bg-[#00f0ff]/10 text-[#00f0ff] text-xs font-mono font-bold uppercase tracking-[0.3em] mb-6 shadow-[0_0_20px_rgba(0,240,255,0.2)]">
            SYSTEM_OPERATORS
          </div>
          <h1
            className="glitch-text font-black uppercase leading-[0.9] tracking-tighter"
            style={{
              fontFamily: "var(--font-syne)",
              fontSize: "clamp(3rem, 8vw, 7rem)",
              background: "linear-gradient(180deg, #ffffff 0%, #a8a8a8 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              filter: "drop-shadow(0 10px 20px rgba(0,0,0,0.5))"
            }}
          >
            Hall of <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#e8ff47] to-[#00f0ff]">Fame</span>
          </h1>
        </header>

        {/* TOP 3 ELITES */}
        <div className="mb-32">
          <h2 className="text-2xl font-bold font-mono text-white mb-10 border-b border-white/10 pb-4 flex items-center gap-4">
            <span className="w-3 h-3 bg-[#e8ff47] shadow-[0_0_10px_#e8ff47]" /> 
            ELITE VANGUARD // RANK 01 - 03
          </h2>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {top3.map((c, i) => (
              <div
                key={c.username}
                className={`elite-card group relative p-1 rounded-2xl bg-gradient-to-b from-white/10 to-transparent overflow-hidden ${i === 0 ? "lg:col-span-2" : ""}`}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-[#00f0ff]/20 via-transparent to-[#e8ff47]/20 opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
                
                <div className={`relative h-full bg-[#0a0a0a] rounded-xl border border-black p-6 sm:p-10 flex flex-col ${i === 0 ? "lg:flex-row items-center gap-10" : "gap-6"}`}>
                  
                  {/* Rank Badge */}
                  <div className="absolute top-0 right-0 px-6 py-2 bg-[#e8ff47] text-black font-black font-mono text-xl sm:text-3xl rounded-bl-3xl shadow-[0_0_30px_#e8ff47]">
                    #{i + 1}
                  </div>

                  {/* Avatar Area */}
                  <div className="relative shrink-0">
                    <div className={`relative ${i === 0 ? "w-32 h-32 sm:w-48 sm:h-48" : "w-24 h-24 sm:w-32 sm:h-32"} rounded-full border-4 border-[#050505] z-10 overflow-hidden`}>
                      <img src={c.avatarUrl} alt={c.username} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
                    </div>
                    {/* Ring glow */}
                    <div className="absolute inset-[-10px] rounded-full border border-[#00f0ff]/50 animate-[spin_10s_linear_infinite]" border-style="dashed" />
                    <div className="absolute inset-[-20px] rounded-full border border-[#e8ff47]/30 animate-[spin_15s_linear_infinite_reverse]" border-style="dotted" />
                  </div>

                  {/* Content Area */}
                  <div className="flex-1 flex flex-col justify-center">
                    <div className="mb-6">
                      <h3 className="font-bold text-3xl sm:text-5xl text-white mb-2" style={{ fontFamily: "var(--font-syne)" }}>
                        {c.username}
                      </h3>
                      <div className="text-[#00f0ff] font-mono tracking-widest text-sm uppercase">
                        &gt; {c.role}
                      </div>
                    </div>

                    <div className="grid grid-cols-3 gap-4 mb-8">
                      <div className="bg-[#050505] border border-white/5 p-4 rounded-lg">
                        <div className="text-3xl font-black text-white">{c.stats.commits}</div>
                        <div className="text-[10px] uppercase tracking-widest text-[#888]">Commits</div>
                      </div>
                      <div className="bg-[#050505] border border-white/5 p-4 rounded-lg">
                        <div className="text-3xl font-black text-white">{c.stats.prs}</div>
                        <div className="text-[10px] uppercase tracking-widest text-[#888]">PRs</div>
                      </div>
                      <div className="bg-[#050505] border border-white/5 p-4 rounded-lg">
                        <div className="text-3xl font-black text-white">{c.stats.issues}</div>
                        <div className="text-[10px] uppercase tracking-widest text-[#888]">Issues</div>
                      </div>
                    </div>

                    <div className="text-[#a8a8a8] font-mono text-sm leading-relaxed mb-6 border-l-2 border-[#e8ff47] pl-4">
                      {c.specialContribution}
                    </div>

                    <a
                      href={`https://github.com/${c.username}`}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-2 text-[#00f0ff] hover:text-[#e8ff47] font-bold uppercase tracking-widest text-xs transition-colors"
                    >
                      <span>Access File</span>
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                      </svg>
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* THE CORE OPERATORS - TERMINAL LIST */}
        <div className="list-container relative">
          <h2 className="text-2xl font-bold font-mono text-white mb-10 border-b border-white/10 pb-4 flex items-center gap-4">
            <span className="w-3 h-3 bg-[#00f0ff] shadow-[0_0_10px_#00f0ff]" /> 
            CORE OPERATORS // INITIATIVES
          </h2>

          <div className="flex flex-col gap-3">
            {/* Table Header */}
            <div className="hidden md:grid grid-cols-12 gap-4 px-6 py-3 text-xs font-mono font-bold text-[#555] uppercase tracking-widest border-b border-white/5">
              <div className="col-span-1">Rank</div>
              <div className="col-span-4">Operator</div>
              <div className="col-span-2 text-center">Commits</div>
              <div className="col-span-2 text-center">PRs</div>
              <div className="col-span-2 text-center">Issues</div>
              <div className="col-span-1 text-right">Link</div>
            </div>

            {rest.map((c, i) => (
              <a
                key={c.username}
                href={`https://github.com/${c.username}`}
                target="_blank"
                rel="noreferrer"
                className="list-row group grid grid-cols-1 md:grid-cols-12 gap-4 items-center p-4 sm:px-6 sm:py-4 bg-[#0a0a0a] border border-white/5 hover:border-[#00f0ff]/50 rounded-xl hover:bg-[#00f0ff]/5 transition-all duration-300"
              >
                <div className="col-span-1 font-mono text-[#888] font-bold text-lg hidden md:block">
                  {(i + 4).toString().padStart(2, '0')}
                </div>
                
                <div className="col-span-1 md:col-span-4 flex items-center gap-4">
                  <img src={c.avatarUrl} alt={c.username} className="w-12 h-12 rounded-full border border-white/10 group-hover:border-[#00f0ff] transition-colors" />
                  <div>
                    <div className="font-bold text-white text-lg group-hover:text-[#00f0ff] transition-colors">{c.username}</div>
                    <div className="text-xs text-[#888] font-mono uppercase truncate">{c.role}</div>
                  </div>
                </div>

                <div className="col-span-1 md:col-span-2 flex justify-between md:block md:text-center">
                  <span className="md:hidden text-xs text-[#555] font-mono uppercase">Commits</span>
                  <span className="font-mono font-bold text-white">{c.stats.commits}</span>
                </div>
                
                <div className="col-span-1 md:col-span-2 flex justify-between md:block md:text-center">
                  <span className="md:hidden text-xs text-[#555] font-mono uppercase">PRs</span>
                  <span className="font-mono font-bold text-white">{c.stats.prs}</span>
                </div>
                
                <div className="col-span-1 md:col-span-2 flex justify-between md:block md:text-center">
                  <span className="md:hidden text-xs text-[#555] font-mono uppercase">Issues</span>
                  <span className="font-mono font-bold text-white">{c.stats.issues}</span>
                </div>

                <div className="col-span-1 hidden md:flex justify-end text-[#555] group-hover:text-[#e8ff47] transition-colors">
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="square" strokeLinejoin="miter" strokeWidth={1.5} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </div>
              </a>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}

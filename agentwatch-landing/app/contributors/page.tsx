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
      gsap.from(".hero-content > *", {
        y: 30,
        opacity: 0,
        duration: 0.9,
        stagger: 0.15,
        ease: "power3.out",
      });

      gsap.from(".contributor-card", {
        y: 40,
        opacity: 0,
        duration: 0.8,
        stagger: 0.2,
        ease: "power3.out",
        scrollTrigger: {
          trigger: ".contributors-grid",
          start: "top 80%",
          once: true,
        },
      });
    }, pageRef);

    return () => ctx.revert();
  }, []);

  return (
    <main ref={pageRef} className="relative min-h-screen pt-32 pb-24 px-6 overflow-hidden">
      {/* Background elements */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-[#e8ff47] rounded-full blur-[150px] opacity-[0.05] pointer-events-none z-0" />
      <div className="absolute inset-0 bg-[url('/noise.png')] opacity-20 pointer-events-none mix-blend-overlay z-0" />

      <div className="max-w-[1000px] mx-auto relative z-10">
        <section className="mb-20 text-center hero-content">
          <h1
            className="font-bold leading-[1.08] mb-5"
            style={{
              fontFamily: "var(--font-syne)",
              fontSize: "clamp(2rem, 5.2vw, 4rem)",
              background: "linear-gradient(135deg, #ffffff 0%, #e8ff47 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              backgroundClip: "text",
              textWrap: "balance",
            }}
          >
            Hall of Fame
          </h1>
          <p
            className="text-[#b8b8b8] max-w-xl mx-auto font-light"
            style={{ fontSize: "clamp(1rem, 2vw, 1.125rem)" }}
          >
            AgentWatch is built by an incredible open-source community. Here are the people making it happen.
          </p>
        </section>

        <div className="contributors-grid grid grid-cols-1 md:grid-cols-2 gap-6">
          {CONTRIBUTORS.map((c, i) => (
            <div
              key={c.username}
              className="contributor-card dark-glass rounded-2xl p-6 sm:p-8 flex flex-col h-full border border-white/5 relative group"
            >
              {/* Highlight gradient on hover */}
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-[#00f0ff]/10 to-[#e8ff47]/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />

              <div className="flex items-center gap-4 mb-6 relative z-10">
                <div className="relative w-16 h-16 rounded-full p-[2px] bg-gradient-to-br from-[#00f0ff] to-[#e8ff47]">
                  <Image
                    src={c.avatarUrl}
                    alt={c.username}
                    fill
                    className="rounded-full object-cover border-2 border-[#050505]"
                    unoptimized
                  />
                </div>
                <div>
                  <h3
                    className="font-bold text-xl text-white mb-1"
                    style={{ fontFamily: "var(--font-syne)" }}
                  >
                    @{c.username}
                  </h3>
                  <div
                    className="text-xs uppercase tracking-widest text-[#e8ff47]"
                    style={{ fontFamily: "var(--font-jetbrains)" }}
                  >
                    {c.role}
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2 mb-6 relative z-10">
                <div className="bg-black/40 rounded-lg p-3 text-center border border-white/5">
                  <div className="text-xl font-bold text-white mb-1">{c.stats.commits}</div>
                  <div className="text-[10px] uppercase text-[#888] tracking-wider">Commits</div>
                </div>
                <div className="bg-black/40 rounded-lg p-3 text-center border border-white/5">
                  <div className="text-xl font-bold text-white mb-1">{c.stats.prs}</div>
                  <div className="text-[10px] uppercase text-[#888] tracking-wider">PRs</div>
                </div>
                <div className="bg-black/40 rounded-lg p-3 text-center border border-white/5">
                  <div className="text-xl font-bold text-white mb-1">{c.stats.issues}</div>
                  <div className="text-[10px] uppercase text-[#888] tracking-wider">Issues</div>
                </div>
              </div>

              <div className="flex-1 relative z-10">
                <p className="text-sm text-[#e5e2e1] mb-4 leading-relaxed">
                  <span className="font-semibold text-[#00f0ff]">Special Contribution: </span>
                  {c.specialContribution}
                </p>

                <div className="space-y-2 mt-4">
                  <p className="text-xs font-semibold text-[#888] uppercase tracking-wider mb-3">Notable Work</p>
                  {c.highlights.map((h, index) => (
                    <div key={index} className="flex items-start gap-2 text-sm text-[#a8a8a8]">
                      <svg className="w-4 h-4 text-[#e8ff47] flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="leading-snug">{h}</span>
                    </div>
                  ))}
                </div>
              </div>

              <a
                href={`https://github.com/${c.username}`}
                target="_blank"
                rel="noreferrer"
                className="mt-6 w-full text-center py-2.5 rounded-lg border border-white/10 hover:border-[#00f0ff]/50 hover:text-[#00f0ff] transition-colors text-xs font-medium uppercase tracking-widest relative z-10"
                style={{ fontFamily: "var(--font-jetbrains)" }}
              >
                View Profile
              </a>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}

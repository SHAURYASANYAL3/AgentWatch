"use client";

import { useEffect, useRef } from "react";
import Image from "next/image";
import gsap from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

// Mocked data for contributors based on user request.
const CONTRIBUTORS = [
  {
    username: "sreerevanth",
    avatarUrl: "https://github.com/sreerevanth.png",
    role: "Creator & Maintainer",
    stats: {
      commits: 154,
      prs: 23,
      issues: 45,
    },
    specialContribution: "Architected the core reasoning auditor, causal memory graph, and live dashboard.",
    highlights: [
      "Implemented git-backed rollback for agent state",
      "Built the independent reasoning auditor model",
      "Designed the pre-execution safety engine"
    ]
  },
  {
    username: "johndoe",
    avatarUrl: "https://github.com/github.png",
    role: "Core Contributor",
    stats: {
      commits: 42,
      prs: 15,
      issues: 12,
    },
    specialContribution: "Led the implementation of the MCP server integration and LangGraph adapter.",
    highlights: [
      "Added support for LangGraph framework (PR #12)",
      "Fixed critical memory leak in event loop (Issue #34)",
      "Built the MCP server schema validation"
    ]
  },
  {
    username: "janedoe",
    avatarUrl: "https://github.com/octocat.png",
    role: "Contributor",
    stats: {
      commits: 18,
      prs: 5,
      issues: 8,
    },
    specialContribution: "Revamped the testing suite and added 100+ unit tests for safety rules.",
    highlights: [
      "Integrated pytest-asyncio for concurrent tests (PR #28)",
      "Identified and fixed prompt injection bypass (Issue #41)",
      "Added CI/CD workflows for automated publishing"
    ]
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

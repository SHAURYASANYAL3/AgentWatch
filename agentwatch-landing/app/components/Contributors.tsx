"use client";

import { useEffect, useState } from "react";

interface Contributor {
  login: string;
  avatar_url: string;
  html_url: string;
}

export default function Contributors() {
  const [contributors, setContributors] = useState<Contributor[]>([]);

  useEffect(() => {
    fetch("https://api.github.com/repos/sreerevanth/agentwatch/contributors")
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) setContributors(data);
      })
      .catch((err) => console.error("Error fetching contributors:", err));
  }, []);

  return (
    <section className="relative z-10 py-32 px-6 max-w-7xl mx-auto border-t border-white/5 text-center">
      <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4 text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-500">
        Built by the community.
      </h2>
      <p className="text-[#888] font-mono text-xs uppercase tracking-[0.2em] mb-12">Join us on GitHub</p>

      <div className="flex flex-wrap justify-center gap-4 mb-16">
        {contributors.map((c) => (
          <a
            key={c.login}
            href={c.html_url}
            target="_blank"
            rel="noopener noreferrer"
            className="group relative"
          >
            <div className="w-14 h-14 rounded-full border border-white/10 bg-[#0a0a0a] overflow-hidden hover:border-[#00f0ff] transition-colors relative z-10">
              <img src={c.avatar_url} alt={c.login} className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all" />
            </div>
            {/* Tooltip */}
            <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-black border border-white/10 text-xs text-white px-2 py-1 rounded whitespace-nowrap z-20 font-mono pointer-events-none">
              {c.login}
            </div>
          </a>
        ))}
      </div>
      
      <div className="flex justify-center mt-8">
        <a
          href="/contributors"
          className="btn-magnetic px-8 py-3 rounded-full bg-[#111] border border-[#e8ff47]/30 text-[#e8ff47] font-semibold text-sm hover:bg-[#e8ff47]/10 transition-colors uppercase tracking-widest inline-block"
          style={{ fontFamily: "var(--font-jetbrains)" }}
        >
          View Hall of Fame
        </a>
      </div>
    </section>
  );
}

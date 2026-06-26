export default function AboutCreator() {
  return (
    <section className="relative z-10 py-32 px-6 max-w-7xl mx-auto border-t border-white/5">
      <div className="flex flex-col lg:flex-row gap-12 items-center">
        <div className="flex-1 w-full flex justify-center">
          <div className="w-64 h-64 rounded-full border-2 border-[#e8ff47] bg-[#0c0c0c] flex items-center justify-center overflow-hidden shadow-[0_0_40px_rgba(232,255,71,0.15)] relative">
            <div className="absolute inset-0 bg-gradient-to-tr from-[#00f0ff]/20 to-[#e8ff47]/20" />
            <span className="text-white/50 text-sm font-mono tracking-widest relative z-10 uppercase">
              Creator Avatar
            </span>
          </div>
        </div>
        <div className="flex-1 w-full text-center lg:text-left">
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight mb-4 text-white">
            Meet the Creator
          </h2>
          <div className="w-12 h-1 bg-gradient-to-r from-[#00f0ff] to-[#e8ff47] mx-auto lg:mx-0 mb-8 rounded-full" />
          <div className="text-[#888] leading-relaxed mb-6 space-y-4 text-sm">
            <p>
              I'm a developer focused on AI systems, developer tools, open-source software, and building technology that solves real-world problems.
            </p>
            <p>
              I'm the creator of AgentWatch and founder of VoidSwift, exploring challenges around AI reliability, transparency, and agentic systems. I strongly believe that the best way to grow as an engineer is to build in public and contribute to real projects.
            </p>
            <p className="font-mono text-xs uppercase tracking-widest text-white mt-8">
              Founder @VoidSwift • Creator of AgentWatch • Open Source Maintainer
              <br/><br/>
              <span className="text-[#e8ff47]">Ideas welcome. PRs preferred.</span>
            </p>
            <div className="pt-4">
              <a href="/about" className="inline-flex items-center gap-2 text-[#00f0ff] hover:text-white transition-colors font-mono text-sm uppercase tracking-widest">
                Read full bio →
              </a>
            </div>
          </div>
          <a href="#" className="inline-flex items-center gap-2 text-[#00f0ff] hover:text-white transition-colors font-mono text-sm uppercase tracking-widest">
            Follow on X
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-4 h-4">
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </a>
        </div>
      </div>
    </section>
  );
}

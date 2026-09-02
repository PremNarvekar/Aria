import React, { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { Shield } from 'lucide-react';

export default function ReportPanel({ session }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current) {
      gsap.fromTo(
        containerRef.current.children,
        { opacity: 0, y: 15 },
        { opacity: 1, y: 0, duration: 0.8, stagger: 0.15, ease: "power3.out" }
      );
    }
  }, [session]);

  if (!session) return null;

  return (
    <div ref={containerRef} className="space-y-24">
      
      {/* Executive Summary */}
      <section className="report-section pt-12 border-t border-gray-200 relative">
        {/* Subtle grid in background of summary */}
        <div className="absolute inset-0 bg-dots opacity-20 pointer-events-none -z-10"></div>
        <p className="text-gray-900 text-2xl md:text-3xl leading-[1.4] font-sans font-light tracking-tight">
          {session.summary}
        </p>
      </section>

      {/* Key Findings with huge dot-matrix numbers */}
      {session.findings && session.findings.length > 0 && (
        <section className="report-section pt-12 border-t border-gray-200">
          <h3 className="text-xs font-pixel text-gray-400 uppercase tracking-widest mb-12">Key Findings</h3>
          
          <div className="flex flex-col gap-12">
            {session.findings.map((finding, idx) => (
              <div key={idx} className="flex flex-col md:flex-row gap-6 md:gap-12 items-start">
                <div className="md:w-32 shrink-0">
                  <span className="font-pixel text-5xl md:text-6xl text-gray-900 leading-none">0{idx + 1}</span>
                </div>
                <div className="flex-1">
                  <p className="text-gray-800 leading-relaxed font-sans font-light text-xl md:text-2xl">{finding}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Evidence & Claims */}
      {session.claims && session.claims.length > 0 && (
        <section className="report-section pt-12 border-t border-gray-200">
          <h3 className="text-xs font-pixel text-gray-400 uppercase tracking-widest mb-12">Evidence Verification</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-gray-200 border border-gray-200 rounded-sm overflow-hidden">
            {session.claims.map((claim, idx) => (
              <div key={claim.id} className="bg-white p-8 hover:bg-gray-50/50 transition-colors">
                <div className="flex items-center gap-3 mb-6">
                  <Shield className="w-4 h-4 text-gray-900" />
                  <span className="text-xs font-pixel text-gray-900 uppercase tracking-wider">Verified Claim</span>
                </div>
                <p className="font-sans font-medium text-gray-900 mb-6 leading-relaxed text-lg">{claim.text}</p>
                <div className="border-l-2 border-gray-900 pl-4">
                  <p className="text-sm text-gray-500 font-sans font-light leading-relaxed italic">
                    "{claim.evidence}"
                  </p>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Full Report */}
      <section className="report-section pt-12 border-t border-gray-200">
        <h3 className="text-xs font-pixel text-gray-400 uppercase tracking-widest mb-12">Full Analysis</h3>
        
        <div className="prose prose-gray prose-lg max-w-none prose-headings:font-sans prose-headings:font-light prose-headings:tracking-tight prose-a:text-blue-600 hover:prose-a:text-blue-500">
          {session.report.split('\n').map((line, i) => {
            if (line.startsWith('## ')) {
              return <h2 key={i} className="mt-16 mb-8 text-3xl text-gray-900">{line.replace('## ', '')}</h2>;
            } else if (line.startsWith('- ')) {
              const content = line.replace('- ', '');
              const parts = content.split(/\*\*(.*?)\*\*/g);
              return (
                <li key={i} className="mb-4 text-gray-700 leading-relaxed font-sans font-light">
                  {parts.map((part, j) => j % 2 === 1 ? <strong key={j} className="text-gray-900 font-medium">{part}</strong> : part)}
                </li>
              );
            } else if (line.trim() !== '') {
              return <p key={i} className="mb-6 text-gray-700 leading-relaxed font-sans font-light">{line}</p>;
            }
            return null;
          })}
        </div>
      </section>
    </div>
  );
}

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
      <section className="report-section">
        <p className="text-gray-900 text-xl md:text-2xl leading-[1.6] font-medium tracking-tight">
          {session.summary}
        </p>
      </section>

      {/* Key Findings */}
      {session.findings && session.findings.length > 0 && (
        <section className="report-section pt-12 border-t border-gray-100">
          <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-10">Key Findings</h3>
          
          <div className="flex flex-col gap-10">
            {session.findings.map((finding, idx) => (
              <div key={idx} className="flex gap-6">
                <div className="w-8 shrink-0 flex justify-center mt-1">
                  <div className="w-1.5 h-1.5 rounded-full bg-gray-300"></div>
                </div>
                <div className="flex-1">
                  <p className="text-gray-800 leading-relaxed font-medium text-lg">{finding}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Evidence & Claims */}
      {session.claims && session.claims.length > 0 && (
        <section className="report-section pt-12 border-t border-gray-100">
          <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-10">Evidence Verification</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {session.claims.map((claim, idx) => (
              <div key={claim.id} className="bg-gray-50 rounded-2xl p-6 border border-gray-100/50 hover:shadow-sm transition-shadow">
                <div className="flex items-center gap-3 mb-4">
                  <Shield className="w-4 h-4 text-gray-400" />
                  <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Verified Claim</span>
                </div>
                <p className="font-semibold text-gray-900 mb-3 leading-snug">{claim.text}</p>
                <p className="text-sm text-gray-500 font-medium leading-relaxed italic border-l-2 border-gray-200 pl-4">
                  "{claim.evidence}"
                </p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Full Report */}
      <section className="report-section pt-12 border-t border-gray-100">
        <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-10">Full Analysis</h3>
        
        <div className="prose prose-gray prose-lg max-w-none prose-headings:font-semibold prose-headings:tracking-tight prose-a:text-blue-600 hover:prose-a:text-blue-500">
          {session.report.split('\n').map((line, i) => {
            if (line.startsWith('## ')) {
              return <h2 key={i} className="mt-16 mb-6 text-2xl text-gray-900">{line.replace('## ', '')}</h2>;
            } else if (line.startsWith('- ')) {
              const content = line.replace('- ', '');
              const parts = content.split(/\*\*(.*?)\*\*/g);
              return (
                <li key={i} className="mb-3 text-gray-700 leading-relaxed font-medium">
                  {parts.map((part, j) => j % 2 === 1 ? <strong key={j} className="text-gray-900">{part}</strong> : part)}
                </li>
              );
            } else if (line.trim() !== '') {
              return <p key={i} className="mb-6 text-gray-700 leading-relaxed font-medium">{line}</p>;
            }
            return null;
          })}
        </div>
      </section>
    </div>
  );
}

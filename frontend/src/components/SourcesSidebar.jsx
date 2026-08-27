import React from 'react';
import { ExternalLink } from 'lucide-react';

export default function SourcesSidebar({ session }) {
  if (!session || !session.sources) return null;

  return (
    <div className="h-full p-6 sm:p-10 relative">
      <div className="flex items-center gap-3 mb-10">
        <div className="w-2 h-2 bg-gray-900"></div>
        <h3 className="font-mono text-xs font-bold text-gray-900 uppercase tracking-widest">Bibliography</h3>
      </div>

      <div className="flex flex-col gap-8">
        {session.sources.map((source, idx) => (
          <a 
            key={idx} 
            href={source.url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="group block"
          >
            <div className="flex gap-4 items-start">
              <span className="font-mono text-xs text-gray-400 font-bold mt-1 shrink-0">[{String(idx + 1).padStart(2, '0')}]</span>
              <div>
                <h4 className="text-sm font-bold text-gray-900 group-hover:text-accent flex items-center gap-2 mb-2 transition-colors">
                  {source.title}
                  <ExternalLink className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                </h4>
                <p className="text-xs text-gray-500 mb-3 leading-relaxed font-medium">
                  {source.snippet}
                </p>
                <div className="flex items-center gap-3 text-[10px] font-mono text-gray-400 uppercase font-bold tracking-wider">
                  <span className="text-accent">{new URL(source.url).hostname.replace('www.', '')}</span>
                  <span className="w-1 h-1 bg-gray-200"></span>
                  <span>{source.relevance}% Match</span>
                </div>
              </div>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}

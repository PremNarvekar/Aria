import React from 'react';
import { ExternalLink } from 'lucide-react';

export default function SourcesSidebar({ session }) {
  if (!session || !session.sources) return null;

  return (
    <div className="h-full p-6 sm:p-10 relative">
      <div className="mb-16">
        <h3 className="text-xs font-pixel text-gray-400 uppercase tracking-widest">Bibliography</h3>
      </div>

      <div className="flex flex-col gap-10">
        {session.sources.map((source, idx) => (
          <a 
            key={idx} 
            href={source.url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="group block relative pl-6 border-l border-gray-200 hover:border-gray-900 transition-colors duration-300"
          >
            {/* Tiny dot on hover */}
            <div className="absolute left-[-2px] top-1.5 w-[3px] h-[3px] bg-gray-900 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            
            <div className="flex flex-col gap-2">
              <span className="font-pixel text-xs text-gray-400">[{String(idx + 1).padStart(2, '0')}]</span>
              <h4 className="text-sm font-sans font-medium text-gray-900 flex items-center gap-2 mb-1">
                {source.title}
                <ExternalLink className="w-3 h-3 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" />
              </h4>
              <p className="text-xs text-gray-500 mb-3 leading-relaxed font-sans font-light">
                {source.snippet}
              </p>
              <div className="flex items-center gap-3 text-[10px] font-pixel text-gray-400 uppercase tracking-wider">
                <span className="text-gray-900">{new URL(source.url).hostname.replace('www.', '')}</span>
                <span className="w-1 h-1 bg-gray-200"></span>
                <span>{source.relevance}% Match</span>
              </div>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}

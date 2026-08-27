import React, { useState, useEffect } from 'react';
import { Sparkles } from 'lucide-react';

export default function AgentTrace({ currentStep }) {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (currentStep && !history.includes(currentStep)) {
      setHistory(prev => [...prev, currentStep]);
    }
  }, [currentStep, history]);

  return (
    <div className="w-full flex flex-col items-center justify-center p-8 md:p-16 relative min-h-[500px]">
      
      {/* Network Animation SVG */}
      <div className="relative w-64 h-64 mb-16 flex items-center justify-center">
        {/* Subtle background glow */}
        <div className="absolute inset-0 bg-gray-100 rounded-full blur-3xl opacity-50"></div>
        
        <svg className="absolute inset-0 w-full h-full animate-[spin_30s_linear_infinite]" viewBox="0 0 200 200">
          {/* Connecting Lines */}
          <line x1="100" y1="100" x2="150" y2="40" stroke="currentColor" className="text-gray-200 animate-pulse" strokeWidth="1" />
          <line x1="100" y1="100" x2="40" y2="60" stroke="currentColor" className="text-gray-200 animate-pulse" strokeWidth="1" style={{animationDelay: '200ms'}} />
          <line x1="100" y1="100" x2="60" y2="160" stroke="currentColor" className="text-gray-200 animate-pulse" strokeWidth="1" style={{animationDelay: '400ms'}} />
          <line x1="100" y1="100" x2="160" y2="140" stroke="currentColor" className="text-gray-200 animate-pulse" strokeWidth="1" style={{animationDelay: '600ms'}} />
          
          {/* Secondary connections (constellation effect) */}
          <line x1="150" y1="40" x2="160" y2="140" stroke="currentColor" className="text-gray-100" strokeWidth="0.5" strokeDasharray="4" />
          <line x1="40" y1="60" x2="60" y2="160" stroke="currentColor" className="text-gray-100" strokeWidth="0.5" strokeDasharray="4" />

          {/* Orbiting Nodes */}
          {/* Top Right Node */}
          <circle cx="150" cy="40" r="4" fill="currentColor" className="text-gray-200 animate-ping" />
          <circle cx="150" cy="40" r="4" fill="currentColor" className="text-gray-400" />
          
          {/* Top Left Node */}
          <circle cx="40" cy="60" r="3" fill="currentColor" className="text-gray-200 animate-ping" style={{animationDelay: '300ms'}} />
          <circle cx="40" cy="60" r="3" fill="currentColor" className="text-gray-400" />
          
          {/* Bottom Left Node */}
          <circle cx="60" cy="160" r="5" fill="currentColor" className="text-gray-200 animate-ping" style={{animationDelay: '600ms'}} />
          <circle cx="60" cy="160" r="5" fill="currentColor" className="text-gray-400" />
          
          {/* Bottom Right Node */}
          <circle cx="160" cy="140" r="3" fill="currentColor" className="text-gray-200 animate-ping" style={{animationDelay: '900ms'}} />
          <circle cx="160" cy="140" r="3" fill="currentColor" className="text-gray-400" />
        </svg>

        {/* Central Core Agent */}
        <div className="absolute w-16 h-16 bg-white border border-gray-100 rounded-full flex items-center justify-center shadow-lg z-10">
          <Sparkles className="w-6 h-6 text-gray-900 animate-pulse" />
        </div>
      </div>

      <div className="text-center z-10">
        <h2 className="text-2xl md:text-3xl font-sans font-semibold text-gray-900 tracking-tight mb-4">
          Synthesizing Intelligence
        </h2>
        
        <div className="h-8 overflow-hidden mb-12 flex justify-center w-full">
          <p className="text-base font-medium text-gray-500 animate-pulse text-center">
            {currentStep || "Initializing autonomous agents..."}
          </p>
        </div>

        <div className="flex flex-col items-center gap-4 w-full max-w-sm mx-auto">
          {history.slice(-3).map((step, index) => {
            const isLast = index === Math.min(history.length - 1, 2);
            const opacity = isLast ? 'opacity-100 blur-none' : index === 0 && history.length === 3 ? 'opacity-20 blur-[1px]' : 'opacity-50 blur-[0.5px]';
            return (
              <div key={step} className={`text-sm font-medium text-gray-400 transition-all duration-700 ${opacity}`}>
                {step}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

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
      
      {/* Sleek Minimalist Breathing Rings */}
      <div className="relative w-32 h-32 mb-12 flex items-center justify-center">
        {/* Expanding Rings */}
        <div className="absolute inset-0 rounded-full border border-gray-200/60 animate-[ping_3s_cubic-bezier(0,0,0.2,1)_infinite]"></div>
        <div className="absolute inset-2 rounded-full border border-gray-100 animate-[ping_3s_cubic-bezier(0,0,0.2,1)_infinite]" style={{animationDelay: '1.5s'}}></div>
        
        {/* Inner Soft Glow */}
        <div className="absolute inset-6 rounded-full bg-gray-50 blur-xl animate-pulse"></div>
        
        {/* Central Core */}
        <div className="absolute w-14 h-14 bg-white border border-gray-100/80 rounded-full flex items-center justify-center shadow-[0_8px_30px_rgb(0,0,0,0.04)] z-10">
          <Sparkles className="w-5 h-5 text-gray-800 animate-pulse" strokeWidth={1.5} />
        </div>
      </div>

      <div className="text-center z-10">
        <h2 className="text-xl md:text-2xl font-sans font-medium text-gray-900 tracking-tight mb-3">
          Synthesizing Intelligence
        </h2>
        
        <div className="h-6 overflow-hidden mb-8 flex justify-center w-full">
          <p className="text-sm font-medium text-gray-500 animate-pulse text-center">
            {currentStep || "Initializing autonomous agents..."}
          </p>
        </div>

        <div className="flex flex-col items-center gap-3 w-full max-w-sm mx-auto">
          {history.slice(-3).map((step, index) => {
            const isLast = index === Math.min(history.length - 1, 2);
            const opacity = isLast ? 'opacity-100 blur-none' : index === 0 && history.length === 3 ? 'opacity-30 blur-[1px]' : 'opacity-60 blur-[0.5px]';
            return (
              <div key={step} className={`text-[13px] font-medium text-gray-400 transition-all duration-700 ${opacity}`}>
                {step}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

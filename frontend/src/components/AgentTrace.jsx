import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

export default function AgentTrace({ currentStep }) {
  const [history, setHistory] = useState([]);
  
  const nodes = [
    { id: 'start', label: 'QUERY', x: 50, y: 100 },
    { id: 'search', label: 'SEARCH', x: 200, y: 150 },
    { id: 'extract', label: 'EXTRACT', x: 350, y: 50 },
    { id: 'synthesize', label: 'SYNTHESIZE', x: 500, y: 150 },
    { id: 'report', label: 'REPORT', x: 650, y: 100 },
  ];

  const edges = [
    { id: 'e1', path: 'M 50 100 C 120 100, 130 150, 200 150' },
    { id: 'e2', path: 'M 200 150 C 270 150, 280 50, 350 50' },
    { id: 'e3', path: 'M 350 50 C 420 50, 430 150, 500 150' },
    { id: 'e4', path: 'M 500 150 C 570 150, 580 100, 650 100' },
  ];

  useEffect(() => {
    if (currentStep && !history.includes(currentStep)) {
      setHistory(prev => [...prev, currentStep]);
    }
  }, [currentStep, history]);

  const progressIndex = Math.min(Math.floor(history.length / 2), nodes.length - 1);

  // Use CSS variable aware colors
  const colors = {
    activeStroke: 'rgb(var(--color-text))',
    activeFill: 'rgb(var(--color-text))',
    inactiveStroke: 'rgb(var(--color-text) / 0.15)',
    inactiveFill: 'rgb(var(--color-text) / 0.08)',
    activeText: 'rgb(var(--color-text))',
    inactiveText: 'rgb(var(--color-text) / 0.3)',
    pillBg: 'rgb(var(--color-bg))',
    pillStrokeActive: 'rgb(var(--color-text) / 0.6)',
    pillStrokeInactive: 'rgb(var(--color-text) / 0.12)',
  };

  return (
    <div className="w-full flex flex-col items-center justify-center p-8 md:p-20 relative min-h-[600px]">
      
      {/* Node Graph */}
      <div className="relative w-full max-w-3xl mb-16 md:mb-24">
        <div className="w-full overflow-x-auto no-scrollbar flex md:justify-center">
          <div className="w-[700px] h-[200px] shrink-0">
            <svg viewBox="0 0 700 200" className="w-full h-full overflow-visible">
              {/* Edges */}
              {edges.map((edge, i) => {
                const isActive = progressIndex > i;
                return (
                  <g key={edge.id}>
                    <path d={edge.path} fill="transparent" stroke={colors.inactiveStroke} strokeWidth="1" />
                    <motion.path 
                      d={edge.path} 
                      fill="transparent" 
                      stroke={colors.activeStroke}
                      strokeWidth="1.5"
                      initial={{ pathLength: 0 }}
                      animate={{ pathLength: isActive ? 1 : 0 }}
                      transition={{ duration: 1.5, ease: "easeInOut" }}
                    />
                  </g>
                );
              })}
              
              {/* Nodes */}
              {nodes.map((node, i) => {
                const isActive = progressIndex >= i;
                const isCurrent = progressIndex === i;
                return (
                  <g key={node.id}>
                    {/* Dot */}
                    <motion.circle 
                      cx={node.x} cy={node.y} r="5" 
                      fill={isActive ? colors.activeFill : colors.inactiveFill}
                      stroke={isActive ? colors.activeStroke : colors.inactiveStroke}
                      strokeWidth="2"
                      animate={{ scale: isCurrent ? [1, 1.4, 1] : 1 }}
                      transition={{ repeat: isCurrent ? Infinity : 0, duration: 2 }}
                    />
                    {/* Label pill background */}
                    <motion.rect
                      x={node.x - 38} y={node.y - 38}
                      width="76" height="22" rx="11"
                      fill={colors.pillBg}
                      stroke={isActive ? colors.pillStrokeActive : colors.pillStrokeInactive}
                      strokeWidth="1"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: isActive ? 1 : 0.5 }}
                    />
                    {/* Label text */}
                    <text 
                      x={node.x} y={node.y - 27} 
                      textAnchor="middle" 
                      dominantBaseline="middle"
                      fill={isActive ? colors.activeText : colors.inactiveText}
                      style={{ 
                        fontSize: '9px', 
                        fontFamily: '"DotGothic16", monospace', 
                        letterSpacing: '0.15em',
                      }}
                    >
                      {node.label}
                    </text>
                  </g>
                );
              })}
            </svg>
          </div>
        </div>
      </div>

      <div className="text-center z-10 px-4">
        <h2 
          className="text-xl md:text-4xl font-pixel tracking-tighter uppercase mb-4"
          style={{ color: 'rgb(var(--color-text))' }}
        >
          SIMULATING RUN
        </h2>
        
        <div className="h-6 overflow-hidden mb-8 flex justify-center w-full">
          <p 
            className="text-xs md:text-sm font-sans font-light text-center"
            style={{ color: 'rgb(var(--color-text-muted))' }}
          >
            {currentStep || "Initializing autonomous agents..."}
          </p>
        </div>
      </div>
    </div>
  );
}

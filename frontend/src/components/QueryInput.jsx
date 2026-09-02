import React, { useState } from 'react';

export default function QueryInput({ onSubmit }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full relative group max-w-3xl mx-auto">
      <div className="relative flex items-center bg-white rounded-full border border-gray-200 hover:border-gray-300 focus-within:border-gray-900 transition-all duration-500 overflow-hidden shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question..."
          className="flex-1 bg-transparent text-gray-900 text-base md:text-xl font-sans font-light py-4 md:py-5 pl-6 md:pl-8 pr-2 outline-none placeholder:text-gray-300 w-full"
        />
        <div className="pr-2 shrink-0">
          <button 
            type="submit" 
            disabled={!query.trim()}
            className={`px-4 md:px-8 py-2 md:py-3 rounded-full flex items-center justify-center font-sans font-medium text-xs md:text-sm transition-all duration-300 whitespace-nowrap ${query.trim() ? 'bg-gray-900 text-white hover:bg-black' : 'bg-gray-100 text-gray-400 cursor-not-allowed'}`}
          >
            <span className="hidden sm:inline">Run AI Model</span>
            <span className="sm:hidden">Run</span>
          </button>
        </div>
      </div>
    </form>
  );
}

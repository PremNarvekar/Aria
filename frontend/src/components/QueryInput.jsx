import React, { useState } from 'react';
import { Search } from 'lucide-react';

export default function QueryInput({ onSubmit }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full relative group">
      <div className="relative flex items-center bg-white rounded-full shadow-sm border border-gray-200/60 hover:border-gray-300 hover:shadow-md focus-within:border-gray-300 focus-within:shadow-md focus-within:ring-4 focus-within:ring-gray-50/50 transition-all duration-500 overflow-hidden">
        <div className="pl-6 pr-3 text-gray-400">
          <Search className="w-5 h-5 stroke-[1.5]" />
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask anything..."
          className="flex-1 bg-transparent text-gray-900 text-lg md:text-[1.1rem] font-medium py-4 outline-none placeholder:text-gray-300 placeholder:font-normal"
        />
        <div className="pr-3 pl-2">
          <button 
            type="submit" 
            disabled={!query.trim()}
            className={`w-9 h-9 rounded-full flex items-center justify-center transition-all duration-300 ${query.trim() ? 'bg-gray-900 text-white shadow-md hover:bg-gray-800' : 'bg-gray-50 text-gray-300 cursor-not-allowed'}`}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M5 12h14"></path>
              <path d="m12 5 7 7-7 7"></path>
            </svg>
          </button>
        </div>
      </div>
    </form>
  );
}

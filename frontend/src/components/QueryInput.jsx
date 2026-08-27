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
      <div className="absolute inset-0 bg-gradient-to-r from-gray-200 to-gray-100 rounded-2xl blur opacity-20 group-hover:opacity-40 transition-opacity duration-500"></div>
      <div className="relative flex items-center bg-white rounded-2xl shadow-sm border border-gray-100 hover:border-gray-300 hover:shadow-md transition-all duration-300 overflow-hidden">
        <div className="pl-6 pr-2 text-gray-400">
          <Search className="w-5 h-5" />
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask anything..."
          className="flex-1 bg-transparent text-gray-900 text-lg md:text-xl font-medium py-5 outline-none placeholder:text-gray-300"
        />
        <div className="pr-3 pl-2">
          <button 
            type="submit" 
            className="w-10 h-10 rounded-xl bg-gray-900 text-white flex items-center justify-center hover:bg-gray-800 transition-colors shadow-sm"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M5 12h14"></path>
              <path d="m12 5 7 7-7 7"></path>
            </svg>
          </button>
        </div>
      </div>
    </form>
  );
}

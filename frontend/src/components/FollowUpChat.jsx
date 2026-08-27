import React, { useState } from 'react';
import { Sparkles, ArrowRight } from 'lucide-react';
import { followupService } from '../services/followupService';

export default function FollowUpChat({ session, setSession }) {
  const [input, setInput] = useState('');
  const [isSending, setIsSending] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isSending) return;

    const userMessage = input;
    setInput('');
    setIsSending(true);

    try {
      const updatedSession = await followupService.askFollowUp(session.id, userMessage);
      setSession({ ...updatedSession });
    } catch (err) {
      console.error(err);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="w-full">
      {session.followUpHistory && session.followUpHistory.length > 0 && (
        <div className="space-y-10 mb-10">
          {session.followUpHistory.map((msg, idx) => (
            <div key={msg.id || idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : ''}`}>
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 shrink-0 rounded-full bg-gray-50 border border-gray-100 flex items-center justify-center mt-1">
                  <Sparkles className="w-4 h-4 text-gray-900" />
                </div>
              )}
              
              <div className={`max-w-[85%] ${msg.role === 'user' ? 'text-right' : ''}`}>
                {msg.role === 'user' ? (
                  <p className="text-xl font-medium text-gray-900 leading-snug bg-gray-50 px-6 py-4 rounded-2xl inline-block border border-gray-100">{msg.text}</p>
                ) : (
                  <div className="prose prose-gray prose-sm max-w-none text-gray-800 font-medium leading-relaxed mt-2">
                    <p>{msg.text}</p>
                  </div>
                )}
              </div>
            </div>
          ))}
          {isSending && (
            <div className="flex gap-4">
              <div className="w-8 h-8 shrink-0 rounded-full bg-gray-50 border border-gray-100 flex items-center justify-center mt-1">
                <Sparkles className="w-4 h-4 text-gray-900 animate-pulse" />
              </div>
              <div className="flex items-center gap-2 px-4 py-3 bg-gray-50 rounded-2xl border border-gray-100">
                <div className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce" style={{animationDelay: '0ms'}}></div>
                <div className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce" style={{animationDelay: '150ms'}}></div>
                <div className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce" style={{animationDelay: '300ms'}}></div>
              </div>
            </div>
          )}
        </div>
      )}

      <form onSubmit={handleSubmit} className="relative group w-full">
        <div className="absolute inset-0 bg-gradient-to-r from-gray-200 to-gray-100 rounded-2xl blur opacity-20 group-hover:opacity-40 transition-opacity duration-500"></div>
        <div className="relative flex items-center bg-white rounded-2xl shadow-sm border border-gray-100 hover:border-gray-300 hover:shadow-md transition-all duration-300 overflow-hidden">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a follow up question..."
            disabled={isSending}
            className="flex-1 bg-transparent text-gray-900 text-lg font-medium pl-6 pr-16 py-5 outline-none disabled:opacity-50 placeholder:text-gray-300"
          />
          <div className="absolute right-3 top-1/2 -translate-y-1/2">
            <button 
              type="submit" 
              disabled={!input.trim() || isSending}
              className="w-10 h-10 rounded-xl bg-gray-900 text-white flex items-center justify-center hover:bg-gray-800 transition-colors shadow-sm disabled:opacity-50 disabled:hover:bg-gray-900"
            >
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

'use client';

import React, { useState } from 'react';
import { api } from '@/lib/api';
import { 
  BrainCircuit, 
  Send, 
  Sparkles, 
  FileText, 
  User, 
  MessageSquare,
  Loader2,
  BookOpen
} from 'lucide-react';
import { motion } from 'framer-motion';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
}

export default function AiKnowledgeNexus() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Welcome to **Nexus Copilot**, the AI Knowledge Assistant for LPU HRDC! How can I assist you with training analytics, session rosters, document queries, or attendance reports today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sampleQuestions = [
    "Which FDP had the highest attendance?",
    "Who attended less than 75%?",
    "Which trainer received the highest rating?",
    "List all programmes conducted by HRDC."
  ];

  const handleSend = async (textToSend?: string) => {
    const text = (textToSend || input).trim();
    if (!text) return;

    if (!textToSend) setInput('');

    // Append user message
    const newMessages: Message[] = [...messages, { role: 'user', content: text }];
    setMessages(newMessages);
    setLoading(true);

    try {
      const res = await api.askAiAssistant(text);
      setMessages([...newMessages, { 
        role: 'assistant', 
        content: res.answer,
        sources: res.sources || []
      }]);
    } catch (err) {
      setMessages([...newMessages, { 
        role: 'assistant', 
        content: 'Error: Failed to obtain a response from the AI pipeline. Make sure the backend server is running and Groq API keys are set.' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6 h-[80vh]">
      <div>
        <h1 className="text-xl font-bold text-white font-outfit">AI Knowledge Nexus</h1>
        <p className="text-[10px] text-gray-500 font-medium">Orchestrated using LangGraph agents & pgvector semantic document matching.</p>
      </div>

      <div className="flex-1 flex flex-col lg:flex-row gap-6 h-full overflow-hidden">
        
        {/* Chat History Panel */}
        <div className="flex-[2.5] glass-panel rounded-2xl border border-white/5 bg-[#1A252C]/10 flex flex-col justify-between overflow-hidden h-full">
          {/* Scrollable messages area */}
          <div className="flex-1 p-6 overflow-y-auto flex flex-col gap-4">
            {messages.map((m, idx) => (
              <div 
                key={idx} 
                className={`flex gap-3 max-w-[85%] ${
                  m.role === 'user' ? 'self-end flex-row-reverse' : 'self-start'
                }`}
              >
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                  m.role === 'user' 
                    ? 'bg-[#E77817]/20 text-[#E77817]' 
                    : 'bg-indigo-500/20 text-indigo-400'
                }`}>
                  {m.role === 'user' ? <User size={16} /> : <BrainCircuit size={16} />}
                </div>

                <div className="flex flex-col gap-2">
                  <div className={`p-4 rounded-2xl text-xs leading-relaxed font-light ${
                    m.role === 'user'
                      ? 'bg-[#E77817] text-white rounded-tr-none'
                      : 'bg-[#0F171A] border border-white/5 text-gray-200 rounded-tl-none'
                  }`}>
                    {/* Render markdown format manually using breaks/bold split or clean render */}
                    <p style={{ whiteSpace: 'pre-line' }}>{m.content}</p>
                  </div>

                  {/* Render dynamic sources cards */}
                  {m.sources && m.sources.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-1">
                      <span className="text-[8px] text-gray-500 font-bold uppercase tracking-wider block w-full">Verified References:</span>
                      {m.sources.map((src, srcIdx) => (
                        <div key={srcIdx} className="bg-white/5 border border-white/5 px-2.5 py-1 rounded-md text-[9px] text-[#E77817] flex items-center gap-1.5 font-semibold">
                          <FileText size={10} />
                          <span>{src.split('/').pop() || src}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="flex items-center gap-2 text-xs text-gray-500 p-4">
                <Loader2 size={16} className="animate-spin text-[#E77817]" />
                <span>LangGraph orchestrating workflow (groq:llama3-8b)...</span>
              </div>
            )}
          </div>

          {/* User Input Bar */}
          <div className="p-4 border-t border-white/5 bg-[#0F171A]/80 flex gap-3">
            <input
              type="text"
              placeholder="Ask about attendance records, ratings, FDP lists..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') handleSend(); }}
              className="flex-1 px-4 py-3 rounded-xl glass-input text-xs"
            />
            <button
              onClick={() => handleSend()}
              className="bg-[#E77817] hover:bg-[#D35400] text-white p-3 rounded-xl shadow-lg shadow-[#E77817]/20 transition-all flex items-center justify-center shrink-0"
            >
              <Send size={16} />
            </button>
          </div>
        </div>

        {/* Right Column: Sample prompts suggestions */}
        <div className="flex-1 glass-panel p-6 rounded-2xl border border-white/5 bg-[#1A252C]/10 flex flex-col gap-4 h-full">
          <div className="flex items-center gap-2 border-b border-white/5 pb-2">
            <Sparkles size={16} className="text-[#E77817]" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-white">Suggested Inquiries</h3>
          </div>

          <div className="flex flex-col gap-2.5 mt-2">
            {sampleQuestions.map((q) => (
              <button
                key={q}
                onClick={() => handleSend(q)}
                className="text-left p-3.5 bg-[#0F171A]/80 border border-white/5 hover:border-[#E77817]/30 hover:bg-[#E77817]/5 rounded-xl text-[10px] font-semibold text-gray-300 hover:text-white transition-all flex items-start gap-2.5"
              >
                <MessageSquare size={14} className="text-[#E77817] shrink-0 mt-0.5" />
                <span>{q}</span>
              </button>
            ))}
          </div>

          <div className="mt-auto border-t border-white/5 pt-4">
            <div className="flex items-center gap-2 bg-[#E77817]/10 p-3 rounded-xl text-[9px] text-gray-500 font-bold leading-normal">
              <BookOpen size={16} className="text-[#E77817] shrink-0" />
              <span>Cites RAG context documents, circulars, and policies indexed directly in pgvector.</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

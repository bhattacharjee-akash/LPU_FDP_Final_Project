'use client';

import React from 'react';
import { usePathname } from 'next/navigation';
import { Calendar } from 'lucide-react';

export default function Navbar() {
  const pathname = usePathname();
  
  const getHeaderTitle = () => {
    switch (pathname) {
      case '/dashboard':
        return 'Overview Dashboard';
      case '/dashboard/upload':
        return 'Upload Course Syllabus';
      case '/dashboard/history':
        return 'Generation History';
      case '/dashboard/analytics':
        return 'Performance Analytics';
      case '/dashboard/settings':
        return 'Copilot Configuration';
      default:
        return 'LPU Academic Copilot';
    }
  };

  const getHeaderDesc = () => {
    switch (pathname) {
      case '/dashboard':
        return 'Monitor generation processes, view quality reports, and compile packages.';
      case '/dashboard/upload':
        return 'Upload your syllabus PDF to trigger the multi-agent design pipeline.';
      case '/dashboard/history':
        return 'Access previously parsed files, generated PDF files, and history records.';
      case '/dashboard/analytics':
        return 'Evaluation stats, curriculum maps compliance, and estimated faculty hours saved.';
      case '/dashboard/settings':
        return 'Configure preferred LLM settings, providers (Gemini/Groq), and temperature levels.';
      default:
        return 'Lovely Professional University Academic Assistant Platform.';
    }
  };

  return (
    <header className="h-20 w-full border-b border-white/5 flex items-center justify-between px-8 z-20">
      <div>
        <h2 className="text-xl font-bold text-white tracking-wide">{getHeaderTitle()}</h2>
        <p className="text-xs text-gray-500 mt-1 font-medium">{getHeaderDesc()}</p>
      </div>

      <div className="flex items-center gap-4">
        {/* FDP Program Indicator Badge */}
        <div className="bg-lpu-orange/10 border border-lpu-orange/20 text-lpu-orange px-3 py-1.5 rounded-full text-xs font-semibold tracking-wider flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-lpu-orange animate-pulse"></span>
          FDP AGENTIC SYSTEMS DEMO
        </div>

        {/* Date Display */}
        <div className="flex items-center gap-2 text-xs text-gray-400 bg-white/5 px-3 py-1.5 rounded-xl border border-white/5">
          <Calendar size={14} className="text-lpu-orange" />
          <span>{new Date().toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}</span>
        </div>
      </div>
    </header>
  );
}

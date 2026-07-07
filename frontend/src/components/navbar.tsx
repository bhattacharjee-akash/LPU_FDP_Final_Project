'use client';

import React from 'react';
import { usePathname } from 'next/navigation';
import { Calendar } from 'lucide-react';

export default function Navbar() {
  const pathname = usePathname();
  
  const getHeaderTitle = () => {
    if (pathname === '/dashboard') return 'HRDC Overview Dashboard';
    if (pathname.startsWith('/dashboard/programmes')) return 'Programmes Lifecycle Portal';
    if (pathname.startsWith('/dashboard/attendance')) return 'GPS & QR Attendance Hub';
    if (pathname.startsWith('/dashboard/assessments')) return 'Assessments & Evaluations';
    if (pathname.startsWith('/dashboard/feedback')) return 'Feedback & Impact Surveys';
    if (pathname.startsWith('/dashboard/certificates')) return 'Digital Certificates Registry';
    if (pathname.startsWith('/dashboard/corporate')) return 'Corporate Training Contracts';
    if (pathname.startsWith('/dashboard/ai')) return 'AI Knowledge Assistant';
    if (pathname.startsWith('/dashboard/settings')) return 'System Settings';
    return 'LPU HRDC Nexus';
  };

  const getHeaderDesc = () => {
    if (pathname === '/dashboard') {
      return 'Monitor upcoming and completed sessions, attendance analytics, and general training statistics.';
    }
    if (pathname.startsWith('/dashboard/programmes')) {
      return 'Create and configure workshops, FDPs, assign trainers, set up schedules, and manage course assets.';
    }
    if (pathname.startsWith('/dashboard/attendance')) {
      return 'Scan class attendance codes, enable geolocation fencing, override logs, and export reports.';
    }
    if (pathname.startsWith('/dashboard/assessments')) {
      return 'Create MCQ tests, code problems or case studies. Submit work and grade participants.';
    }
    if (pathname.startsWith('/dashboard/feedback')) {
      return 'Collect session scores, pre-post skills gain metrics, and track ROI indices.';
    }
    if (pathname.startsWith('/dashboard/certificates')) {
      return 'Generate, verify, and download official LPU HRDC certificates with digital signatures.';
    }
    if (pathname.startsWith('/dashboard/corporate')) {
      return 'Manage billing invoices, vendor contracts, corporate clients accounts, and billing statuses.';
    }
    if (pathname.startsWith('/dashboard/ai')) {
      return 'Ask questions about attendance rates, program schedules, and search documentation using RAG.';
    }
    if (pathname.startsWith('/dashboard/settings')) {
      return 'Configure preferred LLM settings, provider keys, and system parameters.';
    }
    return 'Lovely Professional University Human Resource Development Center.';
  };

  return (
    <header className="h-20 w-full border-b border-white/5 flex items-center justify-between px-8 z-20 bg-[#070A0D]/50 backdrop-blur-md">
      <div>
        <h2 className="text-sm font-bold text-white tracking-wide">{getHeaderTitle()}</h2>
        <p className="text-[10px] text-gray-500 mt-0.5 font-medium">{getHeaderDesc()}</p>
      </div>

      <div className="flex items-center gap-4">
        {/* LPU HRDC Indicator Badge */}
        <div className="bg-[#E77817]/10 border border-[#E77817]/20 text-[#E77817] px-3 py-1 rounded-full text-[10px] font-bold tracking-wider flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-[#E77817] animate-pulse"></span>
          LPU HRDC NEXUS ACTIVE
        </div>

        {/* Date Display */}
        <div className="flex items-center gap-2 text-[10px] text-gray-400 bg-white/5 px-3 py-1 rounded-xl border border-white/5 font-semibold">
          <Calendar size={12} className="text-[#E77817]" />
          <span>{new Date().toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}</span>
        </div>
      </div>
    </header>
  );
}

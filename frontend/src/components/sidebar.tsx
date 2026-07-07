'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { 
  LayoutDashboard, 
  BookOpen, 
  CalendarCheck, 
  FileCheck, 
  MessageSquareReply, 
  Award, 
  Building2, 
  BrainCircuit, 
  Settings, 
  LogOut, 
  Cpu 
} from 'lucide-react';
import { supabase, isSupabaseConfigured } from '@/lib/supabase';

interface SidebarProps {
  profile?: { name: string; department: string };
}

export default function Sidebar({ profile }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();
  const [role, setRole] = useState('Participant');

  useEffect(() => {
    const savedRole = localStorage.getItem('user_role') || 'Participant';
    setRole(savedRole);
  }, []);

  const menuItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Programmes Portal', path: '/dashboard/programmes', icon: BookOpen },
    { name: 'Attendance Hub', path: '/dashboard/attendance', icon: CalendarCheck },
    { name: 'Assessments', path: '/dashboard/assessments', icon: FileCheck },
    { name: 'Feedback & ROI', path: '/dashboard/feedback', icon: MessageSquareReply },
    { name: 'Certificates Registry', path: '/dashboard/certificates', icon: Award },
  ];

  // Conditionally add Corporate Module for Admin, Staff or Corporate roles
  if (['HRDC Administrator', 'HRDC Staff', 'Corporate Client'].includes(role)) {
    menuItems.push({ name: 'Corporate Training', path: '/dashboard/corporate', icon: Building2 });
  }

  // AI Knowledge Assistant & Settings
  menuItems.push(
    { name: 'AI Knowledge Nexus', path: '/dashboard/ai', icon: BrainCircuit },
    { name: 'Settings', path: '/dashboard/settings', icon: Settings }
  );

  const handleSignOut = async () => {
    localStorage.removeItem('fdp_demo_mode');
    localStorage.removeItem('user_role');
    localStorage.removeItem('faculty_name');
    localStorage.removeItem('department');
    
    if (isSupabaseConfigured) {
      await supabase.auth.signOut();
    }
    router.push('/login');
  };

  return (
    <div className="w-64 h-screen fixed left-0 top-0 glass-panel flex flex-col justify-between p-6 z-30 bg-[#0F171A]/95 border-r border-white/5">
      <div className="flex flex-col gap-6 overflow-y-auto max-h-[85vh] pr-1">
        {/* Elegant Logo Header */}
        <div className="flex items-center gap-3">
          <div className="bg-[#E77817] p-2 rounded-lg text-white shadow-lg shadow-[#E77817]/30">
            <Cpu size={24} />
          </div>
          <div>
            <h1 className="font-bold text-md leading-tight tracking-wider text-white">LPU HRDC</h1>
            <p className="text-[10px] text-[#E77817] font-semibold tracking-widest">NEXUS</p>
          </div>
        </div>

        <div className="px-2 py-1 bg-[#E77817]/10 text-[#E77817] rounded-lg text-[10px] font-bold text-center uppercase tracking-wider">
          Role: {role}
        </div>

        {/* Navigation Items */}
        <nav className="flex flex-col gap-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            // Highlight parent paths for sub-paths (e.g. /dashboard/programmes/123 highlights Programmes)
            const isActive = item.path === '/dashboard' 
              ? pathname === '/dashboard' 
              : pathname.startsWith(item.path);

            return (
              <Link
                key={item.path}
                href={item.path}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-300 font-medium text-xs ${
                  isActive
                    ? 'bg-[#E77817] text-white shadow-lg shadow-[#E77817]/20 scale-105'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <Icon size={16} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* User Information Profile Footer */}
      <div className="flex flex-col gap-3 border-t border-white/10 pt-3">
        <div className="flex items-center gap-3 px-1">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-[#E77817] to-amber-500 flex items-center justify-center font-bold text-white text-xs">
            {profile?.name ? profile.name.charAt(0) : 'U'}
          </div>
          <div className="flex flex-col overflow-hidden max-w-[130px]">
            <span className="font-semibold text-xs text-white truncate">{profile?.name || 'Faculty Member'}</span>
            <span className="text-[10px] text-gray-500 truncate">{profile?.department || 'Academic Dept'}</span>
          </div>
        </div>

        <button
          onClick={handleSignOut}
          className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-red-400 hover:text-red-300 hover:bg-red-500/10 transition-all duration-300 font-semibold text-xs w-full"
        >
          <LogOut size={16} />
          <span>Sign Out</span>
        </button>
      </div>
    </div>
  );
}

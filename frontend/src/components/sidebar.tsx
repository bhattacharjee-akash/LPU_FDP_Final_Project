'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { LayoutDashboard, FileUp, History, BarChart3, Settings, LogOut, Cpu } from 'lucide-react';
import { supabase, isSupabaseConfigured } from '@/lib/supabase';

interface SidebarProps {
  profile?: { name: string; department: string };
}

export default function Sidebar({ profile }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();

  const menuItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Upload Syllabus', path: '/dashboard/upload', icon: FileUp },
    { name: 'History', path: '/dashboard/history', icon: History },
    { name: 'Analytics', path: '/dashboard/analytics', icon: BarChart3 },
    { name: 'Settings', path: '/dashboard/settings', icon: Settings },
  ];

  const handleSignOut = async () => {
    if (isSupabaseConfigured) {
      await supabase.auth.signOut();
    }
    router.push('/login');
  };

  return (
    <div className="w-64 h-screen fixed left-0 top-0 glass-panel flex flex-col justify-between p-6 z-30">
      <div className="flex flex-col gap-8">
        {/* Elegant Logo Header */}
        <div className="flex items-center gap-3">
          <div className="bg-lpu-orange p-2 rounded-lg text-white shadow-lg shadow-lpu-orange/30">
            <Cpu size={24} />
          </div>
          <div>
            <h1 className="font-bold text-lg leading-tight tracking-wider text-white">LPU Academic</h1>
            <p className="text-xs text-lpu-orange font-semibold tracking-widest">COPILOT</p>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="flex flex-col gap-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.path;
            return (
              <Link
                key={item.path}
                href={item.path}
                className={`flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-300 font-medium text-sm ${
                  isActive
                    ? 'bg-lpu-orange text-white shadow-lg shadow-lpu-orange/20 scale-105'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <Icon size={18} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* User Information Profile Footer */}
      <div className="flex flex-col gap-4 border-t border-white/10 pt-4">
        <div className="flex items-center gap-3 px-2">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-lpu-orange to-amber-500 flex items-center justify-center font-bold text-white shadow-inner">
            {profile?.name ? profile.name.charAt(0) : 'F'}
          </div>
          <div className="flex flex-col overflow-hidden">
            <span className="font-semibold text-sm text-white truncate">{profile?.name || 'Faculty Member'}</span>
            <span className="text-xs text-gray-500 truncate">{profile?.department || 'Academic Dept'}</span>
          </div>
        </div>

        <button
          onClick={handleSignOut}
          className="flex items-center gap-4 px-4 py-3 rounded-xl text-red-400 hover:text-red-300 hover:bg-red-500/10 transition-all duration-300 font-medium text-sm w-full"
        >
          <LogOut size={18} />
          <span>Sign Out</span>
        </button>
      </div>
    </div>
  );
}

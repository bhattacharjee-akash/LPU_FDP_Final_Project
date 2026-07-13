'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { supabase, isSupabaseConfigured } from '@/lib/supabase';
import { api } from '@/lib/api';
import Sidebar from '@/components/sidebar';
import Navbar from '@/components/navbar';
import { Loader2 } from 'lucide-react';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState({ name: 'Faculty Member', department: 'Computer Science' });

  useEffect(() => {
    async function checkAuth() {
      // 1. Check local demo bypass
      const isDemo = localStorage.getItem('fdp_demo_mode') === 'true';
      if (isDemo) {
        const name = localStorage.getItem('faculty_name') || 'Dr. Amanpreet Singh';
        const dept = localStorage.getItem('department') || 'Computer Science & Engineering';
        setProfile({ name, department: dept });
        setLoading(false);
        return;
      }

      // 2. Check cached session verification for instant UI loading
      const cachedSession = sessionStorage.getItem('fdp_session_verified') === 'true';
      if (cachedSession) {
        setLoading(false);
        const name = localStorage.getItem('faculty_name');
        const dept = localStorage.getItem('department');
        if (name && dept) {
          setProfile({ name, department: dept });
        }
      }

      // 3. Perform actual security verification in background
      if (isSupabaseConfigured) {
        try {
          const { data: { session } } = await supabase.auth.getSession();
          if (!session) {
            sessionStorage.removeItem('fdp_session_verified');
            router.push('/login');
            return;
          }

          // Store verified status in sessionStorage
          sessionStorage.setItem('fdp_session_verified', 'true');

          // Load profile from backend
          const prof = await api.getProfile();
          if (prof) {
            setProfile({ name: prof.name, department: prof.department });
            localStorage.setItem('faculty_name', prof.name);
            localStorage.setItem('department', prof.department);
          }
        } catch (e) {
          console.log("Could not load backend profile metadata", e);
        }
        setLoading(false);
      } else {
        sessionStorage.removeItem('fdp_session_verified');
        router.push('/login');
      }
    }
    
    checkAuth();
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#070A0D] flex items-center justify-center text-lpu-orange">
        <div className="flex flex-col items-center gap-4">
          <Loader2 size={36} className="animate-spin" />
          <span className="text-sm font-semibold tracking-wider">Verifying Session...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#070A0D] text-white flex">
      {/* Fixed Sidebar */}
      <Sidebar profile={profile} />

      {/* Main Content Area */}
      <div className="flex-1 pl-64 flex flex-col min-h-screen">
        {/* Top Navbar */}
        <Navbar />

        {/* Dynamic Page Views */}
        <main className="flex-1 p-8 overflow-y-auto max-w-7xl mx-auto w-full">
          {children}
        </main>
      </div>
    </div>
  );
}

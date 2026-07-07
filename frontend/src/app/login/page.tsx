'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { supabase, isSupabaseConfigured } from '@/lib/supabase';
import { Cpu, Mail, Lock, LogIn, ArrowRight, ShieldCheck, Sparkles, User } from 'lucide-react';
import { motion } from 'framer-motion';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  
  // Profile parameters (captured during login/sign up)
  const [name, setName] = useState('');
  const [role, setRole] = useState('Participant');  // Default role
  const [department, setDepartment] = useState('Computer Science & Engineering');

  useEffect(() => {
    if (isSupabaseConfigured) {
      supabase.auth.getSession().then(({ data: { session } }) => {
        if (session) {
          router.push('/dashboard');
        }
      });
    }
  }, [router]);

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (!isSupabaseConfigured) {
      // Mock Bypass for Demonstration Mode
      localStorage.setItem('fdp_demo_mode', 'true');
      localStorage.setItem('faculty_name', name || 'Dr. Amanpreet Singh');
      localStorage.setItem('user_role', role);
      localStorage.setItem('department', department);
      router.push('/dashboard');
      setLoading(false);
      return;
    }

    try {
      if (isSignUp) {
        // Sign Up Flow
        const { data, error: signUpErr } = await supabase.auth.signUp({
          email,
          password,
          options: {
            data: {
              name: name,
              role: role,
              department: department
            }
          }
        });
        if (signUpErr) throw signUpErr;
        
        // Trigger profile update route on FastAPI
        const token = data.session?.access_token;
        if (token) {
          await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/profile`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ name, role, department, user_id: data.user?.id })
          });
        }

        alert("Sign up successful! Please check your email for verification and log in.");
        setIsSignUp(false);
      } else {
        // Log In Flow
        const { data, error: logInErr } = await supabase.auth.signInWithPassword({
          email,
          password
        });
        if (logInErr) throw logInErr;
        
        // Save token & info to verify setup
        const token = data.session?.access_token;
        if (token && data.user) {
          try {
            await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/profile`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify({
                name: data.user.user_metadata?.name || 'Faculty Member',
                role: data.user.user_metadata?.role || 'Participant',
                department: data.user.user_metadata?.department || 'Computer Science & Engineering',
                user_id: data.user.id
              })
            });
          } catch (e) {
            console.log("Profile save failed or already exists.");
          }
        }
        router.push('/dashboard');
      }
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoMode = (demoRole: string) => {
    localStorage.setItem('fdp_demo_mode', 'true');
    localStorage.setItem('user_role', demoRole);
    
    if (demoRole === 'HRDC Administrator') {
      localStorage.setItem('faculty_name', 'Director HRDC (LPU)');
      localStorage.setItem('department', 'Academic Administration');
    } else if (demoRole === 'Trainer') {
      localStorage.setItem('faculty_name', 'Dr. Amanpreet Singh (AI Trainer)');
      localStorage.setItem('department', 'Computer Science & Engineering');
    } else {
      localStorage.setItem('faculty_name', 'Dr. Ramesh Kumar (Participant)');
      localStorage.setItem('department', 'Mechanical Engineering');
    }
    
    router.push('/dashboard');
  };

  return (
    <div className="min-h-screen bg-[#070A0D] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-lpu-orange/5 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-amber-500/5 rounded-full blur-[120px] pointer-events-none" />

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-4xl glass-panel rounded-3xl overflow-hidden flex flex-col md:flex-row shadow-glass border border-white/5"
      >
        {/* Left column info panel */}
        <div className="md:w-1/2 bg-gradient-to-br from-lpu-charcoal to-lpu-charcoalDark p-8 flex flex-col justify-between border-b md:border-b-0 md:border-r border-white/5">
          <div className="flex items-center gap-3">
            <div className="bg-lpu-orange p-2 rounded-xl text-white">
              <Cpu size={24} />
            </div>
            <div>
              <span className="font-bold text-lg text-white tracking-wide">LPU HRDC</span>
              <span className="text-xs text-lpu-orange font-bold tracking-widest block">NEXUS</span>
            </div>
          </div>

          <div className="my-12 flex flex-col gap-6">
            <div className="flex items-center gap-2 text-lpu-orange text-xs font-semibold tracking-wider bg-lpu-orange/10 px-3 py-1 rounded-full w-max">
              <Sparkles size={12} />
              Training Lifecycle Engine
            </div>
            <h2 className="text-2xl font-bold text-white leading-snug">
              An AI-Powered Training Lifecycle Management Platform.
            </h2>
            <p className="text-gray-400 text-sm font-light leading-relaxed">
              Log in to register for FDPs, verify classroom attendance via QR/GPS, complete evaluations, download digital signatures certificates, and interact with the LangGraph knowledge assistant.
            </p>
          </div>

          <div className="text-xs text-gray-500 flex items-center gap-2">
            <ShieldCheck size={16} className="text-lpu-orange" />
            Secured via Supabase RBAC
          </div>
        </div>

        {/* Right column form panel */}
        <div className="md:w-1/2 p-8 flex flex-col justify-center">
          <h3 className="text-xl font-bold text-white mb-2">
            {isSignUp ? 'Create HRDC Account' : 'Sign In'}
          </h3>
          <p className="text-xs text-gray-400 mb-6">
            {!isSupabaseConfigured 
              ? 'Connect using Supabase, or pick a role below for instant demo access.' 
              : 'Enter your credentials to access the academic portal.'}
          </p>

          <form onSubmit={handleAuth} className="flex flex-col gap-4">
            {isSignUp && (
              <>
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs text-gray-400 font-medium">Full Name</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Dr. Amanpreet Singh"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="px-4 py-3 rounded-xl glass-input text-sm"
                  />
                </div>

                <div className="flex flex-col gap-1.5">
                  <label className="text-xs text-gray-400 font-medium">Access Role</label>
                  <select
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    className="px-4 py-3 rounded-xl glass-input text-sm bg-lpu-charcoal"
                  >
                    <option value="Participant">Participant (Faculty / External)</option>
                    <option value="Trainer">Trainer (Resource Person)</option>
                    <option value="HRDC Staff">HRDC Staff</option>
                    <option value="HRDC Administrator">HRDC Administrator</option>
                    <option value="Corporate Client">Corporate Client</option>
                  </select>
                </div>

                <div className="flex flex-col gap-1.5">
                  <label className="text-xs text-gray-400 font-medium">Department / Organization</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Computer Science"
                    value={department}
                    onChange={(e) => setDepartment(e.target.value)}
                    className="px-4 py-3 rounded-xl glass-input text-sm"
                  />
                </div>
              </>
            )}

            <div className="flex flex-col gap-1.5">
              <label className="text-xs text-gray-400 font-medium">Email Address</label>
              <div className="relative">
                <Mail size={16} className="absolute left-4 top-3.5 text-gray-500" />
                <input
                  type="email"
                  required
                  placeholder="name@lpu.co.in"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-11 pr-4 py-3 rounded-xl glass-input text-sm w-full"
                />
              </div>
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-xs text-gray-400 font-medium">Password</label>
              <div className="relative">
                <Lock size={16} className="absolute left-4 top-3.5 text-gray-500" />
                <input
                  type="password"
                  required
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-11 pr-4 py-3 rounded-xl glass-input text-sm w-full"
                />
              </div>
            </div>

            {error && (
              <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-xs p-3 rounded-xl font-medium">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="bg-lpu-orange hover:bg-lpu-orangeHover disabled:bg-lpu-orange/50 py-3.5 rounded-xl font-bold text-white transition-all duration-300 flex items-center justify-center gap-2 mt-2 shadow-lg shadow-lpu-orange/20"
            >
              <span>{isSignUp ? 'Register & Enter' : 'Sign In to Portal'}</span>
              <LogIn size={18} />
            </button>
          </form>

          {/* Quick Demo Mode triggers if credentials/setup aren't verified */}
          <div className="mt-6 border-t border-white/5 pt-4">
            <span className="text-xs text-gray-500 block mb-3 text-center">Or connect instantly via Demo Portal:</span>
            <div className="grid grid-cols-3 gap-2">
              <button
                onClick={() => handleDemoMode('HRDC Administrator')}
                className="border border-lpu-orange/20 hover:bg-lpu-orange/10 text-white text-[10px] py-2 rounded-lg font-semibold transition-all"
              >
                Admin
              </button>
              <button
                onClick={() => handleDemoMode('Trainer')}
                className="border border-lpu-orange/20 hover:bg-lpu-orange/10 text-white text-[10px] py-2 rounded-lg font-semibold transition-all"
              >
                Trainer
              </button>
              <button
                onClick={() => handleDemoMode('Participant')}
                className="border border-lpu-orange/20 hover:bg-lpu-orange/10 text-white text-[10px] py-2 rounded-lg font-semibold transition-all"
              >
                Participant
              </button>
            </div>
          </div>

          <div className="mt-6 text-center">
            <button
              onClick={() => setIsSignUp(!isSignUp)}
              className="text-xs text-lpu-orange hover:underline font-medium"
            >
              {isSignUp ? 'Already have an account? Sign In' : "Don't have an account? Sign Up"}
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

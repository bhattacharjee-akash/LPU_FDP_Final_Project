'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { supabase, isSupabaseConfigured } from '@/lib/supabase';
import { Cpu, Mail, Lock, LogIn, ArrowRight, ShieldCheck, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  
  // Faculty Profile parameters (captured during login/sign up)
  const [facultyName, setFacultyName] = useState('');
  const [department, setDepartment] = useState('Computer Science & Engineering');

  useEffect(() => {
    // Check if session is already active
    if (isSupabaseConfigured) {
      supabase.auth.getSession().then(({ data: { session } }) => {
        if (session) {
          sessionStorage.setItem('fdp_session_verified', 'true');
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
      // Mock Bypass for FDP Demonstration Mode
      localStorage.setItem('fdp_demo_mode', 'true');
      localStorage.setItem('faculty_name', facultyName || 'Dr. Amanpreet Singh');
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
              name: facultyName,
              department: department
            }
          }
        });
        if (signUpErr) throw signUpErr;
        
        // Trigger profile update route
        const token = data.session?.access_token;
        if (token) {
          try {
            await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/profile`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify({ name: facultyName, department, user_id: data.user?.id })
            });
          } catch (e) {
            console.log("Profile save failed or already exists.");
          }

          // Auto-login since session is active!
          sessionStorage.setItem('fdp_session_verified', 'true');
          router.push('/dashboard');
          return;
        }

        alert("Sign up successful! Please check your email to verify your account, then log in.");
        setIsSignUp(false);
      } else {
        // Log In Flow
        const { data, error: logInErr } = await supabase.auth.signInWithPassword({
          email,
          password
        });
        if (logInErr) throw logInErr;
        
        // Fetch/save profile setup
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
                department: data.user.user_metadata?.department || 'Computer Science & Engineering',
                user_id: data.user.id
              })
            });
          } catch (e) {
            console.log("Profile save failed or already exists.");
          }
        }
        sessionStorage.setItem('fdp_session_verified', 'true');
        router.push('/dashboard');
      }
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoMode = () => {
    localStorage.setItem('fdp_demo_mode', 'true');
    localStorage.setItem('faculty_name', 'Dr. Amanpreet Singh');
    localStorage.setItem('department', 'Computer Science & Engineering');
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
              <span className="font-bold text-lg text-white tracking-wide">LPU Academic</span>
              <span className="text-xs text-lpu-orange font-bold tracking-widest block">COPILOT</span>
            </div>
          </div>

          <div className="my-12 flex flex-col gap-6">
            <div className="flex items-center gap-2 text-lpu-orange text-xs font-semibold tracking-wider bg-lpu-orange/10 px-3 py-1 rounded-full w-max">
              <Sparkles size={12} />
              Multi-Agent Orchestrator
            </div>
            <h2 className="text-2xl font-bold text-white leading-snug">
              Autonomous workflows designed for university faculty.
            </h2>
            <p className="text-gray-400 text-sm font-light leading-relaxed">
              Log in to configure your preferred LLM parameters, upload course documents, and generate complete quality-certified course plans.
            </p>
          </div>

          <div className="text-xs text-gray-500 flex items-center gap-2">
            <ShieldCheck size={16} className="text-lpu-orange" />
            Secured via Supabase Authentication
          </div>
        </div>

        {/* Right column form panel */}
        <div className="md:w-1/2 p-8 flex flex-col justify-center">
          <h3 className="text-xl font-bold text-white mb-2">
            {isSignUp ? 'Create Faculty Account' : 'Welcome Back'}
          </h3>
          <p className="text-xs text-gray-400 mb-6">
            {!isSupabaseConfigured 
              ? 'Supabase is not configured. Running in Local Demo Mode.' 
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
                    value={facultyName}
                    onChange={(e) => setFacultyName(e.target.value)}
                    className="px-4 py-3 rounded-xl glass-input text-sm"
                  />
                </div>

                <div className="flex flex-col gap-1.5">
                  <label className="text-xs text-gray-400 font-medium">Academic Department</label>
                  <select
                    value={department}
                    onChange={(e) => setDepartment(e.target.value)}
                    className="px-4 py-3 rounded-xl glass-input text-sm bg-lpu-charcoal"
                  >
                    <option value="Computer Science & Engineering">Computer Science & Engineering</option>
                    <option value="Information Technology">Information Technology</option>
                    <option value="Electronics & Communication">Electronics & Communication</option>
                    <option value="Mechanical Engineering">Mechanical Engineering</option>
                    <option value="Management & Commerce">Management & Commerce</option>
                  </select>
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
                  placeholder="faculty@lpu.co.in"
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
              {loading ? (
                <span>Validating...</span>
              ) : (
                <>
                  <span>{isSignUp ? 'Register & Enter' : 'Sign In to Dashboard'}</span>
                  <LogIn size={18} />
                </>
              )}
            </button>
          </form>

          {/* Quick Demo Mode triggers if credentials/setup aren't verified */}
          {!isSupabaseConfigured && (
            <button
              onClick={handleDemoMode}
              className="border border-lpu-orange/30 hover:bg-lpu-orange/5 text-lpu-orange text-xs py-3.5 rounded-xl font-bold transition-all duration-300 flex items-center justify-center gap-2 mt-4"
            >
              <span>Instant FDP Demo Access</span>
              <ArrowRight size={14} />
            </button>
          )}

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

'use client';

import React from 'react';
import Link from 'next/link';
import { Cpu, ArrowRight, BookOpen, ShieldCheck, Zap, Sparkles, CheckCircle, BarChart3, Award, BrainCircuit, Globe } from 'lucide-react';
import { motion } from 'framer-motion';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#070A0D] flex flex-col justify-between relative overflow-hidden text-white font-sans">
      {/* Background Glowing Ambient Gradients */}
      <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-[#E77817]/10 rounded-full blur-[150px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-5%] w-[500px] h-[500px] bg-amber-500/5 rounded-full blur-[120px] pointer-events-none" />

      {/* Top Header */}
      <header className="max-w-7xl mx-auto w-full px-6 h-20 flex items-center justify-between z-10">
        <div className="flex items-center gap-3">
          <div className="bg-[#E77817] p-2 rounded-xl text-white shadow-lg shadow-[#E77817]/20">
            <Cpu size={24} />
          </div>
          <div>
            <span className="font-bold text-lg text-white leading-tight tracking-wider">LPU HRDC</span>
            <span className="text-xs text-[#E77817] font-bold tracking-widest block">NEXUS</span>
          </div>
        </div>
        
        <Link 
          href="/login" 
          className="px-5 py-2.5 rounded-xl border border-white/10 hover:border-[#E77817]/30 hover:bg-[#E77817]/5 text-sm font-semibold transition-all duration-300 text-white"
        >
          Portal Login
        </Link>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto w-full px-6 flex-1 flex flex-col justify-center items-center text-center z-10 py-12">
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="bg-white/5 border border-white/10 px-4 py-1.5 rounded-full text-xs font-semibold tracking-wider text-[#E77817] flex items-center gap-2 mb-8"
        >
          <Sparkles size={14} />
          AI-POWERED ACADEMIC DEVELOPMENT SUITE
        </motion.div>

        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="text-4xl md:text-6xl font-extrabold tracking-tight text-white leading-[1.1] max-w-4xl font-outfit"
        >
          LPU HRDC Nexus: An AI-Powered <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#E77817] via-amber-500 to-orange-400">Training Lifecycle</span> Platform
        </motion.h1>

        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="text-gray-400 text-md md:text-lg max-w-2xl mt-6 leading-relaxed font-light"
        >
          Manage internal and external Faculty Development Programmes (FDPs), workshops, and technical certifications. Orchestrate attendance verification (QR/GPS), auto-graded evaluations, feedback indices, and corporate invoice contracts.
        </motion.p>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-10 flex flex-col sm:flex-row gap-4"
        >
          <Link
            href="/login"
            className="bg-[#E77817] hover:bg-[#D35400] px-8 py-4 rounded-xl font-bold text-white shadow-lg shadow-[#E77817]/20 transition-all duration-300 hover:scale-105 flex items-center gap-3 text-md"
          >
            <span>Enter Portal Dashboard</span>
            <ArrowRight size={18} />
          </Link>
          <Link
            href="#features"
            className="bg-white/5 border border-white/10 hover:border-white/20 text-gray-300 hover:text-white px-8 py-4 rounded-xl font-bold transition-all duration-300 text-md"
          >
            Learn More
          </Link>
        </motion.div>

        {/* Features Showcase Grid */}
        <div id="features" className="grid grid-cols-1 md:grid-cols-4 gap-6 w-full max-w-6xl mt-24">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="bg-[#1A252C]/40 p-6 rounded-2xl border border-white/5 text-left flex flex-col gap-4 backdrop-blur-md"
          >
            <div className="bg-[#E77817]/10 p-3 rounded-xl text-[#E77817] w-max">
              <BookOpen size={22} />
            </div>
            <h3 className="font-semibold text-lg text-white">Lifecycle Management</h3>
            <p className="text-sm text-gray-500 leading-relaxed font-light">
              Orchestrate complete programs from planning and syllabus indexing to schedules, participants assignment and coordinators.
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="bg-[#1A252C]/40 p-6 rounded-2xl border border-white/5 text-left flex flex-col gap-4 backdrop-blur-md"
          >
            <div className="bg-[#E77817]/10 p-3 rounded-xl text-[#E77817] w-max">
              <CheckCircle size={22} />
            </div>
            <h3 className="font-semibold text-lg text-white">QR / GPS Attendance</h3>
            <p className="text-sm text-gray-500 leading-relaxed font-light">
              Secure attendance logging checking scans against dynamic time-windows and geolocation classroom parameters.
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="bg-[#1A252C]/40 p-6 rounded-2xl border border-white/5 text-left flex flex-col gap-4 backdrop-blur-md"
          >
            <div className="bg-[#E77817]/10 p-3 rounded-xl text-[#E77817] w-max">
              <Award size={22} />
            </div>
            <h3 className="font-semibold text-lg text-white">Digital Certificates</h3>
            <p className="text-sm text-gray-500 leading-relaxed font-light">
              Automated PDF certificate compilation complete with digital signatures, QR codes, and a public verification registry page.
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="bg-[#1A252C]/40 p-6 rounded-2xl border border-white/5 text-left flex flex-col gap-4 backdrop-blur-md"
          >
            <div className="bg-[#E77817]/10 p-3 rounded-xl text-[#E77817] w-max">
              <BrainCircuit size={22} />
            </div>
            <h3 className="font-semibold text-lg text-white">LangGraph AI Assistant</h3>
            <p className="text-sm text-gray-500 leading-relaxed font-light">
              Conversational search tool utilizing RAG database lookup, intent classification, and source citation cards.
            </p>
          </motion.div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/5 py-6 text-center text-xs text-gray-600 z-10 bg-[#070A0D]/90 backdrop-blur-sm">
        <p>© 2026 Lovely Professional University (LPU) Human Resource Development Center (HRDC). All Rights Reserved.</p>
      </footer>
    </div>
  );
}

'use client';

import React from 'react';
import Link from 'next/link';
import { Cpu, ArrowRight, BookOpen, ShieldCheck, Zap, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#070A0D] flex flex-col justify-between relative overflow-hidden">
      {/* Background Glowing Ambient Gradients */}
      <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-lpu-orange/10 rounded-full blur-[150px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-5%] w-[500px] h-[500px] bg-amber-500/5 rounded-full blur-[120px] pointer-events-none" />

      {/* Top Header */}
      <header className="max-w-7xl mx-auto w-full px-6 h-20 flex items-center justify-between z-10">
        <div className="flex items-center gap-3">
          <div className="bg-lpu-orange p-2 rounded-xl text-white shadow-lg shadow-lpu-orange/20">
            <Cpu size={24} />
          </div>
          <div>
            <span className="font-bold text-lg text-white leading-tight tracking-wider">LPU Academic</span>
            <span className="text-xs text-lpu-orange font-bold tracking-widest block">COPILOT</span>
          </div>
        </div>
        
        <Link 
          href="/login" 
          className="px-5 py-2.5 rounded-xl border border-white/10 hover:border-lpu-orange/30 hover:bg-lpu-orange/5 text-sm font-semibold transition-all duration-300 text-white"
        >
          Faculty Login
        </Link>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto w-full px-6 flex-1 flex flex-col justify-center items-center text-center z-10 py-12">
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="bg-white/5 border border-white/10 px-4 py-1.5 rounded-full text-xs font-semibold tracking-wider text-lpu-orange flex items-center gap-2 mb-8"
        >
          <Sparkles size={14} />
          FDP SPECIAL RELEASE: MULTI-AGENT DESIGN PARADIGM
        </motion.div>

        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="text-4xl md:text-6xl font-extrabold tracking-tight text-white leading-[1.1] max-w-4xl font-outfit"
        >
          Automate Faculty Workflows with <span className="text-transparent bg-clip-text bg-gradient-to-r from-lpu-orange via-amber-500 to-orange-400">Multi-Agent Orchestration</span>
        </motion.h1>

        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="text-gray-400 text-md md:text-lg max-w-2xl mt-6 leading-relaxed font-light"
        >
          Upload your syllabus PDF. Let ten specialized AI agents coordinate to generate lesson plans, progressive assignments, MCQ quizzes, Bloom's Taxonomy maps, and exam papers in minutes.
        </motion.p>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-10 flex flex-col sm:flex-row gap-4"
        >
          <Link
            href="/login"
            className="bg-lpu-orange hover:bg-lpu-orangeHover px-8 py-4 rounded-xl font-bold text-white shadow-lg shadow-lpu-orange/20 transition-all duration-300 hover:scale-105 flex items-center gap-3 text-md"
          >
            <span>Enter Copilot Portal</span>
            <ArrowRight size={18} />
          </Link>
          <Link
            href="#features"
            className="bg-white/5 border border-white/10 hover:border-white/20 text-gray-300 hover:text-white px-8 py-4 rounded-xl font-bold transition-all duration-300 text-md"
          >
            Explore Platform Features
          </Link>
        </motion.div>

        {/* Features Showcase Grid */}
        <div id="features" className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl mt-24">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="glass-panel p-6 rounded-2xl border border-white/5 text-left flex flex-col gap-4"
          >
            <div className="bg-lpu-orange/10 p-3 rounded-xl text-lpu-orange w-max">
              <BookOpen size={22} />
            </div>
            <h3 className="font-semibold text-lg text-white">Full Course Planner</h3>
            <p className="text-sm text-gray-500 leading-relaxed font-light">
              Generates week-by-week syllabus breakdowns, lecture topics, reference materials, and pedagogical strategies.
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="glass-panel p-6 rounded-2xl border border-white/5 text-left flex flex-col gap-4"
          >
            <div className="bg-lpu-orange/10 p-3 rounded-xl text-lpu-orange w-max">
              <Zap size={22} />
            </div>
            <h3 className="font-semibold text-lg text-white">Collaborative Agents</h3>
            <p className="text-sm text-gray-500 leading-relaxed font-light">
              Collaborates using ten AI agents (Planning, Reviewer, Bloom, CO Mappings, Quality Checkers) to review and align materials.
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="glass-panel p-6 rounded-2xl border border-white/5 text-left flex flex-col gap-4"
          >
            <div className="bg-lpu-orange/10 p-3 rounded-xl text-lpu-orange w-max">
              <ShieldCheck size={22} />
            </div>
            <h3 className="font-semibold text-lg text-white">Academic Compliance</h3>
            <p className="text-sm text-gray-500 leading-relaxed font-light">
              Audits and maps every exam question to designated Bloom Taxonomy levels and Course Outcomes (COs).
            </p>
          </motion.div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/5 py-6 text-center text-xs text-gray-600 z-10 bg-[#070A0D]/90 backdrop-blur-sm">
        <p>© 2026 Lovely Professional University (LPU) Faculty Development Program. All Rights Reserved.</p>
      </footer>
    </div>
  );
}

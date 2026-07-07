'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { api } from '@/lib/api';
import { 
  BookOpen, 
  Search, 
  Filter, 
  PlusCircle, 
  MapPin, 
  Calendar, 
  Users, 
  Tag, 
  X,
  Loader2
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function ProgrammesPortal() {
  const [programmes, setProgrammes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [role, setRole] = useState('Participant');

  // Form states
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [objectives, setObjectives] = useState('');
  const [category, setCategory] = useState('FDP');
  const [mode, setMode] = useState('Hybrid');
  const [venue, setVenue] = useState('Block 32, Class 405');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [duration, setDuration] = useState(5);
  const [maxCapacity, setMaxCapacity] = useState(50);
  const [tags, setTags] = useState('AI, Machine Learning');

  useEffect(() => {
    setRole(localStorage.getItem('user_role') || 'Participant');
    loadProgrammes();
  }, [categoryFilter, statusFilter]);

  async function loadProgrammes() {
    setLoading(true);
    try {
      const data = await api.getProgrammes(categoryFilter || undefined, statusFilter || undefined);
      setProgrammes(data);
    } catch (e) {
      console.log('Failed to fetch programmes. Using fallbacks.');
      setProgrammes([
        { id: 1, title: 'Faculty Development Programme on Agentic AI & LangGraph', category: 'FDP', mode: 'Hybrid', venue: 'Block 32, Auditorium', current_enrolment: 48, max_capacity: 50, status: 'Active', start_date: new Date().toISOString(), duration_days: 5 },
        { id: 2, title: 'Workhop on Next.js 15 & React 19 Enterprise Architectures', category: 'Workshop', mode: 'Offline', venue: 'Innovation Lab 2', current_enrolment: 24, max_capacity: 30, status: 'Upcoming', start_date: new Date(Date.now() + 86400000 * 5).toISOString(), duration_days: 3 },
        { id: 3, title: 'Refresher Course on Innovative Engineering Pedagogies', category: 'Refresher Course', mode: 'Online', venue: 'LPU Live Stream', current_enrolment: 120, max_capacity: 150, status: 'Completed', start_date: new Date(Date.now() - 86400000 * 10).toISOString(), duration_days: 14 }
      ]);
    } finally {
      setLoading(false);
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        title,
        description,
        objectives,
        category,
        mode,
        venue,
        start_date: new Date(startDate || Date.now()).toISOString(),
        end_date: new Date(endDate || Date.now() + 86400000 * duration).toISOString(),
        duration_days: Number(duration),
        max_capacity: Number(maxCapacity),
        status: 'Upcoming',
        tags: tags.split(',').map(t => t.trim()).filter(Boolean)
      };
      
      await api.createProgramme(payload);
      setIsModalOpen(false);
      loadProgrammes();
      
      // Clear form
      setTitle('');
      setDescription('');
      setObjectives('');
    } catch (err) {
      alert('Error creating programme. Try running with demo bypass mode.');
    }
  };

  const filtered = programmes.filter(p => 
    p.title.toLowerCase().includes(search.toLowerCase()) ||
    (p.description && p.description.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="flex flex-col gap-6">
      {/* Header operations */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-xl font-bold text-white font-outfit">Programmes Registry</h1>
          <p className="text-[10px] text-gray-500 font-medium">Browse, search, enroll, or create academic cycles.</p>
        </div>

        {['HRDC Administrator', 'HRDC Staff', 'Trainer'].includes(role) && (
          <button
            onClick={() => setIsModalOpen(true)}
            className="bg-[#E77817] hover:bg-[#D35400] text-white px-4 py-2.5 rounded-xl font-bold text-xs flex items-center gap-2 shadow-lg shadow-[#E77817]/10 transition-all duration-300"
          >
            <PlusCircle size={16} />
            <span>Launch Programme</span>
          </button>
        )}
      </div>

      {/* Filters Hub */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 bg-[#1A252C]/20 p-4 rounded-2xl border border-white/5">
        <div className="relative">
          <Search size={16} className="absolute left-3 top-3 text-gray-500" />
          <input
            type="text"
            placeholder="Search FDPs or workshops..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10 pr-4 py-2.5 rounded-xl glass-input text-xs w-full"
          />
        </div>

        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="px-4 py-2.5 rounded-xl glass-input text-xs bg-[#1A252C] text-gray-300"
        >
          <option value="">All Categories</option>
          <option value="FDP">FDP (Faculty Development)</option>
          <option value="Workshop">Workshop</option>
          <option value="Orientation Programme">Orientation Programme</option>
          <option value="Refresher Course">Refresher Course</option>
          <option value="Corporate Training">Corporate Training</option>
        </select>

        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-4 py-2.5 rounded-xl glass-input text-xs bg-[#1A252C] text-gray-300"
        >
          <option value="">All Statuses</option>
          <option value="Upcoming">Upcoming</option>
          <option value="Active">Active</option>
          <option value="Completed">Completed</option>
        </select>

        <button 
          onClick={() => { setCategoryFilter(''); setStatusFilter(''); setSearch(''); }}
          className="border border-white/10 hover:bg-white/5 text-gray-400 hover:text-white px-4 py-2.5 rounded-xl text-xs font-semibold transition-all"
        >
          Reset Filters
        </button>
      </div>

      {/* Programmes List Grid */}
      {loading ? (
        <div className="flex justify-center items-center py-20 text-[#E77817]">
          <Loader2 size={36} className="animate-spin" />
        </div>
      ) : filtered.length === 0 ? (
        <div className="glass-panel text-center py-20 text-gray-500 rounded-2xl border border-white/5">
          No programmes found matching filters.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {filtered.map((item) => (
            <motion.div
              layout
              key={item.id}
              className="glass-panel rounded-2xl border border-white/5 overflow-hidden flex flex-col justify-between hover:border-[#E77817]/20 transition-all duration-300 bg-[#1A252C]/10 h-72"
            >
              <div className="p-6 flex flex-col gap-3">
                <div className="flex justify-between items-center">
                  <span className="text-[9px] font-bold uppercase tracking-wider bg-[#E77817]/10 text-[#E77817] px-2 py-0.5 rounded">
                    {item.category}
                  </span>
                  <span className={`text-[8px] uppercase font-extrabold tracking-widest px-2 py-0.5 rounded-full ${
                    item.status === 'Completed' ? 'bg-gray-500/10 text-gray-400' : (item.status === 'Active' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-blue-500/10 text-blue-400')
                  }`}>
                    {item.status}
                  </span>
                </div>

                <h3 className="font-bold text-xs text-white leading-snug line-clamp-2">{item.title}</h3>
                
                {/* Meta details */}
                <div className="flex flex-col gap-2 mt-2 text-[10px] text-gray-400">
                  <div className="flex items-center gap-2">
                    <MapPin size={12} className="text-gray-500" />
                    <span className="truncate">{item.venue || 'Online'} ({item.mode})</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar size={12} className="text-gray-500" />
                    <span>{new Date(item.start_date).toLocaleDateString()} ({item.duration_days} Days)</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Users size={12} className="text-gray-500" />
                    <span>{item.current_enrolment} / {item.max_capacity} Enrolled</span>
                  </div>
                </div>
              </div>

              {/* Action bar */}
              <div className="border-t border-white/5 p-4 bg-[#0F171A]/40 flex justify-between items-center">
                <div className="flex gap-1 overflow-hidden">
                  {item.tags?.slice(0, 2).map((t: string) => (
                    <span key={t} className="text-[8px] text-gray-500 bg-white/5 px-2 py-0.5 rounded truncate max-w-[80px]">
                      {t}
                    </span>
                  ))}
                </div>

                <Link
                  href={`/dashboard/programmes/${item.id}`}
                  className="bg-white/5 border border-white/10 hover:border-[#E77817]/40 hover:bg-[#E77817]/10 text-white hover:text-white px-4 py-2 rounded-xl text-[10px] font-bold transition-all"
                >
                  Manage Lifecycle
                </Link>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Creation Modal */}
      <AnimatePresence>
        {isModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-[#0F171A] border border-white/10 rounded-2xl w-full max-w-2xl overflow-hidden"
            >
              <div className="p-6 border-b border-white/5 flex justify-between items-center bg-[#1A252C]/30">
                <div>
                  <h3 className="font-bold text-sm text-white">Configure New Training Programme</h3>
                  <p className="text-[9px] text-gray-500 mt-0.5">Define category parameters, syllabus details and duration caps.</p>
                </div>
                <button onClick={() => setIsModalOpen(false)} className="text-gray-500 hover:text-white transition-all">
                  <X size={18} />
                </button>
              </div>

              <form onSubmit={handleSubmit} className="p-6 flex flex-col gap-4 max-h-[75vh] overflow-y-auto">
                <div className="flex flex-col gap-1">
                  <label className="text-[10px] text-gray-400 font-bold uppercase">Course Title</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. FDP on Generative AI Orchestration workflows"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="px-4 py-2.5 rounded-xl glass-input text-xs"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="flex flex-col gap-1">
                    <label className="text-[10px] text-gray-400 font-bold uppercase">Category</label>
                    <select
                      value={category}
                      onChange={(e) => setCategory(e.target.value)}
                      className="px-4 py-2.5 rounded-xl glass-input text-xs bg-[#1A252C]"
                    >
                      <option value="FDP">FDP (Faculty Development)</option>
                      <option value="Workshop">Workshop</option>
                      <option value="Orientation Programme">Orientation Programme</option>
                      <option value="Refresher Course">Refresher Course</option>
                      <option value="Technical Training">Technical Training</option>
                      <option value="Corporate Training">Corporate Training</option>
                    </select>
                  </div>

                  <div className="flex flex-col gap-1">
                    <label className="text-[10px] text-gray-400 font-bold uppercase">Mode</label>
                    <select
                      value={mode}
                      onChange={(e) => setMode(e.target.value)}
                      className="px-4 py-2.5 rounded-xl glass-input text-xs bg-[#1A252C]"
                    >
                      <option value="Online">Online</option>
                      <option value="Offline">Offline</option>
                      <option value="Hybrid">Hybrid</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="flex flex-col gap-1">
                    <label className="text-[10px] text-gray-400 font-bold uppercase">Start Date</label>
                    <input
                      type="date"
                      required
                      value={startDate}
                      onChange={(e) => setStartDate(e.target.value)}
                      className="px-4 py-2.5 rounded-xl glass-input text-xs bg-[#1A252C] text-gray-300"
                    />
                  </div>

                  <div className="flex flex-col gap-1">
                    <label className="text-[10px] text-gray-400 font-bold uppercase">End Date</label>
                    <input
                      type="date"
                      required
                      value={endDate}
                      onChange={(e) => setEndDate(e.target.value)}
                      className="px-4 py-2.5 rounded-xl glass-input text-xs bg-[#1A252C] text-gray-300"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="flex flex-col gap-1">
                    <label className="text-[10px] text-gray-400 font-bold uppercase">Duration (Days)</label>
                    <input
                      type="number"
                      required
                      value={duration}
                      onChange={(e) => setDuration(Number(e.target.value))}
                      className="px-4 py-2.5 rounded-xl glass-input text-xs"
                    />
                  </div>

                  <div className="flex flex-col gap-1">
                    <label className="text-[10px] text-gray-400 font-bold uppercase">Maximum Capacity</label>
                    <input
                      type="number"
                      required
                      value={maxCapacity}
                      onChange={(e) => setMaxCapacity(Number(e.target.value))}
                      className="px-4 py-2.5 rounded-xl glass-input text-xs"
                    />
                  </div>

                  <div className="flex flex-col gap-1">
                    <label className="text-[10px] text-gray-400 font-bold uppercase">Venue / Room</label>
                    <input
                      type="text"
                      placeholder="e.g. Block 32, Rm 202"
                      value={venue}
                      onChange={(e) => setVenue(e.target.value)}
                      className="px-4 py-2.5 rounded-xl glass-input text-xs"
                    />
                  </div>
                </div>

                <div className="flex flex-col gap-1">
                  <label className="text-[10px] text-gray-400 font-bold uppercase">Objectives</label>
                  <textarea
                    placeholder="Enter learning outcomes & objectives..."
                    value={objectives}
                    onChange={(e) => setObjectives(e.target.value)}
                    rows={2}
                    className="px-4 py-2.5 rounded-xl glass-input text-xs resize-none"
                  />
                </div>

                <div className="flex flex-col gap-1">
                  <label className="text-[10px] text-gray-400 font-bold uppercase">Tags (comma separated)</label>
                  <input
                    type="text"
                    placeholder="AI, LangGraph, Python"
                    value={tags}
                    onChange={(e) => setTags(e.target.value)}
                    className="px-4 py-2.5 rounded-xl glass-input text-xs"
                  />
                </div>

                <div className="flex justify-end gap-3 mt-4 border-t border-white/5 pt-4">
                  <button
                    type="button"
                    onClick={() => setIsModalOpen(false)}
                    className="border border-white/10 hover:bg-white/5 text-gray-400 hover:text-white px-4 py-2 rounded-xl text-xs font-semibold transition-all"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="bg-[#E77817] hover:bg-[#D35400] text-white px-5 py-2 rounded-xl font-bold text-xs shadow-lg shadow-[#E77817]/10 transition-all duration-300"
                  >
                    Launch Cycle
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}

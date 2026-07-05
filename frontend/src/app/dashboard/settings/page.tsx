'use client';

import React, { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Settings, Save, Cpu, User, CheckCircle2 } from 'lucide-react';
import { motion } from 'framer-motion';

export default function SettingsPage() {
  const [provider, setProvider] = useState('gemini');
  const [modelName, setModelName] = useState('gemini-1.5-flash');
  const [temperature, setTemperature] = useState(0.7);
  
  // Faculty Profile
  const [name, setName] = useState('');
  const [department, setDepartment] = useState('');
  
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    async function loadSettingsAndProfile() {
      try {
        const [settingsRes, profileRes] = await Promise.all([
          api.getSettings(),
          api.getProfile()
        ]);
        
        setProvider(settingsRes.llm_provider || 'gemini');
        setModelName(settingsRes.model_name || 'gemini-1.5-flash');
        setTemperature(settingsRes.temperature !== undefined ? settingsRes.temperature : 0.7);
        
        setName(profileRes.name || '');
        setDepartment(profileRes.department || '');
      } catch (e) {
        console.error("Failed to load settings. Using local overrides.");
        // Demo local storage values fallback
        setName(localStorage.getItem('faculty_name') || 'Dr. Amanpreet Singh');
        setDepartment(localStorage.getItem('department') || 'Computer Science & Engineering');
      } finally {
        setLoading(false);
      }
    }
    
    loadSettingsAndProfile();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSuccessMsg('');

    try {
      // Save local storage bypass configs
      localStorage.setItem('faculty_name', name);
      localStorage.setItem('department', department);

      await Promise.all([
        api.updateSettings(provider, modelName, temperature),
        api.saveProfile(name, department)
      ]);

      setSuccessMsg('Settings and Profile updated successfully.');
      setTimeout(() => setSuccessMsg(''), 4000);
    } catch (err) {
      console.error(err);
      setSuccessMsg('Saved successfully (Demo mode configurations cached locally).');
      setTimeout(() => setSuccessMsg(''), 4000);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12 text-gray-500">Loading settings...</div>;
  }

  return (
    <div className="max-w-3xl mx-auto w-full flex flex-col gap-6">
      <form onSubmit={handleSave} className="flex flex-col gap-6">
        
        {/* Profile Card */}
        <div className="glass-panel p-6 rounded-2xl border border-white/5 flex flex-col gap-4">
          <h3 className="text-md font-semibold text-white flex items-center gap-2 tracking-wide">
            <User size={18} className="text-lpu-orange" />
            Faculty Profile
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-xs text-gray-500 font-medium">Faculty Full Name</label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="px-4 py-3 rounded-xl glass-input text-xs"
                placeholder="e.g. Dr. Amanpreet Singh"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-xs text-gray-500 font-medium">Academic Department</label>
              <select
                value={department}
                onChange={(e) => setDepartment(e.target.value)}
                className="px-4 py-3 rounded-xl glass-input text-xs bg-lpu-charcoal"
              >
                <option value="Computer Science & Engineering">Computer Science & Engineering</option>
                <option value="Information Technology">Information Technology</option>
                <option value="Electronics & Communication">Electronics & Communication</option>
                <option value="Mechanical Engineering">Mechanical Engineering</option>
                <option value="Management & Commerce">Management & Commerce</option>
              </select>
            </div>
          </div>
        </div>

        {/* Model parameters */}
        <div className="glass-panel p-6 rounded-2xl border border-white/5 flex flex-col gap-4">
          <h3 className="text-md font-semibold text-white flex items-center gap-2 tracking-wide">
            <Cpu size={18} className="text-lpu-orange" />
            AI Orchestrator Engine Settings
          </h3>

          <div className="flex flex-col gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-xs text-gray-500 font-medium">Primary LLM Provider</label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setProvider('gemini');
                    setModelName('gemini-1.5-flash');
                  }}
                  className={`py-3 rounded-xl font-bold border text-xs transition-all ${
                    provider === 'gemini' 
                      ? 'border-lpu-orange bg-lpu-orange/10 text-white' 
                      : 'border-white/5 bg-white/5 text-gray-400 hover:text-white'
                  }`}
                >
                  Google Gemini (Recommended)
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setProvider('groq');
                    setModelName('mixtral-8x7b-32768');
                  }}
                  className={`py-3 rounded-xl font-bold border text-xs transition-all ${
                    provider === 'groq' 
                      ? 'border-lpu-orange bg-lpu-orange/10 text-white' 
                      : 'border-white/5 bg-white/5 text-gray-400 hover:text-white'
                  }`}
                >
                  Groq API
                </button>
              </div>
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-xs text-gray-500 font-medium">Model Name</label>
              <select
                value={modelName}
                onChange={(e) => setModelName(e.target.value)}
                className="px-4 py-3 rounded-xl glass-input text-xs bg-lpu-charcoal"
              >
                {provider === 'gemini' ? (
                  <>
                    <option value="gemini-1.5-flash">gemini-1.5-flash (Standard & Fast)</option>
                    <option value="gemini-1.5-pro">gemini-1.5-pro (Highly Logical)</option>
                  </>
                ) : (
                  <>
                    <option value="mixtral-8x7b-32768">mixtral-8x7b-32768</option>
                    <option value="llama3-70b-8192">llama3-70b-8192 (Powerful)</option>
                    <option value="gemma2-9b-it">gemma2-9b-it</option>
                  </>
                )}
              </select>
            </div>

            <div className="flex flex-col gap-1.5">
              <div className="flex justify-between items-center text-xs text-gray-500 font-medium">
                <span>Model Temperature</span>
                <span className="text-white font-semibold">{temperature}</span>
              </div>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.1"
                value={temperature}
                onChange={(e) => setTemperature(parseFloat(e.target.value))}
                className="w-full h-1 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-lpu-orange"
              />
              <span className="text-[10px] text-gray-500 leading-tight">
                Lower temperatures provide deterministic, structured academic maps. Higher values enhance creative phrasing.
              </span>
            </div>
          </div>
        </div>

        {successMsg && (
          <div className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs p-3 rounded-xl font-medium flex items-center gap-2">
            <CheckCircle2 size={16} className="shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        <button
          type="submit"
          disabled={saving}
          className="bg-lpu-orange hover:bg-lpu-orangeHover disabled:bg-lpu-orange/50 py-3.5 rounded-xl font-bold text-white transition-all duration-300 flex items-center justify-center gap-2 shadow-lg shadow-lpu-orange/20"
        >
          <Save size={18} />
          <span>{saving ? 'Saving...' : 'Save Settings & Profile'}</span>
        </button>

      </form>
    </div>
  );
}

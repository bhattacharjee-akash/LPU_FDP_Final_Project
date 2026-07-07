'use client';

import React, { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { 
  Settings, 
  User, 
  Cpu, 
  Save, 
  Loader2,
  CheckCircle
} from 'lucide-react';
import { motion } from 'framer-motion';

export default function SettingsPage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');

  // Profile states
  const [name, setName] = useState('');
  const [role, setRole] = useState('Participant');
  const [department, setDepartment] = useState('');
  const [phone, setPhone] = useState('');
  const [designation, setDesignation] = useState('');

  // LLM settings states
  const [provider, setProvider] = useState('groq');
  const [modelName, setModelName] = useState('llama3-8b-8192');
  const [temp, setTemp] = useState(0.2);

  useEffect(() => {
    loadSettingsData();
  }, []);

  async function loadSettingsData() {
    setLoading(true);
    try {
      const [profileData, settingsData] = await Promise.all([
        api.getProfile(),
        api.getSettings()
      ]);
      
      setName(profileData.name);
      setRole(profileData.role);
      setDepartment(profileData.department || '');
      setPhone(profileData.phone || '');
      setDesignation(profileData.designation || '');

      setProvider(settingsData.llm_provider);
      setModelName(settingsData.model_name);
      setTemp(settingsData.temperature);
    } catch (e) {
      console.log('Failed to fetch settings details. Loading defaults.');
      setName(localStorage.getItem('faculty_name') || 'Dr. Amanpreet Singh');
      setRole(localStorage.getItem('user_role') || 'Participant');
      setDepartment(localStorage.getItem('department') || 'Computer Science');
      setDesignation('Assistant Professor');
    } finally {
      setLoading(false);
    }
  }

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setStatusMsg('');

    try {
      await Promise.all([
        api.saveProfile({ name, role, department, phone, designation }),
        api.updateSettings({ llm_provider: provider, model_name: modelName, temperature: Number(temp) })
      ]);
      // Update local storage demo settings
      localStorage.setItem('faculty_name', name);
      localStorage.setItem('user_role', role);
      localStorage.setItem('department', department);

      setStatusMsg('Configuration settings saved successfully!');
    } catch (err) {
      // Mock bypass simulation save
      localStorage.setItem('faculty_name', name);
      localStorage.setItem('user_role', role);
      localStorage.setItem('department', department);
      setStatusMsg('Configuration saved (Local simulation updated).');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-20 text-[#E77817]">
        <Loader2 size={36} className="animate-spin" />
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-bold text-white font-outfit">System Settings</h1>
        <p className="text-[10px] text-gray-500 font-medium">Configure profile attributes and reasoning parameters.</p>
      </div>

      <form onSubmit={handleSave} className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Profile Card settings */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-2xl border border-white/5 bg-[#1A252C]/10 flex flex-col gap-4">
          <div className="flex items-center gap-2 border-b border-white/5 pb-2">
            <User size={18} className="text-[#E77817]" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-white">Profile Attributes</h3>
          </div>

          <div className="flex flex-col gap-3.5">
            <div className="flex flex-col gap-1">
              <label className="text-[9px] text-gray-500 font-bold uppercase">Display Name</label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="px-4 py-2.5 rounded-xl glass-input text-xs"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-1">
                <label className="text-[9px] text-gray-500 font-bold uppercase">Academic Role</label>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  className="px-4 py-2.5 rounded-xl glass-input text-xs bg-[#1A252C] text-gray-300"
                >
                  <option value="Participant">Participant</option>
                  <option value="Trainer">Trainer (Resource Person)</option>
                  <option value="HRDC Staff">HRDC Staff</option>
                  <option value="HRDC Administrator">HRDC Administrator</option>
                </select>
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-[9px] text-gray-500 font-bold uppercase">Department</label>
                <input
                  type="text"
                  value={department}
                  onChange={(e) => setDepartment(e.target.value)}
                  className="px-4 py-2.5 rounded-xl glass-input text-xs"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-1">
                <label className="text-[9px] text-gray-500 font-bold uppercase">Academic Designation</label>
                <input
                  type="text"
                  value={designation}
                  onChange={(e) => setDesignation(e.target.value)}
                  className="px-4 py-2.5 rounded-xl glass-input text-xs"
                />
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-[9px] text-gray-500 font-bold uppercase">Contact Phone</label>
                <input
                  type="text"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  className="px-4 py-2.5 rounded-xl glass-input text-xs"
                />
              </div>
            </div>
          </div>
        </div>

        {/* LLM / Model configuration */}
        <div className="flex flex-col gap-6">
          <div className="glass-panel p-6 rounded-2xl border border-white/5 bg-[#1A252C]/10 flex flex-col gap-4">
            <div className="flex items-center gap-2 border-b border-white/5 pb-2">
              <Cpu size={18} className="text-[#E77817]" />
              <h3 className="text-xs font-bold uppercase tracking-wider text-white">AI Engine Setup</h3>
            </div>

            <div className="flex flex-col gap-3.5">
              <div className="flex flex-col gap-1">
                <label className="text-[9px] text-gray-500 font-bold uppercase">Model Provider</label>
                <select
                  value={provider}
                  onChange={(e) => setProvider(e.target.value)}
                  className="px-4 py-2.5 rounded-xl glass-input text-xs bg-[#1A252C] text-gray-300"
                >
                  <option value="groq">Groq Cloud API</option>
                  <option value="gemini">Gemini API</option>
                </select>
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-[9px] text-gray-500 font-bold uppercase">Model Name</label>
                <select
                  value={modelName}
                  onChange={(e) => setModelName(e.target.value)}
                  className="px-4 py-2.5 rounded-xl glass-input text-xs bg-[#1A252C] text-gray-300"
                >
                  {provider === 'groq' ? (
                    <>
                      <option value="llama3-8b-8192">llama3-8b-8192 (Fast)</option>
                      <option value="llama3-70b-8192">llama3-70b-8192 (Thorough)</option>
                      <option value="mixtral-8x7b-32768">mixtral-8x7b-32768 (Context)</option>
                    </>
                  ) : (
                    <>
                      <option value="gemini-1.5-flash">gemini-1.5-flash</option>
                      <option value="gemini-1.5-pro">gemini-1.5-pro</option>
                    </>
                  )}
                </select>
              </div>

              <div className="flex flex-col gap-1">
                <div className="flex justify-between text-[9px] text-gray-500 font-bold uppercase">
                  <span>Temperature</span>
                  <span>{temp}</span>
                </div>
                <input
                  type="range"
                  min="0.0"
                  max="1.0"
                  step="0.1"
                  value={temp}
                  onChange={(e) => setTemp(Number(e.target.value))}
                  className="w-full mt-2 accent-[#E77817]"
                />
              </div>
            </div>
          </div>

          {statusMsg && (
            <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-xl text-xs flex items-center gap-2 font-semibold">
              <CheckCircle size={16} />
              <span>{statusMsg}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={saving}
            className="bg-[#E77817] hover:bg-[#D35400] text-white py-3.5 rounded-xl font-bold text-xs shadow-lg shadow-[#E77817]/20 transition-all flex items-center justify-center gap-2 disabled:bg-[#E77817]/50"
          >
            {saving ? <Loader2 size={16} className="animate-spin" /> : <Save size={16} />}
            <span>Save Configuration</span>
          </button>
        </div>

      </form>
    </div>
  );
}

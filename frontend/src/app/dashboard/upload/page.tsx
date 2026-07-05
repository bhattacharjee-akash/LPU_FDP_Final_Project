'use client';

import React, { useState, useEffect, useRef } from 'react';
import { api } from '@/lib/api';
import AgentTimeline, { LogEntry } from '@/components/agent-timeline';
import { FileUp, Eye, Download, AlertTriangle, CheckCircle, HelpCircle } from 'lucide-react';
import Link from 'next/link';

export default function SyllabusUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [syllabusId, setSyllabusId] = useState<number | null>(null);
  const [status, setStatus] = useState<string>('PENDING'); // PENDING, PROCESSING, COMPLETED, FAILED
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [error, setError] = useState<string>('');
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const pollTimerRef = useRef<any>(null);

  // Poll status endpoint every 2 seconds
  const startPolling = (id: number) => {
    if (pollTimerRef.current) clearInterval(pollTimerRef.current);
    
    pollTimerRef.current = setInterval(async () => {
      try {
        const res = await api.getStatus(id);
        setStatus(res.status);
        setLogs(res.logs || []);

        if (res.status === 'COMPLETED' || res.status === 'FAILED') {
          clearInterval(pollTimerRef.current);
          setUploading(false);
        }
      } catch (err) {
        console.error("Polling error", err);
      }
    }, 2000);
  };

  useEffect(() => {
    return () => {
      if (pollTimerRef.current) clearInterval(pollTimerRef.current);
    };
  }, []);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const dropped = e.dataTransfer.files[0];
      if (dropped.type === 'application/pdf') {
        setFile(dropped);
        setError('');
      } else {
        setError('Only PDF syllabi files are supported.');
      }
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError('');
    }
  };

  const triggerUpload = async () => {
    if (!file) return;
    setUploading(true);
    setError('');
    setStatus('PROCESSING');
    setLogs([]);

    try {
      const res = await api.uploadSyllabus(file);
      setSyllabusId(res.syllabus_id);
      setStatus(res.status);
      startPolling(res.syllabus_id);
    } catch (err: any) {
      setError(err.message || 'Syllabus upload failed.');
      setUploading(false);
      setStatus('FAILED');
    }
  };

  return (
    <div className="flex flex-col gap-8">
      {status === 'PENDING' && (
        <div className="max-w-3xl mx-auto w-full flex flex-col gap-6">
          {/* Syllabus instructions */}
          <div className="glass-panel p-6 rounded-2xl border border-white/5 flex flex-col gap-4">
            <h3 className="text-md font-semibold text-white tracking-wide flex items-center gap-2">
              <HelpCircle size={18} className="text-lpu-orange" />
              Syllabus Guidelines
            </h3>
            <p className="text-xs text-gray-400 leading-relaxed font-light">
              For best generation results, upload a standard syllabus PDF containing Course Code, Name, Learning Objectives, Reference Books, and topics divided into units (e.g. Unit 1 to Unit 5).
            </p>
          </div>

          {/* Drag & Drop Area */}
          <div 
            onDragOver={handleDragOver}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className="border-2 border-dashed border-white/10 hover:border-lpu-orange/40 bg-white/5 rounded-3xl p-12 text-center cursor-pointer transition-all duration-300 flex flex-col items-center gap-4"
          >
            <input 
              type="file" 
              ref={fileInputRef}
              onChange={handleFileSelect}
              accept="application/pdf"
              className="hidden"
            />
            
            <div className="p-4 bg-lpu-orange/10 rounded-full text-lpu-orange">
              <FileUp size={32} />
            </div>
            <div>
              <p className="font-semibold text-sm text-white">
                {file ? file.name : 'Select or drop syllabus PDF'}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {file ? `${(file.size / 1024 / 1024).toFixed(2)} MB` : 'PDF files up to 10MB'}
              </p>
            </div>
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-xs p-3 rounded-xl font-medium flex items-center gap-2">
              <AlertTriangle size={14} className="shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {file && (
            <button
              onClick={triggerUpload}
              disabled={uploading}
              className="bg-lpu-orange hover:bg-lpu-orangeHover w-full py-4 rounded-xl font-bold text-white transition-all duration-300 flex items-center justify-center gap-2 shadow-lg shadow-lpu-orange/20"
            >
              <span>Trigger Multi-Agent Workflow</span>
            </button>
          )}
        </div>
      )}

      {status !== 'PENDING' && (
        <div className="flex flex-col gap-6 w-full">
          {/* Generation header banner */}
          <div className="glass-panel p-6 rounded-2xl border border-white/5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h3 className="text-md font-semibold text-white tracking-wide">
                Agent Orchestration Status: <span className="text-lpu-orange">{status}</span>
              </h3>
              <p className="text-xs text-gray-500 mt-1">
                Currently running 10-agent pipeline. Do not close this window.
              </p>
            </div>

            {status === 'COMPLETED' && syllabusId && (
              <div className="flex gap-2">
                <Link
                  href={`/dashboard/history?id=${syllabusId}`}
                  className="bg-white/5 border border-white/10 hover:bg-white/10 text-white px-5 py-2.5 rounded-xl text-xs font-semibold flex items-center gap-2 transition-all"
                >
                  <Eye size={14} />
                  <span>Review Artifacts</span>
                </Link>
                
                <a
                  href={api.getDownloadUrl(syllabusId)}
                  className="bg-lpu-orange hover:bg-lpu-orangeHover text-white px-5 py-2.5 rounded-xl text-xs font-semibold flex items-center gap-2 transition-all shadow-lg shadow-lpu-orange/25"
                >
                  <Download size={14} />
                  <span>Download Report</span>
                </a>
              </div>
            )}
          </div>

          {/* Timeline and Logs component */}
          <AgentTimeline logs={logs} currentStatus={status} />
        </div>
      )}
    </div>
  );
}

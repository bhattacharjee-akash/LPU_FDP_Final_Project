'use client';

import React from 'react';
import { CheckCircle2, Loader2, PlayCircle, AlertCircle } from 'lucide-react';

export interface LogEntry {
  id: number;
  agent_name: string;
  status: string; // STARTED, COMPLETED, FAILED
  log_message: string;
  created_at: string;
}

interface AgentTimelineProps {
  logs: LogEntry[];
  currentStatus: string; // PENDING, PROCESSING, COMPLETED, FAILED
}

export default function AgentTimeline({ logs, currentStatus }: AgentTimelineProps) {
  // Ordered pipeline of agents matching backend execution sequence
  const pipelineAgents = [
    { key: 'System', label: 'PDF Parser / Setup' },
    { key: 'PlanningAgent', label: 'Planning Agent' },
    { key: 'LessonPlanAgent', label: 'Lesson Plan Agent' },
    { key: 'AssignmentAgent', label: 'Assignment Agent' },
    { key: 'QuizAgent', label: 'Quiz Agent' },
    { key: 'QuestionPaperAgent', label: 'Question Paper Agent' },
    { key: 'BloomAgent', label: 'Bloom Taxonomy Agent' },
    { key: 'COMappingAgent', label: 'CO Mapping Agent' },
    { key: 'ReviewerAgent', label: 'Reviewer Agent' },
    { key: 'AcademicQualityAgent', label: 'Academic Quality Agent' },
    { key: 'PDFGenerator', label: 'PDF Report Generator' }
  ];

  const getAgentStatus = (agentKey: string) => {
    const agentLogs = logs.filter(l => l.agent_name === agentKey);
    if (agentLogs.length === 0) return 'PENDING';
    
    const isCompleted = agentLogs.some(l => l.status === 'COMPLETED');
    const isFailed = agentLogs.some(l => l.status === 'FAILED');
    const isStarted = agentLogs.some(l => l.status === 'STARTED');

    if (isFailed) return 'FAILED';
    if (isCompleted) return 'COMPLETED';
    if (isStarted) return 'PROCESSING';
    return 'PENDING';
  };

  return (
    <div className="flex flex-col lg:flex-row gap-8 w-full">
      {/* 1. Visual Node Connectors */}
      <div className="flex-1 glass-panel p-6 rounded-2xl border border-white/5">
        <h3 className="text-md font-semibold text-white mb-6 tracking-wide">Orchestration Flow Timeline</h3>
        
        <div className="relative border-l-2 border-white/10 ml-4 pl-6 flex flex-col gap-6">
          {pipelineAgents.map((agent, idx) => {
            const status = getAgentStatus(agent.key);
            
            let statusIcon = <div className="w-5 h-5 rounded-full bg-gray-800 border-2 border-gray-700" />;
            let textColor = 'text-gray-500';
            let dotBg = 'bg-gray-900';

            if (status === 'COMPLETED') {
              statusIcon = <CheckCircle2 size={20} className="text-emerald-500" />;
              textColor = 'text-gray-200';
              dotBg = 'bg-emerald-500/10';
            } else if (status === 'PROCESSING') {
              statusIcon = <Loader2 size={20} className="text-lpu-orange animate-spin" />;
              textColor = 'text-lpu-orange font-semibold';
              dotBg = 'bg-lpu-orange/10';
            } else if (status === 'FAILED') {
              statusIcon = <AlertCircle size={20} className="text-red-500" />;
              textColor = 'text-red-400 font-semibold';
              dotBg = 'bg-red-500/10';
            }

            return (
              <div key={agent.key} className="relative flex items-start gap-4">
                {/* Absolute position connector dot */}
                <div className={`absolute -left-9 p-0.5 rounded-full bg-background z-10`}>
                  {statusIcon}
                </div>
                
                <div className={`flex-1 p-3 rounded-xl transition-all duration-300 border ${
                  status === 'PROCESSING' 
                    ? 'border-lpu-orange/30 bg-lpu-orange/5 shadow-glassLight' 
                    : 'border-white/5 bg-white/5'
                }`}>
                  <div className="flex justify-between items-center">
                    <span className={`text-sm ${textColor}`}>{agent.label}</span>
                    <span className="text-[10px] uppercase font-bold tracking-widest text-gray-500">
                      {status}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 2. Text Logs stream */}
      <div className="flex-1 glass-panel p-6 rounded-2xl border border-white/5 flex flex-col h-[580px]">
        <h3 className="text-md font-semibold text-white mb-4 tracking-wide">Live Agent Output Stream</h3>
        
        <div className="flex-1 overflow-y-auto bg-black/40 rounded-xl p-4 font-mono text-xs text-gray-400 border border-white/5 flex flex-col gap-3">
          {logs.length === 0 ? (
            <div className="text-gray-600 flex items-center justify-center h-full">
              Waiting for execution loop to start...
            </div>
          ) : (
            logs.map((log) => {
              let logColor = 'text-gray-400';
              if (log.status === 'COMPLETED') logColor = 'text-emerald-400';
              if (log.status === 'FAILED') logColor = 'text-red-400';
              if (log.status === 'STARTED') logColor = 'text-lpu-orange';

              return (
                <div key={log.id} className="border-b border-white/5 pb-2">
                  <div className="flex justify-between text-[10px] text-gray-500 mb-1">
                    <span>{log.agent_name}</span>
                    <span>{new Date(log.created_at).toLocaleTimeString()}</span>
                  </div>
                  <p className={`leading-relaxed ${logColor}`}>
                    [{log.status}] {log.log_message}
                  </p>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}

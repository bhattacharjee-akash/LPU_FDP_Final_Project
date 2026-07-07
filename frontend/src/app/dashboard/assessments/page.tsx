'use client';

import React, { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { 
  FileCheck, 
  HelpCircle, 
  CheckCircle, 
  Clock, 
  Users, 
  Trophy,
  Loader2
} from 'lucide-react';
import { motion } from 'framer-motion';

interface Question {
  id: number;
  question_text: string;
  options: string[];
  correct_option: string;
}

export default function AssessmentsPage() {
  const [assessments, setAssessments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeQuiz, setActiveQuiz] = useState<any>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);
  
  // Results
  const [score, setScore] = useState<number | null>(null);
  const [grade, setGrade] = useState<string | null>(null);
  const [feedback, setFeedback] = useState('');

  // Leaderboard data
  const [leaderboard, setLeaderboard] = useState<any[]>([]);

  useEffect(() => {
    loadAssessments();
    // Seed sample leaderboard data
    setLeaderboard([
      { rank: 1, name: 'Dr. Ramesh Kumar', department: 'Mechanical Eng.', score: 94.0, grade: 'Outstanding' },
      { rank: 2, name: 'Prof. Sunita Sharma', department: 'Computer Science', score: 88.0, grade: 'Excellent' },
      { rank: 3, name: 'Dr. Amanpreet Singh', department: 'Electronics', score: 84.5, grade: 'Excellent' },
      { rank: 4, name: 'Faculty Member', department: 'Computer Science', score: 78.0, grade: 'Good' }
    ]);
  }, []);

  async function loadAssessments() {
    setLoading(true);
    try {
      // Fetch assessments for default program 1
      const data = await api.getAssessments(1);
      setAssessments(data);
    } catch (e) {
      console.log('Failed to fetch assessments. Seeding demo quiz.');
      setAssessments([
        {
          id: 1,
          title: 'LangGraph Concepts Assessment',
          type: 'MCQ',
          max_marks: 50.0,
          passing_marks: 20.0,
          content: {
            questions: [
              { id: 1, question_text: 'What are the main components of a LangGraph workflow?', options: ['Nodes and Edges', 'Lists and Queues', 'Tables and Rows', 'Prompts and Keys'], correct_option: 'A' },
              { id: 2, question_text: 'Which node represents the starting execution entry point?', options: ['Entry Node', 'Base Node', 'Root Node', 'Start Node'], correct_option: 'A' },
              { id: 3, question_text: 'How are conditions evaluated to route execution flows?', options: ['Using conditional edges', 'Using loop branches', 'Using switch cases', 'Using callback hooks'], correct_option: 'A' }
            ]
          }
        }
      ]);
    } finally {
      setLoading(false);
    }
  }

  const handleSelectOption = (qId: number, optLetter: string) => {
    setAnswers({ ...answers, [String(qId)]: optLetter });
  };

  const handleSubmitQuiz = async () => {
    if (!activeQuiz) return;
    setSubmitting(true);
    try {
      const payload = {
        submission_data: { answers }
      };
      const res = await api.submitAssessment(activeQuiz.id, payload);
      setScore(res.score ?? 40.0); // fallback mock score
      setGrade(res.grade ?? 'Pass');
      setFeedback(res.feedback ?? 'Evaluation complete.');
      
      // Update leaderboard user entry
      setLeaderboard([
        { rank: 1, name: 'Dr. Ramesh Kumar', department: 'Mechanical Eng.', score: 94.0, grade: 'Outstanding' },
        { rank: 2, name: 'Prof. Sunita Sharma', department: 'Computer Science', score: 88.0, grade: 'Excellent' },
        { rank: 3, name: 'Dr. Amanpreet Singh', department: 'Electronics', score: 84.5, grade: 'Excellent' },
        { rank: 4, name: 'Faculty Member', department: 'Computer Science', score: res.score ?? 40.0, grade: res.grade ?? 'Pass' }
      ].sort((a,b) => b.score - a.score).map((x, idx) => ({ ...x, rank: idx + 1 })));

    } catch (err) {
      alert('Error submitting quiz answers.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-bold text-white font-outfit">Assessments & Evaluations</h1>
        <p className="text-[10px] text-gray-500 font-medium">Verify your skills by completing automatic auto-evaluated quizzes.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Quiz list / active quiz view */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          {activeQuiz ? (
            <div className="glass-panel p-6 rounded-2xl border border-white/5 bg-[#1A252C]/10 flex flex-col gap-4">
              <div className="flex justify-between items-center border-b border-white/5 pb-3">
                <div>
                  <h3 className="font-bold text-sm text-white">{activeQuiz.title}</h3>
                  <span className="text-[9px] text-[#E77817] font-semibold tracking-wider bg-[#E77817]/10 px-2 py-0.5 rounded uppercase">
                    Max Score: {activeQuiz.max_marks} Marks
                  </span>
                </div>
                
                <button
                  onClick={() => { setActiveQuiz(null); setScore(null); setAnswers({}); }}
                  className="text-xs text-gray-500 hover:text-white transition-all font-semibold"
                >
                  Exit Test
                </button>
              </div>

              {score !== null ? (
                // Display Results
                <div className="flex flex-col items-center justify-center text-center p-8 gap-4">
                  <div className="bg-emerald-500/10 p-4 rounded-full text-emerald-500">
                    <CheckCircle size={36} />
                  </div>
                  <h4 className="font-bold text-sm text-white">Assessment Submitted!</h4>
                  <p className="text-xs text-gray-400 max-w-sm font-light">
                    Your answers were processed and automatically evaluated.
                  </p>

                  <div className="grid grid-cols-3 gap-6 w-full max-w-md bg-[#0F171A] p-4 rounded-xl border border-white/5 mt-2">
                    <div>
                      <span className="text-[9px] text-gray-500 font-bold uppercase">Your Score</span>
                      <h5 className="text-lg font-bold text-white mt-1">{score} / {activeQuiz.max_marks}</h5>
                    </div>
                    <div>
                      <span className="text-[9px] text-gray-500 font-bold uppercase">Grade</span>
                      <h5 className="text-lg font-bold text-emerald-400 mt-1">{grade}</h5>
                    </div>
                    <div>
                      <span className="text-[9px] text-gray-500 font-bold uppercase">Feedback</span>
                      <p className="text-[10px] text-gray-400 mt-1 font-semibold truncate">{feedback}</p>
                    </div>
                  </div>
                </div>
              ) : (
                // Quiz Questions Taker
                <div className="flex flex-col gap-6 mt-2">
                  {activeQuiz.content?.questions?.map((q: Question, index: number) => (
                    <div key={q.id} className="flex flex-col gap-3">
                      <h4 className="text-xs font-semibold text-white">
                        {index + 1}. {q.question_text}
                      </h4>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {q.options.map((opt: string, optIdx: number) => {
                          const letter = String.fromCharCode(65 + optIdx); // A, B, C, D
                          const isSelected = answers[String(q.id)] === letter;
                          return (
                            <button
                              key={opt}
                              onClick={() => handleSelectOption(q.id, letter)}
                              className={`text-left p-3 rounded-xl border text-xs font-medium transition-all ${
                                isSelected 
                                  ? 'border-[#E77817] bg-[#E77817]/10 text-white' 
                                  : 'border-white/5 bg-[#0F171A] hover:bg-white/5 text-gray-300'
                              }`}
                            >
                              <span className="font-bold mr-2 text-[#E77817]">{letter}.</span>
                              {opt}
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  ))}

                  <button
                    onClick={handleSubmitQuiz}
                    disabled={submitting}
                    className="bg-[#E77817] hover:bg-[#D35400] disabled:bg-[#E77817]/50 py-3.5 rounded-xl font-bold text-xs text-white transition-all duration-300 mt-6 flex items-center justify-center gap-2"
                  >
                    {submitting ? <Loader2 size={16} className="animate-spin" /> : <FileCheck size={16} />}
                    <span>Submit & Auto-Evaluate</span>
                  </button>
                </div>
              )}

            </div>
          ) : (
            // Assessments list
            <div className="flex flex-col gap-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-white">Assigned Evaluations</h3>
              {loading ? (
                <div className="text-xs text-gray-500 text-center py-8">Loading tests...</div>
              ) : assessments.length === 0 ? (
                <div className="glass-panel text-center py-10 text-gray-500 rounded-xl border border-white/5">
                  No exams assigned to your profile.
                </div>
              ) : (
                assessments.map((a) => (
                  <div key={a.id} className="bg-[#1A252C]/10 border border-white/5 rounded-xl p-6 flex justify-between items-center hover:border-[#E77817]/20 transition-all">
                    <div className="flex items-center gap-3">
                      <div className="bg-[#E77817]/10 p-2.5 rounded-lg text-[#E77817]">
                        <HelpCircle size={20} />
                      </div>
                      <div>
                        <h4 className="font-bold text-xs text-white">{a.title}</h4>
                        <span className="text-[9px] text-gray-500 font-bold uppercase">Format: {a.type} | Max Marks: {a.max_marks}</span>
                      </div>
                    </div>

                    <button
                      onClick={() => setActiveQuiz(a)}
                      className="bg-white/5 border border-white/10 hover:bg-[#E77817]/10 hover:border-[#E77817]/40 px-4 py-2 rounded-xl text-[10px] font-bold transition-all text-white"
                    >
                      Start Test
                    </button>
                  </div>
                ))
              )}
            </div>
          )}
        </div>

        {/* Right Column: Leaderboard */}
        <div className="flex-1 glass-panel p-6 rounded-2xl border border-white/5 bg-[#1A252C]/10 flex flex-col gap-4">
          <div className="flex items-center gap-2 border-b border-white/5 pb-2">
            <Trophy size={18} className="text-[#E77817]" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-white">Class Leaderboard</h3>
          </div>

          <div className="flex flex-col gap-3">
            {leaderboard.map((user) => (
              <div 
                key={user.rank} 
                className={`p-3 rounded-xl border flex justify-between items-center bg-[#0F171A]/80 ${
                  user.name === 'Faculty Member' ? 'border-[#E77817]/30' : 'border-white/5'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <span className={`w-5 h-5 rounded-md flex items-center justify-center font-bold text-[10px] ${
                    user.rank === 1 ? 'bg-amber-500/20 text-amber-400' : (user.rank === 2 ? 'bg-gray-400/20 text-gray-300' : 'bg-orange-800/20 text-orange-400')
                  }`}>
                    {user.rank}
                  </span>
                  <div>
                    <h4 className="text-[10px] font-semibold text-white truncate max-w-[120px]">{user.name}</h4>
                    <span className="text-[8px] text-gray-500 block font-semibold">{user.department}</span>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-[10px] font-bold text-white block">{user.score} pts</span>
                  <span className="text-[8px] text-gray-500 font-bold uppercase">{user.grade}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

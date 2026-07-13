'use client';

import React, { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { FileText, Eye, Download, Calendar, ArrowLeft, BarChart3, AlertCircle, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';

interface HistoryItem {
  id: number;
  status: string;
  created_at: string;
  syllabus: {
    id: number;
    filename: string;
    course_name: string;
    course_code: string;
    created_at: string;
  };
}

export default function HistoryPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const syllabusId = searchParams.get('id');

  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [selectedReport, setSelectedReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [reportLoading, setReportLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('lesson_plan');

  // Load history list
  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await api.getHistory();
        setHistory(data);
      } catch (e) {
        console.error("Failed to load history list. Mock defaults will be set.", e);
        // Fallback FDP demonstration history items
        setHistory([
          {
            id: 1,
            status: "COMPLETED",
            created_at: new Date().toISOString(),
            syllabus: {
              id: 1,
              filename: "Modern_Software_Engineering.pdf",
              course_name: "Modern Software Engineering & AI Systems",
              course_code: "CSE421",
              created_at: new Date().toISOString()
            }
          }
        ]);
      } finally {
        setLoading(false);
      }
    }
    loadHistory();
  }, []);

  // Load details if a report is selected
  useEffect(() => {
    async function loadReport() {
      if (!syllabusId) {
        setSelectedReport(null);
        return;
      }
      setReportLoading(true);
      try {
        const data = await api.getReport(parseInt(syllabusId));
        setSelectedReport(data);
      } catch (e) {
        console.error("Could not load report.", e);
        // Load fallback mock dataset
        setSelectedReport(getMockReportData());
      } finally {
        setReportLoading(false);
      }
    }
    loadReport();
  }, [syllabusId]);

  const getMockReportData = () => {
    // Generate fallback data matching DB structure
    return {
      syllabus: {
        id: 1,
        course_name: "Modern Software Engineering & AI Systems",
        course_code: "CSE421",
        filename: "Modern_Software_Engineering.pdf",
        created_at: new Date().toISOString()
      },
      lesson_plan: {
        weeks: Array.from({ length: 15 }, (_, i) => ({
          week_number: i + 1,
          unit_number: Math.floor(i / 3) + 1,
          topics: [
            i % 3 === 0 ? "Introduction to Concepts" : "Advanced Architecture Patterns",
            "Practical Labs and Code Exercises"
          ],
          learning_objectives: ["Identify foundational models.", "Formulate scaling scripts."],
          pedagogy: "Flipped classroom and programming labs",
          resources: "Core Text chapter " + (Math.floor(i / 3) + 1)
        }))
      },
      assignments: {
        assignments: [
          {
            assignment_number: 1,
            title: "Agile Estimation and User Story Generation",
            total_marks: 30,
            instructions: "Submit Scrum ceremony answers and board diagrams.",
            questions: [
              { question_number: 1, question_text: "State Agile estimation principles.", marks: 15, suggested_solution_guideline: "Check planning poker reference." }
            ]
          }
        ]
      },
      quiz: {
        questions: Array.from({ length: 20 }, (_, i) => ({
          question_number: i + 1,
          unit_number: Math.floor(i / 4) + 1,
          question_text: `Test Question number ${i + 1} regarding Software Engineering.`,
          options: { A: "First Option", B: "Second Option", C: "Third Option", D: "Fourth Option" },
          correct_option: "A",
          explanation: "Option A is correct due to standard software architectures."
        }))
      },
      mid_sem_paper: {
        total_marks: 50,
        duration: "2 Hours",
        instructions: "Solve all questions.",
        sections: [
          {
            section_name: "Section A",
            marks_per_question: 2,
            questions: [{ question_number: 1, text: "What is Git?", unit_reference: 1 }]
          }
        ]
      },
      end_sem_paper: {
        total_marks: 100,
        duration: "3 Hours",
        instructions: "Solve all questions.",
        sections: [
          {
            section_name: "Section C",
            marks_per_question: 10,
            questions: [{ question_number: 16, text: "Explain Kubernetes orchestrations in detail.", unit_reference: 5 }]
          }
        ]
      },
      bloom_mapping: {
        unit_mappings: [
          { unit_number: 1, cognitive_level: "Applying", action_verbs: ["Demonstrate"], justification: "Introduction topics apply standard rules." }
        ],
        co_mappings: [
          { co_code: "CO1", cognitive_level: "Understanding", justification: "Basics of Scrum mapping." }
        ],
        target_distribution: { remembering: 20, understanding: 30, applying: 30, analyzing: 10, evaluating: 5, creating: 5 }
      },
      co_mapping: {
        co_weightage: [
          { co_code: "CO1", marks_allocated: 32, percentage_weightage: 21.3 }
        ]
      },
      quality_report: {
        score: 88.5,
        dimensions: { alignment: 92, coverage: 89, clarity_and_rigor: 85, pedagogy: 88 },
        suggestions: [
          { dimension: "coverage", issue: "Week 14 lacks concrete labs.", recommendation: "Add repository template link." }
        ]
      }
    };
  };

  const handleBack = () => {
    router.push('/dashboard/history');
  };

  if (loading) {
    return <div className="text-center py-12 text-gray-500">Loading history reports...</div>;
  }

  // --- DETAIL VIEW LAYOUT ---
  if (selectedReport) {
    const course = selectedReport.syllabus;
    const rawQRep = selectedReport.quality_report || {};
    const qRep = {
      score: rawQRep.score || rawQRep.content?.overall_score || rawQRep.content?.score || 0,
      dimensions: rawQRep.dimensions || rawQRep.content?.dimensions || {},
      suggestions: rawQRep.suggestions || rawQRep.content?.suggestions || []
    };
    
    const tabs = [
      { id: 'lesson_plan', label: '15-Week Plan' },
      { id: 'assignments', label: 'Assignments' },
      { id: 'quiz', label: 'MCQ Quiz' },
      { id: 'exams', label: 'Exam Papers' },
      { id: 'bloom', label: "Bloom's Map" },
      { id: 'co_mapping', label: 'CO Align' },
      { id: 'quality', label: 'Quality Audit' }
    ];

    return (
      <div className="flex flex-col gap-6">
        {/* Header toolbar */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <button 
            onClick={handleBack}
            className="flex items-center gap-2 text-xs text-gray-400 hover:text-white transition-colors"
          >
            <ArrowLeft size={16} />
            <span>Back to History</span>
          </button>
          
          <div className="flex gap-2 w-full sm:w-auto">
            <a 
              href={api.getDownloadUrl(course.id)}
              className="bg-lpu-orange hover:bg-lpu-orangeHover text-white px-5 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 transition-all shadow-lg shadow-lpu-orange/20"
            >
              <Download size={14} />
              <span>Download Publication PDF</span>
            </a>
          </div>
        </div>

        {/* Title metadata */}
        <div className="glass-panel p-6 rounded-2xl border border-white/5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h2 className="text-xl font-bold text-white font-outfit">{course.course_name}</h2>
            <p className="text-xs text-gray-500 mt-1">
              Course Code: {course.course_code || 'N/A'} | Filename: {course.filename}
            </p>
          </div>

          <div className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-4 py-2 rounded-xl text-sm font-bold flex items-center gap-2">
            <CheckCircle size={16} />
            <span>Audit Score: {qRep.score}/100</span>
          </div>
        </div>

        {/* Tabs switcher header */}
        <div className="flex border-b border-white/10 overflow-x-auto gap-2 pb-px">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-3 text-xs font-semibold whitespace-nowrap border-b-2 transition-all ${
                activeTab === tab.id 
                  ? 'border-lpu-orange text-lpu-orange' 
                  : 'border-transparent text-gray-400 hover:text-white hover:border-white/10'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Dynamic Tab content render */}
        <div className="glass-panel p-6 rounded-2xl border border-white/5 min-h-[400px]">
          {/* TAB: LESSON PLAN */}
          {activeTab === 'lesson_plan' && (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-white/10 text-gray-400 font-bold">
                    <th className="pb-3 w-16">Week</th>
                    <th className="pb-3 w-48">Core Topics</th>
                    <th className="pb-3">Objectives</th>
                    <th className="pb-3 w-56">Pedagogical Delivery & Materials</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 text-gray-300">
                  {selectedReport.lesson_plan?.weeks?.map((w: any) => (
                    <tr key={w.week_number} className="hover:bg-white/5">
                      <td className="py-4 font-semibold text-white">W{w.week_number} <span className="text-[10px] text-gray-500 block">Unit {w.unit_number}</span></td>
                      <td className="py-4 pr-3">
                        <ul className="list-disc pl-4 flex flex-col gap-1">
                          {w.topics?.map((t: string, idx: number) => <li key={idx}>{t}</li>)}
                        </ul>
                      </td>
                      <td className="py-4 pr-3">
                        <ul className="list-disc pl-4 flex flex-col gap-1 text-gray-400">
                          {w.learning_objectives?.map((o: string, idx: number) => <li key={idx}>{o}</li>)}
                        </ul>
                      </td>
                      <td className="py-4 text-xs text-gray-400 leading-relaxed">
                        <div className="mb-1"><b className="text-gray-300">Pedagogy:</b> {w.pedagogy}</div>
                        <div><b className="text-gray-300">Resources:</b> {w.resources}</div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* TAB: ASSIGNMENTS */}
          {activeTab === 'assignments' && (
            <div className="flex flex-col gap-8">
              {selectedReport.assignments?.assignments?.map((asn: any) => (
                <div key={asn.assignment_number} className="border-b border-white/5 pb-6 last:border-b-0">
                  <div className="flex justify-between items-center mb-3">
                    <h4 className="font-bold text-sm text-white">
                      Assignment {asn.assignment_number}: {asn.title}
                    </h4>
                    <span className="text-xs text-lpu-orange bg-lpu-orange/10 px-2 py-0.5 rounded font-medium">
                      Marks: {asn.total_marks}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mb-4"><b>Instructions:</b> {asn.instructions}</p>
                  
                  <div className="flex flex-col gap-4 pl-4 border-l border-white/10">
                    {asn.questions?.map((q: any) => (
                      <div key={q.question_number} className="text-xs">
                        <p className="font-semibold text-white mb-1">
                          Q{q.question_number}. {q.question_text} <span className="text-gray-500 font-normal">({q.marks} Marks)</span>
                        </p>
                        <p className="text-gray-500 italic mt-0.5">Evaluation guideline: {q.suggested_solution_guideline}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* TAB: MCQS QUIZ */}
          {activeTab === 'quiz' && (
            <div className="flex flex-col gap-6">
              {selectedReport.quiz?.questions?.map((q: any) => (
                <div key={q.question_number} className="text-xs border-b border-white/5 pb-4 last:border-b-0">
                  <p className="font-semibold text-white mb-2">
                    Q{q.question_number}. {q.question_text} <span className="text-gray-500 font-normal">[Unit {q.unit_number}]</span>
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mb-3">
                    {Object.entries(q.options || {}).map(([key, val]: any) => (
                      <div key={key} className={`p-2.5 rounded-xl border ${
                        q.correct_option === key 
                          ? 'border-emerald-500/20 bg-emerald-500/5 text-emerald-400 font-medium' 
                          : 'border-white/5 bg-white/5 text-gray-400'
                      }`}>
                        {key}) {val}
                      </div>
                    ))}
                  </div>
                  <p className="text-gray-500 text-[11px] leading-relaxed">
                    <b>Explanation:</b> {q.explanation}
                  </p>
                </div>
              ))}
            </div>
          )}

          {/* TAB: EXAMS */}
          {activeTab === 'exams' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Mid Sem */}
              <div className="border-r border-white/5 pr-6">
                <div className="flex justify-between items-center mb-4 pb-2 border-b border-white/5">
                  <h4 className="font-bold text-sm text-white">Mid-Semester Exam Paper</h4>
                  <span className="text-xs text-gray-500">Marks: 50 | 2 Hours</span>
                </div>
                
                <div className="flex flex-col gap-6">
                  {selectedReport.mid_sem_paper?.sections?.map((sec: any) => (
                    <div key={sec.section_name} className="text-xs">
                      <p className="font-bold text-lpu-orange uppercase tracking-wider mb-2">{sec.section_name} ({sec.marks_per_question} Marks each)</p>
                      <div className="flex flex-col gap-2 pl-2">
                        {sec.questions?.map((q: any) => (
                          <p key={q.question_number} className="text-gray-300">
                            Q{q.question_number}. {q.text} <span className="text-[10px] text-gray-500">[Unit {q.unit_reference}]</span>
                          </p>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* End Sem */}
              <div>
                <div className="flex justify-between items-center mb-4 pb-2 border-b border-white/5">
                  <h4 className="font-bold text-sm text-white">End-Semester Exam Paper</h4>
                  <span className="text-xs text-gray-500">Marks: 100 | 3 Hours</span>
                </div>

                <div className="flex flex-col gap-6">
                  {selectedReport.end_sem_paper?.sections?.map((sec: any) => (
                    <div key={sec.section_name} className="text-xs">
                      <p className="font-bold text-lpu-orange uppercase tracking-wider mb-2">{sec.section_name} ({sec.marks_per_question} Marks each)</p>
                      <div className="flex flex-col gap-2 pl-2">
                        {sec.questions?.map((q: any) => (
                          <p key={q.question_number} className="text-gray-300">
                            Q{q.question_number}. {q.text} <span className="text-[10px] text-gray-500">[Unit {q.unit_reference}]</span>
                          </p>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* TAB: BLOOM */}
          {activeTab === 'bloom' && (
            <div className="flex flex-col gap-6 text-xs">
              <h4 className="font-bold text-sm text-white mb-2">Bloom's Taxonomy Alignment</h4>
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-white/10 text-gray-400 font-bold">
                    <th className="pb-3 w-40">Unit / Outcome</th>
                    <th className="pb-3 w-48">Cognitive Domain</th>
                    <th className="pb-3">Mapping Description / Verbs</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 text-gray-300">
                  {selectedReport.bloom_mapping?.unit_mappings?.map((u: any) => (
                    <tr key={u.unit_number} className="hover:bg-white/5">
                      <td className="py-4 font-semibold text-white">Unit {u.unit_number}</td>
                      <td className="py-4 text-lpu-orange font-medium">{u.cognitive_level}</td>
                      <td className="py-4 leading-relaxed">
                        <div className="mb-1"><b>Verbs:</b> {u.action_verbs?.join(', ')}</div>
                        <p className="text-gray-500 italic">{u.justification}</p>
                      </td>
                    </tr>
                  ))}
                  {selectedReport.bloom_mapping?.co_mappings?.map((co: any) => (
                    <tr key={co.co_code} className="hover:bg-white/5">
                      <td className="py-4 font-semibold text-white">{co.co_code}</td>
                      <td className="py-4 text-emerald-400 font-medium">{co.cognitive_level}</td>
                      <td className="py-4 text-gray-500 italic">{co.justification}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* TAB: CO WEIGHT */}
          {activeTab === 'co_mapping' && (
            <div className="flex flex-col gap-6 text-xs">
              <h4 className="font-bold text-sm text-white mb-2">Course Outcomes Weightage Breakdown</h4>
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-white/10 text-gray-400 font-bold">
                    <th className="pb-3">Course Outcome</th>
                    <th className="pb-3">Total Marks Allocated</th>
                    <th className="pb-3">Percentage Weightage</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 text-gray-300">
                  {selectedReport.co_mapping?.co_weightage?.map((co: any) => (
                    <tr key={co.co_code}>
                      <td className="py-4 font-semibold text-white">{co.co_code}</td>
                      <td className="py-4">{co.marks_allocated} Marks</td>
                      <td className="py-4 text-lpu-orange font-semibold">{co.percentage_weightage}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* TAB: QUALITY AUDIT */}
          {activeTab === 'quality' && (
            <div className="flex flex-col gap-6 text-xs">
              {/* Dimension scores */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                {Object.entries(qRep.dimensions || {}).map(([dim, score]: any) => (
                  <div key={dim} className="bg-white/5 border border-white/5 p-4 rounded-xl">
                    <p className="text-[10px] text-gray-500 uppercase font-bold tracking-wider mb-2">{dim.replace('_', ' ')}</p>
                    <p className="text-xl font-bold text-white">{score}/100</p>
                  </div>
                ))}
              </div>

              {/* Suggestions list */}
              <div>
                <h4 className="font-bold text-sm text-white mb-4">Improvement Recommendations</h4>
                <div className="flex flex-col gap-3">
                  {qRep.suggestions?.map((sug: any, idx: number) => (
                    <div key={idx} className="bg-white/5 border border-white/5 p-4 rounded-xl">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-[10px] font-bold text-lpu-orange uppercase tracking-wider">
                          {sug.dimension}
                        </span>
                      </div>
                      <p className="text-gray-300 mb-1"><b>Issue:</b> {sug.issue}</p>
                      <p className="text-gray-400 font-light"><b>Action:</b> {sug.recommendation}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // --- MASTER HISTORY DIRECTORY LIST ---
  return (
    <div className="flex flex-col gap-6">
      <div className="glass-panel p-6 rounded-2xl border border-white/5">
        <h3 className="text-md font-semibold text-white tracking-wide mb-6">Generated Course Packages</h3>
        
        {history.length === 0 ? (
          <div className="text-center py-12 text-gray-500 text-xs">
            No course packages found in configuration archives.
          </div>
        ) : (
          <div className="flex flex-col gap-4">
            {history.map((item) => (
              <div 
                key={item.id}
                className="bg-white/5 border border-white/5 rounded-xl p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 hover:border-lpu-orange/20 transition-all duration-300"
              >
                <div className="flex items-center gap-3">
                  <div className="bg-lpu-orange/10 p-2.5 rounded-lg text-lpu-orange">
                    <FileText size={18} />
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm text-white">{item.syllabus?.course_name}</h4>
                    <p className="text-[10px] text-gray-500 mt-0.5 flex items-center gap-2">
                      <span>Code: {item.syllabus?.course_code || 'N/A'}</span>
                      <span>•</span>
                      <span className="flex items-center gap-1">
                        <Calendar size={10} />
                        {new Date(item.created_at).toLocaleDateString()}
                      </span>
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 w-full sm:w-auto justify-end">
                  <span className={`text-[10px] uppercase font-bold tracking-widest px-2.5 py-1 rounded-full ${
                    item.status === 'COMPLETED' 
                      ? 'bg-emerald-500/10 text-emerald-400' 
                      : (item.status === 'PROCESSING' ? 'bg-lpu-orange/10 text-lpu-orange animate-pulse' : 'bg-red-500/10 text-red-400')
                  }`}>
                    {item.status}
                  </span>
                  
                  {item.status === 'COMPLETED' && (
                    <div className="flex gap-2">
                      <button
                        onClick={() => router.push(`/dashboard/history?id=${item.syllabus_id}`)}
                        className="p-2 bg-white/5 hover:bg-white/10 rounded-lg text-gray-300 hover:text-white transition-colors"
                        title="View Full Package"
                      >
                        <Eye size={14} />
                      </button>
                      <a 
                        href={api.getDownloadUrl(item.syllabus_id)}
                        className="p-2 bg-lpu-orange/20 hover:bg-lpu-orange text-lpu-orange hover:text-white rounded-lg transition-colors"
                        title="Download PDF"
                      >
                        <Download size={14} />
                      </a>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

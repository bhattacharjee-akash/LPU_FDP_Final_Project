import json
from app.agents.base_agent import BaseAgent

class ReviewerAgent(BaseAgent):
    def run(
        self,
        planning_data: dict,
        lesson_plan: dict,
        assignments: dict,
        quiz: dict,
        question_papers: dict,
        bloom_mapping: dict,
        co_mapping: dict
    ) -> dict:
        system_instruction = self.read_prompt_template("reviewer_prompt.txt")
        # Condense large artifacts to prevent exceeding Groq TPM limits
        condensed_lesson_plan = {}
        if isinstance(lesson_plan, dict) and "weeks" in lesson_plan:
            condensed_lesson_plan = {
                "course_name": lesson_plan.get("course_name"),
                "weeks": [
                    {"week": w.get("week"), "topics": w.get("topics"), "unit": w.get("unit")}
                    for w in lesson_plan["weeks"]
                ]
            }
        else:
            condensed_lesson_plan = lesson_plan

        condensed_quiz = {}
        if isinstance(quiz, dict) and "questions" in quiz:
            condensed_quiz = {
                "questions": [
                    {"question_number": q.get("question_number"), "question_text": q.get("question_text")}
                    for q in quiz["questions"]
                ]
            }
        else:
            condensed_quiz = quiz

        condensed_assignments = {}
        if isinstance(assignments, dict) and "assignments" in assignments:
            condensed_assignments = {
                "assignments": [
                    {"assignment_number": a.get("assignment_number"), "title": a.get("title"), "units_covered": a.get("units_covered")}
                    for a in assignments["assignments"]
                ]
            }
        else:
            condensed_assignments = assignments

        user_prompt = (
            "Review the following generated academic artifacts for consistency, completeness, and quality:\n\n"
            f"1. Planning Data:\n{json.dumps(planning_data, indent=2)}\n\n"
            f"2. Lesson Plan (Condensed for tokens):\n{json.dumps(condensed_lesson_plan, indent=2)}\n\n"
            f"3. Assignments (Condensed for tokens):\n{json.dumps(condensed_assignments, indent=2)}\n\n"
            f"4. Quiz (Condensed for tokens):\n{json.dumps(condensed_quiz, indent=2)}\n\n"
            f"5. Question Papers:\n{json.dumps(question_papers, indent=2)}\n\n"
            f"6. Bloom Mapping:\n{json.dumps(bloom_mapping, indent=2)}\n\n"
            f"7. Course Outcome Mapping:\n{json.dumps(co_mapping, indent=2)}\n\n"
        )
        
        if self.should_use_fallback():
            return self._get_mock_response()
            
        for attempt in range(2):
            try:
                response_text = self.generate(system_instruction, user_prompt, json_mode=True)
                return self.clean_json_response(response_text)
            except Exception as e:
                if attempt == 1:
                    raise e
                print(f"ReviewerAgent generation failed: {str(e)}. Retrying...")

    def _get_mock_response(self) -> dict:
        return {
          "overall_status": "APPROVED",
          "artifact_reviews": {
            "lesson_plan": {
              "status": "APPROVED",
              "comments": "The 15-week plan covers all 5 syllabus units sequentially with appropriate lecture topics, pedagogy, and resource list."
            },
            "assignments": {
              "status": "APPROVED",
              "comments": "All 3 assignments contain clear marks, instructions, and progressive complexity suitable for evaluation."
            },
            "quiz": {
              "status": "APPROVED",
              "comments": "Contains exactly 20 distinct MCQs mapped to course topics with full answers and explanations."
            },
            "question_papers": {
              "status": "APPROVED",
              "comments": "Mid semester (50 marks) and End semester (100 marks) papers match LPU's structural guidelines perfectly."
            },
            "bloom_mapping": {
              "status": "APPROVED",
              "comments": "Bloom classification shows appropriate cognitive levels for foundations (K1/K2) versus design and development (K3/K4/K6)."
            },
            "co_mapping": {
              "status": "APPROVED",
              "comments": "All questions have clear Course Outcomes mappings, ensuring transparent weightage evaluation."
            }
          }
        }

import json
from app.agents.base_agent import BaseAgent

class AcademicQualityAgent(BaseAgent):
    def run(
        self,
        planning_data: dict,
        lesson_plan: dict,
        assignments: dict,
        quiz: dict,
        question_papers: dict,
        bloom_mapping: dict,
        co_mapping: dict,
        reviewer_status: dict
    ) -> dict:
        system_instruction = self.read_prompt_template("academic_quality_prompt.txt")
        
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
            "Evaluate the quality of the generated course package using the following inputs:\n\n"
            f"1. Planning Data:\n{json.dumps(planning_data, indent=2)}\n\n"
            f"2. Lesson Plan (Condensed for tokens):\n{json.dumps(condensed_lesson_plan, indent=2)}\n\n"
            f"3. Assignments (Condensed for tokens):\n{json.dumps(condensed_assignments, indent=2)}\n\n"
            f"4. Quiz (Condensed for tokens):\n{json.dumps(condensed_quiz, indent=2)}\n\n"
            f"5. Question Papers:\n{json.dumps(question_papers, indent=2)}\n\n"
            f"6. Bloom Mapping:\n{json.dumps(bloom_mapping, indent=2)}\n\n"
            f"7. Course Outcome Mapping:\n{json.dumps(co_mapping, indent=2)}\n\n"
            f"8. Reviewer Status:\n{json.dumps(reviewer_status, indent=2)}\n"
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
                print(f"AcademicQualityAgent generation failed: {str(e)}. Retrying...")

    def _get_mock_response(self) -> dict:
        return {
          "overall_score": 88.5,
          "dimensions": {
            "alignment": 92.0,
            "coverage": 89.0,
            "clarity_and_rigor": 85.0,
            "pedagogy": 88.0
          },
          "suggestions": [
            {
              "dimension": "coverage",
              "issue": "Week 14 covers advanced agentic workflows but leaves very little practical coding exercises.",
              "recommendation": "Incorporate a small GitHub repository link or template for hands-on experience during the lab session."
            },
            {
              "dimension": "clarity_and_rigor",
              "issue": "Mid Semester Section A consists mostly of definitional questions.",
              "recommendation": "Include at least one conceptual question testing 'Why' or 'How' to prompt critical analysis."
            },
            {
              "dimension": "pedagogy",
              "issue": "Flipped classroom is mentioned, but student preparation materials aren't specified.",
              "recommendation": "Assign specific preparatory video readings in the resources column of the week prior."
            }
          ],
          "conclusion": "The generated course package meets academic quality compliance. There is high correspondence between targeted outcomes and exam questions."
        }

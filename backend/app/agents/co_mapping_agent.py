import json
from app.agents.base_agent import BaseAgent

class COMappingAgent(BaseAgent):
    def run(self, planning_data: dict, question_paper_data: dict) -> dict:
        system_instruction = self.read_prompt_template("co_mapping_prompt.txt")
        user_prompt = (
            f"Using the course outcomes:\n{json.dumps(planning_data, indent=2)}\n\n"
            f"And the generated question papers:\n{json.dumps(question_paper_data, indent=2)}\n\n"
            f"Perform a Course Outcome (CO) mapping weightage analysis."
        )
        
        if not self.gemini_key and not self.groq_key:
            return self._get_mock_response(planning_data, question_paper_data)
            
        try:
            response_text = self.generate(system_instruction, user_prompt, json_mode=True)
            return self.clean_json_response(response_text)
        except Exception as e:
            print(f"COMappingAgent Error: {str(e)}. Using fallback mock data.")
            return self._get_mock_response(planning_data, question_paper_data)

    def _get_mock_response(self, planning_data: dict, question_paper_data: dict) -> dict:
        cos = planning_data.get("course_outcomes", [])
        
        co_weightage = []
        for idx, co in enumerate(cos):
            co_code = co.get("co_code", f"CO{idx+1}")
            # Mock some percentages
            weight = [25, 20, 25, 15, 15]
            marks_allocated = [37, 30, 38, 22, 23]
            co_weightage.append({
                "co_code": co_code,
                "marks_allocated": marks_allocated[idx % len(marks_allocated)],
                "percentage_weightage": weight[idx % len(weight)]
            })
            
        return {
          "question_mappings": {
            "mid_semester": [
              {"section": "Section A", "question_number": 1, "mapped_co": "CO1", "weightage_marks": 2},
              {"section": "Section A", "question_number": 2, "mapped_co": "CO2", "weightage_marks": 2},
              {"section": "Section A", "question_number": 3, "mapped_co": "CO3", "weightage_marks": 2},
              {"section": "Section A", "question_number": 4, "mapped_co": "CO1", "weightage_marks": 2},
              {"section": "Section A", "question_number": 5, "mapped_co": "CO2", "weightage_marks": 2},
              {"section": "Section B", "question_number": 6, "mapped_co": "CO1", "weightage_marks": 5},
              {"section": "Section B", "question_number": 7, "mapped_co": "CO2", "weightage_marks": 5},
              {"section": "Section B", "question_number": 8, "mapped_co": "CO3", "weightage_marks": 5},
              {"section": "Section B", "question_number": 9, "mapped_co": "CO3", "weightage_marks": 5},
              {"section": "Section C", "question_number": 10, "mapped_co": "CO2", "weightage_marks": 10},
              {"section": "Section C", "question_number": 11, "mapped_co": "CO1", "weightage_marks": 10}
            ],
            "end_semester": [
              {"section": "Section A", "question_number": 1, "mapped_co": "CO4", "weightage_marks": 2},
              {"section": "Section A", "question_number": 2, "mapped_co": "CO4", "weightage_marks": 2},
              {"section": "Section A", "question_number": 3, "mapped_co": "CO5", "weightage_marks": 2},
              {"section": "Section A", "question_number": 4, "mapped_co": "CO5", "weightage_marks": 2},
              {"section": "Section A", "question_number": 5, "mapped_co": "CO2", "weightage_marks": 2},
              {"section": "Section A", "question_number": 6, "mapped_co": "CO3", "weightage_marks": 2},
              {"section": "Section A", "question_number": 7, "mapped_co": "CO5", "weightage_marks": 2},
              {"section": "Section A", "question_number": 8, "mapped_co": "CO1", "weightage_marks": 2},
              {"section": "Section A", "question_number": 9, "mapped_co": "CO4", "weightage_marks": 2},
              {"section": "Section A", "question_number": 10, "mapped_co": "CO3", "weightage_marks": 2},
              {"section": "Section B", "question_number": 11, "mapped_co": "CO1", "weightage_marks": 6},
              {"section": "Section B", "question_number": 12, "mapped_co": "CO2", "weightage_marks": 6},
              {"section": "Section B", "question_number": 13, "mapped_co": "CO4", "weightage_marks": 6},
              {"section": "Section B", "question_number": 14, "mapped_co": "CO5", "weightage_marks": 6},
              {"section": "Section B", "question_number": 15, "mapped_co": "CO3", "weightage_marks": 6},
              {"section": "Section C", "question_number": 16, "mapped_co": "CO5", "weightage_marks": 10},
              {"section": "Section C", "question_number": 17, "mapped_co": "CO4", "weightage_marks": 10},
              {"section": "Section C", "question_number": 18, "mapped_co": "CO3", "weightage_marks": 10},
              {"section": "Section C", "question_number": 19, "mapped_co": "CO2", "weightage_marks": 10},
              {"section": "Section C", "question_number": 20, "mapped_co": "CO1", "weightage_marks": 10}
            ]
          },
          "co_weightage": co_weightage,
          "coverage_gaps": [
            "Assessments are relatively well-balanced. However, CO5 (monitoring and live telemetry) is tested mostly in the final section. Consider raising early exposure through minor quizzes."
          ]
        }

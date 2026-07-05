import json
from app.agents.base_agent import BaseAgent

class BloomAgent(BaseAgent):
    def run(self, planning_data: dict) -> dict:
        system_instruction = self.read_prompt_template("bloom_prompt.txt")
        user_prompt = f"Using the course outcomes and units below, generate a Bloom's Taxonomy report:\n\n{json.dumps(planning_data, indent=2)}"
        
        if not self.gemini_key and not self.groq_key:
            return self._get_mock_response(planning_data)
            
        try:
            response_text = self.generate(system_instruction, user_prompt, json_mode=True)
            return self.clean_json_response(response_text)
        except Exception as e:
            print(f"BloomAgent Error: {str(e)}. Using fallback mock data.")
            return self._get_mock_response(planning_data)

    def _get_mock_response(self, planning_data: dict) -> dict:
        units = planning_data.get("units", [])
        cos = planning_data.get("course_outcomes", [])
        
        unit_mappings = []
        for u in units:
            num = u.get("unit_number", 1)
            title = u.get("title", "Core concepts")
            
            # Formulate mappings
            cog_level = "Remembering / Understanding" if num == 1 else ("Applying" if num in [2, 3] else "Analyzing / Creating")
            verbs = ["Define", "Describe", "Identify"] if num == 1 else (["Apply", "Implement", "Design"] if num in [2, 3] else ["Analyze", "Critique", "Formulate"])
            
            unit_mappings.append({
                "unit_number": num,
                "cognitive_level": cog_level,
                "action_verbs": verbs,
                "justification": f"Focuses on building the fundamental parameters and introductory models of {title}."
            })
            
        co_mappings = []
        for idx, co in enumerate(cos):
            co_code = co.get("co_code", f"CO{idx+1}")
            cog_level = "Understanding" if idx == 0 else ("Applying" if idx in [1, 2] else "Analyzing / Creating")
            
            co_mappings.append({
                "co_code": co_code,
                "cognitive_level": cog_level,
                "justification": f"Addresses the student's capability to operate and implement concepts related to the {co_code} statement."
            })
            
        return {
          "unit_mappings": unit_mappings,
          "co_mappings": co_mappings,
          "target_distribution": {
            "remembering": 20,
            "understanding": 30,
            "applying": 25,
            "analyzing": 15,
            "evaluating": 5,
            "creating": 5
          }
        }

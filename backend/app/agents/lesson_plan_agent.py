import json
from app.agents.base_agent import BaseAgent

class LessonPlanAgent(BaseAgent):
    def run(self, planning_data: dict) -> dict:
        system_instruction = self.read_prompt_template("lesson_plan_prompt.txt")
        user_prompt = f"Using the course structure below, generate a 15-week lesson plan:\n\n{json.dumps(planning_data, indent=2)}"
        
        if self.should_use_fallback():
            return self._get_mock_response(planning_data)
            
        for attempt in range(2):
            try:
                response_text = self.generate(system_instruction, user_prompt, json_mode=True)
                return self.clean_json_response(response_text)
            except Exception as e:
                if attempt == 1:
                    raise e
                print(f"LessonPlanAgent generation failed: {str(e)}. Retrying...")

    def _get_mock_response(self, planning_data: dict) -> dict:
        course_name = planning_data.get("course_name", "Software Engineering")
        course_code = planning_data.get("course_code", "CSE421")
        units = planning_data.get("units", [])
        
        weeks = []
        # Distribute units across 15 weeks
        # 5 units total: unit 1 (weeks 1-3), unit 2 (weeks 4-6), unit 3 (weeks 7-9), unit 4 (weeks 10-12), unit 5 (weeks 13-15)
        for w in range(1, 16):
            unit_index = min((w - 1) // 3, len(units) - 1)
            current_unit = units[unit_index] if units else {"unit_number": (w-1)//3 + 1, "title": "General Core Concepts", "topics": ["Introduction", "Advanced Analysis"]}
            
            # Simple topic selection
            topics = current_unit.get("topics", [])
            selected_topics = [topics[(w - 1) % len(topics)]] if topics else ["General overview"]
            if len(topics) > 1:
                selected_topics.append(topics[(w) % len(topics)])
                
            weeks.append({
                "week_number": w,
                "unit_number": current_unit.get("unit_number", 1),
                "topics": selected_topics,
                "learning_objectives": [
                    f"Explain foundational aspects of {selected_topics[0]}.",
                    f"Synthesize principles relating to {selected_topics[-1]}."
                ],
                "pedagogy": "Interactive Lecture and Team Discussion" if w % 2 == 1 else "Lab demonstration and case study",
                "resources": f"Core Textbook Chapter {unit_index + 1}, online documentation."
            })
            
        return {
            "course_name": course_name,
            "course_code": course_code,
            "weeks": weeks
        }

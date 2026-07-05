import json
from app.agents.base_agent import BaseAgent

class AssignmentAgent(BaseAgent):
    def run(self, planning_data: dict) -> dict:
        system_instruction = self.read_prompt_template("assignment_prompt.txt")
        user_prompt = f"Using the course structure below, generate exactly 3 assignments:\n\n{json.dumps(planning_data, indent=2)}"
        
        if not self.gemini_key and not self.groq_key:
            return self._get_mock_response(planning_data)
            
        try:
            response_text = self.generate(system_instruction, user_prompt, json_mode=True)
            return self.clean_json_response(response_text)
        except Exception as e:
            print(f"AssignmentAgent Error: {str(e)}. Using fallback mock data.")
            return self._get_mock_response(planning_data)

    def _get_mock_response(self, planning_data: dict) -> dict:
        return {
          "assignments": [
            {
              "assignment_number": 1,
              "title": "Requirement Specification & Agile Execution",
              "units_covered": [1],
              "total_marks": 30,
              "instructions": "Draft clean requirements and a Scrum board layout. Submit as a single PDF.",
              "questions": [
                {
                  "question_number": 1,
                  "question_text": "Draft user stories and acceptance criteria for a library management login and search system.",
                  "marks": 15,
                  "suggested_solution_guideline": "Expect at least 3 user stories with detailed Given-When-Then criteria."
                },
                {
                  "question_number": 2,
                  "question_text": "Explain Scrum ceremonies and the key responsibilities of a Scrum Master versus a Product Owner.",
                  "marks": 15,
                  "suggested_solution_guideline": "Look for descriptions of Daily Standup, Sprint Planning, Review, and Retrospective."
                }
              ]
            },
            {
              "assignment_number": 2,
              "title": "Architectural Design and Design Patterns",
              "units_covered": [2],
              "total_marks": 30,
              "instructions": "Answer the design pattern questions below, focusing on architectural patterns.",
              "questions": [
                {
                  "question_number": 1,
                  "question_text": "Illustrate with a class diagram how you would apply the Factory Method and Observer pattern to a real-time notification service.",
                  "marks": 15,
                  "suggested_solution_guideline": "Class diagram must clearly show relationships, Abstract Creator, Concrete Creators, Observers and Subject."
                },
                {
                  "question_number": 2,
                  "question_text": "Compare microservices and monolithic architectures. What are the key strategies for managing data consistency across service boundaries?",
                  "marks": 15,
                  "suggested_solution_guideline": "Explain Saga pattern, Event sourcing, and transactional outbox. Compare database per service strategy."
                }
              ]
            },
            {
              "assignment_number": 3,
              "title": "CI/CD Setup and Agentic Architectures",
              "units_covered": [3, 4],
              "total_marks": 30,
              "instructions": "Complete assignments covering devops workflows and AI integrations.",
              "questions": [
                {
                  "question_number": 1,
                  "question_text": "Write a complete GitHub Actions YAML workflow that builds a dockerized FastAPI container and pushes it to Docker Hub on every main branch commit.",
                  "marks": 15,
                  "suggested_solution_guideline": "YAML syntax should be correct, showing jobs, steps, action tags, and secrets variables configuration."
                },
                {
                  "question_number": 2,
                  "question_text": "Design a multi-agent system workflow to review pull requests automatically. Draw a state diagram showing interactions.",
                  "marks": 15,
                  "suggested_solution_guideline": "Agent roles should cover ReviewerAgent, CriticAgent, and ArchitectAgent. State transitions must show validation loops."
                }
              ]
            }
          ]
        }

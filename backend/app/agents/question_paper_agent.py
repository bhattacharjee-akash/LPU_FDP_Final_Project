import json
from app.agents.base_agent import BaseAgent

class QuestionPaperAgent(BaseAgent):
    def run(self, planning_data: dict) -> dict:
        system_instruction = self.read_prompt_template("question_paper_prompt.txt")
        user_prompt = f"Using the course structure below, generate Mid Sem and End Sem question papers:\n\n{json.dumps(planning_data, indent=2)}"
        
        if not self.gemini_key and not self.groq_key:
            return self._get_mock_response(planning_data)
            
        try:
            response_text = self.generate(system_instruction, user_prompt, json_mode=True)
            return self.clean_json_response(response_text)
        except Exception as e:
            print(f"QuestionPaperAgent Error: {str(e)}. Using fallback mock data.")
            return self._get_mock_response(planning_data)

    def _get_mock_response(self, planning_data: dict) -> dict:
        # Construct standard LPU structured mock papers
        return {
          "mid_semester": {
            "total_marks": 50,
            "duration": "2 Hours",
            "instructions": "Attempt all questions from Section A, any four from Section B, and both from Section C.",
            "sections": [
              {
                "section_name": "Section A",
                "marks_per_question": 2,
                "questions": [
                  {"question_number": 1, "text": "Define the term 'Sprint backlog' in Scrum.", "unit_reference": 1},
                  {"question_number": 2, "text": "State the Single Responsibility Principle.", "unit_reference": 2},
                  {"question_number": 3, "text": "What is containerization?", "unit_reference": 3},
                  {"question_number": 4, "text": "List any two Scrum ceremonies.", "unit_reference": 1},
                  {"question_number": 5, "text": "What is the key difference between monorepos and polyrepos?", "unit_reference": 2}
                ]
              },
              {
                "section_name": "Section B",
                "marks_per_question": 5,
                "questions": [
                  {"question_number": 6, "text": "Explain agile software estimation using Planning Poker.", "unit_reference": 1},
                  {"question_number": 7, "text": "Contrast the Factory Method and Abstract Factory patterns.", "unit_reference": 2},
                  {"question_number": 8, "text": "Describe the main stages of building and pushing a Docker image.", "unit_reference": 3},
                  {"question_number": 9, "text": "Detail how you would implement continuous integration using GitHub actions.", "unit_reference": 3}
                ]
              },
              {
                "section_name": "Section C",
                "marks_per_question": 10,
                "questions": [
                  {"question_number": 10, "text": "Design a complete microservices architecture for an e-commerce cart. Draw details on database separation, communication (REST vs Message Brokers), and consistency.", "unit_reference": 2},
                  {"question_number": 11, "text": "Analyze a scenario where a team is transitioning from Waterfall to Scrum. Identify 3 major risks and suggest mitigation strategies.", "unit_reference": 1}
                ]
              }
            ]
          },
          "end_semester": {
            "total_marks": 100,
            "duration": "3 Hours",
            "instructions": "All sections are compulsory. Internal choice is provided in Sections B and C.",
            "sections": [
              {
                "section_name": "Section A",
                "marks_per_question": 2,
                "questions": [
                  {"question_number": 1, "text": "Define the concept of an 'Agent' in AI frameworks.", "unit_reference": 4},
                  {"question_number": 2, "text": "What is a multi-agent orchestration pattern?", "unit_reference": 4},
                  {"question_number": 3, "text": "Define container orchestration.", "unit_reference": 5},
                  {"question_number": 4, "text": "What is application telemetry?", "unit_reference": 5},
                  {"question_number": 5, "text": "State the Open-Closed Principle (SOLID).", "unit_reference": 2},
                  {"question_number": 6, "text": "Why is git tagging useful in releases?", "unit_reference": 3},
                  {"question_number": 7, "text": "What is the purpose of Prometheus?", "unit_reference": 5},
                  {"question_number": 8, "text": "What are Course Outcomes?", "unit_reference": 1},
                  {"question_number": 9, "text": "Identify one difference between Gemini and Groq model architectures.", "unit_reference": 4},
                  {"question_number": 10, "text": "What is a Dockerfile?", "unit_reference": 3}
                ]
              },
              {
                "section_name": "Section B",
                "marks_per_question": 6,
                "questions": [
                  {"question_number": 11, "text": "Compare Flipped Classroom pedagogy with standard lectures.", "unit_reference": 1},
                  {"question_number": 12, "text": "Explain the Saga architectural pattern for distributed transactions.", "unit_reference": 2},
                  {"question_number": 13, "text": "Explain how multi-agent structures like AutoGen manage chat loops.", "unit_reference": 4},
                  {"question_number": 14, "text": "Describe the logging process using Sentry in web frameworks.", "unit_reference": 5},
                  {"question_number": 15, "text": "Explain Docker Compose configurations and its role in local testing.", "unit_reference": 3}
                ]
              },
              {
                "section_name": "Section C",
                "marks_per_question": 10,
                "questions": [
                  {"question_number": 16, "text": "Design a container orchestration setup in Kubernetes for a high-traffic API. Detail Pods, Deployments, Services, and ingress rules.", "unit_reference": 5},
                  {"question_number": 17, "text": "Evaluate the use of AI coding assistants like Github Copilot. What is the impact on code quality and security?", "unit_reference": 4},
                  {"question_number": 18, "text": "Design a complete CI/CD pipeline detailing static code analysis, unit testing, docker build, scanning, and staging deployment.", "unit_reference": 3},
                  {"question_number": 19, "text": "Explain SOLID principles in detail, showing code snippet examples of violating and applying the Liskov Substitution Principle.", "unit_reference": 2},
                  {"question_number": 20, "text": "Describe the implementation of a full-stack Next.js project layout showing route groups, layouts, and API integrations.", "unit_reference": 1}
                ]
              }
            ]
          }
        }

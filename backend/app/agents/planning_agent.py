import json
from app.agents.base_agent import BaseAgent

class PlanningAgent(BaseAgent):
    def run(self, syllabus_text: str) -> dict:
        system_instruction = self.read_prompt_template("planning_prompt.txt")
        user_prompt = f"Analyze this course syllabus text:\n\n{syllabus_text}"
        
        if self.should_use_fallback():
            return self._get_mock_response(syllabus_text)
            
        for attempt in range(2):
            try:
                response_text = self.generate(system_instruction, user_prompt, json_mode=True)
                return self.clean_json_response(response_text)
            except Exception as e:
                if attempt == 1:
                    raise e
                print(f"PlanningAgent generation failed: {str(e)}. Retrying...")

    def _get_mock_response(self, syllabus_text: str) -> dict:
        # Standard mock parsing if no API key
        course_name = "Modern Software Engineering & AI Systems"
        course_code = "CSE421"
        
        # Simple heuristics to detect name
        lines = syllabus_text.split("\n")
        for line in lines[:5]:
            if len(line) > 5 and len(line) < 100:
                course_name = line
                break

        return {
          "course_name": course_name,
          "course_code": course_code,
          "units": [
            {
              "unit_number": 1,
              "title": "Introduction to Software Engineering & Agile Principles",
              "topics": ["Agile Manifesto", "Scrum framework", "User Stories", "Sprint planning"]
            },
            {
              "unit_number": 2,
              "title": "System Architecture & Design Patterns",
              "topics": ["Microservices architecture", "Creational, Structural, and Behavioral Patterns", "SOLID principles"]
            },
            {
              "unit_number": 3,
              "title": "Testing, CI/CD, and DevOps Pipelines",
              "topics": ["Unit testing and Integration testing", "Jenkins & GitHub Actions", "Docker containerization"]
            },
            {
              "unit_number": 4,
              "title": "AI-Assisted Development & Multi-Agent Frameworks",
              "topics": ["Large Language Models API integration", "LangChain & AutoGen concepts", "Prompt engineering for code generation"]
            },
            {
              "unit_number": 5,
              "title": "Monitoring, Scaling & Cloud Deployment",
              "topics": ["Kubernetes orchestration", "Sentry logging & Prometheus monitoring", "Serverless architectures"]
            }
          ],
          "course_outcomes": [
            {
              "co_code": "CO1",
              "description": "Understand and apply Agile Scrum workflows in software development projects."
            },
            {
              "co_code": "CO2",
              "description": "Design secure and scalable microservices architectures using proper software design patterns."
            },
            {
              "co_code": "CO3",
              "description": "Set up CI/CD pipelines and containerized configurations for automated application deployment."
            },
            {
              "co_code": "CO4",
              "description": "Incorporate LLM models and agentic workflows to build automated coding solutions."
            },
            {
              "co_code": "CO5",
              "description": "Implement container orchestration and live application telemetry in cloud environments."
            }
          ]
        }

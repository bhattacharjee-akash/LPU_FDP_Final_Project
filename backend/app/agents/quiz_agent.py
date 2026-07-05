import json
from app.agents.base_agent import BaseAgent

class QuizAgent(BaseAgent):
    def run(self, planning_data: dict) -> dict:
        system_instruction = self.read_prompt_template("quiz_prompt.txt")
        user_prompt = f"Using the course structure below, generate exactly 20 multiple-choice questions:\n\n{json.dumps(planning_data, indent=2)}"
        
        if not self.gemini_key and not self.groq_key:
            return self._get_mock_response(planning_data)
            
        try:
            response_text = self.generate(system_instruction, user_prompt, json_mode=True)
            return self.clean_json_response(response_text)
        except Exception as e:
            print(f"QuizAgent Error: {str(e)}. Using fallback mock data.")
            return self._get_mock_response(planning_data)

    def _get_mock_response(self, planning_data: dict) -> dict:
        questions = []
        mock_questions_data = [
            ("Which model is best suited for incremental developments with active user feedback?", "Scrum", "Waterfall", "V-Model", "Spiral", "A", "Scrum allows rapid feedback loops through sprint iterations."),
            ("What is the primary role of a Product Owner in Scrum?", "Write code", "Manage team schedules", "Prioritize product backlog", "Perform system testing", "C", "The Product Owner is responsible for maximizing product value and prioritizing backlog."),
            ("What does the 'S' in SOLID principles stand for?", "Systematic Design", "Single Responsibility", "Structural Pattern", "State Management", "B", "Single Responsibility Principle dictates that a class should have only one reason to change."),
            ("Which pattern is best to dynamically attach additional responsibilities to an object?", "Decorator", "Factory", "Singleton", "Adapter", "A", "Decorator pattern allows wrapping objects to extend behavior dynamically."),
            ("In RESTful API design, which HTTP method is typically used to update an existing resource partially?", "POST", "PUT", "PATCH", "DELETE", "C", "PATCH is used for partial updates, whereas PUT is for complete replacements."),
            ("What does CI/CD stand for?", "Code Integration / Code Delivery", "Continuous Integration / Continuous Deployment", "Constant Improvement / Constant Development", "Collaborative Integration / Core Development", "B", "Continuous Integration and Continuous Deployment/Delivery."),
            ("Which of the following is a container virtualization technology?", "Jenkins", "Kubernetes", "Docker", "Prometheus", "C", "Docker package software in isolated lightweight containerized environments."),
            ("In Docker, which instruction is used to copy local files into the container filesystem?", "ADD", "COPY", "RUN", "ENV", "B", "The COPY instruction duplicates local files/directories into the container."),
            ("What is the purpose of Kubernetes in deployment?", "Version control", "Container orchestration", "Database management", "Code compilation", "B", "Kubernetes automates scaling, deployment, and operation of application containers."),
            ("Which agent configuration focuses on a single LLM loop without external tool permissions?", "ReAct agent", "Zero-shot agent", "Conversational agent", "Planning agent", "B", "Zero-shot processes inputs directly without iterative tool execution cycles."),
            ("What is temperature configuration used for in LLMs?", "Model speed", "Context window size", "Output randomness", "Token limit", "C", "Higher temperatures increase randomness; lower temperatures yield deterministic results."),
            ("Which of the following is an example of an application-level metrics monitoring system?", "Sentry", "Git", "Prometheus", "SonarQube", "C", "Prometheus gathers and monitors time-series metrics data."),
            ("What is a course outcome (CO)?", "List of grading categories", "Expected capabilities of a student at course completion", "Table of contents", "Lecture timetable", "B", "COs outline what skills students acquire by the end of a syllabus."),
            ("Under Bloom's Taxonomy, which category is 'Formulate a new testing plan' classified in?", "Remembering", "Applying", "Analyzing", "Creating", "D", "Formulation of something new maps to 'Creating' (K6)."),
            ("What is the role of a Reviewer Agent in a multi-agent system?", "Write the base code", "Validate and refine outputs of other agents", "Upload the PDF", "Query the database", "B", "Reviewer agents examine drafts for errors and completeness."),
            ("Which command is used to run database migrations in Alembic?", "alembic init", "alembic upgrade head", "alembic revision", "alembic stamp", "B", "Upgrade head applies all pending migrations to the current database state."),
            ("Which HTTP status code represents unauthorized client access?", "400 Bad Request", "401 Unauthorized", "403 Forbidden", "404 Not Found", "B", "401 represents credentials verification failure."),
            ("What does RLS stand for in database design?", "Relational Linkage Schema", "Row Level Security", "Read Line Storage", "Recovery Log System", "B", "Row Level Security restricts data access based on user credentials per table row."),
            ("Why is PDF report generation helpful in academic auditing?", "Provides raw textual copy", "Standardizes records in locked formats for easy verification", "Improves execution speed", "Decreases database storage size", "B", "Standardized PDFs secure layout consistency for formal evaluation."),
            ("Which SQLAlchemy attribute establishes linkages between relational tables?", "ForeignKey", "relationship", "Column", "declarative_base", "B", "The relationship helper creates ORM properties linking associated tables.")
        ]
        
        for idx, item in enumerate(mock_questions_data):
            q_text, opt_a, opt_b, opt_c, opt_d, ans, exp = item
            questions.append({
                "question_number": idx + 1,
                "unit_number": (idx // 4) + 1,
                "question_text": q_text,
                "options": {
                    "A": opt_a,
                    "B": opt_b,
                    "C": opt_c,
                    "D": opt_d
                },
                "correct_option": ans,
                "explanation": exp
            })
            
        return {
            "quiz_title": f"Quiz for {planning_data.get('course_name', 'Syllabus Course')}",
            "questions": questions
        }

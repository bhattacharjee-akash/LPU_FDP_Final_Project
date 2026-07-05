import os
import json
import google.generativeai as genai
from groq import Groq
from app.config import settings

class BaseAgent:
    def __init__(self, provider: str = None, model_name: str = None, temperature: float = None):
        self.provider = provider or settings.DEFAULT_LLM_PROVIDER
        self.model_name = model_name or (
            settings.DEFAULT_GEMINI_MODEL if self.provider == "gemini" else settings.DEFAULT_GROQ_MODEL
        )
        self.temperature = temperature if temperature is not None else settings.DEFAULT_TEMPERATURE
        
        # Setup clients
        self.gemini_key = settings.GEMINI_API_KEY
        self.groq_key = settings.GROQ_API_KEY
        
        if self.provider == "gemini" and self.gemini_key:
            genai.configure(api_key=self.gemini_key)
        self.groq_client = Groq(api_key=self.groq_key) if self.groq_key else None

    def read_prompt_template(self, filename: str) -> str:
        """
        Reads prompt text file from backend/app/prompts directory.
        """
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_path = os.path.join(current_dir, "prompts", filename)
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def generate(self, system_instruction: str, user_prompt: str, json_mode: bool = True) -> str:
        """
        Executes generation using the chosen LLM provider (Gemini or Groq).
        """
        if self.provider == "gemini":
            return self._generate_gemini(system_instruction, user_prompt, json_mode)
        elif self.provider == "groq":
            return self._generate_groq(system_instruction, user_prompt, json_mode)
        else:
            # Fallback to gemini if provider unrecognized
            return self._generate_gemini(system_instruction, user_prompt, json_mode)

    def _generate_gemini(self, system_instruction: str, user_prompt: str, json_mode: bool) -> str:
        if not self.gemini_key:
            # Raise error or fallback mock response for demo if keys not provided
            raise ValueError("GEMINI_API_KEY is not set.")
        
        generation_config = {
            "temperature": self.temperature,
        }
        if json_mode:
            generation_config["response_mime_type"] = "application/json"

        model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config,
            system_instruction=system_instruction
        )
        
        response = model.generate_content(user_prompt)
        return response.text

    def _generate_groq(self, system_instruction: str, user_prompt: str, json_mode: bool) -> str:
        if not self.groq_key:
            raise ValueError("GROQ_API_KEY is not set.")
        
        response_format = {"type": "json_object"} if json_mode else None
        
        chat_completion = self.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            model=self.model_name,
            temperature=self.temperature,
            response_format=response_format
        )
        return chat_completion.choices[0].message.content

    def clean_json_response(self, text: str) -> dict:
        """
        Cleans markdown wrappers if present and parses text to python dict.
        """
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            # Fallback parsing/handling
            raise ValueError(f"Agent response was not valid JSON: {str(e)}\nResponse was: {text}")

import json
from src.llm.llm_client import LLMClient
from src.retrieval.vector_store import VectorDB

class SchedulerAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.vector_db = VectorDB()
    
    def create_initial_schedule(self, context: dict) -> list:
        """Generate task list from LLM"""
        project_id = context.get("project_id", "Unknown")
        location = context.get("location", "Unknown")
        notes = context.get("notes", "")
        
        prompt = f"""
        You are a construction project manager. Create a realistic construction schedule for:
        - Project ID: {project_id}
        - Location: {location}
        - Notes: {notes}
        
        Generate a JSON list of construction tasks. Each task should have:
        - id (e.g., "T-001")
        - description (what work is done)
        - phase (Site Prep, Foundation, Framing, Enclosure, MEP, Finishes)
        - dependencies (list of task IDs that must complete first)
        
        Output ONLY valid JSON, no other text.
        
        Example format:
        [
          {{"id": "T-001", "description": "Clear and grade site", "phase": "Site Preparation", "dependencies": []}},
          {{"id": "T-002", "description": "Pour foundation concrete", "phase": "Foundation", "dependencies": ["T-001"]}}
        ]
        """
        
        response = self.llm.generate(prompt)
        
        try:
            # Clean response if needed
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            
            tasks = json.loads(response)
            return tasks
        except json.JSONDecodeError:
            return [{"id": "T-001", "description": "Review project requirements", "phase": "General", "dependencies": []}]
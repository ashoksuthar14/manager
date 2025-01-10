from crewai import Agent
from utils.gemini_helper import GeminiHelper

class TaskManagerAgent:
    def __init__(self, gemini_helper: GeminiHelper):
        self.gemini = gemini_helper
        
    def create_agent(self) -> Agent:
        return Agent(
            role='Task Manager',
            goal='Break down project into detailed tasks and establish dependencies',
            backstory="""You are a skilled task manager with expertise in creating 
            detailed work breakdown structures and managing task dependencies.""",
            tools=[
                self.create_task_breakdown,
                self.define_dependencies,
                self.estimate_task_effort
            ],
            verbose=True
        )
    
    def create_task_breakdown(self, project_analysis: str) -> str:
        """Create detailed task breakdown from project analysis"""
        prompt = f"""
        Create a detailed task breakdown including:
        1. Task name
        2. Description
        3. Deliverables
        4. Required skills
        5. Priority level
        
        Project Analysis: {project_analysis}
        """
        return self.gemini.model.generate_content(prompt).text
    
    def define_dependencies(self, tasks: str) -> str:
        """Define dependencies between tasks"""
        prompt = f"""
        Analyze these tasks and identify:
        1. Task dependencies
        2. Sequential requirements
        3. Parallel possibilities
        4. Critical path tasks
        5. Bottlenecks
        
        Tasks: {tasks}
        """
        return self.gemini.model.generate_content(prompt).text
    
    def estimate_task_effort(self, tasks: str) -> str:
        """Estimate effort required for each task"""
        prompt = f"""
        For each task, provide:
        1. Estimated hours
        2. Required skill level
        3. Risk factors
        4. Complexity rating
        5. Resource requirements
        
        Tasks: {tasks}
        """
        return self.gemini.model.generate_content(prompt).text 
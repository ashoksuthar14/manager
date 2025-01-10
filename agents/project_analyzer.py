from crewai import Agent
from utils.gemini_helper import GeminiHelper

class ProjectAnalyzerAgent:
    def __init__(self, gemini_helper: GeminiHelper):
        self.gemini = gemini_helper
        
    def create_agent(self) -> Agent:
        return Agent(
            role='Project Analyzer',
            goal='Analyze project requirements and create detailed documentation',
            backstory="""You are an experienced project manager and business analyst with 
            expertise in breaking down complex projects into manageable components.""",
            tools=[
                self.analyze_requirements,
                self.identify_technical_stack,
                self.estimate_timeline
            ],
            verbose=True
        )
    
    def analyze_requirements(self, project_description: str) -> str:
        """Analyze project requirements and break them down into components"""
        prompt = f"""
        Provide a detailed analysis of the project requirements including:
        1. Core functionality
        2. User requirements
        3. System requirements
        4. Integration points
        5. Potential challenges
        
        Project: {project_description}
        """
        return self.gemini.model.generate_content(prompt).text
    
    def identify_technical_stack(self, requirements: str) -> str:
        """Identify the technical stack needed for the project"""
        prompt = f"""
        Based on these requirements, recommend:
        1. Programming languages
        2. Frameworks
        3. Databases
        4. Third-party services
        5. Development tools
        
        Requirements: {requirements}
        """
        return self.gemini.model.generate_content(prompt).text
    
    def estimate_timeline(self, requirements: str) -> str:
        """Estimate project timeline and milestones"""
        prompt = f"""
        Create a high-level project timeline including:
        1. Major milestones
        2. Phase durations
        3. Dependencies
        4. Critical path activities
        5. Resource requirements
        
        Requirements: {requirements}
        """
        return self.gemini.model.generate_content(prompt).text 
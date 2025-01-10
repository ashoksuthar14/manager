from crewai import Agent
from utils.gemini_helper import GeminiHelper

class TeamManagerAgent:
    def __init__(self, gemini_helper: GeminiHelper):
        self.gemini = gemini_helper
        
    def create_agent(self) -> Agent:
        return Agent(
            role='Team Manager',
            goal='Optimize task assignments based on team skills and availability',
            backstory="""You are an experienced team manager with expertise in 
            resource allocation and team optimization.""",
            tools=[
                self.assign_tasks,
                self.balance_workload,
                self.identify_skill_gaps
            ],
            verbose=True
        )
    
    def assign_tasks(self, tasks: str, team_members: dict) -> str:
        """Assign tasks to team members based on skills and experience"""
        prompt = f"""
        Create optimal task assignments considering:
        1. Skill match
        2. Experience level
        3. Current workload
        4. Task dependencies
        5. Team collaboration
        
        Tasks: {tasks}
        Team Members: {team_members}
        """
        return self.gemini.model.generate_content(prompt).text
    
    def balance_workload(self, assignments: str, team_members: dict) -> str:
        """Balance workload across team members"""
        prompt = f"""
        Analyze and optimize workload distribution:
        1. Hours per team member
        2. Task complexity distribution
        3. Parallel work opportunities
        4. Resource utilization
        5. Schedule conflicts
        
        Assignments: {assignments}
        Team Members: {team_members}
        """
        return self.gemini.model.generate_content(prompt).text
    
    def identify_skill_gaps(self, tasks: str, team_members: dict) -> str:
        """Identify skill gaps in the team"""
        prompt = f"""
        Analyze and identify:
        1. Missing required skills
        2. Training needs
        3. External resource requirements
        4. Risk areas
        5. Improvement opportunities
        
        Tasks: {tasks}
        Team Members: {team_members}
        """
        return self.gemini.model.generate_content(prompt).text 
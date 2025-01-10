import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

class GeminiHelper:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def analyze_project(self, project_description):
        prompt = f"""
        Analyze the following project description and break it down into:
        1. Main objectives
        2. Key features
        3. Technical requirements
        4. Estimated timeline
        5. Required skills
        
        Project Description: {project_description}
        """
        response = self.model.generate_content(prompt)
        return response.text

    def create_tasks(self, project_analysis):
        prompt = f"""
        Based on this project analysis, create a detailed list of tasks with:
        1. Task name
        2. Description
        3. Required skills
        4. Estimated duration
        5. Dependencies
        
        Project Analysis: {project_analysis}
        """
        response = self.model.generate_content(prompt)
        return response.text

    def match_tasks_to_team(self, tasks: str, team_members: dict) -> str:
        """Match tasks to team members based on skills and experience"""
        prompt = f"""
        Match the following tasks to team members based on their skills and experience.
        Format your response as follows:

        ## Task Assignments

        ### [Team Member Name]
        - Task: [Task Name]
        - Reason: [Why this team member is suitable for this task]
        - Required Skills: [Skills needed]
        - Estimated Time: [Time estimate]

        ### [Next Team Member Name]
        ...

        Consider:
        1. Skill match
        2. Experience level
        3. Current workload
        4. Task dependencies
        5. Team collaboration

        Available Team Members and their details:
        {json.dumps(team_members, indent=2)}

        Tasks to be assigned:
        {tasks}
        """
        response = self.model.generate_content(prompt)
        return response.text 
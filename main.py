import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from utils.gemini_helper import GeminiHelper
import json
from agents.project_analyzer import ProjectAnalyzerAgent
from agents.task_manager import TaskManagerAgent
from agents.team_manager import TeamManagerAgent
from crewai import Crew, Task
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_team_data():
    try:
        with open('data/team_skills.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("team_skills.json not found, creating empty data")
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        # Create empty json file
        with open('data/team_skills.json', 'w') as f:
            json.dump({}, f)
        return {}
    except Exception as e:
        logger.error(f"Error loading team data: {str(e)}")
        return {}

def save_team_data(team_data):
    try:
        os.makedirs('data', exist_ok=True)
        with open('data/team_skills.json', 'w') as f:
            json.dump(team_data, f)
    except Exception as e:
        logger.error(f"Error saving team data: {str(e)}")
        st.error("Failed to save team data")

def display_team_members():
    """Display current team members and their details"""
    team_data = load_team_data()
    if team_data:
        st.sidebar.subheader("Current Team Members")
        for name, details in team_data.items():
            with st.sidebar.expander(f"🧑‍💻 {name}"):
                st.write(f"**Role:** {details.get('role', 'Team Member')}")
                st.write(f"**Experience:** {details['experience']}")
                st.write(f"**Availability:** {details.get('availability', 40)}h/week")
                st.write("**Skills:**")
                for skill in details['skills']:
                    st.write(f"- {skill}")
                if st.button("Remove Member", key=f"remove_{name}"):
                    remove_team_member(name)
                    st.rerun()

def remove_team_member(name):
    """Remove a team member from the team"""
    team_data = load_team_data()
    if name in team_data:
        del team_data[name]
        save_team_data(team_data)
        return True
    return False

def migrate_team_data():
    """Migrate existing team data to new format"""
    team_data = load_team_data()
    updated = False
    
    for name, details in team_data.items():
        # Add missing fields with default values
        if 'role' not in details:
            details['role'] = 'Team Member'
            updated = True
        if 'availability' not in details:
            details['availability'] = 40  # Default to full-time
            updated = True
    
    if updated:
        save_team_data(team_data)
    return team_data

def main():
    try:
        st.set_page_config(
            page_title="AI Project Manager",
            page_icon="🤖",
            layout="wide"
        )
        
        st.title("AI Project Manager")
        
        # Migrate existing data
        migrate_team_data()
        
        try:
            gemini = GeminiHelper()
        except Exception as e:
            st.error(f"Failed to initialize Gemini API: {str(e)}")
            logger.error(f"Gemini initialization error: {str(e)}")
            return

        # Sidebar for team management
        with st.sidebar:
            st.title("Team Management")
            
            # Add team member form
            with st.form("add_team_member"):
                st.write("Add Team Member")
                name = st.text_input("Name")
                skills = st.text_area("Skills (comma-separated)")
                experience = st.selectbox("Experience Level", ["Junior", "Mid-level", "Senior"])
                role = st.text_input("Role/Position")
                availability = st.slider("Availability (hours/week)", 0, 40, 40)
                submitted = st.form_submit_button("Add Member")
                
                if submitted and name and skills:
                    team_data = load_team_data()
                    if name in team_data:
                        st.error(f"Team member {name} already exists!")
                    else:
                        team_data[name] = {
                            "skills": [skill.strip() for skill in skills.split(",")],
                            "experience": experience,
                            "role": role,
                            "availability": availability
                        }
                        save_team_data(team_data)
                        st.success(f"Added {name} to the team!")
            
            # Display current team members
            display_team_members()

        # Main content
        tab1, tab2, tab3, tab4 = st.tabs(["Project Analysis", "Task Management", "Team Assignment", "Team Overview"])
        
        with tab1:
            st.header("Project Analysis")
            project_description = st.text_area("Enter Project Description", height=200)
            if st.button("Analyze Project"):
                if not project_description:
                    st.warning("Please enter a project description")
                    return
                    
                with st.spinner("Analyzing project..."):
                    try:
                        analysis = gemini.analyze_project(project_description)
                        st.session_state['project_analysis'] = analysis
                        st.markdown(analysis)
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")
                        logger.error(f"Project analysis error: {str(e)}")

        with tab2:
            st.header("Task Management")
            if 'project_analysis' in st.session_state:
                if st.button("Generate Tasks"):
                    with st.spinner("Generating tasks..."):
                        try:
                            tasks = gemini.create_tasks(st.session_state['project_analysis'])
                            st.session_state['tasks'] = tasks
                            st.markdown(tasks)
                        except Exception as e:
                            st.error(f"Task generation failed: {str(e)}")
                            logger.error(f"Task generation error: {str(e)}")
            else:
                st.warning("Please analyze the project first!")

        with tab3:
            st.header("Team Assignment")
            if 'tasks' in st.session_state:
                team_data = load_team_data()
                if team_data:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        if st.button("Assign Tasks"):
                            with st.spinner("Matching tasks to team members..."):
                                try:
                                    assignments = gemini.match_tasks_to_team(
                                        st.session_state['tasks'],
                                        team_data
                                    )
                                    st.session_state['assignments'] = assignments
                                    st.markdown(assignments)
                                except Exception as e:
                                    st.error(f"Task assignment failed: {str(e)}")
                                    logger.error(f"Task assignment error: {str(e)}")
                    
                    with col2:
                        if 'assignments' in st.session_state:
                            st.subheader("Team Workload")
                            for name in team_data.keys():
                                workload = team_data[name]['availability']
                                st.progress(workload/40, text=f"{name}: {workload}h/week")
                else:
                    st.warning("Please add team members first!")
            else:
                st.warning("Please generate tasks first!")
        
        with tab4:
            st.header("Team Overview")
            team_data = load_team_data()
            if team_data:
                # Display team statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Team Size", len(team_data))
                with col2:
                    total_skills = set()
                    for member in team_data.values():
                        total_skills.update(member['skills'])
                    st.metric("Total Skills", len(total_skills))
                with col3:
                    experience_levels = [member['experience'] for member in team_data.values()]
                    st.metric("Senior Members", experience_levels.count("Senior"))
                
                # Display team skills matrix
                st.subheader("Team Skills Matrix")
                all_skills = sorted(list(total_skills))
                
                # Create a DataFrame for skills
                import pandas as pd
                skills_data = []
                for name, details in team_data.items():
                    row = [name]
                    row.extend(['✓' if skill in details['skills'] else '' for skill in all_skills])
                    skills_data.append(row)
                
                df = pd.DataFrame(skills_data, columns=['Team Member'] + all_skills)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No team members added yet!")

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        logger.error(f"Main app error: {str(e)}")

if __name__ == "__main__":
    main() 
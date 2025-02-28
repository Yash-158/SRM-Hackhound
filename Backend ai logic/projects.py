import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Configure your API key
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")  # Replace with your Gemini API key

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def collect_completed_courses():
    """Collect information about courses the user has completed."""
    print("\n===== COMPLETED COURSES =====\n")
    print("Enter details about the courses you've completed.")
    
    courses = []
    while True:
        print("\nEnter course details (or type 'done' to finish):")
        
        course_name = input("Course name: ").strip()
        if course_name.lower() == 'done':
            break
        
        platform = input("Platform/Provider (e.g., Coursera, Udemy): ").strip()
        skill_level = input("Skill level (beginner/intermediate/advanced): ").strip().lower()
        
        # Validate skill level
        if skill_level not in ["beginner", "intermediate", "advanced"]:
            skill_level = "intermediate"  # Default if invalid input
        
        # Optional: topics covered
        topics = input("Main topics covered (comma-separated): ").strip()
        topics_list = [topic.strip() for topic in topics.split(',') if topic.strip()]
        
        courses.append({
            "name": course_name,
            "platform": platform,
            "skill_level": skill_level,
            "topics": topics_list
        })
        
        print(f"Added: {course_name}")
    
    return courses

def get_career_field():
    """Get the user's career field or goal."""
    print("\n===== CAREER INFORMATION =====")
    field = input("What field are you working in or aiming for? ").strip()
    experience_level = input("Your experience level (beginner/intermediate/advanced): ").strip().lower()
    
    # Validate experience level
    if experience_level not in ["beginner", "intermediate", "advanced"]:
        experience_level = "intermediate"  # Default if invalid input
    
    return field, experience_level

def generate_project_recommendations(completed_courses, field, experience_level):
    """Generate project recommendations using the Gemini API."""
    prompt = f"""
    Based on the courses a user has completed:
    {json.dumps(completed_courses, indent=2)}
    
    And their career information:
    - Field/Goal: {field}
    - Experience Level: {experience_level}
    
    Please suggest 3-5 portfolio projects that would:
    1. Build on the knowledge gained from the completed courses
    2. Be relevant to their career field ({field})
    3. Demonstrate their skills at an appropriate difficulty level ({experience_level})
    4. Create meaningful additions to their professional portfolio
    
    For each project, include:
    - A title and detailed description
    - The specific skills this project will demonstrate
    - Estimated completion time
    - Difficulty level
    - Key features or components to implement
    - Why this project would be valuable in a portfolio
    - Resources and technologies needed to complete it
    - Learning outcomes
    
    Format the output as a JSON object with the following structure:
    {{
        "recommended_projects": [
            {{
                "title": "string",
                "description": "string",
                "skills_demonstrated": ["string"],
                "estimated_time": "string",
                "difficulty": "beginner|intermediate|advanced",
                "key_features": ["string"],
                "portfolio_value": "string",
                "resources_needed": ["string"],
                "learning_outcomes": ["string"]
            }}
        ],
        "learning_progression": "string",
        "project_selection_tips": ["string"],
        "additional_resources": ["string"]
    }}
    
    Return only valid JSON with no additional text or formatting.
    """
    
    response = model.generate_content(prompt)
    
    try:
        # Try to parse the response as JSON
        recommendations = json.loads(response.text)
        return recommendations
    except json.JSONDecodeError:
        # If direct parsing fails, try to extract JSON from markdown code blocks
        import re
        json_match = re.search(r'```(?:json)?\n(.*?)\n```', response.text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Return an error message if JSON extraction fails
        return {
            "error": "Could not generate proper project recommendations. Please try again.",
            "raw_response": response.text
        }

def display_project_recommendations(recommendations):
    """Displays the project recommendations in a formatted way."""
    if "error" in recommendations:
        print("\n⚠️ Error generating project recommendations:")
        print(recommendations["error"])
        return
    
    print("\n" + "=" * 80)
    print(" " * 25 + "PROJECT RECOMMENDATIONS")
    print("=" * 80 + "\n")
    
    # Display projects
    print("🚀 RECOMMENDED PROJECTS:")
    for i, project in enumerate(recommendations["recommended_projects"], 1):
        print(f"\n{i}. {project['title']}")
        print(f"   Difficulty: {project['difficulty'].title()}")
        print(f"   Estimated Time: {project['estimated_time']}")
        print(f"   Description: {project['description']}")
        print("\n   Skills Demonstrated:")
        for j, skill in enumerate(project['skills_demonstrated'], 1):
            print(f"     {j}. {skill}")
        
        print("\n   Key Features:")
        for j, feature in enumerate(project['key_features'], 1):
            print(f"     {j}. {feature}")
        
        print(f"\n   Portfolio Value: {project['portfolio_value']}")
        
        print("\n   Resources Needed:")
        for j, resource in enumerate(project['resources_needed'], 1):
            print(f"     {j}. {resource}")
        
        print("\n   Learning Outcomes:")
        for j, outcome in enumerate(project['learning_outcomes'], 1):
            print(f"     {j}. {outcome}")
    
    print("\n" + "-" * 80 + "\n")
    
    # Display learning progression
    print("📈 LEARNING PROGRESSION:")
    print(recommendations["learning_progression"])
    
    print("\n" + "-" * 80 + "\n")
    
    # Display project selection tips
    print("💡 PROJECT SELECTION TIPS:")
    for i, tip in enumerate(recommendations["project_selection_tips"], 1):
        print(f"   {i}. {tip}")
    
    print("\n" + "-" * 80 + "\n")
    
    # Display additional resources
    if "additional_resources" in recommendations:
        print("📚 ADDITIONAL RESOURCES:")
        for i, resource in enumerate(recommendations["additional_resources"], 1):
            print(f"   {i}. {resource}")
    
    print("\n" + "=" * 80)

def save_recommendations_to_file(recommendations, filename="project_recommendations.json"):
    """Save project recommendations to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(recommendations, f, indent=2)
        print(f"\nRecommendations saved to {filename}")
    except Exception as e:
        print(f"Error saving recommendations: {str(e)}")

def main():
    """Main function to run the project recommendation system."""
    # Check if API key is configured
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        print("Please set your API key by running: export GOOGLE_API_KEY='your-api-key'")
        return
    
    try:
        print("\n====== PROJECT RECOMMENDATION SYSTEM ======")
        print("This tool suggests projects based on courses you've completed.")
        
        # Collect information about completed courses
        completed_courses = collect_completed_courses()
        
        # Check if any courses were entered
        if not completed_courses:
            print("No courses entered. Exiting...")
            return
        
        # Get career field information
        field, experience_level = get_career_field()
        
        # Generate recommendations
        print("\nGenerating project recommendations...")
        recommendations = generate_project_recommendations(completed_courses, field, experience_level)
        
        # Display recommendations
        display_project_recommendations(recommendations)
        
        # Ask if user wants to save recommendations
        save_choice = input("\nWould you like to save these recommendations to a file? (y/n): ").lower()
        if save_choice in ['y', 'yes']:
            save_recommendations_to_file(recommendations)
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted. Exiting...")
    except Exception as e:
        print(f"\n\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
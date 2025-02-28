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

def get_user_inputs():
    """Collects the 6 questions from the user through terminal input."""
    print("\n===== COURSE RECOMMENDATION SYSTEM =====\n")
    
    # Question 1: What do you want to learn?
    learning_goal = input("1. What do you want to learn? ")
    
    # Question 2: How much do you want to learn?
    while True:
        try:
            learning_level = int(input("2. How much do you want to learn? (0 for beginner, 1 for intermediate, 2 for advanced) "))
            if learning_level in [0, 1, 2]:
                break
            print("Please enter 0, 1, or 2.")
        except ValueError:
            print("Please enter a valid number (0, 1, or 2).")
    
    level_names = ["beginner", "intermediate", "advanced"]
    learning_level_name = level_names[learning_level]
    
    # Question 3: What are your expectations?
    expectations = input("3. What are your expectations from this course? ")
    
    # Question 4: Are you planning to pursue your career in the selected field?
    while True:
        career_choice = input("4. Are you planning to pursue your career in the selected field? (yes/no) ").lower()
        if career_choice in ["yes", "no", "y", "n"]:
            career_pursuit = career_choice in ["yes", "y"]
            break
        print("Please enter yes or no.")
    
    # Question 5: Current Occupation
    occupation_types = ["student", "professional", "unemployed", "business owner"]
    print("5. Current Occupation:")
    for i, occupation in enumerate(occupation_types):
        print(f"   {i} - {occupation.title()}")
    
    while True:
        try:
            occupation_index = int(input("   Enter the number that best describes your occupation: "))
            if occupation_index in range(len(occupation_types)):
                occupation = occupation_types[occupation_index]
                break
            print(f"Please enter a number between 0 and {len(occupation_types)-1}.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Question 6: How much time are you willing to complete the course in?
    while True:
        try:
            completion_time = int(input("6. How many weeks are you willing to spend to complete this course? "))
            if completion_time > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Return all collected inputs as a dictionary
    return {
        "learning_goal": learning_goal,
        "learning_level": learning_level_name,
        "expectations": expectations,
        "career_pursuit": career_pursuit,
        "occupation": occupation,
        "completion_time": completion_time
    }

def generate_course_recommendations(user_inputs):
    """Generate course recommendations using the Gemini API."""
    prompt = f"""
    Generate a personalized course recommendation plan based on the following inputs:
    
    - Learning Goal: {user_inputs['learning_goal']}
    - Desired Learning Level: {user_inputs['learning_level']}
    - User Expectations: {user_inputs['expectations']}
    - Career Pursuit in Field: {"Yes" if user_inputs['career_pursuit'] else "No"}
    - Current Occupation: {user_inputs['occupation'].title()}
    - Desired Completion Time: {user_inputs['completion_time']} weeks
    
    Please provide:
    1. A summary analysis of the user's needs based on these inputs
    2. A list of 3-5 recommended courses that match these requirements, including:
       - Course name
       - Platform or provider
       - Brief description
       - Estimated duration
       - Skill level
       - Whether it includes practical projects
       - Whether it offers certification
    3. A suggested weekly learning schedule that fits within their {user_inputs['completion_time']} week timeframe
    4. Additional resources and complementary materials
    5. Next steps after completing these courses
    
    Format the output as a JSON object with the following structure:
    {{
        "needs_analysis": "string",
        "recommended_courses": [
            {{
                "title": "string",
                "platform": "string",
                "description": "string",
                "duration_weeks": number,
                "skill_level": "string",
                "includes_projects": boolean,
                "certification": boolean,
                "key_topics": ["string"]
            }}
        ],
        "learning_schedule": {{
            "weekly_breakdown": [
                {{
                    "week": number,
                    "focus": "string",
                    "hours_required": number,
                    "goals": ["string"]
                }}
            ],
            "total_hours_weekly": number
        }},
        "additional_resources": [
            {{
                "type": "string",
                "name": "string",
                "url": "string" (optional)
            }}
        ],
        "next_steps": ["string"]
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
            "error": "Could not generate proper recommendations. Please try again.",
            "raw_response": response.text
        }

def display_recommendations(recommendations):
    """Displays the course recommendations in a formatted way."""
    if "error" in recommendations:
        print("\n⚠️ Error generating recommendations:")
        print(recommendations["error"])
        return
    
    print("\n" + "=" * 80)
    print(" " * 25 + "COURSE RECOMMENDATIONS")
    print("=" * 80 + "\n")
    
    # Display needs analysis
    print("🔍 NEEDS ANALYSIS:")
    print(recommendations["needs_analysis"])
    print("\n" + "-" * 80 + "\n")
    
    # Display recommended courses
    print("📚 RECOMMENDED COURSES:")
    for i, course in enumerate(recommendations["recommended_courses"], 1):
        print(f"\n{i}. {course['title']}")
        print(f"   Platform: {course['platform']}")
        print(f"   Level: {course['skill_level']}")
        print(f"   Duration: {course['duration_weeks']} weeks")
        print(f"   Certification: {'Yes' if course['certification'] else 'No'}")
        print(f"   Projects Included: {'Yes' if course['includes_projects'] else 'No'}")
        print(f"   Description: {course['description']}")
        print(f"   Key Topics: {', '.join(course['key_topics'])}")
    
    print("\n" + "-" * 80 + "\n")
    
    # Display learning schedule
    print("📅 LEARNING SCHEDULE:")
    print(f"   Recommended weekly time commitment: {recommendations['learning_schedule']['total_hours_weekly']} hours\n")
    
    for week in recommendations["learning_schedule"]["weekly_breakdown"]:
        print(f"   Week {week['week']}: {week['focus']}")
        print(f"   Hours: {week['hours_required']}")
        print(f"   Goals: {', '.join(week['goals'])}")
        print()
    
    print("-" * 80 + "\n")
    
    # Display additional resources
    print("🔗 ADDITIONAL RESOURCES:")
    for resource in recommendations["additional_resources"]:
        print(f"   {resource['type']}: {resource['name']}")
        if "url" in resource and resource["url"]:
            print(f"   URL: {resource['url']}")
        print()
    
    print("-" * 80 + "\n")
    
    # Display next steps
    print("👣 NEXT STEPS:")
    for i, step in enumerate(recommendations["next_steps"], 1):
        print(f"   {i}. {step}")
    
    print("\n" + "=" * 80)

def main():
    """Main function to run the recommendation system."""
    # Check if API key is configured
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        print("Please set your API key by running: export GOOGLE_API_KEY='your-api-key'")
        return
    
    try:
        # Get user inputs
        user_inputs = get_user_inputs()
        
        print("\nGenerating personalized course recommendations...")
        # Generate recommendations
        recommendations = generate_course_recommendations(user_inputs)
        
        # Display recommendations
        display_recommendations(recommendations)
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted. Exiting...")
    except Exception as e:
        print(f"\n\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
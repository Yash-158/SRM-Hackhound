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

def collect_skills():
    """Collect user's skills in a streamlined manner."""
    skills_data = {
        "technical_skills": [],
        "soft_skills": [],
        "industry_knowledge": []
    }
    
    print("\n===== SKILLS ASSESSMENT =====\n")
    
    # Streamlined input for technical skills
    print("TECHNICAL SKILLS:")
    print("Enter your technical skills one by one (e.g., Python, JavaScript, Docker)")
    print("For each skill, you can optionally add years of experience and proficiency level.")
    print("Format: skill_name [years_experience] [proficiency_level]")
    print("Example: Python 3 advanced")
    print("Type 'done' when finished with technical skills.")
    
    while True:
        skill_input = input("> ").strip()
        if skill_input.lower() == 'done':
            break
            
        parts = skill_input.split()
        skill_entry = {"skill": parts[0]}
        
        if len(parts) > 1:
            try:
                # Check if second part is a number (years of experience)
                years = float(parts[1])
                skill_entry["years_experience"] = years
                
                # If there's a third part, it's the proficiency level
                if len(parts) > 2:
                    skill_entry["proficiency_level"] = parts[2]
            except ValueError:
                # If second part is not a number, it's part of the skill name or proficiency
                if len(parts) > 1:
                    if parts[1].lower() in ["beginner", "intermediate", "advanced", "expert"]:
                        skill_entry["skill"] = parts[0]
                        skill_entry["proficiency_level"] = parts[1]
                    else:
                        skill_entry["skill"] = " ".join(parts)
        
        skills_data["technical_skills"].append(skill_entry)
        print(f"Added: {skill_entry}")
    
    # Soft skills collection
    print("\nSOFT SKILLS:")
    print("Enter your soft skills one by one (e.g., Communication, Leadership, Teamwork)")
    print("Format: skill_name [proficiency_level]")
    print("Example: Communication advanced")
    print("Type 'done' when finished with soft skills.")
    
    while True:
        skill_input = input("> ").strip()
        if skill_input.lower() == 'done':
            break
            
        parts = skill_input.split()
        skill_entry = {"skill": parts[0]}
        
        if len(parts) > 1:
            if parts[1].lower() in ["beginner", "intermediate", "advanced", "expert"]:
                skill_entry["skill"] = parts[0]
                skill_entry["proficiency_level"] = parts[1]
            else:
                skill_entry["skill"] = " ".join(parts)
        
        skills_data["soft_skills"].append(skill_entry)
        print(f"Added: {skill_entry}")
    
    # Industry knowledge collection
    print("\nINDUSTRY KNOWLEDGE:")
    print("Enter your industry knowledge areas one by one (e.g., Healthcare, Fintech, Digital Marketing)")
    print("Format: knowledge_area [years_experience] [proficiency_level]")
    print("Example: Healthcare 5 expert")
    print("Type 'done' when finished with industry knowledge.")
    
    while True:
        knowledge_input = input("> ").strip()
        if knowledge_input.lower() == 'done':
            break
            
        parts = knowledge_input.split()
        knowledge_entry = {"knowledge_area": parts[0]}
        
        if len(parts) > 1:
            try:
                # Check if second part is a number (years of experience)
                years = float(parts[1])
                knowledge_entry["years_experience"] = years
                
                # If there's a third part, it's the proficiency level
                if len(parts) > 2:
                    knowledge_entry["proficiency_level"] = parts[2]
            except ValueError:
                # If second part is not a number, it's part of the knowledge area or proficiency
                if len(parts) > 1:
                    if parts[1].lower() in ["beginner", "intermediate", "advanced", "expert"]:
                        knowledge_entry["knowledge_area"] = parts[0]
                        knowledge_entry["proficiency_level"] = parts[1]
                    else:
                        knowledge_entry["knowledge_area"] = " ".join(parts)
        
        skills_data["industry_knowledge"].append(knowledge_entry)
        print(f"Added: {knowledge_entry}")
    
    return skills_data

def quick_add_skills():
    """Alternative method to quickly add multiple skills at once."""
    skills_data = {
        "technical_skills": [],
        "soft_skills": [],
        "industry_knowledge": []
    }
    
    print("\n===== QUICK SKILLS INPUT =====")
    print("This method lets you add multiple skills at once, separated by commas.")
    
    # Technical skills
    print("\nTECHNICAL SKILLS (comma-separated):")
    tech_skills = input("> ").split(',')
    for skill in tech_skills:
        skill = skill.strip()
        if skill:
            skills_data["technical_skills"].append({"skill": skill})
    
    print(f"Added {len(skills_data['technical_skills'])} technical skills.")
    
    # Add experience years and proficiency for technical skills?
    add_details = input("\nWould you like to add experience years and proficiency for these skills? (y/n): ").lower()
    if add_details in ['y', 'yes']:
        for i, skill_entry in enumerate(skills_data["technical_skills"]):
            print(f"\nFor {skill_entry['skill']}:")
            
            # Years of experience
            years_input = input("Years of experience (press Enter to skip): ").strip()
            if years_input:
                try:
                    skills_data["technical_skills"][i]["years_experience"] = float(years_input)
                except ValueError:
                    print("Invalid input, skipping years of experience.")
            
            # Proficiency level
            prof_input = input("Proficiency level (beginner/intermediate/advanced/expert, press Enter to skip): ").strip().lower()
            if prof_input in ["beginner", "intermediate", "advanced", "expert"]:
                skills_data["technical_skills"][i]["proficiency_level"] = prof_input
    
    # Soft skills
    print("\nSOFT SKILLS (comma-separated):")
    soft_skills = input("> ").split(',')
    for skill in soft_skills:
        skill = skill.strip()
        if skill:
            skills_data["soft_skills"].append({"skill": skill})
    
    print(f"Added {len(skills_data['soft_skills'])} soft skills.")
    
    # Industry knowledge
    print("\nINDUSTRY KNOWLEDGE (comma-separated):")
    knowledge_areas = input("> ").split(',')
    for area in knowledge_areas:
        area = area.strip()
        if area:
            skills_data["industry_knowledge"].append({"knowledge_area": area})
    
    print(f"Added {len(skills_data['industry_knowledge'])} knowledge areas.")
    
    # Add experience years and proficiency for industry knowledge?
    add_details = input("\nWould you like to add experience years and proficiency for these knowledge areas? (y/n): ").lower()
    if add_details in ['y', 'yes']:
        for i, knowledge_entry in enumerate(skills_data["industry_knowledge"]):
            print(f"\nFor {knowledge_entry['knowledge_area']}:")
            
            # Years of experience
            years_input = input("Years of experience (press Enter to skip): ").strip()
            if years_input:
                try:
                    skills_data["industry_knowledge"][i]["years_experience"] = float(years_input)
                except ValueError:
                    print("Invalid input, skipping years of experience.")
            
            # Proficiency level
            prof_input = input("Proficiency level (beginner/intermediate/advanced/expert, press Enter to skip): ").strip().lower()
            if prof_input in ["beginner", "intermediate", "advanced", "expert"]:
                skills_data["industry_knowledge"][i]["proficiency_level"] = prof_input
    
    return skills_data

def get_course_field():
    """Get the field to explore from the user."""
    print("\n===== CAREER GOAL =====")
    field = input("What field would you like to explore or advance in? ")
    return field

def generate_course_recommendations(skills_data, target_field):
    """Generate course recommendations using the Gemini API."""
    prompt = f"""
    Based on the following skills profile:
    {json.dumps(skills_data, indent=2)}
    
    And the user's target field: {target_field}
    
    Please provide a personalized learning path with specific courses that will help the user advance in their career goal.
    
    Include in your response:
    1. Assessment of current skills relative to the field
    2. Identification of skill gaps
    3. A sequential course path with:
       - Beginner courses (if needed)
       - Intermediate courses
       - Advanced/specialized courses
    4. Estimated timeline
    5. Recommended learning platforms
    
    Format the output as a JSON object with the following structure:
    {{
        "assessment": "string",
        "skill_gaps": ["string"],
        "learning_path": [
            {{
                "level": "beginner|intermediate|advanced",
                "courses": [
                    {{
                        "title": "string",
                        "platform": "string",
                        "description": "string",
                        "estimated_duration": "string",
                        "key_topics": ["string"]
                    }}
                ]
            }}
        ],
        "estimated_timeline": "string",
        "recommended_platforms": ["string"],
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
    
    # Display skills assessment
    print("🔍 SKILLS ASSESSMENT:")
    print(recommendations["assessment"])
    print("\n" + "-" * 80 + "\n")
    
    # Display skill gaps
    print("🔍 IDENTIFIED SKILL GAPS:")
    for i, gap in enumerate(recommendations["skill_gaps"], 1):
        print(f"   {i}. {gap}")
    print("\n" + "-" * 80 + "\n")
    
    # Display learning path
    print("📚 RECOMMENDED LEARNING PATH:")
    for level_group in recommendations["learning_path"]:
        print(f"\n[{level_group['level'].upper()} LEVEL COURSES]")
        for i, course in enumerate(level_group["courses"], 1):
            print(f"\n{i}. {course['title']}")
            print(f"   Platform: {course['platform']}")
            print(f"   Duration: {course['estimated_duration']}")
            print(f"   Description: {course['description']}")
            print(f"   Key Topics: {', '.join(course['key_topics'])}")
    
    print("\n" + "-" * 80 + "\n")
    
    # Display estimated timeline
    print("⏱️ ESTIMATED TIMELINE:")
    print(recommendations["estimated_timeline"])
    
    print("\n" + "-" * 80 + "\n")
    
    # Display recommended platforms
    print("🔗 RECOMMENDED LEARNING PLATFORMS:")
    for platform in recommendations["recommended_platforms"]:
        print(f"   • {platform}")
    
    print("\n" + "-" * 80 + "\n")
    
    # Display next steps
    print("👣 NEXT STEPS:")
    for i, step in enumerate(recommendations["next_steps"], 1):
        print(f"   {i}. {step}")
    
    print("\n" + "=" * 80)

def main():
    """Main function to run the skills-based course recommendation system."""
    # Check if API key is configured
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        print("Please set your API key by running: export GOOGLE_API_KEY='your-api-key'")
        return
    
    try:
        print("\n====== SKILLS-BASED COURSE RECOMMENDER ======\n")
        print("This tool will help you find courses based on your current skills and career goals.")
        
        # Ask user which input method they prefer
        print("\nHow would you like to enter your skills?")
        print("1. Detailed input (one by one)")
        print("2. Quick input (comma-separated lists)")
        
        choice = input("Enter your choice (1 or 2): ")
        
        if choice == "1":
            skills_data = collect_skills()
        else:
            skills_data = quick_add_skills()
        
        # Show summary of entered skills
        print("\nSKILLS SUMMARY:")
        print(f"Technical Skills: {len(skills_data['technical_skills'])}")
        print(f"Soft Skills: {len(skills_data['soft_skills'])}")
        print(f"Industry Knowledge: {len(skills_data['industry_knowledge'])}")
        
        # Get the target field
        target_field = get_course_field()
        
        print("\nGenerating personalized course recommendations...")
        # Generate recommendations
        recommendations = generate_course_recommendations(skills_data, target_field)
        
        # Display recommendations
        display_recommendations(recommendations)
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted. Exiting...")
    except Exception as e:
        print(f"\n\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
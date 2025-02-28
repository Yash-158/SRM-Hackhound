import google.generativeai as genai
import requests
import json
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure your API keys and credentials
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_REDIRECT_URI = "http://127.0.0.1:8000/social-auth/complete/linkedin-oauth2/"  # Should match your LinkedIn app configuration

# Check for required credentials
missing_credentials = []
if not GOOGLE_API_KEY:
    missing_credentials.append("GOOGLE_API_KEY")
if not LINKEDIN_CLIENT_ID:
    missing_credentials.append("LINKEDIN_CLIENT_ID")
if not LINKEDIN_CLIENT_SECRET:
    missing_credentials.append("LINKEDIN_CLIENT_SECRET")

if missing_credentials:
    print(f"Error: Missing required environment variables: {', '.join(missing_credentials)}")
    print("Please create a .env file with these variables or set them in your environment.")
    print("Example .env file:")
    print('GOOGLE_API_KEY="your_gemini_api_key"')
    print('LINKEDIN_CLIENT_ID="your_linkedin_client_id"')
    print('LINKEDIN_CLIENT_SECRET="your_linkedin_client_secret"')
    sys.exit(1)

# Configure Gemini
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    sys.exit(1)

def get_linkedin_auth_url():
    """Generates the LinkedIn authorization URL."""
    auth_url = "https://www.linkedin.com/oauth/v2/authorization"
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "state": "random_string",
        "scope": "r_liteprofile r_emailaddress"  # Updated scope to use available permissions
    }
    return f"{auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

def get_linkedin_access_token(auth_code):
    """Gets an access token from LinkedIn using authorization code."""
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    token_params = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
    }
    
    try:
        token_response = requests.post(token_url, data=token_params)
        token_response.raise_for_status()
        return token_response.json().get("access_token")
    except requests.exceptions.HTTPError as e:
        print(f"LinkedIn API Error: {e}")
        print(f"Response: {token_response.text}")
        return None

def get_linkedin_profile_data(access_token):
    """Fetches LinkedIn profile data from the API."""
    profile_url_api = "https://api.linkedin.com/v2/me"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    try:
        profile_response = requests.get(profile_url_api, headers=headers)
        profile_response.raise_for_status()
        profile_data = profile_response.json()
        
        # Get skills (This would require a different API endpoint and permissions)
        # For simplicity, we'll use manual input for skills in this example
        
        return profile_data
    except requests.exceptions.HTTPError as e:
        print(f"LinkedIn API Error: {e}")
        print(f"Response: {profile_response.text if 'profile_response' in locals() else 'No response'}")
        return None

def manually_collect_profile_data():
    """Collects profile data manually from user input."""
    print("\n--- Please enter your profile information manually ---")
    profile_data = {
        "skills": [],
        "experience": []
    }
    
    # Collect skills
    print("\nEnter your skills (one per line, blank line to finish):")
    while True:
        skill = input("> ")
        if not skill:
            break
        profile_data["skills"].append(skill)
    
    # Collect experience
    print("\nEnter your work experience (format: Company | Title | Years):")
    print("Example: 'Google | Software Engineer | 2.5'")
    print("Enter a blank line to finish")
    
    while True:
        exp = input("> ")
        if not exp:
            break
        try:
            company, title, years = exp.split("|")
            profile_data["experience"].append({
                "company": company.strip(),
                "title": title.strip(),
                "years": years.strip()
            })
        except ValueError:
            print("Invalid format. Please use 'Company | Title | Years'")
    
    return profile_data

def extract_skills_and_experience(profile_data):
    """Extracts skills, experience, and other relevant information."""
    try:
        prompt = f"""Extract technical skills, soft skills, industry knowledge, and years of experience from the following profile data:
        Skills: {profile_data.get('skills', [])}
        Experience: {profile_data.get('experience', [])}

        Output the data in JSON format, including:
        1. Technical skills
        2. Soft skills
        3. Industry knowledge
        4. Years of experience in each skill (if mentioned)
        5. Proficiency level (if indicated)
        """

        response = model.generate_content(prompt)
        try:
            # Try to parse as JSON, but handle text response as well
            if hasattr(response, 'text'):
                # Find JSON in the response if it's not a pure JSON response
                text = response.text
                json_start = text.find('{')
                json_end = text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = text[json_start:json_end]
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        pass
                
                # If we can't parse JSON, return the text response
                return {"extracted_text": text}
            else:
                # Handle the response object structure
                parts = response.candidates[0].content.parts
                text = ''.join(part.text for part in parts)
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return {"extracted_text": text}
        except (json.JSONDecodeError, AttributeError, IndexError) as e:
            print(f"Error processing Gemini response: {e}")
            if hasattr(response, 'text'):
                return {"extracted_text": response.text}
            return {"error": "Could not extract data"}
    except Exception as e:
        print(f"Error generating content: {e}")
        return {"error": f"Could not extract data: {str(e)}"}

def generate_job_suggestions(extracted_data, target_industry):
    """Generates job suggestions based on extracted data and target industry."""
    prompt = f"""Based on the following profile data:
    {json.dumps(extracted_data, indent=4)}

    And the user's target industry: {target_industry}

    Recommend 3 to 5 suitable job titles and roles, considering the user's skills and experience.
    Provide a brief description of each role and why it's a good fit.
    """
    try:
        response = model.generate_content(prompt)
        if hasattr(response, 'text'):
            return response.text
        else:
            parts = response.candidates[0].content.parts
            return ''.join(part.text for part in parts)
    except Exception as e:
        print(f"Error generating job suggestions: {e}")
        return "Error generating job suggestions. Please try again."

def generate_learning_path(extracted_data, job_choice):
    """Generates a learning path for a chosen career path."""
    prompt = f"""Based on the following profile data:
    {json.dumps(extracted_data, indent=4)}

    And the user's chosen career path: {job_choice}

    Recommend a detailed learning path, including specific skills to acquire, courses, platforms, projects, and networking strategies.
    Explain how this path will help the user achieve their career goal.
    """
    try:
        response = model.generate_content(prompt)
        if hasattr(response, 'text'):
            return response.text
        else:
            parts = response.candidates[0].content.parts
            return ''.join(part.text for part in parts)
    except Exception as e:
        print(f"Error generating learning path: {e}")
        return "Error generating learning path. Please try again."

if __name__ == "__main__":
    print("===== LinkedIn Career Path Advisor =====")
    
    # Ask if user wants to use LinkedIn API or manual input
    use_api = input("Do you want to use LinkedIn API for authentication? (y/n): ").lower() == 'y'
    
    profile_data = None
    
    if use_api:
        # Generate auth URL
        auth_url = get_linkedin_auth_url()
        print(f"\nPlease visit this URL in your browser to authorize the app:")
        print(auth_url)
        print("\nAfter authorization, you'll be redirected to a URL. Copy the entire URL and paste it here.")
        redirect_url = input("Paste the redirect URL here: ")
        
        # Extract authorization code from redirect URL
        try:
            code_param = "code="
            if code_param in redirect_url:
                auth_code = redirect_url.split(code_param)[1].split("&")[0]
                print("Authorization code extracted successfully.")
                
                # Get access token
                access_token = get_linkedin_access_token(auth_code)
                if access_token:
                    print("Successfully obtained access token.")
                    profile_data = get_linkedin_profile_data(access_token)
                else:
                    print("Failed to obtain access token. Switching to manual input.")
                    profile_data = manually_collect_profile_data()
            else:
                print("Authorization code not found in redirect URL. Switching to manual input.")
                profile_data = manually_collect_profile_data()
        except Exception as e:
            print(f"Error processing authentication: {e}")
            print("Switching to manual input.")
            profile_data = manually_collect_profile_data()
    else:
        profile_data = manually_collect_profile_data()
    
    if profile_data:
        print("\nExtracting skills and experience...")
        extracted_data = extract_skills_and_experience(profile_data)
        
        if "error" not in extracted_data:
            print("\nExtracted Data:")
            print(json.dumps(extracted_data, indent=4))
            
            target_industry = input("\nEnter your target industry: ")
            print("\nGenerating job suggestions...")
            job_suggestions = generate_job_suggestions(extracted_data, target_industry)
            
            print("\n===== Job Suggestions =====")
            print(job_suggestions)
            
            job_choice = input("\nEnter the job title you want to pursue: ")
            print("\nGenerating learning path...")
            learning_path = generate_learning_path(extracted_data, job_choice)
            
            print("\n===== Learning Path =====")
            print(learning_path)
            
            print("\nThank you for using LinkedIn Career Path Advisor!")
        else:
            print("Error during data extraction.")
    else:
        print("Failed to collect profile data. Exiting.")
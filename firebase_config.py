import requests
import json

# Firebase Realtime Database URL (from your project)
FIREBASE_DB_URL = "https://chatter-insights-tdrbu-default-rtdb.firebaseio.com"

def get_gemini_api_key():
    """
    Fetches the Gemini API key directly from Firebase Realtime Database
    """
    try:
        # Construct the URL to fetch the API key
        url = f"{FIREBASE_DB_URL}/GeminiGEMINI_API_KEY.json"
        
        # Make the request to Firebase
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the response
        api_key = response.text.strip('"')  # Remove quotes from the response
        
        if not api_key or api_key == 'null':
            print("Error: API key not found in the database")
            return None
            
        print("Successfully retrieved API key from Firebase")
        return api_key
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API key from Firebase: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# For testing
if __name__ == "__main__":
    print("Testing Firebase connection...")
    api_key = get_gemini_api_key()
    if api_key:
        print("Success! API key retrieved:", api_key[:5] + "..." + api_key[-5:] if len(api_key) > 10 else api_key)
    else:
        print("Failed to retrieve API key")

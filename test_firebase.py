import os
import sys
import logging
from firebase_config import get_gemini_api_key

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def test_firebase_connection():
    print("\n=== Testing Firebase Connection ===")
    print("1. Checking environment...")
    
    # Check if service account key is set
    service_account_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    print(f"Service account path: {service_account_path}")
    
    if service_account_path:
        print(f"Service account exists: {os.path.exists(service_account_path)}")
    else:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
    
    print("\n2. Attempting to get API key...")
    api_key = get_gemini_api_key()
    
    if api_key:
        print("\n✅ Success! Retrieved API key:")
        print(f"Key: {api_key[:5]}...{api_key[-5:] if api_key and len(api_key) > 10 else ''}")
    else:
        print("\n❌ Failed to retrieve API key. Check the logs above for details.")
        print("\nTroubleshooting steps:")
        print("1. Make sure GOOGLE_APPLICATION_CREDENTIALS is set to your service account JSON file")
        print("2. Verify the service account has read access to your Firebase Realtime Database")
        print("3. Check if the 'GeminiGEMINI_API_KEY' exists in your database")
        print("4. Ensure your internet connection is working")
        print("\nTo set the service account, run this command in your terminal:")
        print(f'set GOOGLE_APPLICATION_CREDENTIALS="C:\\path\\to\\your\\service-account-key.json"')

if __name__ == "__main__":
    test_firebase_connection()

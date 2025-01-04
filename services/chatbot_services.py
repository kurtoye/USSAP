from openai import OpenAI
from google.cloud import firestore
from google.oauth2 import service_account
import os

# Load credentials
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if not credentials_path:
    raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS not set in environment variables")

credentials = service_account.Credentials.from_service_account_file(credentials_path)
db = firestore.Client(credentials=credentials)

# Set OpenAI API Key
def get_chatbot_response(user_message: str) -> str:
    try:
        client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))  # Create a new client instance
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Chatbot Error: {e}")
        return "An error occurred while generating the chatbot response."

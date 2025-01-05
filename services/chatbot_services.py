import openai
import os
from config.firestore_client import db

# Set OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Chatbot Response Function
def get_chatbot_response(user_message: str) -> str:
    try:
        # Log API key for debugging (Ensure it's masked if sensitive)
        print("OpenAI API Key Loaded Successfully.")

        # Make API call to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )

        print("Full Response:", response)

        # Validate and extract content
        if response and "choices" in response and response["choices"]:
            message = response["choices"][0].get("message", {})
            content = message.get("content", "").strip()
            if content:
                return content
            
        print("Unexpected response structure:", response)
        return "Chatbot could not process your request at this time."

    except Exception as e:
        print(f"Chatbot Error: {e}")
        return f"Chatbot Error: {str(e)}"



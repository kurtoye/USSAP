import openai
import os

# Explicitly set API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Print the key for verification (Ensure it's NOT None)
print("API Key:", openai.api_key)

# Make a basic API call
try:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": "Hello, chatbot!"}
        ],
        max_tokens=150,
        temperature=0.7
    )
    print(response)
    print(response.choices[0].message.content.strip())
except Exception as e:
    print("API Call Error:", e)

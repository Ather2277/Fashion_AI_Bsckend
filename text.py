import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def generate_output(model_name, user_input):
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=model_name)

    try:
        t = {"parts": [{"text": user_input}]}
        response = model.generate_content(t)
        generated_text = response.text.strip()
        return generated_text
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    model_name = "tunedModels/outfitsuggestiongenerator-usqw4b296kfe"
    user_input = input("Enter your outfit suggestion prompt: ")
    result = generate_output(model_name, user_input)
    print(f"Generated output: {result}")

if __name__ == "__main__":
    main()

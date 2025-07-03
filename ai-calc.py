#! /usr/bin/python3

import os
import google.generativeai as genai

# Set your Gemini API key
GEMINI_API_KEY = "<Gemin API key here>" #os.getenv("GEMINI_API_KEY")  # Or replace with a string for quick testing

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Configure the Gemini client
genai.configure(api_key=GEMINI_API_KEY)

# Create a model instance
model = genai.GenerativeModel("gemini-2.5-flash")

def calculate_natural_language(prompt):
    try:
        response = model.generate_content(f"Evaluate this as a math problem and give only the numeric result: {prompt}")
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    while True:
        user_input = input("Enter a math instruction (or 'exit'): ").strip()
        if user_input.lower() in ['exit', 'quit']:
            break
        result = calculate_natural_language(user_input)
        print(f"Result: {result}")

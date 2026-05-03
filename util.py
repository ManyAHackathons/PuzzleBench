from google import genai
from google.genai import types


client = genai.Client()

# Bomb defuser tools

# technition tools

# https://ai.google.dev/gemini-api/docs/function-calling?example=meeting#automatic_function_calling_python_only


def call_llm(messages, tools, system_prompt):

    
    contents = [
        types.Content
    ]
    
    response = client.models.generate_content(
        model="",
        contents=contents
        
    )
    
    return response.choices[0].message.content
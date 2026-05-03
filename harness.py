from litellm import completion




# bomb defuser harness
from google import genai
from google.genai import types
from bomb.bomb import Bomb
client = genai.Client(api_key="")

def take_turn(messages, tools):
    config = types.GenerateContentConfig(
        tools=tools
    )  # Pass the function itself
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=messages,
        config=config,
    )
    
    return response.text
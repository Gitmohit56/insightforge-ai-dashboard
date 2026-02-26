import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Restart VS Code.")

client = genai.Client(api_key=api_key)

def generate_insights(summary):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        You are a senior data analyst.
        Analyze the following dataset summary and provide:
        - Key insights
        - Patterns
        - Business recommendations

        Dataset summary:
        {summary}
        """
    )
    return response.text
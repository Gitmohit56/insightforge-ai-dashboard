import os
import google.generativeai as genai

api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in Streamlit Secrets.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_insights(summary):
    response = model.generate_content(
        f"""
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

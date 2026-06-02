import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def fact_check(statistics):

    prompt = f"""
You are a fact-checking analyst.

Review these extracted statistics.

Tasks:

1. Remove duplicate statistics.
2. Identify conflicting numbers.
3. Highlight the most reliable figures.
4. Assign a confidence level:
   - High
   - Medium
   - Low

Return format:

# ✅ Validation Report

Confidence: [Level]

## Verified Statistics
- ...

## Potential Conflicts
- ...

Statistics:

{statistics}
"""

    response = model.generate_content(prompt)

    if response.text:
        return response.text

    return "Validation unavailable."
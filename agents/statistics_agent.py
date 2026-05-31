import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def extract_statistics(content):

    prompt = f"""
Extract EXACTLY 5 business-critical statistics.

Rules:
- Return EXACTLY 5 statistics.
- No introduction.
- No conclusion.
- No regional breakdowns.
- No duplicate numbers.
- Prefer:
  1. Market size
  2. CAGR/Growth rate
  3. Future forecast
  4. Adoption rate
  5. Business impact metric

Format:

# 📊 Key Statistics

- Statistic 1
- Statistic 2
- Statistic 3
- Statistic 4
- Statistic 5

Content:

{content}
"""

    response = model.generate_content(prompt)

    if response.text:
        return response.text

    return "No significant statistics found."
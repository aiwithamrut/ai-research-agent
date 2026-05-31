import google.generativeai as genai
from agents.statistics_agent import extract_statistics
from tools.search_tool import web_search
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def research_agent(query):

    results = web_search(query)

    content = "\n".join(
        [r["content"] for r in results[:5]]
    )

    sources = [
        r["url"]
        for r in results[:5]
        if "url" in r
    ]
    statistics = extract_statistics(content)
    prompt = f"""
You are a Senior Research Analyst at a top consulting firm.

Research Topic:
{query}

Source Information:
{content}

Extracted Statistics:
{statistics}

Create a PROFESSIONAL research report.

Rules:

- Use clear markdown formatting.
- Use short paragraphs.
- Use bullet points.
- Be concise but insightful.
- Avoid repetition.
- Focus on actionable insights.
- Write like a consultant, not a chatbot.

Structure:

# 📋 Executive Summary
(100-150 words)

# 🔍 Key Findings
(5-8 bullet points)

# 📈 Major Trends
(3-5 important trends)

# ⚠️ Risks & Challenges
(3-5 risks)

# 💡 Strategic Opportunities
(3-5 opportunities)

# 🎯 Conclusion
(Short conclusion)

Important:
Make the report visually clean and easy to scan.
"""

    response = model.generate_content(prompt)

    return {
    "report": response.text,
    "statistics": statistics,
    "sources": sources
     }
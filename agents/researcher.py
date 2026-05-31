from openai import OpenAI
from tools.search_tool import web_search
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def research_agent(query):

    results = web_search(query)

    content = "\n".join(
        [r["content"] for r in results[:5]]
    )

    prompt = f"""
    Research this topic:

    {query}

    Here is information from web:

    {content}

    Give a clean summary with key points.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
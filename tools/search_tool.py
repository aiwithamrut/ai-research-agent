from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def web_search(query):

    response = client.search(
        query=query,
        search_depth="advanced"
    )

    return response["results"]
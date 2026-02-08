from fastmcp import FastMCP
from typing import Annotated
from tavily import TavilyClient
import os

mcp = FastMCP("Online web search")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


@mcp.tool(description='Scrap provided web page')
def get_predicted_weather(
    url: Annotated[str, "URL to the page we want to scrap"],
) -> str:

    return tavily.get_search_context(query=url, search_depth="basic", max_tokens=1000)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8002)

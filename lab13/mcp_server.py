import datetime
from fastmcp import FastMCP

mcp = FastMCP("Weather forecast")


@mcp.tool(description='Get current date in the format "Year-Month-Day" (YYYY-MM-DD).')
def get_current_date() -> str:
    return datetime.date.today().isoformat()


@mcp.tool(description='Get current datetime in the format "Year-Month-Day-Hour-Minute-Second" (YYYY-MM-DD-HH:MM:SS).')
def get_current_datetime() -> str:
    return datetime.datetime.today().isoformat(timespec='seconds')


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8002)

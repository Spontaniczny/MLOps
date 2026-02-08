import requests
from fastmcp import FastMCP
from typing import Annotated
from geopy.geocoders import Nominatim
import os

mcp = FastMCP("Weather forecast")

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")


@mcp.tool(description='Get predicted weather in the specified location')
def get_predicted_weather(
    city_name: Annotated[str, "Name of a city that you want to predict weather in"],
    cnt: Annotated[int, "A number of days, which will be returned in the API response"],
) -> list[dict]:

    location = Nominatim(user_agent="mcp-weather-app").geocode(city_name)
    if not location:
        raise Exception("Unknown City")

    lat = location.latitude
    lon = location.longitude

    url = f"api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={cnt}&appid={OPEN_WEATHER_API_KEY}"
    response = requests.get(url)
    ret = []
    for elem in response.json()["list"]:
        ret.append({
            "temperature": elem["temp"]["day"],
            "weather": elem["weather"]
        })

    return ret


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8002)

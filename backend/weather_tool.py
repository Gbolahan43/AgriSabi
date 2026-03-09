import os
import requests

def get_weather_data(location: str) -> dict:
    """
    Fetch weather data from OpenWeatherMap API for a given location.
    Requires OPENWEATHERMAP_API_KEY environment variable.
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        return {"error": "Weather data unavailable. API key not configured."}
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"]
        }
    except Exception as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}

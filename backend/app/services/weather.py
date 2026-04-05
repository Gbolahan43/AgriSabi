import os
import requests

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_current_weather(location_name: str) -> str:
    """
    Native Tool for Advisory Agent: Fetches weather for a given Nigerian location.
    """
    if not OPENWEATHER_API_KEY:
        return "Weather data is currently unavailable. No API key configured."
        
    try:
        # 1. Geocode the location
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location_name},NG&limit=1&appid={OPENWEATHER_API_KEY}"
        geo_resp = requests.get(geo_url)
        geo_data = geo_resp.json()
        
        if not geo_data:
            return f"Could not find coordinates for {location_name} in Nigeria."
            
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        
        # 2. Get Weather via OneCall or simple Current Weather
        # Using Current Weather API for simplicity
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        weather_resp = requests.get(weather_url)
        w_data = weather_resp.json()
        
        temp = w_data.get("main", {}).get("temp", "Unknown")
        desc = w_data.get("weather", [{}])[0].get("description", "Unknown")
        humidity = w_data.get("main", {}).get("humidity", "Unknown")
        
        return f"Current weather in {location_name}: {temp}°C, {desc}. Humidity: {humidity}%."
        
    except Exception as e:
        print(f"Weather Tool Error: {e}")
        return "Failed to fetch weather data due to a network error."

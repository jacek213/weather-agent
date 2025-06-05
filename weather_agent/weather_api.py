import os
import requests

class WeatherAPI:
    def __init__(self, api_key, city):
        self.api_key = api_key
        self.city = city

    def get_weather(self, api_url):
        api_url = api_url.replace("{WEATHER_API_KEY}", self.api_key)
        api_url = api_url.replace("{city}", self.city)
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API error: {response.status_code} - {response.text}")
            return None

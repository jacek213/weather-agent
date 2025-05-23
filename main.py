import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")
CITY = os.getenv("CITY")


def get_weather(api_key, city):
    print(f"Fetching weather data for {city}.... API key: {api_key}")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        print(f"Weather in {city}: {weather}, {temp}°C")
    else:
        print("Failed to fetch weather data. Check your API key and city name.")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")


def main():
    get_weather(API_KEY, CITY)


if __name__ == "__main__":
    main()

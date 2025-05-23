import requests

API_KEY = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
CITY = "Warsaw"


def get_weather(api_key, city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        print(f"Weather in {city}: {weather}, {temp}°C")
    else:
        print("Failed to fetch weather data. Check your API key and city name.")


def main():
    get_weather(API_KEY, CITY)


if __name__ == "__main__":
    main()

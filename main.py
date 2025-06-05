import os
from dotenv import load_dotenv
from weather_agent.agent import WeatherAgent

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CITY = os.getenv("CITY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def main():
    agent = WeatherAgent(WEATHER_API_KEY, CITY, GEMINI_API_KEY)
    agent.run()

if __name__ == "__main__":
    main()

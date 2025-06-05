import os
from .speech import SpeechRecognizer
from .weather_api import WeatherAPI
from .gemini import GeminiClient

class WeatherAgent:
    def __init__(self, weather_api_key, city, gemini_api_key):
        self.speech = SpeechRecognizer()
        self.weather_api = WeatherAPI(weather_api_key, city)
        self.gemini = GeminiClient(gemini_api_key)
        self.city = city

    def run(self):
        question = self.speech.recognize()
        if question:
            print(f"Your question: {question}")
            endpoint_json = self.gemini.ask_for_endpoint(question, self.city)
            print(f"Endpoint response: {endpoint_json}")
            weather_json = self.weather_api.get_weather(endpoint_json["api_url"])
            if weather_json:
                answer = self.gemini.ask_for_answer(question, weather_json, endpoint_json["instructions"])
                print(f"Answer: {answer}")
                os.system(f'say -v Zosia "{answer}"')

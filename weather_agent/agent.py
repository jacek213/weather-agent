import os
import json
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
            endpoint_response = self.gemini.ask_for_endpoint(question, self.city)
            print(f"Endpoint response: {endpoint_response}")
            cleaned_response = endpoint_response.strip()
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response.split('\n', 1)[-1]
                if cleaned_response.endswith('```'):
                    cleaned_response = cleaned_response.rsplit('```', 1)[0]
                cleaned_response = cleaned_response.strip()
            try:
                endpoint_json = json.loads(cleaned_response)
            except Exception as e:
                print(f"Could not parse endpoint_response as JSON: {e}\nGemini response: {endpoint_response}")
                return
            api_url = endpoint_json.get("api_url")
            instructions = endpoint_json.get("instructions")
            print(f"API URL: {api_url}")
            print(f"Instructions: {instructions}")
            weather_json = self.weather_api.get_weather(api_url)
            if weather_json:
                answer = self.gemini.ask_for_answer(question, weather_json, instructions)
                print(f"Answer: {answer}")
                os.system(f'say -v Zosia "{answer}"')

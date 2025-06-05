from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def ask_for_endpoint(self, question, city):
        # ...system_prompt as in main.py...
        system_prompt = (
            "You are a openweathermap api expert. The user asked the following question: '"
            f"{question}'. Here is the city: {city}.\n"
            "Your goal is to provide an API URL that can be used to answer the user's question plus instructions on how to extract the relevant data from the API response. "
            "Please provide a JSON object having the following structure:\n"
            "{\n"
            "  \"api_url\": \"<API_URL>\",\n"
            "  \"instructions\": \"<INSTRUCTIONS>\"\n"
            "}\n"
            "Closely follow the API documentation. General indication on which endpoint should be used: https://openweathermap.org/guide."
            "Eg for current weather, use endpoint described at https://openweathermap.org/current. \n"
            "For past weather you can use history: https://openweathermap.org/history   \n"
            "For forecast - the most applicable of https://openweathermap.org/api/hourly-forecast, https://openweathermap.org/forecast5, https://openweathermap.org/forecast16 or https://openweathermap.org/api/forecast30"
            "Just return a JSON object with the api_url and instructions. Do not include any other text or explanation, so it can be easily parsed by the Python agent.\n Do not wrap the code into a fenced code block. Dont add newlines. Example response: \n"
            "{\"api_url\": \"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric\", \"instructions\": \"Check the 'weather' array and 'main'/'description' for current weather.\"}\n"
            "If the answer cannot be determined, return an error message in the JSON object and give nulls to api_url and instructions\n"
            "If the question requires knowledge on topics different than weather, you're now an expert in that topic (e.g. fishing) and try to provide the best instructions to extract data relevant to that question. \n"
        )
        contents = types.Content(
            role='user',
            parts=[types.Part.from_text(text=system_prompt)]
        )
        response = self.client.models.generate_content(
            model='models/gemini-2.0-flash-001',
            contents=[contents]
        )
        return response.text

    def ask_for_answer(self, question, weather_json, instructions):
        prompt = (
            "You are a weather assistant and a openweathermap api expert, also a fishing expert consultant. The user asked the following question: '"
            f"{question}'. Here is the JSON response from the weather API: {weather_json}\n"
            f"Based on the instructions provided: {instructions} extract the relevant data from the API response and provide a human-friendly answer. "
            "If the answer cannot be determined, say so."
            "The answer should be in the same lanuage as the question. Should not include technical details, api response, we need to hide that from the end user. Just a concise answer, keep it short, dont say full date and stuff. Respond like a friendly AI assistant but not a robot. "
        )
        contents = types.Content(
            role='user',
            parts=[types.Part.from_text(text=prompt)],
        )
        response = self.client.models.generate_content(
            model='models/gemini-2.0-flash-001',
            contents=[contents]
        )
        return response.text

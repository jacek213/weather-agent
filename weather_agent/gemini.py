from google import genai
from google.genai import types
import json

SYSTEM_PROMPT_ENDPOINT = '''
You are a openweathermap api expert. The user asked the following question: '{question}'. Here is the city: '{city}'.
Your goal is to provide an API URL that can be used to answer the user's question plus instructions on how to extract the relevant data from the API response.
Please provide a JSON object having the following structure:
{{
  "api_url": "<API_URL>",
  "instructions": "<INSTRUCTIONS>"
}}
Closely follow the API documentation. General indication on which endpoint should be used: https://openweathermap.org/guide.
Eg for current weather, use endpoint described at https://openweathermap.org/current.
For past weather you can use history: https://openweathermap.org/history
For forecast - the most applicable of https://openweathermap.org/api/hourly-forecast, https://openweathermap.org/forecast5, https://openweathermap.org/forecast16 or https://openweathermap.org/api/forecast30
Just return a JSON object with the api_url and instructions. Do not include any other text or explanation, so it can be easily parsed by the Python agent. Do not wrap the code into a fenced code block. Dont add newlines. Example response:
{{"api_url": "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={{WEATHER_API_KEY}}&units=metric", "instructions": "Check the 'weather' array and 'main'/'description' for current weather."}}
If the answer cannot be determined, return an error message in the JSON object and give nulls to api_url and instructions
If the question requires knowledge on topics going beyond weather but somehow related to it, you're now an expert in that topic (e.g. fishing) and try to provide the best instructions to extract data relevant to that question.
'''

SYSTEM_PROMPT_ANSWER = '''
You are a weather assistant and a openweathermap api expert, also a fishing expert consultant. The user asked the following question: '{question}'. Here is the JSON response from the weather API: {weather_json}
Based on the instructions provided: <{instructions}> extract the relevant data from the API response and provide a human-friendly answer.
If the answer cannot be determined, say so.
The answer should be in the same language as the question. Should not include technical details, api response, we need to hide that from the end user. Just a concise answer, keep it short, dont say full date and stuff. Respond like a friendly AI assistant but not a robot.
'''

class GeminiClient:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def ask_for_endpoint(self, question, city):
        system_prompt = SYSTEM_PROMPT_ENDPOINT.format(question=question, city=city)
        contents = types.Content(
            role='user',
            parts=[types.Part.from_text(text=system_prompt)]
        )
        response = self.client.models.generate_content(
            model='models/gemini-2.0-flash-001',
            contents=[contents]
        )
        return self._prepare_endpoint_json(response.text)

    def ask_for_answer(self, question, weather_json, instructions):
        prompt = SYSTEM_PROMPT_ANSWER.format(question=question, weather_json=weather_json, instructions=instructions)
        contents = types.Content(
            role='user',
            parts=[types.Part.from_text(text=prompt)],
        )
        response = self.client.models.generate_content(
            model='models/gemini-2.0-flash-001',
            contents=[contents]
        )
        return response.text

    def _prepare_endpoint_json(self, endpoint_response):
        cleaned_response = endpoint_response.strip()
        if cleaned_response.startswith('```'):
            cleaned_response = cleaned_response.split('\n', 1)[-1]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response.rsplit('```', 1)[0]
            cleaned_response = cleaned_response.strip()
        try:
            return json.loads(cleaned_response)
        except Exception as e:
            print(f"Could not parse endpoint_response as JSON: {e}\nGemini response: {endpoint_response}")
            raise

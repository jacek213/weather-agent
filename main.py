import os
from dotenv import load_dotenv
import requests
import speech_recognition as sr
from google import genai
from google.genai import types
import json

load_dotenv()
API_KEY = os.getenv("API_KEY")
CITY = os.getenv("CITY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

geminiClient = genai.Client(api_key=GEMINI_API_KEY)


def recognize_speech(lang="pl-PL"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language=lang)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Speech recognition service error: {e}")
    return None


def ask_gemini_for_endpoint(question, city):
    system_prompt = (
        "You are a openweathermap api expert. The user asked the following question: '"
        f"{question}'. Here is the city: {city}.\n"
        "Your goal is to provide an API URL that can be used to answer the user's question plus instructions on how to extract the relevant data from the API response. "
        "Please provide a JSON object having the following structure:\n"
        "{\n"
        "  \"api_url\": \"<API_URL>\",\n" # embed API_KEY to be replaced in the actual api call. Include the city name in the URL.\n"
        "  \"instructions\": \"<INSTRUCTIONS>\"\n"
        "}\n"
        "Closely follow the API documentation. General indication on which endpoint should be used: https://openweathermap.org/guide."
        "Eg for current weather, use endpoint described at https://openweathermap.org/current. \n"
        "For past weather you can use history: https://openweathermap.org/history   \n"
        "For forecast - the most applicable of https://openweathermap.org/api/hourly-forecast, https://openweathermap.org/forecast5, https://openweathermap.org/forecast16 or https://openweathermap.org/api/forecast30"
        "Just return a JSON object with the api_url and instructions. Do not include any other text or explanation, so it can be easily parsed by the Python agent.\n Do not wrap the code into a fenced code block. Dont add newlines. Example response: \n"
        "{\"api_url\": \"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric\", \"instructions\": \"Check the 'weather' array and 'main'/'description' for current weather.\"}\n"
        "If the answer cannot be determined, return an error message in the JSON object and give nulls to api_url and instructions\n"
        "If the question requires knowledge on topics different than weather, you're now an expert in that topic (e.g. fishing) and try to provide the best instructions to extract data relevant to that question. \n"
    )

    contents = types.Content(
        role='user',
        parts=[types.Part.from_text(text=system_prompt)]

    )
    response = geminiClient.models.generate_content(
        model='models/gemini-2.0-flash-001',
        contents=[contents]
    )
    return response.text


def ask_gemini_for_answer(question, weather_json, instructions):
    prompt = (
        "You are a weather assistant and a openweathermap api expert, also a fishing expert consultant. The user asked the following question: '"
        f"{question}'. Here is the JSON response from the weather API: {weather_json}\n"
        f"Based on the instructions provided: {instructions} extract the relevant data from the API response and provide a human-friendly answer. "
        "If the answer cannot be determined, say so."
        "The answer should be in Polish. Should not include technical details, api response, we need to hide that from the end user. Just a concise answer, keep it short, dont say full date and stuff. Respond like an old uncle joker, not a robot. "
    )
    contents = types.Content(
        role='user',
        parts=[types.Part.from_text(text=prompt)],
    )
    response = geminiClient.models.generate_content(
        model='models/gemini-2.0-flash-001',
        contents=[contents]
    )
    return response.text


def main():
    question = recognize_speech()
    if question:
        print(f"Your question: {question}")
        endpoint_response = ask_gemini_for_endpoint(question, CITY)
        print(f"Endpoint response: {endpoint_response}")  # Debug: show raw Gemini output
        # Try to extract JSON from code block if present
        cleaned_response = endpoint_response.strip()
        if cleaned_response.startswith('```'):
            # Remove code block markers and possible language specifier
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
        # Make the API call after swapping the API_KEY
        api_url = api_url.replace("{API_KEY}", API_KEY)
        api_url = api_url.replace("{city}", CITY)
        response = requests.get(api_url)
        if response.status_code == 200:
            weather_json = response.json()
            answer = ask_gemini_for_answer(question, weather_json, instructions)
            print(f"Answer: {answer}")
            os.system(f'say -v Zosia "{answer}"')
        else:
            print(f"API error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()

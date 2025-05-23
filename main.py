import os
from dotenv import load_dotenv
import requests
import speech_recognition as sr

load_dotenv()
API_KEY = os.getenv("API_KEY")
CITY = os.getenv("CITY")


def get_weather(api_key, city):
    print(f"Fetching weather data for {city}.... API key: {api_key}")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        print(f"Weather in {city}: {weather}, {temp}°C")
    else:
        print("Failed to fetch weather data. Check your API key and city name.")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")


def recognize_speech(lang="pl-PL"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Powiedz coś (Say something)...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language=lang)
        print(f"Rozpoznano (Recognized): {text}")
        return text
    except sr.UnknownValueError:
        print("Nie rozpoznano mowy (Could not understand audio)")
    except sr.RequestError as e:
        print(f"Błąd połączenia z usługą rozpoznawania mowy: {e}")
    return None


def main():
    question = recognize_speech()
    if question:
        # For now, just print the recognized question
        print(f"Twoje pytanie: {question}")
    get_weather(API_KEY, CITY)


if __name__ == "__main__":
    main()

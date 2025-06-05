# Weather Notification Agent

This is a Python agent that fetches weather data from OpenWeatherMap and answers user questions about the weather using voice recognition and Gemini AI. The agent can also speak the answer aloud.

The goal was to creatively use LLMs to make it's own decisions (make it a true agent).

## How it works

- The agent listens for a question via your microphone.
- It uses Gemini AI to determine the most suitable OpenWeatherMap API endpoint based on the question (current weather/history/forecast?) and prepare instructions on how to extract the relevant data from the json response.
- Proper Weather API endpoint is called from python as indicated in the Gemini response.
- Gemini AI recevies the api response, extraction instructions and original question to provide the final response.
- The Gemini response is spoken out loud (macOS only).

## Features
- Voice recognition (Polish, via microphone)
- Fetches current weather or forecast for a specified city
- Uses Gemini AI to interpret user questions and extract relevant weather data
- Answers are spoken aloud (macOS, Polish voice)

## Setup
1. Install portaudio via brew
```sh
brew install portaudio
```
2. Create a virtual environment
```sh
python3 -m venv .venv
source .venv/bin/activate
```
3. Install dependencies:
```sh
pip install -r requirements.txt
```
4. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api).
5. Get a Gemini API key from Google AI Studio.
6. Copy the example environment file and update it:
```sh
cp .env.example .env
```
7. Edit `.env` and fill in your API keys and city name:
- `WEATHER_API_KEY` (OpenWeatherMap)
- `GEMINI_API_KEY` (Google Gemini)
- `CITY` (e.g., Warsaw)


## Usage
Run the agent:
```sh
python main.py
```

Or run via a Copilot task:
```sh
⇧⌘B # then select "Run Weather Agent"
```

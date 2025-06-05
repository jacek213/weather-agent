# Weather Notification Agent

This is a Python agent that fetches weather data from OpenWeatherMap and answers user questions about the weather using voice recognition and Gemini AI. The agent can also speak the answer aloud.

## Features
- Voice recognition (Polish, via microphone)
- Fetches current weather or forecast for a specified city
- Uses Gemini AI to interpret user questions and extract relevant weather data
- Answers are spoken aloud (macOS, Polish voice)
- Terminal output for debugging and transparency
- Easily extendable for more notification channels

## Setup
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api).
3. Get a Gemini API key from Google AI Studio.
4. Copy the example environment file and update it:
   ```sh
   cp .env.example .env
   ```
5. Edit `.env` and fill in your API keys and city name:
   - `API_KEY` (OpenWeatherMap)
   - `GEMINI_API_KEY` (Google Gemini)
   - `CITY` (e.g., Warsaw)

## Virtual Environment (Recommended)
To avoid dependency conflicts, create a virtual environment before installing dependencies:

```sh
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate   # On Windows
```

Then install dependencies:

```sh
pip install -r requirements.txt
```

## Usage
Run the agent:
```sh
python main.py
```

Or run via a Copilot task:
```sh
⇧⌘B # then select the task
```

## How it works
- The agent listens for a question in Polish via your microphone.
- It uses Gemini AI to determine the correct OpenWeatherMap API endpoint and how to extract the answer.
- It fetches the weather data, asks Gemini to generate a friendly answer in Polish, and speaks it aloud (macOS only).
- All steps and errors are printed in the terminal for transparency.

---
Feel free to extend this agent with more features, such as scheduled notifications, desktop notifications, or support for more languages!

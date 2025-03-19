import os
import requests # type: ignore
import logging
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()

OWM_API_KEY = os.getenv("OWM_API_KEY") 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  

genai.configure(api_key=GEMINI_API_KEY)

cityname = "Stamford"
statecode = "CT"
countrycode = "US"
limit = 1

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_location_coordinates(city, state, country):
    try:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit={limit}&appid={OWM_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        if not data:
            raise ValueError("No location data found. Check city/state/country inputs.")
        
        return data[0]["lat"], data[0]["lon"]
    
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None, None
    except KeyError:
        logging.error("Unexpected response format from API.")
        return None, None
    except ValueError as e:
        logging.error(e)
        return None, None

def get_weather(lat, lon):
    try:
        if lat is None or lon is None:
            raise ValueError("Invalid coordinates provided.")
        
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Weather API request failed: {e}")
        return None
    except ValueError as e:
        logging.error(e)
        return None

def analyze_weather(weather_data):
    """Use Gemini API to analyze and summarize weather data."""
    try:
        if not weather_data:
            raise ValueError("No weather data available.")
        
        weather_desc = weather_data["weather"][0]["description"]
        temp = weather_data["main"]["temp"]
        prompt = f"The current weather is described as '{weather_desc}' with a temperature of {(9/5)*(temp) + 32}°F. Can you provide a brief summary and give a suggestion for what to wear?"

        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        
        return response.text if response.text else "Weather analysis unavailable at the moment."
    
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        return "Weather analysis unavailable at the moment."

lat, lon = get_location_coordinates(cityname, statecode, countrycode)
weather_data = get_weather(lat, lon)
if weather_data:
    summary = analyze_weather(weather_data)
    print("AI Weather Analysis:", summary)
else:
    print("Failed to retrieve weather data.")

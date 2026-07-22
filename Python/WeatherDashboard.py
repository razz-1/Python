"""
Weather Dashboard
-----------------
Fetches live current weather conditions for a user-specified city using
the OpenWeatherMap "Current Weather Data" API.

Setup:
1. Sign up for a free API key at https://openweathermap.org/api
2. Either:
   - set an environment variable: export OPENWEATHERMAP_API_KEY="your_key_here"
   - or paste your key into the API_KEY variable below
3. Run: python weather_dashboard.py
"""

import os
import sys
import requests

API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "")  # or paste your key here
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str, api_key: str, units: str = "metric") -> dict:
    """
    Fetch current weather data for a given city.

    Args:
        city: City name, e.g. "Edmonton" or "Edmonton,CA"
        api_key: Your OpenWeatherMap API key
        units: "metric" (Celsius), "imperial" (Fahrenheit), or "standard" (Kelvin)

    Returns:
        Parsed JSON response as a dict.

    Raises:
        requests.HTTPError: if the API returns an error status code.
    """
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def format_weather(data: dict, units: str = "metric") -> str:
    """Format the raw API response into a readable dashboard string."""
    unit_symbol = {"metric": "°C", "imperial": "°F", "standard": "K"}.get(units, "")
    speed_unit = "m/s" if units != "imperial" else "mph"

    city_name = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "")
    weather_desc = data["weather"][0]["description"].title()
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    temp_min = data["main"]["temp_min"]
    temp_max = data["main"]["temp_max"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    clouds = data.get("clouds", {}).get("all", "N/A")

    lines = [
        "=" * 40,
        f"  Weather Dashboard: {city_name}, {country}",
        "=" * 40,
        f"  Conditions:   {weather_desc}",
        f"  Temperature:  {temp}{unit_symbol} (feels like {feels_like}{unit_symbol})",
        f"  Min / Max:    {temp_min}{unit_symbol} / {temp_max}{unit_symbol}",
        f"  Humidity:     {humidity}%",
        f"  Pressure:     {pressure} hPa",
        f"  Wind Speed:   {wind_speed} {speed_unit}",
        f"  Cloud Cover:  {clouds}%",
        "=" * 40,
    ]
    return "\n".join(lines)


def main():
    api_key = API_KEY
    if not api_key:
        api_key = input("Enter your OpenWeatherMap API key: ").strip()
    if not api_key:
        print("Error: No API key provided. Get one free at https://openweathermap.org/api")
        sys.exit(1)

    print("\nWeather Dashboard (type 'quit' or 'exit' to stop)\n")

    while True:
        city = input("Enter a city name: ").strip()
        if city.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if not city:
            print("Please enter a valid city name.\n")
            continue

        try:
            data = get_weather(city, api_key)
            print("\n" + format_weather(data) + "\n")
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status == 404:
                print(f"City '{city}' not found. Please check the spelling.\n")
            elif status == 401:
                print("Invalid API key. Please check your OpenWeatherMap key.\n")
            else:
                print(f"HTTP error occurred: {e}\n")
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}\n")
        except (KeyError, IndexError):
            print("Unexpected response format from the API. Please try again.\n")


if __name__ == "__main__":
    main()
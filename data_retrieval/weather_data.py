# data_retrieval/weather_data.py
import requests

def get_weather_data():
    try:
        response = requests.get('https://api.example.com/weather')
        response.raise_for_status()  # Raise an exception for HTTP errors
        weather_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        weather_data = {'temp': 30, 'condition': 'Sunny', 'lat': 35.6828, 'lon': 139.7595}
    return weather_data

def get_earthquake_data():
    try:
        response = requests.get('https://api.example.com/earthquakes')
        response.raise_for_status()  # Raise an exception for HTTP errors
        earthquake_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching earthquake data: {e}")
        earthquake_data = [
            {'magnitude': 5.2, 'lat': 36.2048, 'lon': 138.2529, 'time': '2024-07-18 12:34'}
        ]
    return earthquake_data

def get_weather_forecast_data():
    try:
        response = requests.get('https://api.example.com/weather_forecast')
        response.raise_for_status()  # Raise an exception for HTTP errors
        forecast_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather forecast data: {e}")
        forecast_data = [
            {'date': '2024-07-19', 'temp': 30, 'condition': 'Sunny'},
            {'date': '2024-07-20', 'temp': 28, 'condition': 'Partly Cloudy'},
        ]
    return forecast_data

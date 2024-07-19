# data_retrieval/safety_data.py
import requests

def get_safety_data():
    try:
        response = requests.get('https://api.example.com/safety')
        response.raise_for_status()  # Raise an exception for HTTP errors
        safety_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching safety data: {e}")
        safety_data = [
            {'name': 'Hospital', 'lat': 35.6895, 'lon': 139.6917, 'type': 'Hospital', 'contact': '03-1234-5678', 'hours': '24/7'},
            {'name': 'Police Station', 'lat': 35.6828, 'lon': 139.7595, 'type': 'Police Station', 'contact': '03-8765-4321', 'hours': '24/7'},
        ]
    return safety_data
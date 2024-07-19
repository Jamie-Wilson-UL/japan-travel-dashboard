# data_retrieval/travel_data.py
import requests

def get_travel_data():
    try:
        response = requests.get('https://api.example.com/travel')
        response.raise_for_status()  # Raise an exception for HTTP errors
        travel_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching travel data: {e}")
        travel_data = [
            {'name': 'Tokyo Tower', 'lat': 35.6586, 'lon': 139.7454, 'category': 'Modern', 'description': 'A famous landmark', 'opening_hours': '9:00 AM - 11:00 PM', 'ticket_price': 'Adult: 1200 yen, Child: 500 yen'},
            {'name': 'Senso-ji Temple', 'lat': 35.7148, 'lon': 139.7967, 'category': 'Historical', 'description': 'An ancient Buddhist temple', 'opening_hours': '6:00 AM - 5:00 PM', 'ticket_price': 'Free'},
        ]
    return travel_data
            
# data_retrieval/transport_data.py
import requests

def get_transport_data():
    try:
        response = requests.get('https://api.example.com/transport')
        response.raise_for_status()  # Raise an exception for HTTP errors
        transport_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching transport data: {e}")
        transport_data = [
            {'name': 'Train 1', 'lat': 35.6814, 'lon': 139.7670, 'status': 'On Time', 'type': 'Train', 'platform': '2', 'next_arrival': '5 mins'},
            {'name': 'Bus 22', 'lat': 35.6895, 'lon': 139.6917, 'status': 'Delayed', 'type': 'Bus', 'platform': 'N/A', 'next_arrival': '15 mins'},
        ]
    return transport_data
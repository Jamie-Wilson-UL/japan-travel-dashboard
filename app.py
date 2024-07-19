# app.py
from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objs as go
from data_retrieval.travel_data import get_travel_data
from data_retrieval.transport_data import get_transport_data
from data_retrieval.safety_data import get_safety_data
from data_retrieval.weather_data import get_weather_data, get_earthquake_data, get_weather_forecast_data

app = Dash(__name__)
app.title = "Cat's Japan Travel Hub, Meow!"

categories = ['All', 'Historical', 'Nature', 'Modern', 'Shopping', 'Food']
transport_types = ['All', 'Train', 'Bus', 'Subway']
safety_types = ['All', 'Hospital', 'Police Station', 'Fire Station']

app.layout = html.Div([
    html.H1("Cat's Japan Travel Hub, Meow!", style={'textAlign': 'center', 'marginBottom': '30px'}),
    dcc.Tabs([
        dcc.Tab(label='Itinerary Planner', children=[
            html.Div([
                html.H3('Must-Visit Attractions'),
                dcc.Input(id='attraction-filter', type='text', placeholder='Search for attractions', className='dcc-control', style={'width': '300px'}),
                dcc.Dropdown(id='category-dropdown', options=[{'label': category, 'value': category} for category in categories], value='All', className='dcc-control', style={'width': '200px'}),
                dcc.DatePickerRange(id='date-picker-range', start_date='2024-07-19', end_date='2024-07-25', className='dcc-control'),
                html.Button(id='submit-button', n_clicks=0, children='Search', className='button'),
                dcc.Graph(id='attractions-map'),
                dcc.Interval(id='interval-attractions', interval=60000, n_intervals=0)
            ], className='tab-content')
        ]),
        dcc.Tab(label='Public Transportation Navigator', children=[
            html.Div([
                html.H3('Public Transportation Status'),
                dcc.Dropdown(id='transport-type-dropdown', options=[{'label': t, 'value': t} for t in transport_types], value='All', className='dcc-control', style={'width': '200px'}),
                dcc.Graph(id='transport-map'),
                dcc.Interval(id='interval-transport', interval=60000, n_intervals=0)
            ], className='tab-content')
        ]),
        dcc.Tab(label='Emergency and Safety Information', children=[
            html.Div([
                html.H3('Emergency and Safety Information'),
                dcc.Dropdown(id='safety-type-dropdown', options=[{'label': s, 'value': s} for s in safety_types], value='All', className='dcc-control', style={'width': '200px'}),
                dcc.Graph(id='safety-map'),
                dcc.Interval(id='interval-safety', interval=60000, n_intervals=0)
            ], className='tab-content')
        ]),
        dcc.Tab(label='Weather and Natural Disasters', children=[
            html.Div([
                html.H3('Local Weather and Earthquake Alerts'),
                dcc.Graph(id='weather-map'),
                dcc.Interval(id='interval-weather', interval=60000, n_intervals=0),
                html.H4('7-Day Weather Forecast'),
                dcc.Graph(id='weather-forecast'),
                html.H4('Recent Earthquakes'),
                html.Div(id='earthquake-alerts')
            ], className='tab-content')
        ]),
    ])
])

@app.callback(
    Output('attractions-map', 'figure'),
    [Input('submit-button', 'n_clicks'), Input('interval-attractions', 'n_intervals')],
    [State('attraction-filter', 'value'), State('category-dropdown', 'value'), State('date-picker-range', 'start_date'), State('date-picker-range', 'end_date')]
)
def update_attractions_map(n_clicks, n_intervals, filter_value, category_value, start_date, end_date):
    travel_data = get_travel_data()
    if filter_value:
        travel_data = [place for place in travel_data if filter_value.lower() in place['name'].lower()]
    if category_value and category_value != 'All':
        travel_data = [place for place in travel_data if place['category'] == category_value]
    # Add date filtering logic here if applicable

    attractions = go.Scattermapbox(
        lat=[place['lat'] for place in travel_data],
        lon=[place['lon'] for place in travel_data],
        mode='markers',
        marker={'size': 12, 'color': 'blue', 'symbol': 'marker'},
        text=[f"{place['name']}<br>{place.get('description', '')}<br>Open: {place.get('opening_hours', 'N/A')}<br>Price: {place.get('ticket_price', 'Free')}" for place in travel_data]
    )
    layout = go.Layout(
        mapbox={'style': "carto-positron", 'center': {'lat': 35.682839, 'lon': 139.759455}, 'zoom': 12},
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        paper_bgcolor='#f0f2f5',
        plot_bgcolor='#f0f2f5',
    )
    return {'data': [attractions], 'layout': layout}

@app.callback(
    Output('transport-map', 'figure'),
    [Input('interval-transport', 'n_intervals'), Input('transport-type-dropdown', 'value')]
)
def update_transport_map(n, transport_type):
    transport_data = get_transport_data()
    if transport_type and transport_type != 'All':
        transport_data = [t for t in transport_data if t['type'] == transport_type]
    transport = go.Scattermapbox(
        lat=[point['lat'] for point in transport_data],
        lon=[point['lon'] for point in transport_data],
        mode='markers',
        marker={'size': 12, 'color': ['green' if point['status'] == 'On Time' else 'red' for point in transport_data]},
        text=[f"{point['name']} - {point['status']}<br>Platform: {point.get('platform', 'N/A')}<br>Next Arrival: {point.get('next_arrival', 'N/A')}" for point in transport_data]
    )
    layout = go.Layout(
        mapbox={'style': "carto-positron", 'center': {'lat': 35.682839, 'lon': 139.759455}, 'zoom': 12},
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        paper_bgcolor='#f0f2f5',
        plot_bgcolor='#f0f2f5',
    )
    return {'data': [transport], 'layout': layout}

@app.callback(
    Output('safety-map', 'figure'),
    [Input('interval-safety', 'n_intervals'), Input('safety-type-dropdown', 'value')]
)
def update_safety_map(n, safety_type):
    safety_data = get_safety_data()
    if safety_type and safety_type != 'All':
        safety_data = [s for s in safety_data if s['type'] == safety_type]
    safety = go.Scattermapbox(
        lat=[place['lat'] for place in safety_data],
        lon=[place['lon'] for place in safety_data],
        mode='markers',
        marker={'size': 12, 'color': 'blue', 'symbol': 'hospital'},
        text=[f"{place['name']}<br>Contact: {place.get('contact', 'N/A')}<br>Hours: {place.get('hours', 'N/A')}" for place in safety_data]
    )
    layout = go.Layout(
        mapbox={'style': "carto-positron", 'center': {'lat': 35.682839, 'lon': 139.759455}, 'zoom': 12},
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        paper_bgcolor='#f0f2f5',
        plot_bgcolor='#f0f2f5',
    )
    return {'data': [safety], 'layout': layout}

@app.callback(
    [Output('weather-map', 'figure'), Output('weather-forecast', 'figure'), Output('earthquake-alerts', 'children')],
    Input('interval-weather', 'n_intervals')
)
def update_weather_and_earthquake(n):
    weather_data = get_weather_data()
    forecast_data = get_weather_forecast_data()  # Assuming a function to get forecast data
    weather = go.Scattermapbox(
        lat=[weather_data['lat']],
        lon=[weather_data['lon']],
        mode='markers',
        marker={'size': 12, 'color': 'orange'},
        text=[f"Temp: {weather_data['temp']}°C, Condition: {weather_data['condition']}"]
    )
    forecast = go.Figure()
    for day in forecast_data:
        forecast.add_trace(go.Bar(
            x=[day['date']],
            y=[day['temp']],
            name=day['condition'],
            marker_color='#2980b9'
        ))
    forecast.update_layout(
        title='7-Day Weather Forecast',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        paper_bgcolor='#f0f2f5',
        plot_bgcolor='#f0f2f5',
    )

    layout = go.Layout(
        mapbox={'style': "carto-positron", 'center': {'lat': 35.682839, 'lon': 139.759455}, 'zoom': 12},
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        paper_bgcolor='#f0f2f5',
        plot_bgcolor='#f0f2f5',
    )
    earthquake_data = get_earthquake_data()
    earthquake_alerts = [html.P(f"Magnitude {quake['magnitude']} earthquake at {quake['time']} near ({quake['lat']}, {quake['lon']})") for quake in earthquake_data]
    return {'data': [weather], 'layout': layout}, forecast, earthquake_alerts

if __name__ == '__main__':
    app.run_server(debug=True)

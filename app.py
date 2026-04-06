"""Global Weather Monitor - Flask Backend using Open-Meteo (Free, No API Key)"""
from typing import Optional
from concurrent.futures import ThreadPoolExecutor
import requests
from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

# Open-Meteo API (free, no API key required)
BASE_URL = 'https://api.open-meteo.com/v1/forecast'

# Weather code to description mapping
WEATHER_CODES = {
    0: ('Clear Sky', '01d'),
    1: ('Mainly Clear', '01d'),
    2: ('Partly Cloudy', '02d'),
    3: ('Overcast', '03d'),
    45: ('Foggy', '50d'),
    48: ('Depositing Rime Fog', '50d'),
    51: ('Light Drizzle', '09d'),
    53: ('Moderate Drizzle', '09d'),
    55: ('Dense Drizzle', '09d'),
    61: ('Slight Rain', '10d'),
    63: ('Moderate Rain', '10d'),
    65: ('Heavy Rain', '10d'),
    71: ('Slight Snow', '13d'),
    73: ('Moderate Snow', '13d'),
    75: ('Heavy Snow', '13d'),
    80: ('Slight Rain Showers', '09d'),
    81: ('Moderate Rain Showers', '09d'),
    82: ('Violent Rain Showers', '09d'),
    95: ('Thunderstorm', '11d'),
    96: ('Thunderstorm with Hail', '11d'),
    99: ('Thunderstorm with Heavy Hail', '11d'),
}

# Major cities around the world with coordinates
CITIES = [
    {'name': 'New York', 'country': 'US', 'lat': 40.7128, 'lon': -74.0060},
    {'name': 'London', 'country': 'GB', 'lat': 51.5074, 'lon': -0.1278},
    {'name': 'Tokyo', 'country': 'JP', 'lat': 35.6762, 'lon': 139.6503},
    {'name': 'Paris', 'country': 'FR', 'lat': 48.8566, 'lon': 2.3522},
    {'name': 'Sydney', 'country': 'AU', 'lat': -33.8688, 'lon': 151.2093},
    {'name': 'Beijing', 'country': 'CN', 'lat': 39.9042, 'lon': 116.4074},
    {'name': 'Dubai', 'country': 'AE', 'lat': 25.2048, 'lon': 55.2708},
    {'name': 'Singapore', 'country': 'SG', 'lat': 1.3521, 'lon': 103.8198},
    {'name': 'Moscow', 'country': 'RU', 'lat': 55.7558, 'lon': 37.6173},
    {'name': 'Mumbai', 'country': 'IN', 'lat': 19.0760, 'lon': 72.8777},
    {'name': 'Los Angeles', 'country': 'US', 'lat': 34.0522, 'lon': -118.2437},
    {'name': 'Berlin', 'country': 'DE', 'lat': 52.5200, 'lon': 13.4050},
    {'name': 'Toronto', 'country': 'CA', 'lat': 43.6532, 'lon': -79.3832},
    {'name': 'Sao Paulo', 'country': 'BR', 'lat': -23.5505, 'lon': -46.6333},
    {'name': 'Seoul', 'country': 'KR', 'lat': 37.5665, 'lon': 126.9780},
    {'name': 'Hong Kong', 'country': 'HK', 'lat': 22.3193, 'lon': 114.1694},
    {'name': 'Cairo', 'country': 'EG', 'lat': 30.0444, 'lon': 31.2357},
    {'name': 'Mexico City', 'country': 'MX', 'lat': 19.4326, 'lon': -99.1332},
    {'name': 'Bangkok', 'country': 'TH', 'lat': 13.7563, 'lon': 100.5018},
    {'name': 'Istanbul', 'country': 'TR', 'lat': 41.0082, 'lon': 28.9784},
    {'name': 'Shanghai', 'country': 'CN', 'lat': 31.2304, 'lon': 121.4737},
]


def fetch_weather(city: dict) -> Optional[dict]:
    """Fetch weather data for a single city using Open-Meteo."""
    try:
        params = {
            'latitude': city['lat'],
            'longitude': city['lon'],
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,surface_pressure',
            'timezone': 'auto'
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data['current']

        weather_code = current.get('weather_code', 0)
        description, icon = WEATHER_CODES.get(weather_code, ('Unknown', '01d'))

        return {
            'city': city['name'],
            'country': city['country'],
            'temp': round(current['temperature_2m'], 1),
            'feels_like': round(current['apparent_temperature'], 1),
            'humidity': current['relative_humidity_2m'],
            'description': description,
            'icon': icon,
            'wind_speed': round(current['wind_speed_10m'], 1),
            'pressure': round(current['surface_pressure']),
            'timestamp': datetime.utcnow().isoformat()
        }
    except requests.RequestException as e:
        print(f"Error fetching weather for {city['name']}: {e}")
        return None


@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')


@app.route('/api/weather')
def get_all_weather():
    """Get weather data for all cities using parallel requests."""
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_weather, CITIES))

    weather_data = [r for r in results if r is not None]

    return jsonify({
        'data': weather_data,
        'updated': datetime.utcnow().isoformat(),
        'count': len(weather_data)
    })


@app.route('/api/weather/<city_name>')
def get_city_weather(city_name: str):
    """Get weather data for a specific city."""
    city = next((c for c in CITIES if c['name'].lower() == city_name.lower()), None)
    if not city:
        return jsonify({'error': 'City not found'}), 404

    data = fetch_weather(city)
    if not data:
        return jsonify({'error': 'Failed to fetch weather data'}), 500

    return jsonify(data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)

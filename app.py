"""Global Weather Monitor - Flask Backend"""
import os
import requests
from flask import Flask, render_template, jsonify
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# OpenWeatherMap API configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

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
]


def fetch_weather(city: dict) -> dict | None:
    """Fetch weather data for a single city."""
    if not API_KEY:
        return None

    try:
        params = {
            'lat': city['lat'],
            'lon': city['lon'],
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            'city': city['name'],
            'country': city['country'],
            'temp': round(data['main']['temp'], 1),
            'feels_like': round(data['main']['feels_like'], 1),
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
            'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # m/s to km/h
            'pressure': data['main']['pressure'],
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
    """Get weather data for all cities."""
    if not API_KEY:
        return jsonify({
            'error': 'API key not configured',
            'message': 'Please set OPENWEATHER_API_KEY environment variable'
        }), 500

    weather_data = []
    for city in CITIES:
        data = fetch_weather(city)
        if data:
            weather_data.append(data)

    return jsonify({
        'data': weather_data,
        'updated': datetime.utcnow().isoformat(),
        'count': len(weather_data)
    })


@app.route('/api/weather/<city_name>')
def get_city_weather(city_name: str):
    """Get weather data for a specific city."""
    if not API_KEY:
        return jsonify({'error': 'API key not configured'}), 500

    city = next((c for c in CITIES if c['name'].lower() == city_name.lower()), None)
    if not city:
        return jsonify({'error': 'City not found'}), 404

    data = fetch_weather(city)
    if not data:
        return jsonify({'error': 'Failed to fetch weather data'}), 500

    return jsonify(data)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

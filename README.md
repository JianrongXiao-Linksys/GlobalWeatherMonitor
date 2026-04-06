# Global Weather Monitor

A real-time weather monitoring web application that displays current weather conditions for major cities worldwide.

## Features

- Real-time weather data for 20 major cities across the globe
- Beautiful, responsive UI with dark theme
- Temperature unit toggle (Celsius/Fahrenheit)
- City search functionality
- Auto-refresh every 5 minutes
- Weather details including:
  - Current temperature
  - Feels like temperature
  - Humidity
  - Wind speed
  - Atmospheric pressure

## Cities Covered

New York, London, Tokyo, Paris, Sydney, Beijing, Dubai, Singapore, Moscow, Mumbai, Los Angeles, Berlin, Toronto, Sao Paulo, Seoul, Hong Kong, Cairo, Mexico City, Bangkok, Istanbul

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: OpenWeatherMap
- **Styling**: Custom CSS with glassmorphism effects

## Prerequisites

- Python 3.9+
- OpenWeatherMap API key (free tier available)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/GlobalWeatherMonitor.git
cd GlobalWeatherMonitor
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenWeatherMap API key
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and visit `http://localhost:5000`

## Getting an API Key

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Navigate to your API keys section
3. Generate a new API key (free tier allows 1000 calls/day)
4. Add the key to your `.env` file

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/api/weather` | GET | Get weather for all cities |
| `/api/weather/<city>` | GET | Get weather for a specific city |

## Project Structure

```
GlobalWeatherMonitor/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── css/
    │   └── style.css     # Styling
    └── js/
        └── main.js       # Frontend logic
```

## Deployment

### Using Gunicorn (Production)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## License

MIT License

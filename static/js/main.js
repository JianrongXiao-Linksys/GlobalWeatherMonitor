// Global state
let weatherData = [];
let useCelsius = true;
let refreshInterval = null;

// DOM elements
const weatherGrid = document.getElementById('weather-grid');
const loadingEl = document.getElementById('loading');
const errorEl = document.getElementById('error');
const errorMessage = document.getElementById('error-message');
const updateTime = document.getElementById('update-time');
const searchInput = document.getElementById('search');
const refreshBtn = document.getElementById('refresh');
const unitC = document.getElementById('unit-c');
const unitF = document.getElementById('unit-f');

// Fetch weather data from API
async function loadWeather() {
    showLoading(true);
    hideError();

    try {
        const response = await fetch('/api/weather');
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message || result.error || 'Failed to fetch weather data');
        }

        weatherData = result.data;
        updateTime.textContent = formatTime(result.updated);

        // Show demo mode banner if applicable
        const demoBanner = document.getElementById('demo-banner');
        if (result.demo && demoBanner) {
            demoBanner.classList.remove('hidden');
        }

        renderWeather(weatherData);
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

// Render weather cards
function renderWeather(data) {
    const filteredData = filterBySearch(data);

    if (filteredData.length === 0) {
        weatherGrid.innerHTML = '<p class="no-results">No cities found matching your search.</p>';
        return;
    }

    weatherGrid.innerHTML = filteredData.map((city, index) => createWeatherCard(city, index)).join('');
}

// Create a single weather card
function createWeatherCard(data, index) {
    const temp = useCelsius ? data.temp : celsiusToFahrenheit(data.temp);
    const feelsLike = useCelsius ? data.feels_like : celsiusToFahrenheit(data.feels_like);
    const unit = useCelsius ? '°C' : '°F';

    return `
        <article class="weather-card" style="animation-delay: ${index * 0.05}s">
            <div class="card-header">
                <div>
                    <h2 class="city-name">${data.city}</h2>
                    <p class="country">${getCountryName(data.country)}</p>
                </div>
                <img
                    src="https://openweathermap.org/img/wn/${data.icon}@2x.png"
                    alt="${data.description}"
                    class="weather-icon"
                >
            </div>
            <div class="temp-main">
                ${temp}<span class="unit">${unit}</span>
            </div>
            <p class="description">${data.description}</p>
            <div class="details">
                <div class="detail-item">
                    <span class="detail-label">Feels Like</span>
                    <span class="detail-value">${feelsLike}${unit}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Humidity</span>
                    <span class="detail-value">${data.humidity}%</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Wind</span>
                    <span class="detail-value">${data.wind_speed} km/h</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Pressure</span>
                    <span class="detail-value">${data.pressure} hPa</span>
                </div>
            </div>
        </article>
    `;
}

// Convert Celsius to Fahrenheit
function celsiusToFahrenheit(celsius) {
    return Math.round((celsius * 9/5) + 32);
}

// Filter data by search term
function filterBySearch(data) {
    const searchTerm = searchInput.value.toLowerCase().trim();
    if (!searchTerm) return data;

    return data.filter(city =>
        city.city.toLowerCase().includes(searchTerm) ||
        city.country.toLowerCase().includes(searchTerm) ||
        getCountryName(city.country).toLowerCase().includes(searchTerm)
    );
}

// Get country name from code
function getCountryName(code) {
    const countries = {
        'US': 'United States',
        'GB': 'United Kingdom',
        'JP': 'Japan',
        'FR': 'France',
        'AU': 'Australia',
        'CN': 'China',
        'AE': 'UAE',
        'SG': 'Singapore',
        'RU': 'Russia',
        'IN': 'India',
        'DE': 'Germany',
        'CA': 'Canada',
        'BR': 'Brazil',
        'KR': 'South Korea',
        'HK': 'Hong Kong',
        'EG': 'Egypt',
        'MX': 'Mexico',
        'TH': 'Thailand',
        'TR': 'Turkey'
    };
    return countries[code] || code;
}

// Format timestamp
function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString(undefined, {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Show/hide loading state
function showLoading(show) {
    loadingEl.classList.toggle('hidden', !show);
    weatherGrid.classList.toggle('hidden', show);
    refreshBtn.classList.toggle('loading', show);
}

// Show error message
function showError(message) {
    errorEl.classList.remove('hidden');
    errorMessage.textContent = message;
    weatherGrid.classList.add('hidden');
}

// Hide error message
function hideError() {
    errorEl.classList.add('hidden');
}

// Event listeners
refreshBtn.addEventListener('click', () => {
    loadWeather();
});

searchInput.addEventListener('input', () => {
    renderWeather(weatherData);
});

unitC.addEventListener('click', () => {
    if (!useCelsius) {
        useCelsius = true;
        unitC.classList.add('active');
        unitF.classList.remove('active');
        renderWeather(weatherData);
    }
});

unitF.addEventListener('click', () => {
    if (useCelsius) {
        useCelsius = false;
        unitF.classList.add('active');
        unitC.classList.remove('active');
        renderWeather(weatherData);
    }
});

// Auto-refresh every 5 minutes
function startAutoRefresh() {
    if (refreshInterval) clearInterval(refreshInterval);
    refreshInterval = setInterval(loadWeather, 5 * 60 * 1000);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadWeather();
    startAutoRefresh();
});

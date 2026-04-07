# ============================================================
# WEATHER SERVICE - Get weather data and alerts
# ============================================================

import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional
import config

logger = logging.getLogger(__name__)


class WeatherService:
    """
    Fetch weather data from OpenWeatherMap API
    Provide alerts for severe weather conditions
    """

    def __init__(self):
        """Initialize weather service"""
        self.api_key = config.WEATHER_API_KEY
        self.city = config.WEATHER_CITY
        self.country = config.WEATHER_COUNTRY
        self.units = config.WEATHER_UNITS
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.current_weather = {}
        self.forecast = []
        self.alerts = []
        
        logger.info(f"Weather service initialized for {self.city}, {self.country}")

    def get_weather(self) -> Dict:
        """Get current weather data"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': f"{self.city},{self.country}",
                'appid': self.api_key,
                'units': self.units
            }
            
            response = requests.get(url, params=params, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            self.current_weather = {
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'main': data['weather'][0]['main'],
                'wind_speed': round(data['wind']['speed'], 1),
                'clouds': data['clouds']['all'],
                'timestamp': datetime.now().isoformat(),
                'city': data['name'],
                'country': data['sys']['country']
            }
            
            logger.info(f"Weather updated: {self.current_weather['temperature']}°, {self.current_weather['description']}")
            return self.current_weather
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API error: {e}")
            return {}
        except KeyError as e:
            logger.error(f"Weather data parsing error: {e}")
            return {}

    def get_forecast(self, days: int = 3) -> List[Dict]:
        """Get weather forecast"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': f"{self.city},{self.country}",
                'appid': self.api_key,
                'units': self.units,
                'cnt': days * 8  # 5-day forecast, 8 per day
            }
            
            response = requests.get(url, params=params, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            self.forecast = []
            
            for item in data['list']:
                forecast_item = {
                    'timestamp': item['dt'],
                    'datetime': datetime.fromtimestamp(item['dt']).isoformat(),
                    'temperature': round(item['main']['temp']),
                    'feels_like': round(item['main']['feels_like']),
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'],
                    'main': item['weather'][0]['main'],
                    'wind_speed': round(item['wind']['speed'], 1),
                    'clouds': item['clouds']['all'],
                    'pop': item.get('pop', 0)  # Probability of precipitation
                }
                self.forecast.append(forecast_item)
            
            logger.info(f"Forecast updated: {len(self.forecast)} time periods")
            return self.forecast
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Forecast API error: {e}")
            return []
        except KeyError as e:
            logger.error(f"Forecast parsing error: {e}")
            return []

    def check_weather_alerts(self) -> List[Dict]:
        """Check for severe weather alerts"""
        self.alerts = []
        
        if not self.current_weather:
            return self.alerts
        
        # Temperature alerts
        temp = self.current_weather.get('temperature', 0)
        if temp >= config.TEMP_HIGH_ALERT:
            self.alerts.append({
                'type': 'high_temperature',
                'severity': 'high',
                'message': f"🌡️ EXTREME HEAT: {temp}°F - Stay hydrated!",
                'temperature': temp
            })
        elif temp <= config.TEMP_LOW_ALERT:
            self.alerts.append({
                'type': 'low_temperature',
                'severity': 'high',
                'message': f"❄️ FREEZING: {temp}°F - Dangerous conditions!",
                'temperature': temp
            })
        
        # Severe weather alerts
        main = self.current_weather.get('main', '').upper()
        severe_conditions = ['THUNDERSTORM', 'TORNADO', 'SNOW', 'RAIN']
        
        if any(condition in main for condition in severe_conditions):
            self.alerts.append({
                'type': 'severe_weather',
                'severity': 'high',
                'message': f"⚠️ SEVERE WEATHER: {self.current_weather.get('description', 'Unknown')}",
                'condition': main
            })
        
        # High wind alerts
        wind_speed = self.current_weather.get('wind_speed', 0)
        if wind_speed > 25:  # mph/kph threshold
            self.alerts.append({
                'type': 'high_wind',
                'severity': 'medium',
                'message': f"💨 HIGH WINDS: {wind_speed} - Use caution",
                'wind_speed': wind_speed
            })
        
        # High humidity alerts
        humidity = self.current_weather.get('humidity', 0)
        if humidity > 90:
            self.alerts.append({
                'type': 'high_humidity',
                'severity': 'low',
                'message': f"💧 HIGH HUMIDITY: {humidity}% - Muggy conditions",
                'humidity': humidity
            })
        
        if self.alerts:
            logger.warning(f"Weather alerts: {len(self.alerts)}")
        
        return self.alerts

    def get_alerts(self) -> List[Dict]:
        """Get all current weather alerts"""
        return self.alerts

    def get_weather_icon(self) -> str:
        """Get emoji icon for current weather"""
        main = self.current_weather.get('main', '').upper()
        
        icon_map = {
            'CLEAR': '☀️',
            'CLOUDS': '☁️',
            'RAIN': '🌧️',
            'DRIZZLE': '🌦️',
            'THUNDERSTORM': '⛈️',
            'SNOW': '❄️',
            'MIST': '🌫️',
            'SMOKE': '💨',
            'HAZE': '🌫️',
            'DUST': '🌪️',
            'FOG': '🌫️',
            'SAND': '🏜️',
            'ASH': '🌋',
            'SQUALL': '💨',
            'TORNADO': '🌪️'
        }
        
        return icon_map.get(main, '🌡️')

    def get_summary(self) -> Dict:
        """Get weather summary"""
        return {
            'city': self.current_weather.get('city', 'Unknown'),
            'country': self.current_weather.get('country', 'Unknown'),
            'temperature': self.current_weather.get('temperature', 0),
            'feels_like': self.current_weather.get('feels_like', 0),
            'description': self.current_weather.get('description', 'N/A'),
            'humidity': self.current_weather.get('humidity', 0),
            'wind_speed': self.current_weather.get('wind_speed', 0),
            'alerts': len(self.alerts),
            'icon': self.get_weather_icon()
        }

    def format_for_display(self) -> str:
        """Format weather for display"""
        if not self.current_weather:
            return "Weather data unavailable"
        
        temp = self.current_weather.get('temperature', 'N/A')
        desc = self.current_weather.get('description', 'N/A').title()
        humidity = self.current_weather.get('humidity', 'N/A')
        wind = self.current_weather.get('wind_speed', 'N/A')
        icon = self.get_weather_icon()
        
        units = '°F' if self.units == 'imperial' else '°C'
        wind_units = 'mph' if self.units == 'imperial' else 'm/s'
        
        return f"{icon} {temp}{units} - {desc}\n💧 {humidity}% 💨 {wind}{wind_units}"

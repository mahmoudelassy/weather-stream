import requests

api_key='API_KEY'
api_url=f'http://api.weatherstack.com/current?access_key={api_key}&query=alexandria'


def fetch_data():
    print(f"Fetching weather data from weatherstack API....")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("API response received successfully")
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        raise

def mock_fetch_data():
    return {'request': {'type': 'City', 'query': 'New York, United States of America', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'New York', 'country': 'United States of America', 'region': 'New York', 'lat': '40.714', 'lon': '-74.006', 'timezone_id': 'America/New_York', 'localtime': '2026-06-10 06:27', 'localtime_epoch': 1781072820, 'utc_offset': '-4.0'}, 'current': {'observation_time': '10:27 AM', 'temperature': 21, 'weather_code': 113, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'], 'weather_descriptions': ['Sunny'], 'astro': {'sunrise': '05:25 AM', 'sunset': '08:27 PM', 'moonrise': '01:55 AM', 'moonset': '03:26 PM', 'moon_phase': 'Waning Crescent', 'moon_illumination': 33}, 'air_quality': {'co': '136', 'no2': '21.9', 'o3': '44', 'so2': '2.1', 'pm2_5': '13.6', 'pm10': '16.2', 'us-epa-index': '1', 'gb-defra-index': '1'}, 'wind_speed': 12, 'wind_degree': 210, 'wind_dir': 'SSW', 'pressure': 1016, 'precip': 0, 'humidity': 64, 'cloudcover': 0, 'feelslike': 21, 'uv_index': 0, 'visibility': 16, 'is_day': 'yes'}}


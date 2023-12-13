import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import requests



load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class WeatherData:
    temperature: float
    humidity: float

def get_lat_lon():
    res = requests.get('https://ipinfo.io?token=4f6b8efea1342c').json()
    lat = res['loc'].split(',')[0]
    lon = res['loc'].split(',')[1]

    return lat, lon

def get_current_weather(lat, lon, API_key):
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
    data = WeatherData(
        temperature = resp.get('main').get('temp'),
        humidity = resp.get('main').get('humidity')
    )
    return data

def main():
    lat, lon = get_lat_lon()
    weather_data = get_current_weather(lat, lon, api_key)
    return weather_data

if __name__ == "__main__":
    lat, lon = get_lat_lon('Amravati', 'MH', 'IN', api_key)
    print(get_current_weather(lat, lon, api_key))

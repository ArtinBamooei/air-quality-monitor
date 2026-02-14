import os
import json
import requests
import sqlite3
from datetime import datetime
from dotenv import load_dotenv  

# بارگذاری متغیرهای امنیتی
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_db_connection():
    return sqlite3.connect('air_quality.db')

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS air_quality_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT, country TEXT, aqi INTEGER,
            pm2_5 REAL, pm10 REAL, co REAL, no2 REAL, o3 REAL, so2 REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_cities():
    file_path = r'C:\Users\ASUS\Desktop\air-quality-monitor\config\cities.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def fetch_air_quality(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        return response.json()['list'][0] if response.status_code == 200 else None
    except:
        return None

def save_to_db(city_name, country, data):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "INSERT INTO air_quality_data (city_name, country, aqi, pm2_5, pm10, co, no2, o3, so2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = (city_name, country, data['main']['aqi'], data['components']['pm2_5'], data['components']['pm10'], data['components']['co'], data['components']['no2'], data['components']['o3'], data['components']['so2'])
    cur.execute(query, values)
    conn.commit()
    conn.close()
    print(f"✅ Data for {city_name} saved!")

def run_pipeline():
    print(f"🚀 Starting... {datetime.now()}")
    init_db()
    cities = get_cities()
    for city in cities:
        air_data = fetch_air_quality(city['lat'], city['lon'])
        if air_data:
            save_to_db(city['name'], city['country'], air_data)

if __name__ == "__main__":
    run_pipeline()
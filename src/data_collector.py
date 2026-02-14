import os
import json
import requests
import sqlite3
from datetime import datetime
from dotenv import load_dotenv  

# تنظیمات مربوط به متغیرهای محیطی برای جلوگیری از لو رفتن API Key در گیت‌هاب
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_db_connection():
    """ایجاد اتصال به دیتابیس محلی - در پروژه‌های بزرگتر بهتر است از PostgreSQL استفاده شود"""
    return sqlite3.connect('air_quality.db')

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # ساخت جدول ذخیره‌سازی داده‌ها اگر از قبل وجود نداشته باشد
    # استفاده از REAL برای دقت بیشتر در مقادیر آلاینده‌ها
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
    # مسیر فایل کانفیگ شهرها - فعلاً به صورت لوکال آدرس‌دهی شده
    # TODO: استفاده از مسیر نسبی (Relative Path) برای اجرای راحت‌تر در سرور
    file_path = r'C:\Users\ASUS\Desktop\air-quality-monitor\config\cities.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
def fetch_air_quality(lat, lon):
    """دریافت داده‌های آلودگی هوا از سرویس Open-Meteo (بدون نیاز به کلید)"""
    # این آدرس مستقیماً پارامترهای آلودگی را می‌گیرد
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=european_aqi,pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            raw_data = response.json()['current']
            # تبدیل فرمت Open-Meteo به فرمتی که با دیتابیس قبلی ما سازگار باشد
            formatted_data = {
                'main': {'aqi': raw_data['european_aqi']},
                'components': {
                    'pm2_5': raw_data['pm2_5'],
                    'pm10': raw_data['pm10'],
                    'co': raw_data['carbon_monoxide'],
                    'no2': raw_data['nitrogen_dioxide'],
                    'o3': raw_data['ozone'],
                    'so2': raw_data['sulphur_dioxide']
                }
            }
            return formatted_data
        else:
            print(f"🚨 API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Connection Error: {e}")
        return None
def save_to_db(city_name, country, data):
    conn = get_db_connection()
    cur = conn.cursor()
    # استفاده از پارامتر (?) برای جلوگیری از حملات SQL Injection
    query = "INSERT INTO air_quality_data (city_name, country, aqi, pm2_5, pm10, co, no2, o3, so2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = (
        city_name, country, 
        data['main']['aqi'], 
        data['components']['pm2_5'], 
        data['components']['pm10'], 
        data['components']['co'], 
        data['components']['no2'], 
        data['components']['o3'], 
        data['components']['so2']
    )
    cur.execute(query, values)
    conn.commit()
    conn.close()
    print(f"✅ Data for {city_name} successfully saved at {datetime.now().strftime('%H:%M:%S')}")

def run_pipeline():
    """تابع اصلی برای مدیریت چرخه ETL"""
    print(f"🚀 Pipeline execution started... {datetime.now()}")
    init_db()
    cities = get_cities()
    
    # پیمایش روی لیست شهرها و دریافت اطلاعات تک‌تک آن‌ها
    for city in cities:
        air_data = fetch_air_quality(city['lat'], city['lon'])
        if air_data:
            save_to_db(city['name'], city['country'], air_data)
        else:
            print(f"❌ Failed to get data for {city['name']}")

if __name__ == "__main__":
    # نقطه شروع برنامه
    run_pipeline()
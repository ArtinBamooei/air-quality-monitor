import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# تنظیمات صفحه
st.set_page_config(page_title="Air Quality Monitor", layout="wide")

st.title("🌍 Air Quality Monitor Dashboard")
st.markdown("مقایسه لحظه‌ای کیفیت هوای شهرهای منتخب")

# اتصال به دیتابیس و خواندن داده‌ها
def load_data():
    conn = sqlite3.connect('air_quality.db')
    query = "SELECT * FROM air_quality_data ORDER BY timestamp DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

try:
    df = load_data()

    if not df.empty:
        # ۱. نمایش کارت‌های خلاصه (آخرین وضعیت تهران و برلین)
        col1, col2 = st.columns(2)
        
        latest_tehran = df[df['city_name'] == 'Tehran'].iloc[0]
        latest_berlin = df[df['city_name'] == 'Berlin'].iloc[0]
        
        col1.metric("Tehran AQI", int(latest_tehran['aqi']), delta="Polluted" if latest_tehran['aqi'] > 3 else "Good")
        col2.metric("Berlin AQI", int(latest_berlin['aqi']), delta="Clean" if latest_berlin['aqi'] < 2 else "Moderate")

        st.divider()

        # ۲. نمودار مقایسه‌ای ذرات معلق PM2.5
        st.subheader("📊 Comparison of PM2.5 (Dangerous Particles)")
        fig = px.bar(df.drop_duplicates('city_name'), x='city_name', y='pm2_5', 
                     color='city_name', title="Latest PM2.5 Levels by City")
        st.plotly_chart(fig, use_container_width=True)

        # ۳. نمایش جدول کامل داده‌ها
        st.subheader("📋 Raw Data from Database")
        st.dataframe(df)
        
    else:
        st.warning("دیتابیس خالی است. ابتدا فایل data_collector.py را اجرا کنید.")

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# تنظیمات صفحه - این بخش به پروژه هویت می‌دهد
st.set_page_config(page_title="Air Quality Monitor", layout="wide")

def get_data():
    conn = sqlite3.connect('air_quality.db')
    # خواندن داده‌ها و مرتب‌سازی بر اساس آخرین زمان ثبت شده
    df = pd.read_sql_query("SELECT * FROM air_quality_data ORDER BY timestamp DESC", conn)
    conn.close()
    return df

# هدر برنامه با استایل انسانی
st.title("🌍 Air Quality Comparison Dashboard")

df = get_data()

if not df.empty:
    # --- بخش سایدبار برای فیلتر کردن ---
    st.sidebar.header("Filter Options")
    
    # فیلتر کشور
    countries = ["All"] + list(df['country'].unique())
    selected_country = st.sidebar.selectbox("Select Country:", countries)
    
    # اعمال فیلتر روی دیتا
    filtered_df = df if selected_country == "All" else df[df['country'] == selected_country]
    
    # --- نمایش کارت‌های وضعیت (Metrics) ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Cities Tracked", len(filtered_df['city_name'].unique()))
    with col2:
        avg_aqi = round(filtered_df['aqi'].mean(), 1)
        st.metric("Average AQI", avg_aqi)
    with col3:
        st.info("AQI 1 is Good, 5 is Poor")

    # --- نمودار میله‌ای مقایسه‌ای ---
    st.subheader(f"Pollution Levels in {selected_country}")
    
    # انتخاب نوع آلاینده توسط کاربر
    pollutant = st.selectbox("Select Pollutant to Compare:", ["aqi", "pm2_5", "pm10", "co", "no2"])
    
    fig = px.bar(
        filtered_df.drop_duplicates(subset=['city_name']), # نمایش آخرین مقدار هر شهر
        x='city_name', 
        y=pollutant,
        color=pollutant,
        color_continuous_scale='RdYlGn_r', # سبز به قرمز (معکوس برای آلودگی)
        title=f"Comparison of {pollutant.upper()} across cities",
        labels={pollutant: pollutant.upper(), 'city_name': 'City'}
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- نمایش جدول داده‌های خام ---
    with st.expander("See Raw Data"):
        st.write(filtered_df)
else:
    st.warning("No data found! Please run the data collector first.")

# پانویس (Footer) برای شخصی‌سازی بیشتر
st.markdown("---")
st.caption("Developed by Artin BZ | Data source: Open-Meteo")
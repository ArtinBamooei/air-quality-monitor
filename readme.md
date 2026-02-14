# Urban Air Quality Monitor: Iran & Europe Comparison

A professional data engineering project that tracks and compares real-time air quality indices (AQI) between major cities in **Iran** (Tehran, Isfahan, Mashhad), **Germany** (Berlin, Munich, Hamburg), and **Austria** (Vienna, Salzburg).

This tool was developed to demonstrate a complete **ETL (Extract, Transform, Load)** pipeline, transitioning from raw API data to a polished, interactive analytics dashboard.



---

## Key Features

* **Automated ETL Pipeline**: Systematically fetches environmental data, cleans it, and stores it in a structured SQLite database.
* **Live Comparison Dashboard**: Built with Streamlit to provide side-by-side analysis of cities using dynamic filtering.
* **Smart API Integration**: Implemented with a fallback mechanism to switch between Open-Meteo and OpenWeather providers.
* **Scientific Visualization**: Utilizes Plotly for high-fidelity rendering of pollutant concentrations (PM2.5, PM10, CO, NO2, SO2).

## Tech Stack

* **Language**: Python 3.12
* **Data Handling**: Pandas (DataFrames) & SQLite (Persistence)
* **Visualization**: Plotly Express
* **Web Framework**: Streamlit
* **Environment**: Python-dotenv (Security)

---

## Installation & Usage

### 1. Setup Environment
Clone the repository and install the required dependencies:
```bash
pip install -r requirements.txt
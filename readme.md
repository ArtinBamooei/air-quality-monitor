```markdown
# 🌍 Air Quality Monitor Network (Luftqualitätsmonitor)

Ein Echtzeit-Daten-Engineering-Projekt, das Luftqualitätsdaten von wichtigen globalen Städten (Teheran, Berlin, Delhi usw.) über die OpenWeather-API abruft, speichert und visualisiert.

## 🚀 Überblick
Dieses Projekt demonstriert eine vollständige Daten-Pipeline (ETL):
1. **Extraktion (Extraction)**: Automatisierter Datenabruf von der OpenWeatherMap-API.
2. **Speicherung (Storage)**: Lokale persistente Speicherung mittels SQLite.
3. **Visualisierung (Visualization)**: Interaktives Web-Dashboard, erstellt mit Streamlit und Plotly.

## 🛠️ Tech Stack
* **Sprache**: Python 3.x
* **Datenerfassung**: Requests Library
* **Datenbank**: SQLite (SQL)
* **Dashboard**: Streamlit
* **Visualisierung**: Plotly Express
* **Umgebungsverwaltung**: Python-dotenv

## 📂 Projektstruktur
```text
air-quality-monitor/
├── config/
│   └── cities.json         # Liste der überwachten Städte
├── dashboard/
│   └── app.py              # Code für das Streamlit-Dashboard
├── src/
│   └── data_collector.py   # Haupt-ETL/Pipeline-Skript
├── .env                    # API-Schlüssel (nicht in Git enthalten)
├── .gitignore              # Ausschlussregeln für Git
├── air_quality.db          # SQLite Datenbank
└── requirements.txt        # Projektabhängigkeiten

```

## ⚙️ Installation & Setup

1. **Repository klonen**:
```bash
git clone [https://github.com/ArtinBamooei/air-quality-monitor.git](https://github.com/ArtinBamooei/air-quality-monitor.git)
cd air-quality-monitor

```


2. **Virtuelle Umgebung erstellen**:
```bash
python -m venv venv
source venv/Scripts/activate  # Unter Windows: venv\Scripts\activate

```


3. **Abhängigkeiten installieren**:
```bash
pip install -r requirements.txt

```


4. **Umgebungsvariablen**:
Erstellen Sie eine `.env`-Datei im Stammverzeichnis (oder im `config/` Ordner, falls angepasst) und fügen Sie Ihren API-Schlüssel hinzu:
```env
OPENWEATHER_API_KEY=ihr_api_schlüssel_hier

```



## 🏃 Ausführung

### Schritt 1: Daten sammeln

Führen Sie das Collector-Skript aus, um die neuesten Daten abzurufen:

```bash
python src/data_collector.py

```

### Schritt 2: Dashboard starten

Starten Sie das Dashboard zur Visualisierung:

```bash
streamlit run dashboard/app.py

```

## 📊 Features

* **Echtzeit-Metriken**: Anzeige des aktuellen AQI (Luftqualitätsindex).
* **Detaillierte Schadstoffe**: Vergleich von PM2.5, PM10, CO und NO2.
* **Datenpersistenz**: Historische Daten werden in SQLite gespeichert.
* **Benutzerfreundliche UI**: Interaktive Diagramme mit Plotly.

## 📈 Zukünftige Roadmap

* [ ] **Dockerisierung**: Containerisierung für einfachere Bereitstellung.
* [ ] **Zeitreihenanalyse**: Vorhersage von Verschmutzungstrends.
* [ ] **Cloud-Integration**: Migration der Datenbank zu AWS/Azure.

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

---

Erstellt von **Artin BamooeiZowj**

`

# Documentație Tehnică - Aplicație Predicție Calitate Aer

## Arhitectură Sistem

### Overview
Aplicația este structurată în trei componente principale:
1. **Data Collection** - Colectare și procesare date
2. **ML Model** - Antrenare și predicție
3. **Dashboard** - Interfață web interactivă

### Diagrama Fluxului de Date

```
┌──────────────┐     ┌──────────────┐
│  OpenAQ API  │────▶│     Data     │
└──────────────┘     │  Collection  │
                     │    Module    │
┌──────────────┐     │              │
│ Weather API  │────▶└──────┬───────┘
└──────────────┘            │
                            ▼
                     ┌─────────────┐
                     │   Training  │
                     │    Data     │
                     │   (CSV)     │
                     └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐
                     │  ML Model   │
                     │  Training   │
                     └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐     ┌──────────────┐
                     │   Trained   │────▶│   Streamlit  │
                     │    Model    │     │   Dashboard  │
                     └─────────────┘     └──────────────┘
```

## Module Detaliate

### 1. Data Collection Module (`data_collection.py`)

#### Clasa DataCollector

**Responsabilități:**
- Colectare date PM2.5 din OpenAQ API
- Colectare date meteo din OpenWeatherMap API
- Generare date simulate (fallback)
- Creare dataset de antrenare

**Metode Principale:**

##### `get_air_quality_data(days: int) -> pd.DataFrame`
Colectează date PM2.5 pentru un număr specificat de zile.

**Parametri:**
- `days`: Număr de zile în trecut

**Returns:**
- DataFrame cu coloane: timestamp, pm25, location, city, country

**API Call:**
```python
GET https://api.openaq.org/v2/measurements
?country=RO
&city=Bucharest
&parameter=pm25
&date_from=2025-12-07T00:00:00
&date_to=2026-01-06T00:00:00
&limit=10000
```

##### `get_weather_data(timestamp: datetime) -> Dict`
Obține date meteo pentru un timestamp specific.

**Returns:**
```python
{
    'temperature': 15.5,      # °C
    'humidity': 65.0,         # %
    'pressure': 1013.0,       # hPa
    'wind_speed': 3.5,        # m/s
    'wind_direction': 180.0,  # grade
    'clouds': 50.0            # %
}
```

##### `create_training_dataset(days: int, output_file: str) -> pd.DataFrame`
Creează dataset complet pentru antrenare.

**Proces:**
1. Colectează date PM2.5
2. Pentru fiecare timestamp, adaugă date meteo
3. Adaugă features temporale (hour, day_of_week, month)
4. Salvează în CSV

**Output CSV Columns:**
- timestamp, pm25, location, city, country
- temperature, humidity, pressure, wind_speed, wind_direction, clouds
- hour, day_of_week, month

### 2. ML Model Module (`model.py`)

#### Clasa PM25Predictor

**Algorithm:** Random Forest Regressor (scikit-learn)

**Features (9 total):**
- Meteo: temperature, humidity, pressure, wind_speed, wind_direction, clouds
- Temporale: hour, day_of_week, month

**Target:** pm25 (μg/m³)

**Metode Principale:**

##### `train(data_path: str)`
Antrenează modelul pe date.

**Proces:**
1. Încarcă date din CSV
2. Elimină valori lipsă
3. Normalizează features cu StandardScaler
4. Split train/test (80/20)
5. Antrenează Random Forest
6. Evaluează performanță
7. Salvează model

**Hyperparametri:**
```python
RandomForestRegressor(
    n_estimators=100,        # Număr arbori
    max_depth=15,           # Adâncime maximă
    min_samples_split=5,    # Min samples pentru split
    min_samples_leaf=2,     # Min samples în frunze
    random_state=42,        # Reproducibilitate
    n_jobs=-1               # Paralelizare
)
```

##### `predict(weather_data: Dict) -> float`
Prezice PM2.5 pentru condiții meteo date.

**Input:**
```python
{
    'temperature': 22.5,
    'humidity': 65.0,
    'pressure': 1013.0,
    'wind_speed': 3.5,
    'wind_direction': 180.0,
    'clouds': 40.0,
    'hour': 14,
    'day_of_week': 2,
    'month': 1
}
```

**Returns:** Valoare PM2.5 prezisă (≥ 0)

##### `predict_next_24h(current_weather: Dict) -> pd.DataFrame`
Generează predicții orare pentru 24h.

**Returns DataFrame:**
```
timestamp           | pm25_predicted | temperature | humidity | wind_speed
2026-01-06 10:00:00 | 25.5          | 22.5        | 65.0     | 3.5
2026-01-06 11:00:00 | 27.2          | 23.1        | 63.5     | 3.7
...
```

**Feature Engineering:**
- Simulează variații meteo realiste
- Trend ciclic temperatură (sinusoidal)
- Variații umiditate inverse cu temperatura
- Noise gaussian pentru realism

##### `_evaluate_model(X_train, y_train, X_test, y_test)`
Evaluează performanța modelului.

**Metrici Calculare:**

1. **RMSE (Root Mean Square Error)**
   ```
   RMSE = sqrt(mean((y_pred - y_true)²))
   ```
   - Penalizează mai mult erorile mari
   - În aceleași unități ca target (μg/m³)

2. **MAE (Mean Absolute Error)**
   ```
   MAE = mean(|y_pred - y_true|)
   ```
   - Eroare medie absolută
   - Mai robustă la outlieri

3. **R² Score (Coefficient of Determination)**
   ```
   R² = 1 - (SS_res / SS_tot)
   ```
   - Proporția varianței explicate
   - Interval: [-∞, 1], optim = 1

**Feature Importance:**
- Calculată din Random Forest
- Normalizată la sum = 1.0
- Indică contribuția fiecărui feature

### 3. Dashboard Module (`app.py`)

#### Arhitectură Streamlit

**Layout:**
- Sidebar: Setări și info proiect
- Main area: 4 tabs (Predicții, Date Istorice, Analiză, Despre)

**State Management:**
- `st.session_state['predictions']`: Predicții generate
- `st.session_state['current_weather']`: Date meteo curente
- `st.session_state['historical_data']`: Date istorice

**Funcții Principale:**

##### `get_aqi_category(pm25: float) -> tuple`
Clasifică PM2.5 conform EPA standards.

**Categories:**
| Range (μg/m³) | Category | Color |
|---------------|----------|-------|
| 0-12 | Bună | Verde |
| 12-35.4 | Moderată | Galben |
| 35.4-55.4 | Nesănătoasă (sensibili) | Portocaliu |
| 55.4-150.4 | Nesănătoasă | Roșu |
| 150.4-250.4 | Foarte nesănătoasă | Mov |
| 250.4+ | Periculoasă | Maro |

##### `plot_24h_prediction(predictions_df: pd.DataFrame)`
Creează grafic Plotly pentru predicții 24h.

**Features:**
- Linie cu markere pentru predicții
- Zone colorate pentru categorii AQI
- Hover interactiv
- Responsive design

##### `plot_historical_data(df: pd.DataFrame)`
Grafic pentru date istorice PM2.5.

##### `plot_weather_correlation(df: pd.DataFrame)`
Scatter plot pentru corelație PM2.5 vs factori meteo.

## API Integration

### OpenAQ API v2

**Endpoint:** `https://api.openaq.org/v2/measurements`

**Parametri:**
- `country`: Cod țară (ex: RO)
- `city`: Nume oraș
- `parameter`: pm25
- `date_from`: ISO 8601 format
- `date_to`: ISO 8601 format
- `limit`: Max results (10000)

**Response Format:**
```json
{
  "meta": {...},
  "results": [
    {
      "date": {
        "utc": "2026-01-06T10:00:00.000Z"
      },
      "value": 25.5,
      "parameter": "pm25",
      "location": "Station Name",
      "city": "Bucharest",
      "country": "RO"
    }
  ]
}
```

**Rate Limits:** 
- Free tier: unlimited pentru v2
- Delay recomandat: 100ms între requests

### OpenWeatherMap API

**Endpoint:** `https://api.openweathermap.org/data/2.5/weather`

**Parametri:**
- `lat`: Latitudine
- `lon`: Longitudine
- `appid`: API key
- `units`: metric

**Response Format:**
```json
{
  "main": {
    "temp": 15.5,
    "humidity": 65,
    "pressure": 1013
  },
  "wind": {
    "speed": 3.5,
    "deg": 180
  },
  "clouds": {
    "all": 50
  }
}
```

**Rate Limits:**
- Free tier: 60 calls/minute
- 1,000,000 calls/month

## Performanță Model

### Metrici Așteptate (Date Simulate)

**Training Set:**
- RMSE: 5-10 μg/m³
- MAE: 4-8 μg/m³
- R²: 0.85-0.95

**Test Set:**
- RMSE: 8-12 μg/m³
- MAE: 6-10 μg/m³
- R²: 0.75-0.90

### Feature Importance (Typic)

1. **hour** (25-30%): Variație diurnă PM2.5
2. **temperature** (20-25%): Influență termică
3. **humidity** (15-20%): Acumulare particule
4. **wind_speed** (10-15%): Dispersie particule
5. **pressure** (8-12%): Stabilitate atmosferică
6. Altele (10-15%)

## Optimizări și Îmbunătățiri Viitoare

### Optimizări Cod
1. **Caching**: Implementare `@st.cache_data` pentru date istorice
2. **Async API calls**: Folosire `asyncio` pentru requests paralele
3. **Database**: Migrare de la CSV la SQLite/PostgreSQL

### Îmbunătățiri Model
1. **Ensemble**: Combinare Random Forest + XGBoost
2. **Deep Learning**: LSTM pentru serii temporale
3. **More Features**: 
   - Trafic rutier
   - Industrie locală
   - Evenimente (sărbători)
4. **Hyperparameter Tuning**: GridSearchCV/RandomizedSearchCV

### Dashboard Features
1. **Notificări**: Alerte când PM2.5 > prag
2. **Export**: Download predicții CSV/PDF
3. **Comparare**: Locații multiple
4. **Istoricul Acurateței**: Track predicții vs realitate

## Securitate

### API Keys
- Stocate în `.env` (nu în git)
- Validare la runtime
- Fallback la date simulate

### Data Privacy
- Nu se stochează date personale
- Date publice (OpenAQ, OpenWeatherMap)

## Testing Strategy

### Unit Tests
- Test fiecare metodă individual
- Mock API calls
- Fixtures pentru date

### Integration Tests
- Test workflow complet
- Verificare date → model → predicție

### Performance Tests
- Benchmark training time
- Măsurare prediction latency

## Deployment

### Local
```bash
streamlit run src/app.py
```

### Streamlit Cloud
1. Push la GitHub
2. Connect repository la Streamlit Cloud
3. Set secrets (API keys)
4. Deploy

### Docker (opțional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "src/app.py"]
```

## Licență și Atribuiri

- **OpenAQ**: CC BY 4.0
- **OpenWeatherMap**: ODbL
- **Cod**: MIT License

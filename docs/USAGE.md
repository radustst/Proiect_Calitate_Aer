# Ghid de Utilizare - Aplicație Predicție Calitate Aer

## Introducere
Acest ghid descrie pașii necesari pentru utilizarea aplicației de predicție a calității aerului.

## Pregătire Mediu

### 1. Instalare Python
Asigurați-vă că aveți Python 3.8 sau superior instalat:
```bash
python --version
```

### 2. Creare Environment Virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instalare Dependențe
```bash
pip install -r requirements.txt
```

### 4. Configurare API Keys

#### 4.1. Copiere fișier .env
```bash
copy .env.example .env
```

#### 4.2. Obținere API Key OpenWeatherMap
1. Accesați [https://openweathermap.org/api](https://openweathermap.org/api)
2. Creați un cont gratuit
3. Generați un API key
4. Editați `.env` și adăugați cheia:
   ```
   WEATHER_API_KEY=vostra_cheie_aici
   ```

## Utilizare Aplicație

### Pasul 1: Colectare Date

Rulați scriptul de colectare date pentru a obține date istorice PM2.5 și meteo:

```bash
python src/data_collection.py
```

**Output așteptat:**
- Fișier `data/training_data.csv` cu date colectate
- Aproximativ 700+ înregistrări pentru 30 zile

**Parametri configurabili:**
- `days`: numărul de zile de date (modificați în cod)
- Locație: editați variabilele din `.env`

### Pasul 2: Antrenare Model

Antrenați modelul Random Forest pe datele colectate:

```bash
python src/model.py
```

**Output așteptat:**
- Model salvat în `models/pm25_model.joblib`
- Metrici de performanță afișate în terminal
- Fișier `models/pm25_model_metrics.json` cu statistici

**Metrici evaluate:**
- RMSE (Root Mean Square Error)
- MAE (Mean Absolute Error)
- R² Score

### Pasul 3: Rulare Dashboard

Porniți aplicația web Streamlit:

```bash
streamlit run src/app.py
```

**Acces aplicație:**
- URL: `http://localhost:8501`
- Browserul se va deschide automat

## Funcționalități Dashboard

### Tab 1: Predicții
- **Generează Predicție**: Click pentru a genera predicții PM2.5 pe 24h
- **Metrici afișate**: PM2.5 curent, medie, maxim, minim
- **Grafic interactiv**: Evoluție PM2.5 pe ore
- **Categorie calitate**: Culoare-codată conform EPA

### Tab 2: Date Istorice
- Selectați numărul de zile (1-30)
- Click "Încarcă Date Istorice"
- Vizualizați grafice și distribuții

### Tab 3: Analiză
- Corelații între PM2.5 și factori meteo
- Matrice de corelație
- Grafice scatter

### Tab 4: Despre
- Informații despre proiect
- Categorii calitate aer EPA
- Resurse și legături utile

## Testare

### Rulare Teste Unitare
```bash
pytest tests/ -v
```

### Teste Specifice
```bash
pytest tests/test_data_collection.py -v
pytest tests/test_model.py -v
pytest tests/test_integration.py -v
```

## Rezolvare Probleme

### Problema: "Model nu există"
**Soluție:** Rulați `python src/model.py` pentru a antrena modelul

### Problema: "Date lipsă"
**Soluție:** Rulați `python src/data_collection.py` pentru a colecta date

### Problema: "API Key invalid"
**Soluție:** 
1. Verificați că ați setat corect cheia în `.env`
2. Aplicația va folosi date simulate dacă API key-ul lipsește

### Problema: "Module not found"
**Soluție:** 
```bash
pip install -r requirements.txt
```

## Structura Date

### Format Date Antrenare (CSV)
```
timestamp,pm25,location,city,country,temperature,humidity,pressure,wind_speed,wind_direction,clouds,hour,day_of_week,month
2026-01-06 10:00:00,25.5,Station1,Bucharest,RO,15.3,65,1013,3.5,180,50,10,0,1
```

### Format Model Salvat
- **Fișier**: `models/pm25_model.joblib`
- **Conține**: model, scaler, feature_columns, metrici

## Best Practices

### Colectare Date
- Colectați minim 7 zile de date
- Pentru rezultate optime: 30 zile
- Re-colectați periodic pentru actualizare

### Antrenare Model
- Re-antrenați lunar cu date noi
- Monitorizați metricile de performanță
- Salvați versiuni diferite ale modelului

### Utilizare Dashboard
- Generați predicții în timpul zilei pentru acuratețe
- Comparați predicțiile cu realitatea
- Analizați corelațiile pentru înțelegere

## Integrare CI/CD

### GitHub Actions (opțional)
Creați `.github/workflows/test.yml`:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/
```

## Contribuții

Pentru contribuții la proiect:
1. Fork repository
2. Creați branch nou
3. Implementați modificări
4. Rulați teste
5. Creați Pull Request

## Resurse Adiționale

- [Streamlit Documentation](https://docs.streamlit.io/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [OpenAQ API Docs](https://docs.openaq.org/)
- [EPA Air Quality Index](https://www.airnow.gov/aqi/aqi-basics/)

## Contact

Pentru întrebări sau probleme:
- Berciu Antonio: colectare date
- Munteanu Radu: model predicție
- Roman Silviu: dashboard
- Student 4: documentare

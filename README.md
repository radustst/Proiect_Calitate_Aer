# Aplicație Web de Predicție a Calității Aerului

## Descriere
Aplicație web pentru predicția nivelului PM2.5 în următoarele 24 de ore, bazată pe date publice de la OpenAQ API și condiții meteo actuale.

## Echipa (Grupa 421 B)
- **Berciu Antonio** - Colectare date (data_collection.py)
- **Munteanu Radu** - Model de predicție (model.py)
- **Roman Silviu** - Vizualizare / Dashboard (app.py)
- **Student 4** - Documentare + Testare (docs/, tests/)

## Tehnologii
- **pandas** - Procesare și analiză date
- **scikit-learn** - Model de machine learning
- **Streamlit** - Dashboard interactiv
- **OpenAQ API** - Date calitate aer
- **OpenWeatherMap API** - Date meteo

## Instalare

### 1. Clonare repository
```bash
git clone <repository-url>
cd Proiect_Calitate_Aer
```

### 2. Creare environment virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# sau
source venv/bin/activate  # Linux/Mac
```

### 3. Instalare dependențe
```bash
pip install -r requirements.txt
```

### 4. Configurare variabile de mediu
```bash
copy .env.example .env
```
Editați `.env` și adăugați cheia API de la OpenWeatherMap (obținută gratuit de pe [openweathermap.org](https://openweathermap.org/api))

## Utilizare

### Colectare date
```bash
python src/data_collection.py
```

### Antrenare model
```bash
python src/model.py
```

### Rulare aplicație web
```bash
streamlit run src/app.py
```

Aplicația va fi disponibilă la `http://localhost:8501`

## Structura Proiectului
```
Proiect_Calitate_Aer/
├── src/
│   ├── data_collection.py  # Student 1: Colectare date
│   ├── model.py            # Student 2: Model predicție
│   └── app.py              # Student 3: Dashboard Streamlit
├── data/                   # Date colectate (generat)
├── models/                 # Modele antrenate (generat)
├── tests/                  # Teste unitare
├── docs/                   # Documentație
├── requirements.txt        # Dependențe Python
├── .env.example           # Template variabile mediu
└── README.md              # Acest fișier
```

## Funcționalități
- ✅ Colectare automată date PM2.5 din OpenAQ API
- ✅ Integrare date meteo (temperatură, umiditate, vânt, presiune)
- ✅ Model de predicție ML (Random Forest)
- ✅ Predicție PM2.5 pentru următoarele 24h
- ✅ Dashboard interactiv cu grafice
- ✅ Vizualizare date istorice
- ✅ Comparare predicții vs realitate

## Caracteristici Model
- **Algoritm**: Random Forest Regressor
- **Features**: temperatură, umiditate, presiune, viteză vânt, direcție vânt, ora zilei
- **Target**: PM2.5 (μg/m³)
- **Metrici**: RMSE, MAE, R²

## Licență
MIT License

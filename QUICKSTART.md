# Proiect Calitate Aer - Quick Start

## Instalare Rapidă

```bash
# 1. Clonare repository
git clone <repository-url>
cd Proiect_Calitate_Aer

# 2. Creare environment
python -m venv venv
venv\Scripts\activate

# 3. Instalare dependențe
pip install -r requirements.txt

# 4. Configurare .env
copy .env.example .env
# Editați .env și adăugați API key de pe openweathermap.org

# 5. Colectare date
python src/data_collection.py

# 6. Antrenare model
python src/model.py

# 7. Rulare aplicație
streamlit run src/app.py
```

## Acces Aplicație
Deschideți browser la: `http://localhost:8501`

## Testare
```bash
pytest tests/ -v
```

## Echipa
- Berciu Antonio - Data Collection
- Munteanu Radu - ML Model
- Roman Silviu - Dashboard
- Student 4 - Documentation & Testing

Pentru detalii complete, vezi [README.md](README.md)

# Contributing to Proiect Calitate Aer

## Bun venit!

Mulțumim pentru interesul de a contribui la proiectul de predicție a calității aerului!

## Cum să contribui

### 1. Fork și Clone
```bash
git clone https://github.com/your-username/Proiect_Calitate_Aer.git
cd Proiect_Calitate_Aer
```

### 2. Creează un Branch
```bash
git checkout -b feature/nume-feature
```

### 3. Modificări
- Respectă stilul de cod existent
- Adaugă comentarii pentru cod complex
- Actualizează documentația

### 4. Testare
```bash
pytest tests/ -v
```

### 5. Commit și Push
```bash
git add .
git commit -m "Descriere clară a modificărilor"
git push origin feature/nume-feature
```

### 6. Pull Request
- Deschide un Pull Request pe GitHub
- Descrie modificările în detaliu
- Referențiază issue-uri relevante

## Standarde Cod

### Python Style Guide
- Urmează PEP 8
- Folosește type hints unde este posibil
- Docstrings pentru toate funcțiile și clasele

### Exemplu:
```python
def calculate_aqi(pm25: float) -> tuple[str, str]:
    """
    Calculează categoria AQI pentru o valoare PM2.5.
    
    Args:
        pm25: Valoarea PM2.5 în μg/m³
        
    Returns:
        Tuple cu (categorie, culoare)
    """
    # Implementation
    pass
```

### Commit Messages
- Format: `tip: descriere scurtă`
- Tipuri: `feat`, `fix`, `docs`, `test`, `refactor`
- Exemple:
  - `feat: adaugă suport pentru predicții pe 48h`
  - `fix: corectare calcul RMSE`
  - `docs: actualizare README cu noi instrucțiuni`

## Raportare Probleme

### Bug Reports
Includeți:
- Descriere problemă
- Pași de reproducere
- Comportament așteptat vs actual
- Environment (Python version, OS)
- Screenshots (dacă aplicabil)

### Feature Requests
Includeți:
- Descriere feature
- Cazuri de utilizare
- Beneficii
- Implementare propusă (opțional)

## Development Setup

```bash
# Clone
git clone <repo-url>
cd Proiect_Calitate_Aer

# Virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest black flake8 mypy

# Run tests
pytest tests/ -v

# Format code
black src/ tests/

# Lint
flake8 src/ tests/
```

## Întrebări?

Contactați echipa:
- Berciu Antonio - Data Collection
- Munteanu Radu - ML Model
- Roman Silviu - Dashboard
- Student 4 - Documentation

Mulțumim pentru contribuție! 🎉

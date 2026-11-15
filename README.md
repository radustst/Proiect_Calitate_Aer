<div align="center">

# 🌍 Aplicație Web de Predicție a Calității Aerului

### Predicții PM2.5 pentru următoarele 24 de ore bazate pe Machine Learning

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B.svg)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.2-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Despre](#-despre-proiect) •
[Funcționalități](#-funcționalități) •
[Instalare](#-instalare) •
[Utilizare](#-utilizare) •
[Documentație](#-documentație) •
[Echipa](#-echipa)

</div>

---

## 📋 Despre Proiect

Aplicație web interactivă pentru **predicția nivelului PM2.5** (particule fine în aer) în următoarele 24 de ore, utilizând algoritmi de machine learning și date reale de la Open-Meteo Air Quality API (Copernicus CAMS) și Open-Meteo Weather API.

### 🎯 Scop

Să ofere informații precise despre calitatea aerului pentru a ajuta cetățenii să ia decizii informate despre activitățile lor zilnice și să își protejeze sănătatea.

### 🔬 Metodologie

- **Colectare Date**: Date PM2.5 reale din Open-Meteo Air Quality API (Copernicus CAMS) și date meteo reale din Open-Meteo
- **Model ML**: Random Forest Regressor cu 9 features
- **Predicție**: Forecast pentru următoarele 24 de ore
- **Vizualizare**: Dashboard interactiv Streamlit cu grafice Plotly

---

## ✨ Funcționalități

### 📊 Dashboard Interactiv
- ✅ Predicții PM2.5 pentru următoarele 24 de ore
- ✅ Vizualizare date în timp real cu grafice interactive
- ✅ Categorii calitate aer conform standardului EPA
- ✅ Indicatori meteo curenti (temperatură, umiditate, vânt)
- ✅ Analiză date istorice și statistici

### 🤖 Model Machine Learning
- ✅ Random Forest Regressor cu performanță ridicată
- ✅ Evaluare model (RMSE, MAE, R²)
- ✅ Feature importance analysis
- ✅ Predicții precise bazate pe date meteo

### 📈 Analiză și Raportare
- ✅ Corelație PM2.5 cu factori meteo
- ✅ Matrici de corelație
- ✅ Distribuții și histograme
- ✅ Export date și predicții

---

## 🛠️ Tehnologii

<div align="center">

| Categorie | Tehnologii |
|-----------|-----------|
| **Backend** | Python 3.8+, pandas, NumPy |
| **Machine Learning** | scikit-learn, Random Forest |
| **Frontend** | Streamlit, Plotly |
| **APIs** | Open-Meteo Air Quality (CAMS), Open-Meteo Weather, Open-Meteo Geocoding |
| **Testing** | pytest |
| **Version Control** | Git, GitHub |

</div>


## 🚀 Instalare

### Cerințe Sistem

- Python 3.8 sau mai recent
- pip (Python package manager)
- Git

### Pași de Instalare

#### 1️⃣ Clonare Repository

```bash
git clone https://github.com/your-username/Proiect_Calitate_Aer.git
cd Proiect_Calitate_Aer
```

#### 2️⃣ Creare Environment Virtual

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Instalare Dependențe

```bash
pip install -r requirements.txt
```

#### 4️⃣ Configurare Variabile de Mediu

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

> 🔑 **Nu este necesară nicio cheie API.** Toate datele vin de la [Open-Meteo](https://open-meteo.com/), gratuit. Fișierul `.env` este opțional și permite schimbarea orașului implicit.

## 💻 Utilizare

### Quick Start

Pentru a rula rapid aplicația:

```bash
# 1. Activează environment-ul virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Rulează aplicația
streamlit run src/app.py
```

🌐 Aplicația va fi disponibilă la **`http://localhost:8501`**

### Workflow Complet

#### 1️⃣ Colectare Date de Antrenare

```bash
python src/data_collection.py
```

Această comandă:
- Colectează date PM2.5 reale din Open-Meteo Air Quality API (ultimele 90 zile)
- Adaugă datele meteo reale din aceleași ore (Open-Meteo)
- Salvează dataset-ul în `data/training_data.csv`

#### 2️⃣ Antrenare Model

```bash
python src/model.py
```

Această comandă:
- Încarcă dataset-ul de antrenare
- Antrenează modelul Random Forest
- Evaluează performanța (RMSE, MAE, R²)
- Salvează modelul în `models/pm25_model.joblib`

#### 3️⃣ Rulare Dashboard

```bash
streamlit run src/app.py
```

Dashboard-ul oferă:
- 🔮 **Predicții**: Generează predicții pentru 24h
- 📈 **Date Istorice**: Vizualizează datele colectate
- 📊 **Analiză**: Corelații și statistici
- ℹ️ **Despre**: Informații despre proiect

### 🧪 Rulare Teste

```bash
# Rulează toate testele
pytest tests/ -v

# Rulează teste specifice
pytest tests/test_model.py -v

# Cu coverage
pytest tests/ --cov=src --cov-report=html
```

## 📁 Structura Proiectului

```
Proiect_Calitate_Aer/
│
├── 📂 src/                          # Cod sursă
│   ├── __init__.py                  # Package initialization
│   ├── data_collection.py           # 🔹 Modul colectare date (Student 1)
│   ├── model.py                     # 🔹 Modul ML predicție (Student 2)
│   └── app.py                       # 🔹 Dashboard Streamlit (Student 3)
│
├── 📂 tests/                        # Teste unitare și integrare
│   ├── __init__.py
│   ├── test_data_collection.py      # Teste colectare date
│   ├── test_model.py                # Teste model ML
│   └── test_integration.py          # Teste end-to-end
│
├── 📂 data/                         # Date (generat după rulare)
│   └── training_data.csv            # Dataset antrenare
│
├── 📂 models/                       # Modele antrenate (generat)
│   ├── pm25_model.joblib            # Model Random Forest
│   └── pm25_model_metrics.json      # Metrici performanță
│
├── 📂 docs/                         # Documentație tehnică
│   ├── TECHNICAL.md                 # Documentație tehnică
│   └── USAGE.md                     # Ghid utilizare
│
├── 📄 requirements.txt              # Dependențe Python
├── 📄 .env.example                  # Template variabile mediu
├── 📄 .gitignore                    # Git ignore rules
├── 📄 README.md                     # Acest fișier
├── 📄 QUICKSTART.md                 # Ghid rapid
├── 📄 CONTRIBUTING.md               # Ghid contribuții
├── 📄 CHANGELOG.md                  # Istoric versiuni
└── 📄 LICENSE                       # Licență MIT
```

---

## 🧠 Caracteristici Model

<div align="center">

| Aspect | Detalii |
|--------|---------|
| **Algoritm** | Random Forest Regressor |
| **Estimatori** | 100 arbori de decizie |
| **Features (9)** | temperatură, umiditate, presiune, viteză vânt, direcție vânt, nebulozitate, ora zilei, zi săptămână, lună |
| **Target** | PM2.5 (μg/m³) |
| **Validare** | Train/Test Split (80/20) |
| **Metrici** | RMSE, MAE, R² Score |
| **Performanță** | R² > 0.85 (pe date simulate) |

</div>

---

## 📊 Categorii Calitate Aer (EPA)

| PM2.5 (μg/m³) | Categorie | Descriere |
|---------------|-----------|-----------|
| 0-12 | 🟢 **Bună** | Calitatea aerului este satisfăcătoare |
| 12-35.4 | 🟡 **Moderată** | Calitate acceptabilă pentru majoritatea oamenilor |
| 35.4-55.4 | 🟠 **Nesănătoasă (sensibili)** | Grupuri sensibile pot fi afectate |
| 55.4-150.4 | 🔴 **Nesănătoasă** | Toată lumea poate fi afectată |
| 150.4-250.4 | 🟣 **Foarte nesănătoasă** | Avertisment pentru sănătate |
| 250.4+ | 🔴 **Periculoasă** | Alertă de sănătate |

---

## 📚 Documentație

- 📖 [Quick Start Guide](QUICKSTART.md) - Ghid rapid de început
- 🔧 [Technical Documentation](docs/TECHNICAL.md) - Documentație tehnică detaliată
- 📘 [Usage Guide](docs/USAGE.md) - Ghid complet de utilizare
- 🤝 [Contributing Guidelines](CONTRIBUTING.md) - Cum să contribui
- 📝 [Changelog](CHANGELOG.md) - Istoric versiuni
- 🗺️ [Roadmap](ROADMAP.md) - Planuri de dezvoltare viitoare
- 🛡️ [Security Policy](SECURITY.md) - Politică de securitate
- 📜 [Code of Conduct](CODE_OF_CONDUCT.md) - Cod de conduită

---

## 👥 Echipa

**Grupa 421 B - Proiect Calitate Aer**

| Student | Rol | Responsabilități |
|---------|-----|------------------|
| **Berciu Antonio** | Data Engineer | 📡 Colectare date PM2.5 & meteo, integrare API-uri |
| **Munteanu Radu** | ML Engineer | 🤖 Dezvoltare model Random Forest, evaluare performanță |
| **Roman Silviu** | Frontend Developer | 🎨 Dashboard Streamlit, vizualizări interactive |
| **Student 4** | QA & Documentation | 📝 Testare, documentație tehnică |

---

## 🤝 Contribuții

Contribuțiile sunt binevenite! Vă rugăm citiți [CONTRIBUTING.md](CONTRIBUTING.md) pentru detalii despre procesul nostru de contribuție.

### Cum să contribui:

1. 🍴 Fork repository-ul
2. 🌿 Creați un branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit modificările (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push pe branch (`git push origin feature/AmazingFeature`)
5. 🔄 Deschideți un Pull Request

---

## 📄 Licență

Acest proiect este licențiat sub **MIT License** - vezi fișierul [LICENSE](LICENSE) pentru detalii.

---

## 🙏 Mulțumiri

- **Open-Meteo** pentru API-urile gratuite de calitate a aerului, meteo și geocoding
- **Copernicus Atmosphere Monitoring Service (CAMS)** pentru datele PM2.5
- **Streamlit** pentru framework-ul de vizualizare
- **scikit-learn** pentru biblioteca de machine learning

---

## 📞 Contact & Suport

Dacă aveți întrebări sau sugestii:

- 📧 Email: radustmunteanu@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/radustst/Proiect_Calitate_Aer/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/radustst/Proiect_Calitate_Aer/discussions)

---

<div align="center">

**⭐ Dacă acest proiect v-a fost util, vă rugăm să-i dați o stea pe GitHub! ⭐**

Made with ❤️ by Echipa 421 B

</div>

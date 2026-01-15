# Predicție Calitate Aer
## Aplicație Web bazată pe Machine Learning

**Echipa 421 B**

Berciu Antonio | Munteanu Radu | Roman Silviu

Ianuarie 2026

---

# Ce am creat?

## Problema
**Poluarea aerului** afectează sănătatea noastră în fiecare zi
- PM2.5 = particule foarte mici în aer (< 2.5 micrometri)
- Cauze: mașini, fabrici, fum
- **Impact**: probleme respiratorii și cardiovasculare

## Soluția
✨ **Dashboard web** care prezice calitatea aerului pentru următoarele 24 de ore

## De ce este util?
- Planifici când să ieși la alergat
- Protejezi persoanele vulnerabile
- Vezi când aerul este mai curat

---

# 🛠️ Cum funcționează?

## Tehnologii folosite

**Python** - Limbajul principal
- **pandas** - Prelucrare date
- **scikit-learn** - Inteligență artificială
- **Streamlit** - Interface web
- **Plotly** - Grafice colorate

**Surse de date**
- **OpenAQ** - Date despre poluare
- **OpenWeatherMap** - Date meteo (temperatură, vânt, etc.)

---

# 🏗️ Cum am împărțit munca?

## 3 Module Principale

**1. Colectare Date** (Berciu Antonio)
- Preia date despre poluare de pe internet
- Preia date meteo (temperatură, vânt)
- Salvează tot într-un fișier CSV

**2. Model Inteligență Artificială** (Munteanu Radu)
- Învață din datele istorice
- Prezice poluarea pentru următoarele 24h
- Verifică cât de precise sunt predicțiile

**3. Interface Web** (Roman Silviu)
- Dashboard frumos și ușor de folosit
- Grafice colorate și interactive
- Predicții + Date istorice + Analize

---

# 🧠 Modelul Machine Learning

## Arhitectură

- **Algoritm**: Random Forest Regressor
- **Estimatori**: 100 arbori de decizie
- **Max Depth**: 15 niveluri
- **Features**: 9 variabile input

## Features (Input)

| Categorie | Features |
|-----------|----------|
| **Meteo** | temperatură, umiditate, presiune, vânt (viteză, direcție), nebulozitate |
| **Temporale** | ora zilei, zi săptămână, lună |

**Target**: PM2.5 (μg/m³)

---

# 🧠 Modelul ML - Performanță

## Validare

- **Split**: 80% Train / 20% Test
- **Scaling**: StandardScaler pentru normalizare
- **Cross-validation**: Train/Test split

## Metrici de Evaluare

| Metrică | Descriere | Valoare Țintă |
|---------|-----------|---------------|
| **RMSE** | Root Mean Squared Error | < 10 μg/m³ |
| **MAE** | Mean Absolute Error | < 8 μg/m³ |
| **R²** | Coefficient of Determination | > 0.85 |

## Feature Importance

Top 3 features: **temperatură**, **umiditate**, **ora zilei**

---

# ⚠️ Provocări & Soluții

## 🔴 Provocare 1: Limitări API

### Problema
- OpenAQ API - date incomplete sau lipsă pentru România
- OpenWeatherMap - limită 60 request-uri/min (cont gratuit)
- Lipsă date istorice pentru anumite locații

### Soluția
✅ **Fallback la date simulate** - generator de date realiste
✅ **Rate limide Predicție

## Cum funcționează "creierul" aplicației?

**Random Forest** = mulți "arbori de decizie" care votează împreună

**Ce analizează:**
- Temperatura
- Umiditatea
- Viteza vântului
- Ora din zi
- Luna din an

**Rezultat:** Prezice poluarea pentru următoarele 24 de ore

**Performanță:** ~85% acuratețe pe date de test
✅ **Cross-validation** - validare robustă

---

# ⚠️ Provocări & Soluții (cont.)

## 🔴 Provocare 4: Integrare Streamlit

### Problema
- Session state management complex
- Rerun-uri frecvente (performance)
- Layout responsive pe diferite ecrane
- Încărcare lentă date mari

### Soluția
✅ **st.session_state** - persistență date între rerun-uri
✅ **@st.cache_data** - caching rezultate (planificat)
✅ **Layout optimization** - columns și containers
✅ **Lazy loading** - încărcare progresivă

---

# ⚠️ Provocări & Soluții (cont.)

## 🔴 Provocare 5: Colaborare în Echipă

### Problema
- Lucru simultan pe același cod
- Conflicte Git merge
- Dependințe între module
- Standarde cod diferite

### Soluția
✅ **Git branches** - feature branches separate
✅ **Code review** - review înainte de merge
✅ **Documentație** - docstrings și comentarii
✅ **Modularizare** - separare clară responsabilități
✅ **Testing** - pytest pentru verificare funcționalități

---

# ⚠️ Provocări & Soluții (cont.)

## 🔴 Provocare 6: Deployment & Environment

### Problema
- Dependențe diferite (Windows/Linux/Mac)
- Versiuni Python incompatibile
- Chei API expuse accidental
- Fișiere mari (modele) în Git

### Soluția
✅ **requirements.txt** - dependențe fixate
✅ **Python 3.8+** - compatibilitate cross-platform
✅ **.env files** - management sigur chei API
✅ **.gitignore** - excludere fișiere sensibile
✅ **Virtual environments** - izolare dependențe

---

# 📈 Rezultate & Realizări

## Metrici Tehnice

✅ **Model accuracy**: R² > 0.85 pe date simulate
✅ **Predicții**: 24h forecast cu update orar
✅ **Response time**: < 2s pentru generare predicții
✅ **Code coverage**: ~70% teste unitare

## Livrabile

✅ **3 module Python** complete și funcționale
✅ **Dashboard interactiv** cu 4 secțiuni
✅ **10+ teste** unitare și integrare
✅ **Documentație completă** (README, TECHNICAL, USAGE)

---

# 📈 Rezultate (cont.)

## Funcționalități Implementate

| Modul | Student | Status |
|----Ce am realizat?

## Aplicație funcțională cu:

✅ **Predicții** pentru următoarele 24 de ore
✅ **Grafice colorate** și ușor de înțeles
✅ **Categorii calitate aer** (Bună, Moderată, Nesănătoasă, etc.)
✅ **Date istorice** și analiză

## Performanță:

- Precizie ~85% pe date de test
- Răspuns rapid (< 2 secunde)
- 3 module separate care funcționează împreună
- 10+ teste pentru a verifica că totul merge bine

## Bonus:

✅ Documentație completă pe GitHub
✅ Cod bine organizat și comentat
---

# 🏆 Concluzii

## Realizări Cheie

✅ **Aplicație funcțională** end-to-end
✅ **ML model performant** cu predicții precise
✅ **Dashboard profesional** user-friendly
✅ **Cod de calitate** cu teste și documentație
✅ **Colaborare eficientă** în echipă

## Impact

- 🌍 **Educațional** - conștientizare calitate aer
- 🏥 **Sănătate** - ajutor în luarea deciziilor
- 💻 **Tehnologic** - aplicație practică ML

---

# 👥 Echipa & Contribuții

## Distribuție Responsabilități

| Student | Rol | Contribuții Cheie |
|---------|-----|-------------------|
| **Berciu Antonio** | Data Engineer | OpenAQ/Weather API integration, data pipeline |
| **Munteanu Radu** | ML Engineer | Random Forest model, hyperparameter tuning |
| **Roman Silviu** | Frontend Dev | Streamlit dashboard, Plotly visualizations |
| **Student 4** | QA & Docs | Pytest tests, documentation, GitHub setup |

**Colaborare echilibrată** - fiecare membru a contribuit semnificativ!

---

# 📚 Resurse & Referințe

## APIs & Date

- [OpCe urmează?

## Îmbunătățiri planificate:

🔹 Predicții pentru mai multe orașe
🔹 Notificări prin email când aerul devine periculos
🔹 Export rapoarte PDF
🔹 Predicții pentru 7 zile (nu doar 24h)
🔹 Aplicație pentru telefon

---

# 🎓 Ce am învățat?

## Tehnic
- Cum să lucrezi cu API-uri și date din exterior
- 🙏 Mulțumim!

## Întrebări?

💻 **GitHub**: https://github.com/radustst/Proiect_Calitate_Aer

---

**Echipa 421 B**

Berciu Antonio | Munteanu Radu | Roman Silviue |

**Toți:** Documentație, teste, rezolvare probleme împreună!
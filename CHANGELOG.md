# Changelog

Toate modificările notabile ale acestui proiect vor fi documentate în acest fișier.

## [1.0.0] - 2026-01-06

### Adăugat
- Modul de colectare date (`data_collection.py`)
  - Integrare OpenAQ API pentru PM2.5
  - Integrare OpenWeatherMap API pentru date meteo
  - Generare date simulate pentru testare
  - Export date în format CSV

- Model de predicție (`model.py`)
  - Random Forest Regressor pentru predicție PM2.5
  - Normalizare features cu StandardScaler
  - Evaluare performanță (RMSE, MAE, R²)
  - Feature importance analysis
  - Salvare/încărcare model cu joblib
  - Predicție pentru 24h în avans

- Dashboard Streamlit (`app.py`)
  - Interfață web interactivă
  - 4 secțiuni principale: Predicții, Date Istorice, Analiză, Despre
  - Grafice interactive cu Plotly
  - Metrici în timp real
  - Categorii calitate aer conform EPA
  - Matrice de corelație

- Teste unitare și de integrare
  - `test_data_collection.py`: Teste pentru colectare date
  - `test_model.py`: Teste pentru model predicție
  - `test_integration.py`: Teste end-to-end

- Documentație
  - README.md cu ghid instalare și utilizare
  - USAGE.md cu instrucțiuni detaliate
  - TECHNICAL.md cu arhitectură și specificații tehnice
  - Comentarii inline în cod

- Configurare proiect
  - requirements.txt cu toate dependențele
  - .env.example pentru configurare API keys
  - .gitignore pentru fișiere excluse

### Features
- Predicție PM2.5 pentru următoarele 24 de ore
- Colectare automată date din surse publice
- Vizualizare date istorice
- Analiză corelații PM2.5 vs factori meteo
- Clasificare calitate aer conform EPA standards
- Suport pentru date simulate când API-urile nu sunt disponibile

### Performanță
- Model Random Forest cu R² > 0.75
- Timp predicție: < 100ms
- Timp antrenare: 10-30s (depinde de dataset)

## [Planificat pentru versiuni viitoare]

### [1.1.0]
- [ ] Implementare notificări pentru praguri PM2.5
- [ ] Export predicții în PDF
- [ ] Suport pentru multiple locații
- [ ] Îmbunătățire UI/UX dashboard

### [1.2.0]
- [ ] Model LSTM pentru serii temporale
- [ ] Ensemble models (Random Forest + XGBoost)
- [ ] Hyperparameter tuning automat
- [ ] Features adiționale (trafic, industrie)

### [2.0.0]
- [ ] API REST pentru predicții
- [ ] Bază de date PostgreSQL
- [ ] Autentificare utilizatori
- [ ] Deployment cloud (AWS/Azure/GCP)
- [ ] Mobile app (React Native)

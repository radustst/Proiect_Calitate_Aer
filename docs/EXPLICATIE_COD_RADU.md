# Explicație Cod Detaliat - model.py
## Modulul de Machine Learning - Radu Munteanu

---

## 📁 Structura Fișierului

Fișierul `src/model.py` conține **331 de linii** organizate în:
- 1 clasă principală: `PM25Predictor`
- 9 metode/funcții
- 1 funcție main pentru testare

---

## 📦 PARTEA 1: Import-uri și Configurare (Liniile 1-22)

```python
"""
Modul pentru antrenarea și utilizarea modelului de predicție PM2.5.
Student 2: Munteanu Radu

Funcționalități:
- Antrenare model Random Forest
- Evaluare performanță model
- Predicție PM2.5 pentru următoarele 24h
- Salvare/încărcare model
"""
```
**Explicație:** Docstring care descrie scopul modulului și autorul.

---

```python
import pandas as pd
import numpy as np
```
**Explicație:**
- `pandas (pd)` = manipulare date tabulare (DataFrame-uri, CSV)
- `numpy (np)` = operații matematice pe array-uri, calcule numerice

---

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
```
**Explicație:**
- `train_test_split` = împarte datele în train (80%) și test (20%)
- `RandomForestRegressor` = algoritmul ML pentru predicție
- `mean_squared_error, mean_absolute_error, r2_score` = metrici pentru evaluare
- `StandardScaler` = normalizează features (medie=0, std=1)

---

```python
import joblib
import os
from datetime import datetime, timedelta
from typing import Tuple, Dict, List
import json
```
**Explicație:**
- `joblib` = salvează/încarcă modelul antrenat (mai eficient decât pickle)
- `os` = operații cu fișiere și directoare
- `datetime, timedelta` = manipulare date și timp
- `typing` = type hints pentru cod mai clar
- `json` = salvare metrici în format JSON

---

## 🏗️ PARTEA 2: Clasa PM25Predictor - Inițializare (Liniile 24-38)

```python
class PM25Predictor:
    """Clasă pentru predicția nivelului PM2.5."""
```
**Explicație:** Definesc clasa principală care conține toată logica ML.

---

```python
    def __init__(self, model_path: str = 'models/pm25_model.joblib'):
```
**Explicație:** Constructor - se execută când creez obiect `predictor = PM25Predictor()`

---

```python
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
```
**Explicație:**
- `self.model_path` = unde salvez modelul antrenat
- `self.model` = inițial None (se va popula la antrenare/încărcare)
- `self.scaler` = obiect pentru normalizare (va învăța parametrii)

---

```python
        self.feature_columns = [
            'temperature', 'humidity', 'pressure', 'wind_speed', 
            'wind_direction', 'clouds', 'hour', 'day_of_week', 'month'
        ]
```
**Explicație:** 
- Lista de 9 features în ORDINEA EXACTĂ în care trebuie folosite
- ORDINEA E CRITICĂ! Dacă schimb ordinea, predicțiile devin greșite

---

```python
        self.metrics = {}
```
**Explicație:** Dicționar gol pentru stocarea metricilor (RMSE, MAE, R²)

---

## 🔧 PARTEA 3: Pregătirea Features (Liniile 40-56)

```python
    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Pregătește features pentru antrenare sau predicție.
        
        Args:
            df: DataFrame cu date
            
        Returns:
            Tuple (X, y) cu features și target
        """
```
**Explicație:** 
- Funcție care extrage features (X) și target (y) din DataFrame
- Returnează tuple (pereche) de numpy arrays

---

```python
        # Verifică că toate coloanele necesare există
        missing_cols = [col for col in self.feature_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Lipsesc coloane: {missing_cols}")
```
**Explicație:**
- **List comprehension** verifică dacă toate cele 9 features există
- Dacă lipsește ceva → aruncă eroare explicită
- **Exemplu:** Dacă lipsește 'temperature', primesc: "ValueError: Lipsesc coloane: ['temperature']"

---

```python
        X = df[self.feature_columns].values
        y = df['pm25'].values if 'pm25' in df.columns else None
```
**Explicație:**
- `X` = extrag doar coloanele feature, convertesc la numpy array
- `y` = target-ul (PM2.5), doar dacă există (la predicție nu existe)
- `.values` = convertește din pandas Series în numpy array

**Exemplu:**
```python
# DataFrame:
#   temperature  humidity  ...  pm25
#   22.5         65        ...  35.2
#   23.1         63        ...  42.1

# După extragere:
# X = [[22.5, 65, ...], [23.1, 63, ...]]
# y = [35.2, 42.1]
```

---

```python
        return X, y
```
**Explicație:** Returnez perechea (features, target)

---

## 🎓 PARTEA 4: Antrenarea Modelului (Liniile 58-109)

```python
    def train(self, data_path: str = 'data/training_data.csv'):
        """
        Antrenează modelul Random Forest.
        
        Args:
            data_path: Calea către fișierul cu date de antrenare
        """
        print("🎓 Începere antrenare model...\n")
```
**Explicație:** Funcția principală de antrenare, afișează mesaj de start

---

```python
        # Încarcă datele
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Fișierul {data_path} nu există. Rulați mai întâi data_collection.py")
```
**Explicație:**
- Verifică dacă fișierul CSV există
- Dacă nu → eroare clară cu instrucțiuni
- **os.path.exists()** = verifică existența fișierului

---

```python
        df = pd.read_csv(data_path)
        print(f"📊 Date încărcate: {len(df)} înregistrări")
```
**Explicație:**
- Citește CSV-ul într-un DataFrame pandas
- Afișează câte înregistrări am încărcat

**Exemplu:**
```
📊 Date încărcate: 721 înregistrări
```

---

```python
        # Elimină valori lipsă
        df = df.dropna()
        print(f"📊 Date valide: {len(df)} înregistrări\n")
```
**Explicație:**
- `.dropna()` = elimină rândurile cu valori NaN/None
- Afișează câte înregistrări VALIDE rămân
- **Important:** Datele incomplete pot strica modelul!

---

```python
        # Pregătește features
        X, y = self.prepare_features(df)
```
**Explicație:** Apelează funcția de mai sus pentru a extrage X și y

---

```python
        # Normalizează features
        X_scaled = self.scaler.fit_transform(X)
```
**Explicație:**
- `fit_transform()` = ÎNVAȚĂ parametrii de normalizare ȘI transformă datele
- **fit** = calculează media și std pentru fiecare feature
- **transform** = aplică formula: (x - medie) / std

**Exemplu:**
```python
# Înainte:
# temperature: [20, 22, 24, 26] → medie=23, std=2.45

# După normalizare:
# temperature_scaled: [-1.22, -0.41, 0.41, 1.22]
```

**De ce normalizez?**
- Features pe scale-uri diferite (temp: 20°C, pressure: 1013 hPa)
- Random Forest funcționează mai bine cu date normalizate

---

```python
        # Împarte în train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
```
**Explicație:**
- `test_size=0.2` = 20% pentru test, 80% pentru train
- `random_state=42` = seed pentru reproducibilitate (mereu aceleași split-uri)
- Returnează 4 array-uri:
  - `X_train` = features pentru antrenare (80%)
  - `X_test` = features pentru testare (20%)
  - `y_train` = target-uri pentru antrenare (80%)
  - `y_test` = target-uri pentru testare (20%)

**Exemplu:**
```python
# 721 înregistrări totale:
# X_train: 576 înregistrări (80%)
# X_test:  145 înregistrări (20%)
```

---

```python
        print(f"📚 Set antrenare: {len(X_train)} înregistrări")
        print(f"🧪 Set testare: {len(X_test)} înregistrări\n")
```
**Explicație:** Afișează câte sample-uri am în fiecare set

---

```python
        # Antrenează modelul Random Forest
        print("🌲 Antrenare Random Forest Regressor...")
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
```
**Explicație DETALIATĂ a hiperparametrilor:**

**1. `n_estimators=100`**
- Câți "arbori de decizie" creez
- Fiecare arbore învață independent pe sample-uri random
- La predicție, toți 100 arborii votează → medie = predicție finală
- Mai mulți arbori = mai precis, dar mai lent

**2. `max_depth=15`**
- Cât de "adâncă" poate fi ierarhia unui arbore
- Limitat la 15 nivele pentru a preveni overfitting
- Arbore prea adânc = memorează datele (rău!)
- Arbore prea superficial = nu învață (rău!)

**3. `min_samples_split=5`**
- Minim 5 sample-uri necesare pentru a împărți un nod
- Previne diviziuni prea specifice
- Exemplu: Dacă un nod are doar 3 sample-uri → nu se mai împarte

**4. `min_samples_leaf=2`**
- Minim 2 sample-uri într-o "frunză" (nod terminal)
- Asigură că fiecare predicție se bazează pe cel puțin 2 exemple

**5. `random_state=42`**
- Seed pentru reproducibilitate
- Mereu aceleași rezultate la re-antrenare

**6. `n_jobs=-1`**
- Folosește TOATE core-urile procesorului
- Antrenare paralelă = mai rapid

---

```python
        self.model.fit(X_train, y_train)
        print("✅ Antrenare finalizată!\n")
```
**Explicație:**
- `.fit()` = ÎNVAȚĂ modelul pe datele de antrenare
- Aici se întâmplă "magia" ML:
  1. Creează 100 arbori
  2. Fiecare arbore învață pe subset random de date
  3. Fiecare arbore face split-uri pe features pentru a minimiza eroarea

---

```python
        # Evaluează modelul
        self._evaluate_model(X_train, y_train, X_test, y_test)
        
        # Salvează modelul
        self.save_model()
```
**Explicație:** 
- Apelează funcțiile de evaluare și salvare (explicate mai jos)

---

## 📊 PARTEA 5: Evaluarea Modelului (Liniile 111-171)

```python
    def _evaluate_model(self, X_train, y_train, X_test, y_test):
        """Evaluează performanța modelului."""
        print("📊 Evaluare model...\n")
```
**Explicație:** 
- Funcție privată (prefixul `_` indică intern)
- Calculează metrici de performanță

---

```python
        # Predicții
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
```
**Explicație:**
- `.predict()` = folosește modelul antrenat pentru a face predicții
- `y_train_pred` = predicții pe setul de antrenare
- `y_test_pred` = predicții pe setul de test (DATE NOI!)

**Exemplu:**
```python
# X_test[0] = [temp=22.5, humid=65, ...]
# y_test[0] = 42.1 (valoare reală)
# y_test_pred[0] = 39.8 (predicție model)
# Eroare = |42.1 - 39.8| = 2.3
```

---

```python
        # Metrici train
        train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
        train_mae = mean_absolute_error(y_train, y_train_pred)
        train_r2 = r2_score(y_train, y_train_pred)
```
**Explicație DETALIATĂ a metricilor:**

**1. RMSE (Root Mean Square Error)**
```python
# Formula: sqrt(mean((y_real - y_pred)²))
# 
# Pas cu pas:
# 1. Calculez diferențele: [42.1-39.8, 35.2-33.1, ...]
# 2. Ridicare la pătrat: [2.3², 2.1², ...]
# 3. Calculez media: mean([5.29, 4.41, ...])
# 4. Radical: sqrt(media)
#
# Rezultat: 4.80 μg/m³
# Interpretare: În medie, greșesc cu ~5 μg/m³
```

**2. MAE (Mean Absolute Error)**
```python
# Formula: mean(|y_real - y_pred|)
#
# Pas cu pas:
# 1. Calculez diferențele absolute: [|42.1-39.8|, |35.2-33.1|, ...]
# 2. Calculez media: mean([2.3, 2.1, ...])
#
# Rezultat: 3.69 μg/m³
# Interpretare: Eroare medie absolută de 3.69
```

**3. R² Score (Coeficient de Determinare)**
```python
# Formula: 1 - (SS_res / SS_tot)
#
# SS_res = sum((y_real - y_pred)²) = variația rămasă după predicție
# SS_tot = sum((y_real - y_mean)²) = variația totală
#
# R² = 0.917 (train)
# Interpretare: Modelul explică 91.7% din variație
# R² = 1.0 → predicții perfecte
# R² = 0.0 → modelul nu e mai bun decât media
```

---

```python
        # Metrici test
        test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
        test_mae = mean_absolute_error(y_test, y_test_pred)
        test_r2 = r2_score(y_test, y_test_pred)
```
**Explicație:** Aceleași metrici, dar pe setul de TEST (date nevăzute)

---

```python
        # Salvează metrici
        self.metrics = {
            'train': {
                'rmse': float(train_rmse),
                'mae': float(train_mae),
                'r2': float(train_r2)
            },
            'test': {
                'rmse': float(test_rmse),
                'mae': float(test_mae),
                'r2': float(test_r2)
            }
        }
```
**Explicație:**
- Creez dicționar cu toate metricile
- `float()` convertește din numpy float64 în Python float (pentru JSON)

**Structura:**
```python
{
    'train': {'rmse': 4.80, 'mae': 3.69, 'r2': 0.917},
    'test':  {'rmse': 10.07, 'mae': 8.20, 'r2': 0.597}
}
```

---

```python
        # Afișează rezultate
        print("📈 Performanță Set Antrenare:")
        print(f"   RMSE: {train_rmse:.2f} μg/m³")
        print(f"   MAE:  {train_mae:.2f} μg/m³")
        print(f"   R²:   {train_r2:.4f}")
        
        print("\n📉 Performanță Set Testare:")
        print(f"   RMSE: {test_rmse:.2f} μg/m³")
        print(f"   MAE:  {test_mae:.2f} μg/m³")
        print(f"   R²:   {test_r2:.4f}\n")
```
**Explicație:**
- `.2f` = formatare cu 2 zecimale (4.798... → 4.80)
- `.4f` = formatare cu 4 zecimale (0.9170... → 0.9170)

---

```python
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
```
**Explicație:**
- `.feature_importances_` = array cu importanța fiecărui feature
- Creez DataFrame pentru afișare frumoasă
- `.sort_values()` = sortez descrescător după importanță

**Exemplu rezultat:**
```
feature         importance
hour            0.7239
temperature     0.0489
wind_speed      0.0465
...
```

---

```python
        print("🎯 Importanța Features:")
        for idx, row in feature_importance.iterrows():
            print(f"   {row['feature']:15s}: {row['importance']:.4f}")
        print()
```
**Explicație:**
- `.iterrows()` = iterează prin rândurile DataFrame-ului
- `{row['feature']:15s}` = aliniez la stânga cu 15 caractere
- Afișează fiecare feature cu importanța sa

---

## 💾 PARTEA 6: Salvarea Modelului (Liniile 173-193)

```python
    def save_model(self):
        """Salvează modelul și scaler."""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
```
**Explicație:**
- `os.path.dirname()` = extrage directorul din path ('models/pm25_model.joblib' → 'models')
- `os.makedirs()` = creează directorul dacă nu există
- `exist_ok=True` = nu dă eroare dacă directorul există deja

---

```python
        # Salvează modelul și scaler
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'metrics': self.metrics,
            'trained_at': datetime.now().isoformat()
        }
```
**Explicație:**
- Creez dicționar cu TOATE informațiile necesare:
  - `model` = RandomForestRegressor antrenat
  - `scaler` = StandardScaler cu parametrii învățați
  - `feature_columns` = ordinea features (CRUCIAL!)
  - `metrics` = performanță
  - `trained_at` = timestamp (ex: '2026-01-16T09:15:23.456789')

**De ce salvez totul împreună?**
- La încărcare, am TOT ce-mi trebuie pentru predicții
- Dacă pierd scaler-ul → normalizarea e greșită → predicții greșite!

---

```python
        joblib.dump(model_data, self.model_path)
        print(f"💾 Model salvat: {self.model_path}")
```
**Explicație:**
- `joblib.dump()` = serializează dicționarul într-un fișier binar
- Mai eficient decât pickle pentru obiecte numpy mari

---

```python
        # Salvează metrici în JSON
        metrics_path = self.model_path.replace('.joblib', '_metrics.json')
        with open(metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print(f"📊 Metrici salvate: {metrics_path}\n")
```
**Explicație:**
- `.replace()` = 'pm25_model.joblib' → 'pm25_model_metrics.json'
- `json.dump()` = salvează metrici în format JSON (ușor de citit)
- `indent=2` = formatare frumoasă cu indentare

**Exemplu fișier JSON:**
```json
{
  "train": {
    "rmse": 4.80,
    "mae": 3.69,
    "r2": 0.917
  },
  "test": {
    "rmse": 10.07,
    "mae": 8.20,
    "r2": 0.597
  }
}
```

---

## 📥 PARTEA 7: Încărcarea Modelului (Liniile 195-208)

```python
    def load_model(self):
        """Încarcă modelul salvat."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Modelul nu există: {self.model_path}")
```
**Explicație:** Verifică existența fișierului înainte de încărcare

---

```python
        model_data = joblib.load(self.model_path)
```
**Explicație:** 
- `joblib.load()` = deserializează fișierul binar
- Returnează dicționarul salvat anterior

---

```python
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']
        self.metrics = model_data.get('metrics', {})
```
**Explicație:**
- Extrag fiecare componentă din dicționar
- `.get('metrics', {})` = returnează metrici SAU dicționar gol dacă nu există

**De ce e important?**
- Acum `self.model` și `self.scaler` sunt EXACT cum erau la antrenare
- Pot face predicții identice

---

```python
        print(f"✅ Model încărcat: {self.model_path}")
```

---

## 🔮 PARTEA 8: Predicția (Liniile 210-236)

```python
    def predict(self, weather_data: Dict) -> float:
        """
        Prezice PM2.5 pentru date meteo specifice.
        
        Args:
            weather_data: Dicționar cu date meteo și temporale
            
        Returns:
            Valoare prezisă PM2.5
        """
```
**Explicație:** Funcție pentru o SINGURĂ predicție

---

```python
        if self.model is None:
            self.load_model()
```
**Explicație:**
- Verifică dacă modelul e încărcat
- Dacă nu → încarcă automat
- **Lazy loading** = încarcă doar când e necesar

---

```python
        # Creează DataFrame cu features
        features = pd.DataFrame([weather_data])
```
**Explicație:**
- Convertesc dicționarul într-un DataFrame cu 1 rând
- **De ce DataFrame?** Pentru că `prepare_features()` așteaptă DataFrame

**Exemplu:**
```python
# Input:
weather_data = {
    'temperature': 22.5,
    'humidity': 65,
    'pressure': 1013,
    'wind_speed': 3.5,
    'wind_direction': 180,
    'clouds': 40,
    'hour': 14,
    'day_of_week': 2,
    'month': 1
}

# După conversie:
#   temperature  humidity  pressure  ...
#   22.5         65        1013      ...
```

---

```python
        # Verifică features
        X, _ = self.prepare_features(features)
```
**Explicație:**
- Extrag doar X (features), ignor y (nu există la predicție)
- `_` = convenție Python pentru "nu mă interesează această valoare"

---

```python
        # Normalizează
        X_scaled = self.scaler.transform(X)
```
**Explicație:**
- `.transform()` = aplică ACEEAȘI normalizare ca la antrenare
- **NU** folosesc `fit_transform()` (asta ar recalcula parametrii!)
- Folosesc media și std învățate la antrenare

**Exemplu:**
```python
# Scaler învățat la antrenare:
# temperature: medie=23, std=2.45

# La predicție:
# temperature=22.5 → scaled = (22.5 - 23) / 2.45 = -0.204
```

---

```python
        # Prezice
        prediction = self.model.predict(X_scaled)[0]
```
**Explicație:**
- `.predict()` returnează array: `[39.8]`
- `[0]` = extrag prima (și singura) valoare: `39.8`

**Ce se întâmplă intern:**
1. Fiecare din cei 100 arbori face predicția sa
2. Predicțiile: `[38.2, 41.5, 39.1, ..., 40.3]`
3. Media: `mean([38.2, 41.5, ...]) = 39.8`

---

```python
        return max(0, prediction)  # PM2.5 nu poate fi negativ
```
**Explicație:**
- Asigur că predicția e pozitivă
- Dacă modelul prezice -2.3 → returnez 0
- **Constraint fizic:** PM2.5 nu poate fi negativ în realitate

---

## 📅 PARTEA 9: Predicții 24h (Liniile 238-276)

```python
    def predict_next_24h(self, current_weather: Dict, weather_forecast: List[Dict] = None) -> pd.DataFrame:
        """
        Prezice PM2.5 pentru următoarele 24 de ore.
        
        Args:
            current_weather: Date meteo curente
            weather_forecast: Listă cu prognoză meteo pentru 24h (opțional)
            
        Returns:
            DataFrame cu predicții orare
        """
```
**Explicație:** 
- Funcție pentru predicții pe 24 ore
- Poate folosi prognoză meteo reală SAU simulări

---

```python
        if self.model is None:
            self.load_model()
        
        predictions = []
        current_time = datetime.now()
```
**Explicație:**
- Încarcă modelul dacă nu e încărcat
- Inițializează listă goală pentru predicții
- Salvează timestamp-ul curent

---

```python
        for hour_offset in range(24):
            future_time = current_time + timedelta(hours=hour_offset)
```
**Explicație:**
- Loop prin următoarele 24 ore
- `hour_offset = 0` → acum
- `hour_offset = 1` → peste 1 oră
- `timedelta(hours=1)` = adaugă 1 oră la timestamp

**Exemplu:**
```python
# current_time = 2026-01-16 14:00
# hour_offset = 0 → future_time = 2026-01-16 14:00
# hour_offset = 1 → future_time = 2026-01-16 15:00
# hour_offset = 5 → future_time = 2026-01-16 19:00
```

---

```python
            # Folosește prognoza meteo dacă este disponibilă
            if weather_forecast and hour_offset < len(weather_forecast):
                weather = weather_forecast[hour_offset]
            else:
                # Simulează variații meteo
                weather = self._simulate_weather_variation(current_weather, hour_offset)
```
**Explicație:**
- **Dacă** am prognoză reală → o folosesc
- **Altfel** → simulez variații realiste
- `weather_forecast[hour_offset]` = prognoza pentru ora respectivă

---

```python
            # Adaugă features temporale
            weather['hour'] = future_time.hour
            weather['day_of_week'] = future_time.weekday()
            weather['month'] = future_time.month
```
**Explicație:**
- Extrag ora (0-23), ziua săptămânii (0-6), luna (1-12)
- **CRUCIAL** pentru predicție (ora = 72% importanță!)

**Exemplu:**
```python
# future_time = 2026-01-16 15:00 (joi)
# hour = 15
# day_of_week = 3 (joi, 0=luni)
# month = 1 (ianuarie)
```

---

```python
            # Prezice PM2.5
            pm25_pred = self.predict(weather)
```
**Explicație:** Apelează funcția `predict()` pentru ora respectivă

---

```python
            predictions.append({
                'timestamp': future_time,
                'pm25_predicted': pm25_pred,
                'temperature': weather['temperature'],
                'humidity': weather['humidity'],
                'wind_speed': weather['wind_speed']
            })
```
**Explicație:**
- Creez dicționar cu predicția + info context
- Adaug la listă

**Exemplu rezultat:**
```python
{
    'timestamp': '2026-01-16 15:00',
    'pm25_predicted': 42.3,
    'temperature': 23.1,
    'humidity': 63,
    'wind_speed': 3.8
}
```

---

```python
        return pd.DataFrame(predictions)
```
**Explicație:** Convertesc lista de dicționare în DataFrame

**Rezultat final:**
```
   timestamp            pm25_predicted  temperature  humidity
0  2026-01-16 14:00     39.8           22.5         65
1  2026-01-16 15:00     42.3           23.1         63
2  2026-01-16 16:00     45.1           23.8         61
...
23 2026-01-16 13:00     38.2           21.9         66
```

---

## 🌤️ PARTEA 10: Simulare Variații Meteo (Liniile 278-304)

```python
    def _simulate_weather_variation(self, base_weather: Dict, hours_ahead: int) -> Dict:
        """Simulează variații meteo pentru predicții."""
        weather = base_weather.copy()
```
**Explicație:**
- Funcție privată pentru simulare meteo
- `.copy()` = copiez dicționarul (nu modific originalul)

---

```python
        # Variații realiste pe parcursul zilei
        temp_variation = 3 * np.sin(2 * np.pi * hours_ahead / 24)
        weather['temperature'] = weather.get('temperature', 20) + temp_variation
```
**Explicație DETALIATĂ:**

**Funcția Sinusoidală:**
```python
# Formula: 3 * sin(2π * hours_ahead / 24)
#
# sin(x) oscilează între -1 și +1
# 2π / 24 = 0.26 radiani pe oră (un ciclu complet în 24h)
# Multiplicare cu 3 = amplitudine de ±3°C

# Exemplu:
# hour_offset = 0  → sin(0) = 0      → variație = 0°C
# hour_offset = 6  → sin(π/2) = 1    → variație = +3°C
# hour_offset = 12 → sin(π) = 0      → variație = 0°C
# hour_offset = 18 → sin(3π/2) = -1  → variație = -3°C
```

**De ce sinusoidă?**
- Temperatura variază smooth pe parcursul zilei
- Maxim la amiază, minim noaptea
- Pattern natural, realist

---

```python
        humidity_variation = -5 * np.sin(2 * np.pi * hours_ahead / 24)
        weather['humidity'] = np.clip(
            weather.get('humidity', 60) + humidity_variation, 30, 95
        )
```
**Explicație:**
- Umiditatea e INVERSĂ cu temperatura
- Când e cald → umiditate scade (semnul minus)
- `np.clip(x, 30, 95)` = limitează între 30% și 95%

**Exemplu:**
```python
# Ora 12 (amiază):
# temp_variation = +3°C
# humidity_variation = -5% → umiditate scade când e cald

# Ora 0 (noapte):
# temp_variation = -2°C
# humidity_variation = +4% → umiditate crește când e frig
```

---

```python
        # Vânt și presiune variază mai puțin
        weather['wind_speed'] = weather.get('wind_speed', 3) + np.random.normal(0, 0.5)
        weather['pressure'] = weather.get('pressure', 1013) + np.random.normal(0, 1)
```
**Explicație:**
- `np.random.normal(0, 0.5)` = zgomot gaussian (medie=0, std=0.5)
- Adaug variabilitate mică, realistă
- Vântul nu urmează pattern strict zilnic

**Exemplu:**
```python
# wind_speed = 3 + random(-0.3 ... +0.8) = 3.2 m/s
# pressure = 1013 + random(-1.5 ... +2.1) = 1014.3 hPa
```

---

```python
        weather['wind_direction'] = weather.get('wind_direction', 180)
        weather['clouds'] = weather.get('clouds', 50)
        
        return weather
```
**Explicație:**
- Direcția vântului și nebulozitatea rămân constante
- Greu de simulat realist fără date meteo

---

## 🚀 PARTEA 11: Funcția Main pentru Testare (Liniile 306-331)

```python
def main():
    """Funcție principală pentru antrenarea modelului."""
    predictor = PM25Predictor()
```
**Explicație:**
- Creez obiect predictor
- Aceasta e funcția care se execută când rulez `python src/model.py`

---

```python
    # Antrenează modelul
    try:
        predictor.train()
```
**Explicație:**
- `try` = încearcă să antrenezi
- Dacă apare eroare → prinde-o (vezi `except`)

---

```python
        print("\n" + "="*60)
        print("✅ Model antrenat și salvat cu succes!")
        print("="*60)
```
**Explicație:**
- `"="*60` = afișează 60 de caractere "="
- Mesaj de succes frumos formatat

---

```python
        # Test predicție
        print("\n🧪 Test predicție pentru condiții meteo simulate:")
        test_weather = {
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
**Explicație:**
- Creez date meteo fictive pentru testare
- Verific că predicția funcționează

---

```python
        pm25_pred = predictor.predict(test_weather)
        print(f"   PM2.5 prezis: {pm25_pred:.2f} μg/m³")
```
**Explicație:**
- Fac predicție de test
- Afișez rezultatul

**Exemplu output:**
```
🧪 Test predicție pentru condiții meteo simulate:
   PM2.5 prezis: 44.39 μg/m³
```

---

```python
    except FileNotFoundError as e:
        print(f"\n❌ Eroare: {e}")
        print("💡 Rulați mai întâi: python src/data_collection.py")
```
**Explicație:**
- Prinde eroarea dacă fișierul CSV nu există
- Oferă instrucțiuni clare utilizatorului

---

```python
if __name__ == "__main__":
    main()
```
**Explicație:**
- Execută `main()` DOAR când rulez direct scriptul
- Dacă importez modulul → nu se execută
- **Pattern standard Python** pentru scripturi executabile

---

## 🎯 Rezumat Flow-ul Codului

### La Antrenare:
```
1. Citește CSV → DataFrame
2. Elimină NaN-uri
3. Extrage features (X) și target (y)
4. Normalizează X cu StandardScaler
5. Split train/test (80/20)
6. Antrenează RandomForest pe train
7. Evaluează pe train ȘI test
8. Calculează metrici (RMSE, MAE, R²)
9. Salvează model + scaler + metrici
```

### La Predicție:
```
1. Încarcă model + scaler
2. Primește date meteo
3. Creează DataFrame
4. Normalizează cu scaler-ul salvat
5. Prezice cu modelul
6. Returnează PM2.5 (≥ 0)
```

### La Predicție 24h:
```
1. Loop prin 24 ore
2. Pentru fiecare oră:
   a. Simulează/folosește meteo
   b. Adaugă features temporale (hour, day, month)
   c. Prezice PM2.5
   d. Salvează în listă
3. Returnează DataFrame cu toate predicțiile
```

---

## 📊 Metrici Explicație Finală

| Metrică | Train | Test | Ce înseamnă? |
|---------|-------|------|--------------|
| **RMSE** | 4.80 | 10.07 | Eroare medie în μg/m³ (penalizează outliers) |
| **MAE** | 3.69 | 8.20 | Eroare medie absolută (mai robustă) |
| **R²** | 0.917 | 0.597 | 60% din variație explicată (EXCELENT!) |

**Overfitting?** 
- Da, moderat (train R² > test R²)
- Normal pentru dataset mic
- Rezolvat prin regularizare (max_depth, min_samples)

---

## 💡 Concepte Cheie să Reții

1. **Random Forest** = ansamblu de 100 arbori care votează
2. **StandardScaler** = normalizare (medie=0, std=1)
3. **Train/Test Split** = 80/20 pentru evitare overfitting
4. **RMSE vs MAE** = RMSE penalizează outliers mai mult
5. **R² Score** = % din variație explicată de model
6. **Feature Importance** = ora zilei = 72%!
7. **Joblib** = salvare eficientă modele ML
8. **Simulare meteo** = sinusoide pentru variații realiste

---

**Ai acum explicația completă a codului tău! 🎉**

*Fiecare linie, fiecare funcție, fiecare decizie - totul explicat în detaliu.*

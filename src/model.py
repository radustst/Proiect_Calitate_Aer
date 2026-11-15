"""
Modul pentru antrenarea și utilizarea modelului de predicție PM2.5.
Student 2: Munteanu Radu

Funcționalități:
- Antrenare model Random Forest
- Evaluare performanță model
- Predicție PM2.5 pentru următoarele 24h
- Salvare/încărcare model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime, timedelta
from typing import Tuple, Dict, List
import json


class PM25Predictor:
    """Clasă pentru predicția nivelului PM2.5."""
    
    def __init__(self, model_path: str = 'models/pm25_model.joblib'):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'temperature', 'humidity', 'pressure', 'wind_speed', 
            'wind_direction', 'clouds', 'hour', 'day_of_week', 'month'
        ]
        self.metrics = {}
        
    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Pregătește features pentru antrenare sau predicție.
        
        Args:
            df: DataFrame cu date
            
        Returns:
            Tuple (X, y) cu features și target
        """
        # Verifică că toate coloanele necesare există
        missing_cols = [col for col in self.feature_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Lipsesc coloane: {missing_cols}")
        
        X = df[self.feature_columns].values
        y = df['pm25'].values if 'pm25' in df.columns else None
        
        return X, y
    
    def train(self, data_path: str = 'data/training_data.csv'):
        """
        Antrenează modelul Random Forest.
        
        Args:
            data_path: Calea către fișierul cu date de antrenare
        """
        print("🎓 Începere antrenare model...\n")
        
        # Încarcă datele
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Fișierul {data_path} nu există. Rulați mai întâi data_collection.py")
        
        df = pd.read_csv(data_path)
        print(f"📊 Date încărcate: {len(df)} înregistrări")
        
        # Elimină valori lipsă
        df = df.dropna()
        print(f"📊 Date valide: {len(df)} înregistrări\n")
        
        # Pregătește features
        X, y = self.prepare_features(df)
        
        # Normalizează features
        X_scaled = self.scaler.fit_transform(X)
        
        # Împarte în train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        print(f"📚 Set antrenare: {len(X_train)} înregistrări")
        print(f"🧪 Set testare: {len(X_test)} înregistrări\n")
        
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
        
        self.model.fit(X_train, y_train)
        print("✅ Antrenare finalizată!\n")
        
        # Evaluează modelul
        self._evaluate_model(X_train, y_train, X_test, y_test)
        
        # Salvează modelul
        self.save_model()
        
    def _evaluate_model(self, X_train, y_train, X_test, y_test):
        """Evaluează performanța modelului."""
        print("📊 Evaluare model...\n")
        
        # Predicții
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        # Metrici train
        train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
        train_mae = mean_absolute_error(y_train, y_train_pred)
        train_r2 = r2_score(y_train, y_train_pred)
        
        # Metrici test
        test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
        test_mae = mean_absolute_error(y_test, y_test_pred)
        test_r2 = r2_score(y_test, y_test_pred)
        
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
        
        # Afișează rezultate
        print("📈 Performanță Set Antrenare:")
        print(f"   RMSE: {train_rmse:.2f} μg/m³")
        print(f"   MAE:  {train_mae:.2f} μg/m³")
        print(f"   R²:   {train_r2:.4f}")
        
        print("\n📉 Performanță Set Testare:")
        print(f"   RMSE: {test_rmse:.2f} μg/m³")
        print(f"   MAE:  {test_mae:.2f} μg/m³")
        print(f"   R²:   {test_r2:.4f}\n")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("🎯 Importanța Features:")
        for idx, row in feature_importance.iterrows():
            print(f"   {row['feature']:15s}: {row['importance']:.4f}")
        print()
        
    def save_model(self):
        """Salvează modelul și scaler."""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Salvează modelul și scaler
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'metrics': self.metrics,
            'trained_at': datetime.now().isoformat()
        }
        
        joblib.dump(model_data, self.model_path)
        print(f"💾 Model salvat: {self.model_path}")
        
        # Salvează metrici în JSON
        metrics_path = self.model_path.replace('.joblib', '_metrics.json')
        with open(metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print(f"📊 Metrici salvate: {metrics_path}\n")
        
    def load_model(self):
        """Încarcă modelul salvat."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Modelul nu există: {self.model_path}")
        
        model_data = joblib.load(self.model_path)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']
        self.metrics = model_data.get('metrics', {})
        
        print(f"✅ Model încărcat: {self.model_path}")
        
    def predict(self, weather_data: Dict) -> float:
        """
        Prezice PM2.5 pentru date meteo specifice.
        
        Args:
            weather_data: Dicționar cu date meteo și temporale
            
        Returns:
            Valoare prezisă PM2.5
        """
        if self.model is None:
            self.load_model()
        
        # Creează DataFrame cu features
        features = pd.DataFrame([weather_data])
        
        # Verifică features
        X, _ = self.prepare_features(features)
        
        # Normalizează
        X_scaled = self.scaler.transform(X)
        
        # Prezice
        prediction = self.model.predict(X_scaled)[0]
        
        return max(0, prediction)  # PM2.5 nu poate fi negativ
    
    def predict_next_24h(self, current_weather: Dict, weather_forecast: List[Dict] = None) -> pd.DataFrame:
        """
        Prezice PM2.5 pentru următoarele 24 de ore.
        
        Args:
            current_weather: Date meteo curente
            weather_forecast: Listă cu prognoză meteo pentru 24h (opțional)
            
        Returns:
            DataFrame cu predicții orare
        """
        if self.model is None:
            self.load_model()
        
        predictions = []
        current_time = datetime.now().replace(minute=0, second=0, microsecond=0)

        for hour_offset in range(24):
            future_time = current_time + timedelta(hours=hour_offset)

            # Folosește prognoza meteo reală dacă este disponibilă
            if weather_forecast and hour_offset < len(weather_forecast):
                weather = dict(weather_forecast[hour_offset])
                # Ora din prognoză (în fusul orar al orașului) are prioritate
                if weather.get('timestamp') is not None:
                    future_time = weather.pop('timestamp')
            else:
                # Simulează variații meteo
                weather = self._simulate_weather_variation(current_weather, hour_offset)
            
            # Adaugă features temporale
            weather['hour'] = future_time.hour
            weather['day_of_week'] = future_time.weekday()
            weather['month'] = future_time.month
            
            # Prezice PM2.5
            pm25_pred = self.predict(weather)
            
            predictions.append({
                'timestamp': future_time,
                'pm25_predicted': pm25_pred,
                'temperature': weather['temperature'],
                'humidity': weather['humidity'],
                'wind_speed': weather['wind_speed']
            })
        
        return pd.DataFrame(predictions)
    
    def _simulate_weather_variation(self, base_weather: Dict, hours_ahead: int) -> Dict:
        """Simulează variații meteo pentru predicții."""
        weather = base_weather.copy()
        
        # Variații realiste pe parcursul zilei
        temp_variation = 3 * np.sin(2 * np.pi * hours_ahead / 24)
        weather['temperature'] = weather.get('temperature', 20) + temp_variation
        
        humidity_variation = -5 * np.sin(2 * np.pi * hours_ahead / 24)
        weather['humidity'] = np.clip(
            weather.get('humidity', 60) + humidity_variation, 30, 95
        )
        
        # Vânt și presiune variază mai puțin
        weather['wind_speed'] = weather.get('wind_speed', 3) + np.random.normal(0, 0.5)
        weather['pressure'] = weather.get('pressure', 1013) + np.random.normal(0, 1)
        weather['wind_direction'] = weather.get('wind_direction', 180)
        weather['clouds'] = weather.get('clouds', 50)
        
        return weather


def main():
    """Funcție principală pentru antrenarea modelului."""
    predictor = PM25Predictor()
    
    # Antrenează modelul
    try:
        predictor.train()
        
        print("\n" + "="*60)
        print("✅ Model antrenat și salvat cu succes!")
        print("="*60)
        
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
        
        pm25_pred = predictor.predict(test_weather)
        print(f"   PM2.5 prezis: {pm25_pred:.2f} μg/m³")
        
    except FileNotFoundError as e:
        print(f"\n❌ Eroare: {e}")
        print("💡 Rulați mai întâi: python src/data_collection.py")


if __name__ == "__main__":
    main()

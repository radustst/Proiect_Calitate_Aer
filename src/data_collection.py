"""
Modul pentru colectarea datelor de calitate a aerului și meteo.
Student 1: Berciu Antonio

Funcționalități:
- Colectare date PM2.5 din OpenAQ API
- Colectare date meteo din OpenWeatherMap API
- Salvare date în format CSV pentru antrenare model
"""

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
import time

# Încărcare variabile de mediu
load_dotenv()


class DataCollector:
    """Clasă pentru colectarea datelor de calitate a aerului și meteo."""
    
    def __init__(self):
        self.openaq_url = os.getenv('OPENAQ_API_URL', 'https://api.openaq.org/v2')
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.weather_url = os.getenv('WEATHER_API_URL', 'https://api.openweathermap.org/data/2.5')
        
        # Locație implicită
        self.city = os.getenv('DEFAULT_CITY', 'Bucharest')
        self.country = os.getenv('DEFAULT_COUNTRY', 'RO')
        self.lat = float(os.getenv('DEFAULT_LAT', '44.4268'))
        self.lon = float(os.getenv('DEFAULT_LON', '26.1025'))
        
    def get_air_quality_data(self, days: int = 7) -> pd.DataFrame:
        """
        Colectează date PM2.5 din OpenAQ API.
        
        Args:
            days: Numărul de zile în trecut pentru care se colectează date
            
        Returns:
            DataFrame cu date PM2.5
        """
        print(f"📡 Colectare date PM2.5 pentru ultimele {days} zile...")
        
        # Calculează intervalul de date
        date_to = datetime.utcnow()
        date_from = date_to - timedelta(days=days)
        
        params = {
            'country': self.country,
            'city': self.city,
            'parameter': 'pm25',
            'date_from': date_from.isoformat(),
            'date_to': date_to.isoformat(),
            'limit': 10000
        }
        
        try:
            response = requests.get(f'{self.openaq_url}/measurements', params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'results' in data and len(data['results']) > 0:
                # Extrage datele relevante
                records = []
                for measurement in data['results']:
                    records.append({
                        'timestamp': measurement['date']['utc'],
                        'pm25': measurement['value'],
                        'location': measurement.get('location', 'Unknown'),
                        'city': measurement.get('city', self.city),
                        'country': measurement.get('country', self.country)
                    })
                
                df = pd.DataFrame(records)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values('timestamp')
                
                print(f"✅ Colectate {len(df)} înregistrări PM2.5")
                return df
            else:
                print("⚠️ Nu s-au găsit date PM2.5. Se generează date simulate...")
                return self._generate_synthetic_pm25_data(days)
                
        except Exception as e:
            print(f"❌ Eroare la colectarea datelor PM2.5: {e}")
            print("⚠️ Se generează date simulate...")
            return self._generate_synthetic_pm25_data(days)
    
    def _generate_synthetic_pm25_data(self, days: int) -> pd.DataFrame:
        """Generează date PM2.5 simulate pentru testare."""
        import numpy as np
        
        # Generează timestamp-uri la fiecare oră
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        timestamps = pd.date_range(start=start_date, end=end_date, freq='H')
        
        # Generează valori PM2.5 realiste (variază între 10-100 μg/m³)
        np.random.seed(42)
        base_pm25 = 30
        pm25_values = base_pm25 + 20 * np.sin(np.arange(len(timestamps)) * 2 * np.pi / 24) + \
                      np.random.normal(0, 10, len(timestamps))
        pm25_values = np.clip(pm25_values, 5, 150)
        
        df = pd.DataFrame({
            'timestamp': timestamps,
            'pm25': pm25_values,
            'location': 'Simulated Station',
            'city': self.city,
            'country': self.country
        })
        
        return df
    
    def get_weather_data(self, timestamp: datetime) -> Optional[Dict]:
        """
        Colectează date meteo pentru un timestamp specific.
        
        Args:
            timestamp: Momentul pentru care se solicită datele meteo
            
        Returns:
            Dicționar cu date meteo sau None
        """
        if not self.weather_api_key or self.weather_api_key == 'your_api_key_here':
            # Generează date meteo simulate
            return self._generate_synthetic_weather(timestamp)
        
        try:
            params = {
                'lat': self.lat,
                'lon': self.lon,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            
            response = requests.get(f'{self.weather_url}/weather', params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'clouds': data.get('clouds', {}).get('all', 0)
            }
            
        except Exception as e:
            print(f"⚠️ Eroare API meteo: {e}. Se folosesc date simulate.")
            return self._generate_synthetic_weather(timestamp)
    
    def _generate_synthetic_weather(self, timestamp: datetime) -> Dict:
        """Generează date meteo simulate realiste."""
        import numpy as np
        
        hour = timestamp.hour
        day_of_year = timestamp.timetuple().tm_yday
        
        # Temperatură variabilă cu ora și anotimpul
        base_temp = 15 + 10 * np.sin(2 * np.pi * day_of_year / 365)
        temp_variation = 5 * np.sin(2 * np.pi * hour / 24)
        temperature = base_temp + temp_variation + np.random.normal(0, 2)
        
        # Umiditate inversă cu temperatura
        humidity = 70 - (temperature - 15) * 2 + np.random.normal(0, 10)
        humidity = np.clip(humidity, 30, 95)
        
        # Presiune atmosferică
        pressure = 1013 + np.random.normal(0, 5)
        
        # Vânt
        wind_speed = 2 + np.random.exponential(3)
        wind_direction = np.random.uniform(0, 360)
        
        # Nebulozitate
        clouds = np.random.uniform(0, 100)
        
        return {
            'temperature': round(temperature, 2),
            'humidity': round(humidity, 2),
            'pressure': round(pressure, 2),
            'wind_speed': round(wind_speed, 2),
            'wind_direction': round(wind_direction, 2),
            'clouds': round(clouds, 2)
        }
    
    def create_training_dataset(self, days: int = 30, output_file: str = 'data/training_data.csv'):
        """
        Creează un dataset complet pentru antrenarea modelului.
        
        Args:
            days: Numărul de zile de date de colectat
            output_file: Calea fișierului de ieșire
        """
        print(f"\n🚀 Creare dataset de antrenare pentru {days} zile...\n")
        
        # Colectează date PM2.5
        pm25_df = self.get_air_quality_data(days)
        
        if pm25_df.empty:
            print("❌ Nu s-au putut colecta date PM2.5")
            return
        
        # Adaugă date meteo pentru fiecare timestamp
        print("\n🌤️ Colectare date meteo...")
        weather_data = []
        
        total = len(pm25_df)
        for idx, row in pm25_df.iterrows():
            if idx % 50 == 0:
                print(f"  Progres: {idx}/{total} înregistrări")
            
            weather = self.get_weather_data(row['timestamp'])
            weather_data.append(weather)
            
            # Pauză pentru a evita limitele API
            if self.weather_api_key and self.weather_api_key != 'your_api_key_here':
                time.sleep(0.1)
        
        # Combină datele
        weather_df = pd.DataFrame(weather_data)
        combined_df = pd.concat([pm25_df.reset_index(drop=True), weather_df], axis=1)
        
        # Adaugă features temporale
        combined_df['hour'] = combined_df['timestamp'].dt.hour
        combined_df['day_of_week'] = combined_df['timestamp'].dt.dayofweek
        combined_df['month'] = combined_df['timestamp'].dt.month
        
        # Salvează dataset
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        combined_df.to_csv(output_file, index=False)
        
        print(f"\n✅ Dataset salvat: {output_file}")
        print(f"📊 Total înregistrări: {len(combined_df)}")
        print(f"📅 Interval: {combined_df['timestamp'].min()} -> {combined_df['timestamp'].max()}")
        print(f"\n📈 Statistici PM2.5:")
        print(combined_df['pm25'].describe())
        
        return combined_df


def main():
    """Funcție principală pentru colectarea datelor."""
    collector = DataCollector()
    
    # Creează dataset de antrenare
    df = collector.create_training_dataset(days=30)
    
    if df is not None:
        print("\n" + "="*60)
        print("✅ Colectare date finalizată cu succes!")
        print("="*60)


if __name__ == "__main__":
    main()

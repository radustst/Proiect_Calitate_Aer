"""
Modul pentru colectarea datelor de calitate a aerului și meteo.
Student 1: Berciu Antonio

Funcționalități:
- Colectare date PM2.5 reale din Open-Meteo Air Quality API (CAMS / Copernicus)
- Colectare date meteo reale (istoric, curent, prognoză) din Open-Meteo Weather API
- Găsire automată a coordonatelor orașului (Open-Meteo Geocoding API)
- Salvare date în format CSV pentru antrenare model

Toate API-urile folosite sunt gratuite și NU necesită cheie API.
Datele simulate sunt folosite doar ca rezervă, dacă nu există conexiune la internet.
"""

import requests
import pandas as pd
import json
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
import time

# Încărcare variabile de mediu
load_dotenv()

# Variabilele meteo cerute de la Open-Meteo, mapate la numele folosite în proiect
WEATHER_VARIABLES = {
    'temperature_2m': 'temperature',        # °C
    'relative_humidity_2m': 'humidity',     # %
    'pressure_msl': 'pressure',             # hPa
    'wind_speed_10m': 'wind_speed',         # m/s (cu wind_speed_unit=ms)
    'wind_direction_10m': 'wind_direction', # grade
    'cloud_cover': 'clouds',                # %
}

# Open-Meteo permite maxim 92 de zile în trecut
MAX_PAST_DAYS = 92


class DataCollector:
    """Clasă pentru colectarea datelor de calitate a aerului și meteo."""

    def __init__(self, city: Optional[str] = None, country: Optional[str] = None):
        self.air_quality_url = os.getenv(
            'AIR_QUALITY_API_URL', 'https://air-quality-api.open-meteo.com/v1/air-quality'
        )
        self.weather_url = os.getenv('WEATHER_API_URL', 'https://api.open-meteo.com/v1/forecast')
        self.geocoding_url = os.getenv(
            'GEOCODING_API_URL', 'https://geocoding-api.open-meteo.com/v1/search'
        )
        self.timeout = int(os.getenv('API_TIMEOUT', '20'))

        # Locație implicită
        self.city = city or os.getenv('DEFAULT_CITY', 'Bucharest')
        self.country = country or os.getenv('DEFAULT_COUNTRY', 'RO')
        self.lat = float(os.getenv('DEFAULT_LAT', '44.4268'))
        self.lon = float(os.getenv('DEFAULT_LON', '26.1025'))

        # Sursa ultimelor date colectate (afișată în aplicație)
        self.last_source = None

        # Dacă s-a cerut alt oraș decât cel implicit, îi căutăm coordonatele
        if city or country:
            self.set_location(self.city, self.country)

    # ------------------------------------------------------------------
    # Locație
    # ------------------------------------------------------------------
    def set_location(self, city: str, country: Optional[str] = None) -> bool:
        """
        Găsește coordonatele unui oraș folosind Open-Meteo Geocoding API.

        Args:
            city: Numele orașului (ex: "Cluj-Napoca")
            country: Codul țării ISO-2 (ex: "RO"), opțional

        Returns:
            True dacă orașul a fost găsit, False altfel (se păstrează coordonatele vechi)
        """
        params = {'name': city, 'count': 1, 'language': 'ro', 'format': 'json'}
        if country:
            params['countryCode'] = country.upper()

        try:
            response = requests.get(self.geocoding_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            results = response.json().get('results') or []

            if not results:
                print(f"⚠️ Orașul '{city}' nu a fost găsit. Se folosesc coordonatele implicite.")
                return False

            place = results[0]
            self.city = place.get('name', city)
            self.country = place.get('country_code', country or self.country)
            self.lat = float(place['latitude'])
            self.lon = float(place['longitude'])
            print(f"📍 Locație: {self.city}, {self.country} ({self.lat:.4f}, {self.lon:.4f})")
            return True

        except Exception as e:
            print(f"⚠️ Eroare la căutarea orașului: {e}. Se folosesc coordonatele implicite.")
            return False

    # ------------------------------------------------------------------
    # Funcții ajutătoare pentru Open-Meteo
    # ------------------------------------------------------------------
    @staticmethod
    def _local_now(utc_offset_seconds: int = 0) -> datetime:
        """Ora curentă în fusul orar al locației (fără informație de timezone)."""
        now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
        return now_utc + timedelta(seconds=utc_offset_seconds)

    def _hourly_to_dataframe(self, data: Dict, variables: Dict[str, str]) -> pd.DataFrame:
        """Transformă blocul 'hourly' din răspunsul Open-Meteo într-un DataFrame."""
        hourly = data.get('hourly', {})
        df = pd.DataFrame({'timestamp': pd.to_datetime(hourly.get('time', []))})
        for api_name, column in variables.items():
            df[column] = hourly.get(api_name, [None] * len(df))
        return df

    def _fetch_weather_hourly(self, past_days: int, forecast_days: int) -> pd.DataFrame:
        """Descarcă date meteo orare reale (istoric + prognoză) din Open-Meteo."""
        params = {
            'latitude': self.lat,
            'longitude': self.lon,
            'hourly': ','.join(WEATHER_VARIABLES.keys()),
            'past_days': min(max(past_days, 0), MAX_PAST_DAYS),
            'forecast_days': forecast_days,
            'wind_speed_unit': 'ms',
            'timezone': 'auto',
        }
        response = requests.get(self.weather_url, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        df = self._hourly_to_dataframe(data, WEATHER_VARIABLES)
        df.attrs['utc_offset_seconds'] = data.get('utc_offset_seconds', 0)
        return df

    # ------------------------------------------------------------------
    # PM2.5
    # ------------------------------------------------------------------
    def get_air_quality_data(self, days: int = 7, include_weather: bool = True) -> pd.DataFrame:
        """
        Colectează date PM2.5 orare reale din Open-Meteo Air Quality API.

        Datele provin din serviciul european Copernicus (CAMS) și acoperă
        ultimele maxim 92 de zile, pentru orice locație.

        Args:
            days: Numărul de zile în trecut pentru care se colectează date
            include_weather: Adaugă și datele meteo reale pentru aceleași ore

        Returns:
            DataFrame cu date PM2.5 (și meteo, dacă include_weather=True)
        """
        days = min(max(int(days), 1), MAX_PAST_DAYS)
        print(f"📡 Colectare date PM2.5 reale pentru ultimele {days} zile ({self.city})...")

        params = {
            'latitude': self.lat,
            'longitude': self.lon,
            'hourly': 'pm2_5',
            'past_days': days,
            'forecast_days': 1,
            'timezone': 'auto',
        }

        try:
            response = requests.get(self.air_quality_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            df = self._hourly_to_dataframe(data, {'pm2_5': 'pm25'})

            # Păstrăm doar orele trecute (restul sunt prognoză) și valorile existente
            now_local = self._local_now(data.get('utc_offset_seconds', 0))
            df = df[df['timestamp'] <= now_local].dropna(subset=['pm25'])

            if df.empty:
                print("⚠️ Nu s-au găsit date PM2.5. Se generează date simulate...")
                return self._generate_synthetic_pm25_data(days)

            df['location'] = 'Open-Meteo (CAMS)'
            df['city'] = self.city
            df['country'] = self.country
            df = df.sort_values('timestamp').reset_index(drop=True)

            if include_weather:
                try:
                    weather_df = self._fetch_weather_hourly(past_days=days, forecast_days=1)
                    df = df.merge(weather_df, on='timestamp', how='left')
                except Exception as e:
                    print(f"⚠️ Nu s-au putut adăuga datele meteo: {e}")

            self.last_source = 'Open-Meteo (CAMS)'
            print(f"✅ Colectate {len(df)} înregistrări PM2.5 reale")
            return df

        except Exception as e:
            print(f"❌ Eroare la colectarea datelor PM2.5: {e}")
            print("⚠️ Se generează date simulate...")
            return self._generate_synthetic_pm25_data(days)

    def get_pm25_forecast(self, hours: int = 24) -> pd.DataFrame:
        """
        Prognoza oficială PM2.5 (CAMS) pentru următoarele ore.
        Utilă pentru a compara predicțiile modelului nostru cu o sursă reală.
        """
        params = {
            'latitude': self.lat,
            'longitude': self.lon,
            'hourly': 'pm2_5',
            'forecast_days': 2,
            'timezone': 'auto',
        }
        try:
            response = requests.get(self.air_quality_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            df = self._hourly_to_dataframe(data, {'pm2_5': 'pm25_cams'})
            start = self._local_now(data.get('utc_offset_seconds', 0)).replace(
                minute=0, second=0, microsecond=0
            )
            return df[df['timestamp'] >= start].head(hours).reset_index(drop=True)
        except Exception as e:
            print(f"⚠️ Prognoza CAMS indisponibilă: {e}")
            return pd.DataFrame(columns=['timestamp', 'pm25_cams'])

    def _generate_synthetic_pm25_data(self, days: int) -> pd.DataFrame:
        """Generează date PM2.5 simulate (doar ca rezervă, fără internet)."""
        import numpy as np

        self.last_source = 'Date simulate (fără conexiune la API)'

        # Generează timestamp-uri la fiecare oră
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        timestamps = pd.date_range(start=start_date, end=end_date, freq='h')

        # Generează valori PM2.5 (variază între 10-100 μg/m³)
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

    # ------------------------------------------------------------------
    # Meteo
    # ------------------------------------------------------------------
    def get_weather_data(self, timestamp: Optional[datetime] = None) -> Optional[Dict]:
        """
        Colectează datele meteo curente reale din Open-Meteo.

        Args:
            timestamp: Momentul pentru care se solicită datele (folosit doar pentru rezervă)

        Returns:
            Dicționar cu date meteo
        """
        timestamp = timestamp or datetime.now()
        params = {
            'latitude': self.lat,
            'longitude': self.lon,
            'current': ','.join(WEATHER_VARIABLES.keys()),
            'wind_speed_unit': 'ms',
            'timezone': 'auto',
        }

        try:
            response = requests.get(self.weather_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            current = response.json()['current']

            weather = {
                column: float(current[api_name])
                for api_name, column in WEATHER_VARIABLES.items()
            }
            self.last_source = 'Open-Meteo'
            return weather

        except Exception as e:
            print(f"⚠️ Eroare API meteo: {e}. Se folosesc date simulate.")
            return self._generate_synthetic_weather(timestamp)

    def get_weather_forecast(self, hours: int = 24) -> List[Dict]:
        """
        Prognoza meteo orară reală pentru următoarele ore (Open-Meteo).

        Returns:
            Listă de dicționare (câte unul pe oră) cu 'timestamp' și datele meteo.
            Listă goală dacă API-ul nu este disponibil.
        """
        try:
            df = self._fetch_weather_hourly(past_days=0, forecast_days=2)
            start = self._local_now(df.attrs.get('utc_offset_seconds', 0)).replace(
                minute=0, second=0, microsecond=0
            )
            df = df[df['timestamp'] >= start].dropna().head(hours)
            records = df.to_dict('records')
            for record in records:
                record['timestamp'] = pd.Timestamp(record['timestamp']).to_pydatetime()
            return records
        except Exception as e:
            print(f"⚠️ Prognoza meteo indisponibilă: {e}")
            return []

    def _generate_synthetic_weather(self, timestamp: datetime) -> Dict:
        """Generează date meteo simulate (doar ca rezervă, fără internet)."""
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

    # ------------------------------------------------------------------
    # Dataset de antrenare
    # ------------------------------------------------------------------
    def create_training_dataset(self, days: int = 90, output_file: str = 'data/training_data.csv'):
        """
        Creează un dataset complet pentru antrenarea modelului.

        Fiecare oră are valoarea PM2.5 reală și vremea reală din acea oră.

        Args:
            days: Numărul de zile de date de colectat (maxim 92)
            output_file: Calea fișierului de ieșire
        """
        print(f"\n🚀 Creare dataset de antrenare pentru {days} zile...\n")

        # Colectează date PM2.5 + meteo reale pentru aceleași ore
        combined_df = self.get_air_quality_data(days, include_weather=True)

        if combined_df.empty:
            print("❌ Nu s-au putut colecta date PM2.5")
            return

        # Dacă API-ul meteo nu a răspuns, completăm cu date simulate
        if 'temperature' not in combined_df.columns or combined_df['temperature'].isna().all():
            print("\n🌤️ Date meteo reale indisponibile, se folosesc date simulate...")
            weather_df = pd.DataFrame(
                [self._generate_synthetic_weather(ts) for ts in combined_df['timestamp']]
            )
            combined_df = combined_df.drop(
                columns=[c for c in weather_df.columns if c in combined_df.columns]
            )
            combined_df = pd.concat([combined_df.reset_index(drop=True), weather_df], axis=1)

        combined_df = combined_df.dropna(subset=list(WEATHER_VARIABLES.values()))

        # Adaugă features temporale
        combined_df['hour'] = combined_df['timestamp'].dt.hour
        combined_df['day_of_week'] = combined_df['timestamp'].dt.day_of_week
        combined_df['month'] = combined_df['timestamp'].dt.month

        # Salvează dataset
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        combined_df.to_csv(output_file, index=False)

        print(f"\n✅ Dataset salvat: {output_file}")
        print(f"🌐 Sursă date: {self.last_source}")
        print(f"📊 Total înregistrări: {len(combined_df)}")
        print(f"📅 Interval: {combined_df['timestamp'].min()} -> {combined_df['timestamp'].max()}")
        print(f"\n📈 Statistici PM2.5:")
        print(combined_df['pm25'].describe())

        return combined_df


def main():
    """Funcție principală pentru colectarea datelor."""
    collector = DataCollector()

    # Creează dataset de antrenare (maxim 92 de zile disponibile gratuit)
    df = collector.create_training_dataset(days=90)

    if df is not None:
        print("\n" + "="*60)
        print("✅ Colectare date finalizată cu succes!")
        print("="*60)


if __name__ == "__main__":
    main()

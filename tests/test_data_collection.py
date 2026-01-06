"""
Teste unitare pentru modulul de colectare date.
Student 4: Documentare + Testare
"""

import pytest
import pandas as pd
from datetime import datetime
import sys
import os

# Adaugă directorul părinte la path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collection import DataCollector


class TestDataCollector:
    """Teste pentru clasa DataCollector."""
    
    @pytest.fixture
    def collector(self):
        """Fixture pentru inițializare DataCollector."""
        return DataCollector()
    
    def test_initialization(self, collector):
        """Test inițializare corectă."""
        assert collector is not None
        assert collector.city == "Bucharest"
        assert collector.country == "RO"
        
    def test_get_air_quality_data(self, collector):
        """Test colectare date PM2.5."""
        df = collector.get_air_quality_data(days=1)
        
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert 'pm25' in df.columns
        assert 'timestamp' in df.columns
        
    def test_pm25_values_valid(self, collector):
        """Test că valorile PM2.5 sunt valide."""
        df = collector.get_air_quality_data(days=1)
        
        assert (df['pm25'] >= 0).all()
        assert (df['pm25'] < 1000).all()  # Valoare realistă maximă
        
    def test_get_weather_data(self, collector):
        """Test colectare date meteo."""
        weather = collector.get_weather_data(datetime.now())
        
        assert weather is not None
        assert 'temperature' in weather
        assert 'humidity' in weather
        assert 'pressure' in weather
        assert 'wind_speed' in weather
        
    def test_weather_values_realistic(self, collector):
        """Test că valorile meteo sunt realiste."""
        weather = collector.get_weather_data(datetime.now())
        
        assert -50 < weather['temperature'] < 50
        assert 0 <= weather['humidity'] <= 100
        assert 900 < weather['pressure'] < 1100
        assert weather['wind_speed'] >= 0
        
    def test_synthetic_pm25_generation(self, collector):
        """Test generare date PM2.5 simulate."""
        df = collector._generate_synthetic_pm25_data(days=7)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'pm25' in df.columns
        assert (df['pm25'] >= 0).all()
        
    def test_synthetic_weather_generation(self, collector):
        """Test generare date meteo simulate."""
        timestamp = datetime.now()
        weather = collector._generate_synthetic_weather(timestamp)
        
        assert weather is not None
        assert all(key in weather for key in ['temperature', 'humidity', 'pressure', 'wind_speed'])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

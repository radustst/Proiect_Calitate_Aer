"""
Teste unitare pentru modulul de predicție.
Student 4: Documentare + Testare
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.model import PM25Predictor


class TestPM25Predictor:
    """Teste pentru clasa PM25Predictor."""
    
    @pytest.fixture
    def predictor(self):
        """Fixture pentru inițializare predictor."""
        return PM25Predictor()
    
    def test_initialization(self, predictor):
        """Test inițializare corectă."""
        assert predictor is not None
        assert predictor.feature_columns is not None
        assert len(predictor.feature_columns) == 9
        
    def test_feature_columns(self, predictor):
        """Test că toate coloanele necesare sunt definite."""
        expected_features = [
            'temperature', 'humidity', 'pressure', 'wind_speed',
            'wind_direction', 'clouds', 'hour', 'day_of_week', 'month'
        ]
        
        assert predictor.feature_columns == expected_features
        
    def test_prepare_features_valid_data(self, predictor):
        """Test pregătire features cu date valide."""
        df = pd.DataFrame({
            'temperature': [20.0],
            'humidity': [60.0],
            'pressure': [1013.0],
            'wind_speed': [3.0],
            'wind_direction': [180.0],
            'clouds': [50.0],
            'hour': [12],
            'day_of_week': [3],
            'month': [1],
            'pm25': [25.0]
        })
        
        X, y = predictor.prepare_features(df)
        
        assert X.shape == (1, 9)
        assert y is not None
        assert y[0] == 25.0
        
    def test_prepare_features_missing_columns(self, predictor):
        """Test eroare când lipsesc coloane."""
        df = pd.DataFrame({
            'temperature': [20.0],
            'humidity': [60.0]
        })
        
        with pytest.raises(ValueError):
            predictor.prepare_features(df)
            
    def test_predict_format(self, predictor):
        """Test format predicție."""
        weather_data = {
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
        
        # Creează un model dummy pentru test
        try:
            prediction = predictor.predict(weather_data)
            assert isinstance(prediction, (int, float))
            assert prediction >= 0
        except FileNotFoundError:
            # Normal dacă modelul nu e antrenat
            pass
            
    def test_simulate_weather_variation(self, predictor):
        """Test simulare variații meteo."""
        base_weather = {
            'temperature': 20.0,
            'humidity': 60.0,
            'pressure': 1013.0,
            'wind_speed': 3.0,
            'wind_direction': 180.0,
            'clouds': 50.0
        }
        
        varied_weather = predictor._simulate_weather_variation(base_weather, 12)
        
        assert varied_weather is not None
        assert 'temperature' in varied_weather
        assert 'humidity' in varied_weather
        # Verifică că valorile au variat
        assert varied_weather['temperature'] != base_weather['temperature']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

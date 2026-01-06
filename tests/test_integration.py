"""
Teste de integrare pentru workflow complet.
Student 4: Documentare + Testare
"""

import pytest
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collection import DataCollector
from src.model import PM25Predictor


class TestIntegration:
    """Teste de integrare pentru fluxul complet."""
    
    def test_data_collection_to_model(self):
        """Test colectare date și pregătire pentru model."""
        collector = DataCollector()
        
        # Colectează date
        df = collector.get_air_quality_data(days=2)
        
        assert not df.empty
        assert 'pm25' in df.columns
        assert 'timestamp' in df.columns
        
    def test_end_to_end_prediction(self):
        """Test predicție end-to-end (dacă modelul există)."""
        predictor = PM25Predictor()
        collector = DataCollector()
        
        try:
            # Încarcă modelul
            predictor.load_model()
            
            # Obține date meteo
            current_weather = collector.get_weather_data(pd.Timestamp.now())
            
            # Adaugă features temporale
            current_weather['hour'] = pd.Timestamp.now().hour
            current_weather['day_of_week'] = pd.Timestamp.now().dayofweek
            current_weather['month'] = pd.Timestamp.now().month
            
            # Prezice
            prediction = predictor.predict(current_weather)
            
            assert prediction >= 0
            assert prediction < 500  # Valoare realistă
            
        except FileNotFoundError:
            pytest.skip("Model nu este antrenat")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

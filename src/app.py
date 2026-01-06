"""
Dashboard interactiv Streamlit pentru predicția calității aerului.
Student 3: Roman Silviu

Funcționalități:
- Vizualizare date în timp real
- Predicții PM2.5 pentru 24h
- Grafice interactive
- Comparare date istorice vs predicții
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
import sys

# Adaugă directorul părinte la path pentru import module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collection import DataCollector
from src.model import PM25Predictor


# Configurare pagină
st.set_page_config(
    page_title="Predicție Calitate Aer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizat
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .info-box {
        background-color: #e1f5fe;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def get_aqi_category(pm25: float) -> tuple:
    """Returnează categoria și culoarea pentru valoarea PM2.5."""
    if pm25 <= 12:
        return "Bună", "#00e400"
    elif pm25 <= 35.4:
        return "Moderată", "#ffff00"
    elif pm25 <= 55.4:
        return "Nesănătoasă pentru grupuri sensibile", "#ff7e00"
    elif pm25 <= 150.4:
        return "Nesănătoasă", "#ff0000"
    elif pm25 <= 250.4:
        return "Foarte nesănătoasă", "#8f3f97"
    else:
        return "Periculoasă", "#7e0023"


def plot_24h_prediction(predictions_df: pd.DataFrame):
    """Creează grafic pentru predicția pe 24h."""
    fig = go.Figure()
    
    # Linie predicție
    fig.add_trace(go.Scatter(
        x=predictions_df['timestamp'],
        y=predictions_df['pm25_predicted'],
        mode='lines+markers',
        name='PM2.5 Prezis',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    # Zone AQI
    fig.add_hrect(y0=0, y1=12, fillcolor="#00e400", opacity=0.1, line_width=0)
    fig.add_hrect(y0=12, y1=35.4, fillcolor="#ffff00", opacity=0.1, line_width=0)
    fig.add_hrect(y0=35.4, y1=55.4, fillcolor="#ff7e00", opacity=0.1, line_width=0)
    fig.add_hrect(y0=55.4, y1=150.4, fillcolor="#ff0000", opacity=0.1, line_width=0)
    
    fig.update_layout(
        title="Predicție PM2.5 pentru următoarele 24 de ore",
        xaxis_title="Timp",
        yaxis_title="PM2.5 (μg/m³)",
        hovermode='x unified',
        height=500,
        showlegend=True
    )
    
    return fig


def plot_historical_data(df: pd.DataFrame):
    """Creează grafic pentru datele istorice."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['pm25'],
        mode='lines',
        name='PM2.5 Istoric',
        line=dict(color='#ff7f0e', width=2)
    ))
    
    fig.update_layout(
        title="Date Istorice PM2.5",
        xaxis_title="Timp",
        yaxis_title="PM2.5 (μg/m³)",
        hovermode='x unified',
        height=400
    )
    
    return fig


def plot_weather_correlation(df: pd.DataFrame):
    """Creează grafic de corelație între PM2.5 și factori meteo."""
    fig = go.Figure()
    
    # PM2.5 vs Temperatură
    fig.add_trace(go.Scatter(
        x=df['temperature'],
        y=df['pm25'],
        mode='markers',
        name='Temperatură',
        marker=dict(color='#d62728', size=8, opacity=0.6)
    ))
    
    fig.update_layout(
        title="Corelație PM2.5 vs Temperatură",
        xaxis_title="Temperatură (°C)",
        yaxis_title="PM2.5 (μg/m³)",
        height=400
    )
    
    return fig


def main():
    """Funcție principală pentru aplicația Streamlit."""
    
    # Header
    st.markdown('<h1 class="main-header">🌍 Predicție Calitate Aer</h1>', unsafe_allow_html=True)
    st.markdown("### Predicții PM2.5 bazate pe Machine Learning")
    
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Air_pollution_icon.svg/240px-Air_pollution_icon.svg.png", width=150)
        st.markdown("## ⚙️ Setări")
        
        # Opțiuni locație
        city = st.text_input("Oraș", value="Bucharest")
        country = st.text_input("Țară (cod)", value="RO")
        
        st.markdown("---")
        st.markdown("### 📊 Despre Proiect")
        st.markdown("""
        **Echipa 421 B:**
        - Berciu Antonio
        - Munteanu Radu
        - Roman Silviu
        
        **Tehnologii:**
        - Streamlit
        - scikit-learn
        - OpenAQ API
        - OpenWeatherMap
        """)
    
    # Tabs principale
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔮 Predicții", "📈 Date Istorice", "📊 Analiză", "ℹ️ Despre"
    ])
    
    # Tab 1: Predicții
    with tab1:
        st.markdown("## Predicții PM2.5 pentru următoarele 24 de ore")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("🚀 Generează Predicție", type="primary"):
                with st.spinner("Se încarcă modelul și se generează predicții..."):
                    try:
                        # Inițializează predictor și collector
                        predictor = PM25Predictor()
                        predictor.load_model()
                        collector = DataCollector()
                        
                        # Obține date meteo curente
                        current_weather = collector.get_weather_data(datetime.now())
                        
                        # Generează predicții
                        predictions_df = predictor.predict_next_24h(current_weather)
                        
                        # Salvează în session state
                        st.session_state['predictions'] = predictions_df
                        st.session_state['current_weather'] = current_weather
                        
                        st.success("✅ Predicții generate cu succes!")
                        
                    except FileNotFoundError:
                        st.error("❌ Modelul nu este antrenat. Rulați mai întâi `python src/model.py`")
                    except Exception as e:
                        st.error(f"❌ Eroare: {str(e)}")
        
        with col2:
            if 'current_weather' in st.session_state:
                weather = st.session_state['current_weather']
                st.markdown("### 🌤️ Condiții Meteo Curente")
                st.metric("Temperatură", f"{weather['temperature']:.1f} °C")
                st.metric("Umiditate", f"{weather['humidity']:.0f} %")
                st.metric("Vânt", f"{weather['wind_speed']:.1f} m/s")
        
        # Afișează predicții
        if 'predictions' in st.session_state:
            predictions_df = st.session_state['predictions']
            
            # Metrici principale
            st.markdown("### 📊 Rezumat Predicții")
            col1, col2, col3, col4 = st.columns(4)
            
            current_pm25 = predictions_df.iloc[0]['pm25_predicted']
            avg_pm25 = predictions_df['pm25_predicted'].mean()
            max_pm25 = predictions_df['pm25_predicted'].max()
            min_pm25 = predictions_df['pm25_predicted'].min()
            
            category, color = get_aqi_category(current_pm25)
            
            with col1:
                st.metric("PM2.5 Curent", f"{current_pm25:.1f} μg/m³", 
                         delta=None, delta_color="off")
                st.markdown(f'<div style="background-color:{color}; padding:5px; border-radius:5px; text-align:center; color:white; font-weight:bold;">{category}</div>', 
                           unsafe_allow_html=True)
            
            with col2:
                st.metric("Medie 24h", f"{avg_pm25:.1f} μg/m³")
            
            with col3:
                st.metric("Maxim", f"{max_pm25:.1f} μg/m³")
            
            with col4:
                st.metric("Minim", f"{min_pm25:.1f} μg/m³")
            
            # Grafic predicții
            st.plotly_chart(plot_24h_prediction(predictions_df), use_container_width=True)
            
            # Tabel cu predicții
            with st.expander("📋 Detalii Predicții Orare"):
                display_df = predictions_df.copy()
                display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
                display_df['pm25_predicted'] = display_df['pm25_predicted'].round(2)
                st.dataframe(display_df, use_container_width=True)
    
    # Tab 2: Date Istorice
    with tab2:
        st.markdown("## 📈 Date Istorice PM2.5")
        
        days = st.slider("Selectează numărul de zile", min_value=1, max_value=30, value=7)
        
        if st.button("📥 Încarcă Date Istorice"):
            with st.spinner("Se colectează date..."):
                try:
                    collector = DataCollector()
                    historical_df = collector.get_air_quality_data(days=days)
                    
                    st.session_state['historical_data'] = historical_df
                    st.success(f"✅ {len(historical_df)} înregistrări încărcate")
                    
                except Exception as e:
                    st.error(f"❌ Eroare: {str(e)}")
        
        if 'historical_data' in st.session_state:
            df = st.session_state['historical_data']
            
            # Statistici
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Înregistrări", len(df))
            with col2:
                st.metric("Medie", f"{df['pm25'].mean():.1f} μg/m³")
            with col3:
                st.metric("Maxim", f"{df['pm25'].max():.1f} μg/m³")
            with col4:
                st.metric("Minim", f"{df['pm25'].min():.1f} μg/m³")
            
            # Grafic
            st.plotly_chart(plot_historical_data(df), use_container_width=True)
            
            # Distribuție
            fig_dist = px.histogram(df, x='pm25', nbins=50, 
                                   title="Distribuția Valorilor PM2.5")
            st.plotly_chart(fig_dist, use_container_width=True)
    
    # Tab 3: Analiză
    with tab3:
        st.markdown("## 📊 Analiză Corelații")
        
        if 'historical_data' in st.session_state and 'temperature' in st.session_state['historical_data'].columns:
            df = st.session_state['historical_data']
            
            # Corelații
            st.plotly_chart(plot_weather_correlation(df), use_container_width=True)
            
            # Matrice de corelație
            numeric_cols = ['pm25', 'temperature', 'humidity', 'pressure', 'wind_speed']
            available_cols = [col for col in numeric_cols if col in df.columns]
            
            if len(available_cols) > 1:
                corr_matrix = df[available_cols].corr()
                fig_corr = px.imshow(corr_matrix, 
                                    text_auto=True,
                                    aspect="auto",
                                    title="Matrice de Corelație")
                st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("📥 Încărcați mai întâi date istorice din tab-ul 'Date Istorice'")
    
    # Tab 4: Despre
    with tab4:
        st.markdown("## ℹ️ Despre Aplicație")
        
        st.markdown("""
        ### 🎯 Scop
        Această aplicație prezice nivelul PM2.5 (particule fine) în următoarele 24 de ore 
        utilizând date meteo și algoritmi de machine learning.
        
        ### 🔬 Metodologie
        - **Date**: OpenAQ API pentru PM2.5, OpenWeatherMap pentru meteo
        - **Model**: Random Forest Regressor (scikit-learn)
        - **Features**: temperatură, umiditate, presiune, vânt, ora zilei
        
        ### 📊 Categorii Calitate Aer (EPA Standard)
        """)
        
        categories = [
            ("0-12", "Bună", "#00e400", "Calitatea aerului este satisfăcătoare"),
            ("12-35.4", "Moderată", "#ffff00", "Calitate acceptabilă"),
            ("35.4-55.4", "Nesănătoasă (sensibili)", "#ff7e00", "Grupuri sensibile pot fi afectate"),
            ("55.4-150.4", "Nesănătoasă", "#ff0000", "Toată lumea poate fi afectată"),
            ("150.4-250.4", "Foarte nesănătoasă", "#8f3f97", "Avertisment pentru sănătate"),
            ("250.4+", "Periculoasă", "#7e0023", "Alertă de sănătate"),
        ]
        
        for pm_range, category, color, description in categories:
            st.markdown(f"""
            <div style="background-color:{color}; padding:10px; margin:5px 0; border-radius:5px; color:white;">
                <strong>{pm_range} μg/m³</strong> - {category}: {description}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 👥 Echipa
        - **Berciu Antonio**: Colectare date (OpenAQ, Weather API)
        - **Munteanu Radu**: Model de predicție (Random Forest)
        - **Roman Silviu**: Dashboard și vizualizări (Streamlit)
        - **Documentation & Testing**: Documentare și testare
        
        ### 🔗 Resurse
        - [OpenAQ API](https://openaq.org/)
        - [OpenWeatherMap API](https://openweathermap.org/api)
        - [EPA Air Quality Index](https://www.airnow.gov/aqi/)
        """)


if __name__ == "__main__":
    main()

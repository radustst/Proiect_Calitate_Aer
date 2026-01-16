# Explicație Cod Detaliat - app.py
## Modulul Dashboard Streamlit - Roman Silviu

---

## 📁 Structura Fișierului

Fișierul `src/app.py` conține **384 de linii** organizate în:
- 4 funcții helper (helper functions)
- 1 funcție principală `main()`
- 4 tab-uri interactive (Predicții, Date Istorice, Analiză, Despre)

---

## 📦 PARTEA 1: Import-uri și Configurare (Liniile 1-23)

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
```
**Explicație:**
- `streamlit` = framework pentru dashboard-uri web interactive
- `plotly` = grafice interactive (zoom, hover, export)
- `pandas` = manipulare date
- `datetime` = lucru cu timestamp-uri

**De ce Streamlit?** Cod Python pur → aplicație web (fără HTML/CSS/JavaScript)

---

```python
# Adaugă directorul părinte la path pentru import module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collection import DataCollector
from src.model import PM25Predictor
```
**Explicație:**
- Modifică Python path pentru a importa modulele colegilor
- Import `DataCollector` (Antonio) și `PM25Predictor` (Radu)
- **Integrare completă:** dashboard folosește ambele module

---

## 🎨 PARTEA 2: Configurare Pagină și CSS (Liniile 26-59)

```python
st.set_page_config(
    page_title="Predicție Calitate Aer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)
```
**Explicație:**
- `page_title` = titlu browser tab
- `page_icon` = emoji în tab
- `layout="wide"` = folosește tot lățimea ecranului
- `initial_sidebar_state="expanded"` = sidebar deschis by default

---

```python
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)
```
**Explicație:**
- CSS custom pentru styling
- `unsafe_allow_html=True` = permite HTML/CSS în Streamlit
- Clase pentru header și card-uri

---

## 🏷️ PARTEA 3: Funcție AQI Category (Liniile 61-73)

```python
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
```
**Explicație:**
- Clasificare PM2.5 conform **standardului EPA** (Environmental Protection Agency)
- Returnează tuple (categorie text, culoare hex)

**Scale EPA:**
```
0-12:      Bună (verde)
12-35.4:   Moderată (galben)
35.4-55.4: Nesănătoasă sensibili (portocaliu)
55.4+:     Nesănătoasă/Periculoasă (roșu/mov)
```

---

## 📊 PARTEA 4: Grafic Predicție 24h (Liniile 76-107)

```python
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
```
**Explicație:**
- `go.Figure()` = creează grafic Plotly
- `go.Scatter()` = grafic linie cu puncte
- `mode='lines+markers'` = linie continuă + puncte

---

```python
    # Zone AQI
    fig.add_hrect(y0=0, y1=12, fillcolor="#00e400", opacity=0.1, line_width=0)
    fig.add_hrect(y0=12, y1=35.4, fillcolor="#ffff00", opacity=0.1, line_width=0)
    fig.add_hrect(y0=35.4, y1=55.4, fillcolor="#ff7e00", opacity=0.1, line_width=0)
```
**Explicație:**
- `add_hrect()` = adaugă dreptunghi orizontal (zonă colorată)
- `opacity=0.1` = 10% transparență (fundal subtil)
- **Visual:** fundal colorat pentru fiecare categorie EPA

---

```python
    fig.update_layout(
        title="Predicție PM2.5 pentru următoarele 24 de ore",
        xaxis_title="Timp",
        yaxis_title="PM2.5 (μg/m³)",
        hovermode='x unified',
        height=500
    )
```
**Explicație:**
- `update_layout()` = configurează aspect grafic
- `hovermode='x unified'` = tooltip vertical (arată toate valorile la un X)
- `height=500` = înălțime în pixeli

---

## 📈 PARTEA 5: Grafic Date Istorice (Liniile 110-127)

```python
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
```
**Explicație:** Similar cu predicții, dar doar linie (fără markers) și culoare diferită (portocaliu)

---

## 🔗 PARTEA 6: Grafic Corelație (Liniile 130-150)

```python
def plot_weather_correlation(df: pd.DataFrame):
    """Creează grafic de corelație între PM2.5 și factori meteo."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['temperature'],
        y=df['pm25'],
        mode='markers',
        name='Temperatură',
        marker=dict(color='#d62728', size=8, opacity=0.6)
    ))
```
**Explicație:**
- **Scatter plot** = grafic cu puncte (nu linie)
- Axa X = temperatură, Axa Y = PM2.5
- Vizualizează relația între temperatură și poluare

---

## 🚀 PARTEA 7: Funcția Main - Setup (Liniile 153-195)

```python
def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 Predicție Calitate Aer</h1>', unsafe_allow_html=True)
    st.markdown("### Predicții PM2.5 bazate pe Machine Learning")
```
**Explicație:**
- `st.markdown()` = afișează text Markdown (sau HTML)
- Header principal cu emoji și styling CSS

---

```python
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/...", width=150)
        st.markdown("## ⚙️ Setări")
        
        city = st.text_input("Oraș", value="Bucharest")
        country = st.text_input("Țară (cod)", value="RO")
```
**Explicație:**
- `with st.sidebar:` = tot ce urmează merge în sidebar (panou lateral)
- `st.image()` = afișează imagine din URL
- `st.text_input()` = input box pentru utilizator
- **Interactivitate:** utilizatorul poate schimba orașul

---

```python
        st.markdown("""
        **Echipa 421 B:**
        - Berciu Antonio
        - Munteanu Radu
        - Roman Silviu
        
        **Tehnologii:**
        - Streamlit
        - scikit-learn
        - OpenAQ API
        """)
```
**Explicație:** Informații despre echipă în sidebar

---

## 📑 PARTEA 8: Tabs și Predicții (Liniile 197-273)

```python
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔮 Predicții", "📈 Date Istorice", "📊 Analiză", "ℹ️ Despre"
    ])
```
**Explicație:**
- `st.tabs()` = creează tab-uri (file)
- Returnează 4 obiecte pentru fiecare tab

---

```python
    with tab1:
        st.markdown("## Predicții PM2.5 pentru următoarele 24 de ore")
        
        col1, col2 = st.columns([2, 1])
```
**Explicație:**
- `with tab1:` = conținut pentru primul tab
- `st.columns([2, 1])` = 2 coloane (una dublu față de cealaltă)

---

```python
        with col1:
            if st.button("🚀 Generează Predicție", type="primary"):
                with st.spinner("Se încarcă modelul și se generează predicții..."):
                    try:
                        predictor = PM25Predictor()
                        predictor.load_model()
                        collector = DataCollector()
                        
                        current_weather = collector.get_weather_data(datetime.now())
                        predictions_df = predictor.predict_next_24h(current_weather)
```
**Explicație:**
- `st.button()` = buton clickable
- `st.spinner()` = loading indicator
- **Integrare:** folosește `PM25Predictor` (Radu) și `DataCollector` (Antonio)
- `predict_next_24h()` = generează predicții pentru 24 ore

---

```python
                        st.session_state['predictions'] = predictions_df
                        st.session_state['current_weather'] = current_weather
                        
                        st.success("✅ Predicții generate cu succes!")
```
**Explicație:**
- `st.session_state` = dicționar persistent între reruns
- Salvează predicțiile pentru a le folosi mai târziu
- `st.success()` = mesaj verde de succes

---

```python
                    except FileNotFoundError:
                        st.error("❌ Modelul nu este antrenat. Rulați `python src/model.py`")
                    except Exception as e:
                        st.error(f"❌ Eroare: {str(e)}")
```
**Explicație:** Error handling cu mesaje user-friendly

---

```python
        with col2:
            if 'current_weather' in st.session_state:
                weather = st.session_state['current_weather']
                st.markdown("### 🌤️ Condiții Meteo Curente")
                st.metric("Temperatură", f"{weather['temperature']:.1f} °C")
                st.metric("Umiditate", f"{weather['humidity']:.0f} %")
                st.metric("Vânt", f"{weather['wind_speed']:.1f} m/s")
```
**Explicație:**
- `st.metric()` = card cu valoare mare și label
- Afișează datele meteo în coloana 2

---

```python
        if 'predictions' in st.session_state:
            predictions_df = st.session_state['predictions']
            
            # Metrici principale
            col1, col2, col3, col4 = st.columns(4)
            
            current_pm25 = predictions_df.iloc[0]['pm25_predicted']
            avg_pm25 = predictions_df['pm25_predicted'].mean()
            max_pm25 = predictions_df['pm25_predicted'].max()
            min_pm25 = predictions_df['pm25_predicted'].min()
```
**Explicație:**
- 4 coloane pentru metrici
- `.iloc[0]` = prima predicție (ora curentă)
- `.mean()`, `.max()`, `.min()` = statistici

---

```python
            category, color = get_aqi_category(current_pm25)
            
            with col1:
                st.metric("PM2.5 Curent", f"{current_pm25:.1f} μg/m³")
                st.markdown(f'<div style="background-color:{color}; padding:5px; border-radius:5px; text-align:center; color:white; font-weight:bold;">{category}</div>', 
                           unsafe_allow_html=True)
```
**Explicație:**
- Obține categoria EPA și culoarea
- Afișează card colorat cu categoria

---

```python
            st.plotly_chart(plot_24h_prediction(predictions_df), use_container_width=True)
```
**Explicație:**
- `st.plotly_chart()` = afișează grafic Plotly
- `use_container_width=True` = grafic responsive (umple lățimea)

---

```python
            with st.expander("📋 Detalii Predicții Orare"):
                display_df = predictions_df.copy()
                display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
                display_df['pm25_predicted'] = display_df['pm25_predicted'].round(2)
                st.dataframe(display_df, use_container_width=True)
```
**Explicație:**
- `st.expander()` = secțiune expandabilă/colapsabilă
- `.dt.strftime()` = formatează timestamp ca string
- `st.dataframe()` = tabel interactiv (sortare, scroll)

---

## 📊 PARTEA 9: Tab Date Istorice (Liniile 275-318)

```python
    with tab2:
        st.markdown("## 📈 Date Istorice PM2.5")
        
        days = st.slider("Selectează numărul de zile", min_value=1, max_value=30, value=7)
```
**Explicație:**
- `st.slider()` = slider interactiv pentru selectare număr
- User selectează câte zile de date dorește (1-30)

---

```python
        if st.button("📥 Încarcă Date Istorice"):
            with st.spinner("Se colectează date..."):
                try:
                    collector = DataCollector()
                    historical_df = collector.get_air_quality_data(days=days)
                    
                    st.session_state['historical_data'] = historical_df
                    st.success(f"✅ {len(historical_df)} înregistrări încărcate")
```
**Explicație:**
- Buton pentru a încărca date istorice
- Folosește `DataCollector` (Antonio) pentru a colecta date

---

```python
        if 'historical_data' in st.session_state:
            df = st.session_state['historical_data']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Înregistrări", len(df))
            with col2:
                st.metric("Medie", f"{df['pm25'].mean():.1f} μg/m³")
```
**Explicație:** Afișează statistici despre datele istorice

---

```python
            st.plotly_chart(plot_historical_data(df), use_container_width=True)
            
            fig_dist = px.histogram(df, x='pm25', nbins=50, 
                                   title="Distribuția Valorilor PM2.5")
            st.plotly_chart(fig_dist, use_container_width=True)
```
**Explicație:**
- Grafic serie de timp (trend)
- `px.histogram()` = histogram (distribuție valori)
- `nbins=50` = 50 intervale (buckets)

---

## 🔬 PARTEA 10: Tab Analiză (Liniile 320-343)

```python
    with tab3:
        st.markdown("## 📊 Analiză Corelații")
        
        if 'historical_data' in st.session_state and 'temperature' in st.session_state['historical_data'].columns:
            df = st.session_state['historical_data']
            
            st.plotly_chart(plot_weather_correlation(df), use_container_width=True)
```
**Explicație:**
- Verifică dacă există date istorice ȘI coloana temperature
- Afișează scatter plot PM2.5 vs temperatură

---

```python
            numeric_cols = ['pm25', 'temperature', 'humidity', 'pressure', 'wind_speed']
            available_cols = [col for col in numeric_cols if col in df.columns]
            
            if len(available_cols) > 1:
                corr_matrix = df[available_cols].corr()
                fig_corr = px.imshow(corr_matrix, 
                                    text_auto=True,
                                    aspect="auto",
                                    title="Matrice de Corelație")
                st.plotly_chart(fig_corr, use_container_width=True)
```
**Explicație:**
- `.corr()` = calculează matrice de corelație Pearson
- `px.imshow()` = heatmap (matrice colorată)
- `text_auto=True` = afișează valorile în celule

**Interpretare:**
```
1.0  = corelație perfectă pozitivă
0.0  = fără corelație
-1.0 = corelație perfectă negativă
```

---

## ℹ️ PARTEA 11: Tab Despre (Liniile 345-384)

```python
    with tab4:
        st.markdown("## ℹ️ Despre Aplicație")
        
        st.markdown("""
        ### 🎯 Scop
        Această aplicație prezice nivelul PM2.5 în următoarele 24 de ore 
        utilizând date meteo și algoritmi de machine learning.
        
        ### 🔬 Metodologie
        - **Date**: OpenAQ API pentru PM2.5, OpenWeatherMap pentru meteo
        - **Model**: Random Forest Regressor (scikit-learn)
        - **Features**: temperatură, umiditate, presiune, vânt, ora zilei
        """)
```
**Explicație:** Informații despre metodologie și scop

---

```python
        categories = [
            ("0-12", "Bună", "#00e400", "Calitatea aerului este satisfăcătoare"),
            ("12-35.4", "Moderată", "#ffff00", "Calitate acceptabilă"),
            ("35.4-55.4", "Nesănătoasă (sensibili)", "#ff7e00", "Grupuri sensibile afectate"),
            # ...
        ]
        
        for pm_range, category, color, description in categories:
            st.markdown(f"""
            <div style="background-color:{color}; padding:10px; margin:5px 0; border-radius:5px; color:white;">
                <strong>{pm_range} μg/m³</strong> - {category}: {description}
            </div>
            """, unsafe_allow_html=True)
```
**Explicație:**
- Loop prin categoriile EPA
- Afișează fiecare categorie cu culoarea corespunzătoare

---

## 🎯 Rezumat Flow-ul Aplicației

### Structură Dashboard:

```
1. CONFIGURARE
   ├─ Set page config (wide layout, icon)
   ├─ CSS custom pentru styling
   └─ Import module (DataCollector, PM25Predictor)

2. SIDEBAR
   ├─ Imagine logo
   ├─ Input oraș/țară
   └─ Info echipă

3. TAB PREDICȚII
   ├─ Buton "Generează Predicție"
   ├─ Încarcă model (Radu) + date meteo (Antonio)
   ├─ Generează predicții 24h
   ├─ Afișează metrici (curent, medie, min, max)
   ├─ Grafic interactiv cu zone EPA
   └─ Tabel detaliat expandabil

4. TAB DATE ISTORICE
   ├─ Slider pentru selectare zile (1-30)
   ├─ Buton încărcare date
   ├─ Statistici (count, mean, max, min)
   ├─ Grafic serie de timp
   └─ Histogram distribuție

5. TAB ANALIZĂ
   ├─ Scatter plot PM2.5 vs temperatură
   └─ Heatmap matrice corelație

6. TAB DESPRE
   ├─ Metodologie și scop
   ├─ Categorii EPA cu culori
   └─ Link-uri resurse
```

---

## 💡 Concepte Cheie Streamlit

### 1. **Session State**
```python
st.session_state['predictions'] = predictions_df
# Păstrează date între reruns (când user interacționează)
```

### 2. **Layout**
```python
col1, col2 = st.columns([2, 1])  # Coloane cu raport 2:1
with col1:
    # Conținut coloana 1
```

### 3. **Widgets Interactive**
```python
st.button()      # Buton
st.slider()      # Slider numeric
st.text_input()  # Input text
st.selectbox()   # Dropdown
```

### 4. **Vizualizări**
```python
st.metric()           # Card cu valoare mare
st.plotly_chart()     # Grafic Plotly interactiv
st.dataframe()        # Tabel interactiv
```

### 5. **Mesaje**
```python
st.success()   # Mesaj verde
st.error()     # Mesaj roșu
st.warning()   # Mesaj galben
st.info()      # Mesaj albastru
st.spinner()   # Loading indicator
```

---

## 🎨 Plotly: Tipuri de Grafice

### Scatter (linie cu puncte)
```python
go.Scatter(
    x=df['timestamp'],
    y=df['pm25'],
    mode='lines+markers'  # sau 'lines', 'markers'
)
```

### Histogram
```python
px.histogram(df, x='pm25', nbins=50)
```

### Heatmap (matrice corelație)
```python
px.imshow(correlation_matrix, text_auto=True)
```

### Zone colorate
```python
fig.add_hrect(y0=0, y1=12, fillcolor="#00e400", opacity=0.1)
```

---

## ⚙️ Provocări și Soluții

### Problema 1: State management
**Provocare:** Streamlit rerulează tot scriptul la fiecare interacțiune
**Soluție:** `st.session_state` pentru a păstra predicțiile și datele

### Problema 2: Loading time
**Provocare:** Încărcarea modelului durează câteva secunde
**Soluție:** `st.spinner()` + mesaje de status pentru UX bun

### Problema 3: Responsive design
**Provocare:** Graficele trebuie să se adapteze la lățimea ecranului
**Soluție:** `use_container_width=True` la toate graficele

### Problema 4: Erori modelul neantrenat
**Provocare:** Dacă modelul nu există, aplicația crașează
**Soluție:** Try-except cu mesaje clare pentru utilizator

---

## 🚀 Cum să Prezinți Profesorului

### Structură Prezentare (10-15 min):

**1. Demo Live (5 min)**
- Rulează `streamlit run src/app.py`
- Arată interfața (sidebar, tabs, grafice)
- Click "Generează Predicție" → explică ce se întâmplă:
  - Încarcă modelul Random Forest (Radu)
  - Colectează date meteo (Antonio)
  - Generează predicții 24h
  - Afișează grafic cu zone EPA

**2. Integrare Module (3 min)**
- "Dashboard-ul integrează toate componentele proiectului"
- `PM25Predictor` pentru predicții → Radu
- `DataCollector` pentru date → Antonio
- Streamlit pentru vizualizare → Silviu

**3. Features Cheie (3 min)**
- **Interactivitate:** butoane, slider-e, input-uri
- **Vizualizări:** grafice Plotly (zoom, hover, export PNG)
- **Session State:** păstrează datele între interacțiuni
- **Tabs:** organizare clară (Predicții, Istoric, Analiză, Despre)

**4. Provocări Tehnice (2 min)**
- State management în Streamlit
- Responsive design (layout adaptat)
- Error handling pentru UX bun

**5. Q&A (2 min)**

### Întrebări Posibile:

**Q: "De ce Streamlit și nu Flask/Django?"**
A: "Streamlit e specializat pentru dashboards data science - cod Python pur, fără HTML/CSS/JS. Perfect pentru prototipuri rapide și vizualizări interactive."

**Q: "Cum funcționează session_state?"**
A: "Streamlit rerulează tot scriptul la fiecare click. session_state e un dicționar persistent care păstrează date între reruns - salvez predicțiile ca să nu le regenerez de fiecare dată."

**Q: "De ce Plotly și nu Matplotlib?"**
A: "Plotly generează grafice interactive - zoom, pan, hover tooltips, export PNG. Matplotlib e static. Pentru dashboard-uri web, interactivitatea e esențială."

**Q: "Cum integrezi modulele colegilor?"**
A: "Import direct: `from src.data_collection import DataCollector`. Când user apasă buton → instanțiez `PM25Predictor()`, apelez `.predict_next_24h()`, afișez rezultatul."

---

## 📊 Componente Cheie

### Session State Variables:
```python
st.session_state['predictions']      # DataFrame predicții 24h
st.session_state['current_weather']  # Dict date meteo curente
st.session_state['historical_data']  # DataFrame date istorice
```

### Widgets Folosite:
- `st.button()` - 3 butoane (Generează Predicție, Încarcă Istoric)
- `st.slider()` - 1 slider (zile date istorice)
- `st.text_input()` - 2 inputs (oraș, țară)
- `st.tabs()` - 4 tabs
- `st.columns()` - layout multi-coloană
- `st.expander()` - secțiuni expandabile

### Grafice Plotly:
- `plot_24h_prediction()` - linie cu zone EPA colorate
- `plot_historical_data()` - serie de timp
- `plot_weather_correlation()` - scatter plot
- Histogram - distribuție valori
- Heatmap - matrice corelație

---

## 🎯 Output Final

**Aplicație web accesibilă la:** `http://localhost:8501`

**Funcționalități:**
✅ Predicții PM2.5 pentru 24 ore
✅ Vizualizare date istorice (1-30 zile)
✅ Analiză corelații meteo-poluare
✅ Categorii EPA cu coduri culori
✅ Grafice interactive (zoom, export)
✅ Design responsive (desktop + mobile)

---

**Succes la prezentare, Silviu! 🚀**

*Ai creat un dashboard profesional care integrează colectarea de date (Antonio) și modelul ML (Radu) într-o interfață web intuitivă și interactivă!*

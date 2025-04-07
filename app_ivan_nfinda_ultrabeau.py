
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="💧 Water Health Dashboard - Ivan NFINDA",
    layout="wide",
    page_icon="💧"
)

# CSS styles
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    .stApp {
        background-image: url('https://images.unsplash.com/photo-1508614589041-895b88991e3a?auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        position: relative;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-color: rgba(0, 0, 0, 0.6);
        z-index: -1;
    }

    .block {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0px 0px 25px rgba(0,0,0,0.1);
    }

    .sidebar .block-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }

    h1, h2, h3 {
        color: #073b4c;
    }

    .metric-label {
        font-size: 14px;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='block'>", unsafe_allow_html=True)
st.title("💧 Tableau de bord sur la pollution de l'eau & la santé")
st.markdown("### Visualisation interactive mondiale – Protégeons notre eau, ensemble 🌍")

df = pd.read_csv("water_pollution_disease.csv")

with st.sidebar:
    st.header("🎯 Filtres")
    years = sorted(df['Year'].unique())
    selected_year = st.selectbox("📅 Année", years, index=len(years)-1)
    countries = sorted(df['Country'].unique())
    selected_country = st.selectbox("🌐 Pays", ["Tous"] + countries)

filtered_df = df[df['Year'] == selected_year]
if selected_country != "Tous":
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]

st.markdown("## 📊 Indicateurs clés")
k1, k2, k3, k4 = st.columns(4)
k1.metric("☣️ Contamination (ppm)", f"{filtered_df['Contaminant Level (ppm)'].mean():.2f}")
k2.metric("🦠 Choléra / 100k", f"{filtered_df['Cholera Cases per 100,000 people'].mean():.1f}")
k3.metric("🏥 Accès soins", f"{filtered_df['Healthcare Access Index (0-100)'].mean():.1f} / 100")
k4.metric("🚿 Assainissement", f"{filtered_df['Sanitation Coverage (% of Population)'].mean():.1f}%")

st.markdown("## 📈 Teneur en nitrate par pays")
fig1 = px.line(
    df[df['Country'] == selected_country] if selected_country != "Tous" else df,
    x="Year", y="Nitrate Level (mg/L)", color="Country",
    title="Évolution de la teneur en nitrate (mg/L)"
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("## 🧬 Top 5 pays touchés par le choléra")
top_cholera = df[df['Year'] == selected_year].groupby("Country")["Cholera Cases per 100,000 people"].mean().sort_values(ascending=False).head(5)
fig2 = px.bar(
    top_cholera, x=top_cholera.values, y=top_cholera.index,
    orientation='h', labels={'x': 'Cas pour 100k'}, title="Pays les plus touchés"
)
st.plotly_chart(fig2, use_container_width=True)

if df['Country'].nunique() > 5:
    st.markdown("## 🌍 Carte interactive de la pollution")
    map_data = df[df['Year'] == selected_year]
    fig_map = px.choropleth(
        map_data,
        locations="Country",
        locationmode="country names",
        color="Contaminant Level (ppm)",
        hover_name="Country",
        hover_data={
            "Contaminant Level (ppm)": True,
            "Cholera Cases per 100,000 people": True,
            "Healthcare Access Index (0-100)": True
        },
        color_continuous_scale="YlGnBu",
        title="Niveaux de pollution de l'eau (ppm)"
    )
    fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

st.markdown("## 📋 Données interactives")
st.dataframe(filtered_df, use_container_width=True, height=400)

st.markdown("## 💡 Le saviez-vous ?")
fact = filtered_df.sort_values(by="Lead Concentration (µg/L)", ascending=False).iloc[0]
st.info(f"En {selected_year}, {fact['Country']} avait la concentration en plomb la plus élevée : {fact['Lead Concentration (µg/L)']:.2f} µg/L.")

st.markdown("---")
st.caption("🚀 Conçu avec 💙 par Ivan NFINDA | Python & Streamlit | Agissons ensemble pour une eau plus propre 🌊")
st.markdown("</div>", unsafe_allow_html=True)

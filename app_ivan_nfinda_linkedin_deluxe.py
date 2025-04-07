
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="💧 Water Health Dashboard",
    layout="wide",
    page_icon="💧"
)

# Style CSS : police + style épuré + couleurs
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
    }
    .stApp {
        background-color: #f5f9ff;
    }
    .block {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #004e89;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Image d'en-tête
st.image("header.jpg", use_column_width=True, caption="💧 Pour une eau plus propre, une santé meilleure")

# Conteneur principal
st.markdown("<div class='block'>", unsafe_allow_html=True)
st.title("💧 Tableau de bord sur la pollution de l'eau et son impact sur la santé")
st.markdown("### Analyse interactive des effets sanitaires liés à la qualité de l'eau dans le monde 🌍")

# Chargement des données
df = pd.read_csv("water_pollution_disease.csv")

# Filtres
with st.sidebar:
    st.header("🎯 Filtres")
    years = sorted(df['Year'].unique())
    selected_year = st.selectbox("📅 Année", years, index=len(years)-1)
    countries = sorted(df['Country'].unique())
    selected_country = st.selectbox("🌐 Pays", ["Tous"] + countries)

filtered_df = df[df['Year'] == selected_year]
if selected_country != "Tous":
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]

# KPIs
st.markdown("## 📊 Indicateurs clés")
k1, k2, k3, k4 = st.columns(4)
k1.metric("☣️ Contamination (ppm)", f"{filtered_df['Contaminant Level (ppm)'].mean():.2f}")
k2.metric("🦠 Choléra / 100k", f"{filtered_df['Cholera Cases per 100,000 people'].mean():.1f}")
k3.metric("🏥 Accès soins", f"{filtered_df['Healthcare Access Index (0-100)'].mean():.1f} / 100")
k4.metric("🚿 Assainissement", f"{filtered_df['Sanitation Coverage (% of Population)'].mean():.1f}%")

# Graphique 1
st.markdown("## 📈 Évolution du nitrate dans l'eau")
fig1 = px.line(
    df[df['Country'] == selected_country] if selected_country != "Tous" else df,
    x="Year", y="Nitrate Level (mg/L)", color="Country",
    title="Évolution de la teneur en nitrate (mg/L)"
)
st.plotly_chart(fig1, use_container_width=True)

# Graphique 2
st.markdown("## 🧬 Top 5 pays touchés par le choléra")
top_cholera = df[df['Year'] == selected_year].groupby("Country")["Cholera Cases per 100,000 people"].mean().sort_values(ascending=False).head(5)
fig2 = px.bar(
    top_cholera, x=top_cholera.values, y=top_cholera.index,
    orientation='h', labels={'x': 'Cas pour 100k'}, title="Pays les plus touchés"
)
st.plotly_chart(fig2, use_container_width=True)

# Carte
if df['Country'].nunique() > 5:
    st.markdown("## 🌍 Carte de la pollution par pays")
    map_data = df[df['Year'] == selected_year]
    fig_map = px.choropleth(
        map_data, locations="Country", locationmode="country names",
        color="Contaminant Level (ppm)", color_continuous_scale="Teal",
        title="Pollution de l'eau (ppm)"
    )
    st.plotly_chart(fig_map, use_container_width=True)

# Tableau interactif
st.markdown("## 📋 Données détaillées")
st.dataframe(filtered_df, use_container_width=True, height=400)

# Le saviez-vous ?
st.markdown("## 💡 Le saviez-vous ?")
fact = filtered_df.sort_values(by="Lead Concentration (µg/L)", ascending=False).iloc[0]
st.info(f"En {selected_year}, {fact['Country']} avait la concentration en plomb la plus élevée : {fact['Lead Concentration (µg/L)']:.2f} µg/L.")

# Footer
st.markdown("---")
st.caption("🚀 Créé avec 💙 par Ivan NFINDA | Streamlit + Python + Data Viz | Let’s protect our water, together 🌊")
st.markdown("</div>", unsafe_allow_html=True)

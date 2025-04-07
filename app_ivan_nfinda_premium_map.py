
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration
st.set_page_config(
    page_title="💧 Tableau de bord Eau & Santé - Ivan NFINDA",
    layout="wide",
    page_icon="💧"
)

# Design CSS moderne et lumineux
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
}

.stApp {
    background-color: #eef6fb;
}

h1 {
    text-align: center;
    color: #0077cc;
    margin-bottom: 0.5rem;
}

h3 {
    color: #004e89;
    margin-top: 1.5rem;
}

.block {
    background-color: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 15px rgba(0,0,0,0.05);
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("<h1>💧 Dashboard interactif sur l'impact de la pollution de l'eau sur la santé</h1>", unsafe_allow_html=True)
st.markdown("### Une exploration visuelle des données mondiales de santé et qualité de l'eau 🌍")

# Données
df = pd.read_csv("water_pollution_disease.csv")

# Filtres
with st.sidebar:
    st.header("🎯 Filtres interactifs")
    year = st.selectbox("📅 Année", sorted(df['Year'].unique()), index=len(df['Year'].unique())-1)
    country = st.selectbox("🌐 Pays", ["Tous"] + sorted(df['Country'].unique()))

df_year = df[df["Year"] == year]
df_selected = df_year if country == "Tous" else df_year[df_year["Country"] == country]

# KPIs
st.markdown("## 📊 Indicateurs clés")
col1, col2, col3, col4 = st.columns(4)
col1.metric("☣️ Contamination (ppm)", f"{df_selected['Contaminant Level (ppm)'].mean():.2f}")
col2.metric("🦠 Choléra / 100k", f"{df_selected['Cholera Cases per 100,000 people'].mean():.1f}")
col3.metric("🏥 Accès aux soins", f"{df_selected['Healthcare Access Index (0-100)'].mean():.1f}/100")
col4.metric("🚿 Taux d'assainissement", f"{df_selected['Sanitation Coverage (% of Population)'].mean():.1f}%")

# Graphique interactif
st.markdown("## 📈 Évolution du nitrate dans l'eau")
fig = px.line(
    df[df['Country'] == country] if country != "Tous" else df,
    x="Year", y="Nitrate Level (mg/L)", color="Country",
    title="Évolution de la teneur en nitrate (mg/L)"
)
st.plotly_chart(fig, use_container_width=True)

# Carte interactive améliorée
if df['Country'].nunique() > 5:
    st.markdown("## 🗺️ Carte dynamique des niveaux de pollution")
    map_fig = px.scatter_geo(
        df_year,
        locations="Country",
        locationmode="country names",
        size="Contaminant Level (ppm)",
        color="Contaminant Level (ppm)",
        hover_name="Country",
        hover_data={
            "Cholera Cases per 100,000 people": True,
            "Healthcare Access Index (0-100)": True,
            "Sanitation Coverage (% of Population)": True
        },
        projection="natural earth",
        title="Pollution de l'eau par pays (taille & couleur = niveau de contamination)",
        color_continuous_scale="Turbo",
        size_max=40
    )
    map_fig.update_layout(geo=dict(showframe=False, showcoastlines=False))
    st.plotly_chart(map_fig, use_container_width=True)

# Données tabulaires
st.markdown("## 📋 Aperçu des données")
st.dataframe(df_selected, use_container_width=True, height=400)

# Fun Fact
st.markdown("## 💡 Le saviez-vous ?")
worst = df_selected.sort_values(by="Lead Concentration (µg/L)", ascending=False).head(1)
if not worst.empty:
    row = worst.iloc[0]
    st.warning(f"🚨 En {year}, {row['Country']} a enregistré le taux de plomb le plus élevé : {row['Lead Concentration (µg/L)']:.2f} µg/L.")

# Footer
st.markdown("---")
st.caption("🧠 Réalisé par Ivan NFINDA • Python | Streamlit | Data for Impact 💡")


import streamlit as st
import pandas as pd
import plotly.express as px

# Titre principal
st.set_page_config(page_title="Water Pollution & Health Impact", layout="wide")
st.title("💧 Water Pollution & Health Impact")
st.markdown("Analyse interactive des effets de la pollution de l’eau sur la santé à travers le monde 🌍")

# Chargement des données
df = pd.read_csv("water_pollution_disease.csv")

# Filtres
with st.sidebar:
    st.header("🔍 Filtres")
    years = sorted(df['Year'].unique())
    selected_year = st.selectbox("Sélectionne une année", years, index=len(years)-1)
    countries = sorted(df['Country'].unique())
    selected_country = st.selectbox("Sélectionne un pays", ["Tous"] + countries)

# Filtrage des données
filtered_df = df[df['Year'] == selected_year]
if selected_country != "Tous":
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]

# KPI Cards
st.markdown("### 📊 Indicateurs Clés")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Contamination Moy. (ppm)", f"{filtered_df['Contaminant Level (ppm)'].mean():.2f}")
col2.metric("Cas de Choléra / 100k", f"{filtered_df['Cholera Cases per 100,000 people'].mean():.1f}")
col3.metric("Accès aux soins", f"{filtered_df['Healthcare Access Index (0-100)'].mean():.1f} / 100")
col4.metric("Assainissement (%)", f"{filtered_df['Sanitation Coverage (% of Population)'].mean():.1f}%")

# Graphique 1 - Évolution nitrate
st.markdown("### 📈 Évolution du nitrate dans l'eau")
fig1 = px.line(df[df['Country'] == selected_country] if selected_country != "Tous" else df,
               x="Year", y="Nitrate Level (mg/L)", color="Country",
               title="Teneur en nitrate (mg/L) par an")
st.plotly_chart(fig1, use_container_width=True)

# Graphique 2 - Top pays choléra
st.markdown("### 🦠 Top 5 pays avec le plus de cas de choléra")
top_cholera = df[df['Year'] == selected_year].groupby("Country")["Cholera Cases per 100,000 people"].mean().sort_values(ascending=False).head(5)
fig2 = px.bar(top_cholera, x=top_cholera.values, y=top_cholera.index,
              orientation='h', labels={'x': 'Cas pour 100k'},
              title="Top 5 pays - Choléra")
st.plotly_chart(fig2, use_container_width=True)

# Carte interactive (si assez de pays)
if df['Country'].nunique() > 5:
    st.markdown("### 🌍 Carte interactive de la pollution")
    map_data = df[df['Year'] == selected_year]
    fig_map = px.choropleth(map_data, locations="Country", locationmode="country names",
                            color="Contaminant Level (ppm)",
                            color_continuous_scale="Blues",
                            title="Pollution de l'eau par pays (ppm)")
    st.plotly_chart(fig_map, use_container_width=True)

# Le saviez-vous ?
st.markdown("### 💡 Le saviez-vous ?")
fun_fact = filtered_df.sort_values(by="Lead Concentration (µg/L)", ascending=False).iloc[0]
st.info(f"En {selected_year}, le pays avec le plus haut taux de plomb était **{fun_fact['Country']}** avec **{fun_fact['Lead Concentration (µg/L)']:.2f} µg/L**.")

st.markdown("---")
st.caption("📊 Dashboard réalisé avec Python & Streamlit — Partagez vos insights sur LinkedIn !")

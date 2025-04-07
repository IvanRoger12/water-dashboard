
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="💧 Water & Health Dashboard",
    layout="wide",
    page_icon="💧"
)

# Style CSS personnalisé (fond avec effet et texte stylisé)
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1501594907352-04cda38ebc29');
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }
    .block-container {
        backdrop-filter: blur(4px);
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 10px;
        padding: 2rem;
    }
    h1, h2, h3 {
        color: #00d4ff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Titre avec emoji
st.markdown("<div class='block-container'>", unsafe_allow_html=True)
st.title("💧 Water Pollution & Health Impact Dashboard")
st.markdown("### Analyse interactive de l'impact de la pollution de l’eau sur la santé humaine 🌿")

# Chargement des données
df = pd.read_csv("water_pollution_disease.csv")

# Filtres dans la barre latérale
with st.sidebar:
    st.header("🔍 Filtres")
    years = sorted(df['Year'].unique())
    selected_year = st.selectbox("📅 Année", years, index=len(years)-1)
    countries = sorted(df['Country'].unique())
    selected_country = st.selectbox("🌍 Pays", ["Tous"] + countries)

# Filtrage des données
filtered_df = df[df['Year'] == selected_year]
if selected_country != "Tous":
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]

# Indicateurs clés
st.markdown("## 📊 Indicateurs clés")
k1, k2, k3, k4 = st.columns(4)
k1.metric("☣️ Contamination (ppm)", f"{filtered_df['Contaminant Level (ppm)'].mean():.2f}")
k2.metric("🦠 Choléra / 100k", f"{filtered_df['Cholera Cases per 100,000 people'].mean():.1f}")
k3.metric("🏥 Accès soins", f"{filtered_df['Healthcare Access Index (0-100)'].mean():.1f} / 100")
k4.metric("🚿 Assainissement", f"{filtered_df['Sanitation Coverage (% of Population)'].mean():.1f}%")

# Graphique 1 - évolution du nitrate
st.markdown("## 📈 Évolution du nitrate dans l'eau")
fig1 = px.line(df[df['Country'] == selected_country] if selected_country != "Tous" else df,
               x="Year", y="Nitrate Level (mg/L)", color="Country",
               title="Évolution de la teneur en nitrate (mg/L)")
fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
st.plotly_chart(fig1, use_container_width=True)

# Graphique 2 - top choléra
st.markdown("## 🧬 Top 5 pays touchés par le choléra")
top_cholera = df[df['Year'] == selected_year].groupby("Country")["Cholera Cases per 100,000 people"].mean().sort_values(ascending=False).head(5)
fig2 = px.bar(top_cholera, x=top_cholera.values, y=top_cholera.index,
              orientation='h', labels={'x': 'Cas pour 100k'}, title="Pays les plus touchés")
fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
st.plotly_chart(fig2, use_container_width=True)

# Carte interactive
if df['Country'].nunique() > 5:
    st.markdown("## 🌍 Carte mondiale de la pollution")
    map_data = df[df['Year'] == selected_year]
    fig_map = px.choropleth(map_data, locations="Country", locationmode="country names",
                            color="Contaminant Level (ppm)", color_continuous_scale="blues",
                            title="Pollution de l'eau par pays (ppm)")
    fig_map.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_map, use_container_width=True)

# Section le saviez-vous ?
st.markdown("## 💡 Le saviez-vous ?")
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/728/728093.png", width=60)
with col2:
    fact = filtered_df.sort_values(by="Lead Concentration (µg/L)", ascending=False).iloc[0]
    st.info(f"En {selected_year}, **{fact['Country']}** avait la concentration en plomb la plus élevée : **{fact['Lead Concentration (µg/L)']:.2f} µg/L**.")

# Footer personnalisé
st.markdown("---")
st.caption("🚀 Tableau de bord réalisé avec Streamlit | Design premium 💎 par Ivan NFINDA – Ensemble, agissons pour un futur plus propre 💧")
st.markdown("</div>", unsafe_allow_html=True)

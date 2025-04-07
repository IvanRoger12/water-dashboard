
import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="💧 Water Health Dashboard - Ivan NFINDA",
    layout="wide",
    page_icon="💧"
)

# CSS styling
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

# Header
st.markdown("<h1>💧 Interactive Dashboard on Water Pollution & Health Impact</h1>", unsafe_allow_html=True)
st.markdown("### A global exploration of water quality & human health impact 🌍")

# Data
df = pd.read_csv("water_pollution_disease.csv")

# Sidebar filters
with st.sidebar:
    st.header("🎯 Interactive Filters")
    year = st.selectbox("📅 Year", sorted(df['Year'].unique()), index=len(df['Year'].unique())-1)
    country = st.selectbox("🌐 Country", ["All"] + sorted(df['Country'].unique()))

df_year = df[df["Year"] == year]
df_selected = df_year if country == "All" else df_year[df_year["Country"] == country]

# KPIs
st.markdown("## 📊 Key Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("☣️ Contamination (ppm)", f"{df_selected['Contaminant Level (ppm)'].mean():.2f}")
col2.metric("🦠 Cholera / 100k", f"{df_selected['Cholera Cases per 100,000 people'].mean():.1f}")
col3.metric("🏥 Healthcare Access", f"{df_selected['Healthcare Access Index (0-100)'].mean():.1f}/100")
col4.metric("🚿 Sanitation Coverage", f"{df_selected['Sanitation Coverage (% of Population)'].mean():.1f}%")

# Nitrate chart - top 10 countries
st.markdown("## 📈 Nitrate Level Evolution (Top 10 Countries)")
top_nitrate_countries = df.groupby("Country")["Nitrate Level (mg/L)"].mean().nlargest(10).index
filtered_nitrate = df[df["Country"].isin(top_nitrate_countries)]
fig_nitrate = px.line(
    filtered_nitrate,
    x="Year", y="Nitrate Level (mg/L)", color="Country",
    title="Nitrate Level Trends (mg/L)"
)
st.plotly_chart(fig_nitrate, use_container_width=True)

# Download filtered data
st.download_button("📥 Download Filtered Data (CSV)", df_selected.to_csv(index=False), file_name="filtered_data.csv")

# Interactive map
if df['Country'].nunique() > 5:
    st.markdown("## 🌍 Dynamic Pollution Map")
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
        title="Water Pollution by Country (size & color = contamination level)",
        color_continuous_scale="Turbo",
        size_max=40
    )
    map_fig.update_layout(geo=dict(showframe=False, showcoastlines=False))
    st.plotly_chart(map_fig, use_container_width=True)

# Table
st.markdown("## 📋 Data Overview")
st.dataframe(df_selected, use_container_width=True, height=400)

# Fun Fact
st.markdown("## 💡 Did you know?")
worst = df_selected.sort_values(by="Lead Concentration (µg/L)", ascending=False).head(1)
if not worst.empty:
    row = worst.iloc[0]
    st.warning(f"🚨 In {year}, {row['Country']} recorded the highest lead level: {row['Lead Concentration (µg/L)']:.2f} µg/L.")

# Footer
st.markdown("---")
st.caption("🧠 Built by Ivan NFINDA • Python | Streamlit | Data for Impact 💡")

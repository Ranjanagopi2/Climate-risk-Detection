import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

from analysis import analyze_country  
# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(page_title="Climate Risk Dashboard", layout="wide")
st.title("🌍 Climate Trend & Risk Dashboard")

# -----------------------------
# 1️⃣ Country Selection
# -----------------------------
# For simplicity, you can get country list from CSV
country_df = pd.read_csv("GlobalLandTemperaturesByCountry.csv")
countries = sorted(country_df['Country'].dropna().unique())
selected_country = st.selectbox("Select a Country", countries)

if selected_country:
    # -----------------------------
    # 2️⃣ Run Engine
    # -----------------------------
    result = analyze_country(selected_country)
    
    if result is None:
        st.warning("No data available for this country.")
    else:
        yearly_df = result["yearly_data"]

        # -----------------------------
        # 3️⃣ Historical Trend Plot
        # -----------------------------
        st.subheader("📈 Historical Temperature Anomaly")
        fig, ax = plt.subplots(figsize=(10,4))
        ax.plot(yearly_df['Year'], yearly_df['TemperatureAnomaly'], label='Anomaly')
        ax.axhline(0, color='gray', linestyle='--')
        ax.set_xlabel("Year")
        ax.set_ylabel("Temperature Anomaly (°C)")
        ax.legend()
        st.pyplot(fig)
        comparison_data = []

    


        # -----------------------------
        # 4️⃣ Projection 2050
        # -----------------------------
        st.subheader("🔮 Projection to 2050")
        st.metric("Predicted 2050 Anomaly", f"{result['predicted_2050']:.2f} °C")
        st.metric("Warming Rate per Decade", f"{result['warming_rate_decade']:.2f} °C/decade")
        st.metric("R² of Trend", f"{result['r_squared']:.2f}")

        # -----------------------------
        # 5️⃣ Risk Scores
        # -----------------------------
        st.subheader("⚠️ Climate Risk Assessment")
        st.metric("Hazard Score", f"{result['hazard_score']:.2f}")
        st.metric("Exposure Score", f"{result['exposure_score']:.2f}")
        st.metric("Vulnerability Score", f"{result['vulnerability_score']:.2f}")
        st.metric("Final Risk Score", f"{result['final_risk']:.2f}")
        st.info(f"Risk Level: {result['risk_level']}")

        # -----------------------------
        # 6️⃣ Interpretation Text
        # -----------------------------
        st.subheader("📝 Interpretation")
        st.write(f"""
        The country **{selected_country}** has warmed **{result['current_anomaly']:.2f}°C** since the baseline (1850–1900). 
        The warming rate is approximately **{result['warming_rate_decade']:.2f}°C per decade**. 
        If current trends continue, the projected anomaly in 2050 could reach **{result['predicted_2050']:.2f}°C**. 
        This corresponds to a **{result['risk_level']} risk** level, indicating potential stress on infrastructure, agriculture, and population wellbeing.
        """)

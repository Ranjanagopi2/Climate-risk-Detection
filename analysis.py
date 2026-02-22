import pandas as pd
from scipy import stats
import numpy as np
def analyze_country(country_name):

    # -----------------------------
    # 1️⃣ Load Temperature Data
    # -----------------------------
    df = pd.read_csv("GlobalLandTemperaturesByCountry.csv")

    df['dt'] = pd.to_datetime(df['dt'], errors='coerce')
    df = df.dropna(subset=['dt', 'AverageTemperature'])
    df['Year'] = df['dt'].dt.year
    df = df[df['Year'] >= 1850]
    df = df[df['Country'] == country_name]

    if df.empty:
        return None

    # -----------------------------
    # 2️⃣ Yearly Aggregation
    # -----------------------------
    month_counts = df.groupby('Year').size().reset_index(name='MonthCount')
    yearly_df = df.groupby('Year')['AverageTemperature'].mean().reset_index()
    yearly_df = yearly_df.merge(month_counts, on='Year')
    yearly_df = yearly_df[yearly_df['MonthCount'] >= 10]
    yearly_df = yearly_df.drop(columns=['MonthCount'])
    yearly_df.rename(columns={'AverageTemperature': 'YearlyAvgTemperature'}, inplace=True)
    yearly_df = yearly_df.sort_values('Year').reset_index(drop=True)

    # -----------------------------
    # 3️⃣ Baseline & Anomaly
    # -----------------------------
    baseline = yearly_df[
        (yearly_df['Year'] >= 1850) &
        (yearly_df['Year'] <= 1900)
    ]['YearlyAvgTemperature'].mean()

    yearly_df['TemperatureAnomaly'] = (
        yearly_df['YearlyAvgTemperature'] - baseline
    )

    # -----------------------------
    # 4️⃣ Modern Trend (1950+)
    # -----------------------------
    modern_df = yearly_df[yearly_df['Year'] >= 1950]

    x_mod = modern_df['Year'] - 1950
    y_mod = modern_df['TemperatureAnomaly']

    slope_mod, intercept_mod, r_mod, p_mod, std_err_mod = stats.linregress(
        x_mod, y_mod
    )

    pred_2050 = intercept_mod + slope_mod * (2050 - 1950)

    modern_slope_decade = slope_mod * 10
    r_squared = r_mod**2
    current_anomaly = yearly_df.iloc[-1]['TemperatureAnomaly']

    # -----------------------------
    # 5️⃣ Hazard Score
    # -----------------------------
    anomaly_score = min(current_anomaly / 2.0, 1) * 40
    slope_score = min(modern_slope_decade / 0.3, 1) * 40
    confidence_score = r_squared * 20

    hazard_score = anomaly_score + slope_score + confidence_score

    # -----------------------------
    # 6️⃣ Load Population & GDP
    # -----------------------------
    pop_df = pd.read_csv("API_SP.POP.TOTL_DS2_en_csv_v2_40826.csv", skiprows=4)
    gdp_df = pd.read_csv("API_NY.GDP.PCAP.CD_DS2_en_csv_v2_31.csv", skiprows=4)

    latest_year = "2022"

    pop_df = pop_df[['Country Name', latest_year]].copy()
    gdp_df = gdp_df[['Country Name', latest_year]].copy()

    pop_df.columns = ['Country', 'Population']
    gdp_df.columns = ['Country', 'GDP']

    pop_df['Population'] = pd.to_numeric(pop_df['Population'], errors='coerce')
    gdp_df['GDP'] = pd.to_numeric(gdp_df['GDP'], errors='coerce')

    pop_df = pop_df.dropna()
    gdp_df = gdp_df.dropna()

    country_pop = pop_df[pop_df['Country'] == country_name]
    country_gdp = gdp_df[gdp_df['Country'] == country_name]

    if country_pop.empty or country_gdp.empty:
        return None

    population = float(country_pop['Population'].iloc[0])
    gdp = float(country_gdp['GDP'].iloc[0])

    max_pop = pop_df['Population'].max()
    gdp_min = gdp_df['GDP'].min()
    gdp_max = gdp_df['GDP'].max()

    exposure_score = (population / max_pop) * 100

    if gdp_max != gdp_min:
        gdp_normalized = (gdp - gdp_min) / (gdp_max - gdp_min)
    else:
        gdp_normalized = 0

    vulnerability_score = (1 - gdp_normalized) * 100

    # -----------------------------
    # 7️⃣ Final Risk
    # -----------------------------
    final_risk = (
        hazard_score * 0.5 +
        exposure_score * 0.3 +
        vulnerability_score * 0.2
    )

    if final_risk >= 80:
        level = "Critical"
    elif final_risk >= 60:
        level = "High"
    elif final_risk >= 30:
        level = "Moderate"
    else:
        level = "Low"

    # -----------------------------
    # 8️⃣ RETURN DATA (IMPORTANT)
    # -----------------------------
    return {
        "yearly_data": yearly_df,
        "current_anomaly": current_anomaly,
        "warming_rate_decade": modern_slope_decade,
        "predicted_2050": pred_2050,
        "r_squared": r_squared,
        "hazard_score": hazard_score,
        "exposure_score": exposure_score,
        "vulnerability_score": vulnerability_score,
        "final_risk": final_risk,
        "risk_level": level
    }

🌍 Global Climate Risk Dashboard

An interactive Streamlit-based analytics dashboard that analyzes historical temperature trends, projects future warming, and evaluates country-level climate risk using hazard, exposure, and vulnerability metrics.

📌 Project Overview

This project transforms raw climate, population, and economic data into actionable insights through:

Historical temperature anomaly analysis

Linear regression-based 2050 projections

Climate risk scoring framework

Multi-country comparison

Executive-ready interactive dashboard

The goal is to support data-driven climate awareness and regional risk assessment.

📊 Features
1️⃣ Historical Climate Trend Analysis

Computes yearly average temperatures.

Calculates temperature anomalies relative to 1850–1900 baseline.

Visualizes long-term warming patterns.

2️⃣ Future Projections (2050)

Uses linear regression to estimate:

Warming rate (°C per decade)

Predicted temperature anomaly in 2050

R² goodness-of-fit metric

3️⃣ Climate Risk Assessment Model

The final risk score is derived from:

Hazard Score → Magnitude of temperature anomaly + warming rate

Exposure Score → Population size

Vulnerability Score → GDP per capita (economic resilience proxy)

Outputs:

Final Risk Score

Risk Level (Low / Moderate / High / Critical)

4️⃣ Multi-Country Comparison

Compare warming trends across multiple countries.

Side-by-side risk metrics.

🛠️ Tech Stack

Python 3.x

Streamlit

Pandas

NumPy

Matplotlib

SciPy (Linear Regression)

📂 Dataset Sources

Global Land Temperature Dataset

World Bank Population Data

World Bank GDP per Capita Data

🚀 Installation & Setup
1. Clone the repository
git clone <your-repo-url>
cd <project-folder>
2. Install dependencies
python -m pip install streamlit pandas matplotlib scipy
3. Run the dashboard
python -m streamlit run step2_dashboard.py

Open the local URL shown in the terminal (usually http://localhost:8501
).

🧠 How It Works

Data is cleaned and aggregated by country and year.

Baseline temperature (1850–1900) is calculated.

Temperature anomaly is computed.

Linear regression estimates warming rate and 2050 projection.

Risk scores are computed using normalized hazard, exposure, and vulnerability indicators.

Results are displayed in an interactive dashboard.

📈 Use Cases

Climate risk awareness

Academic analysis

Regional comparison studies

Policy planning support

Hackathon demonstration

⚠️ Limitations

Linear regression assumes constant trend.

GDP used as proxy for vulnerability (simplified assumption).

Does not include precipitation or extreme event data.

🔮 Future Improvements

Add uncertainty intervals for projections

Include additional climate indicators (precipitation, sea level)

Integrate map-based risk visualization

Deploy to Streamlit Cloud

📎 License

This project is for educational and analytical purposes.

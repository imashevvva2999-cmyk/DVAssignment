import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(page_title="Bike Rental Dashboard", layout="wide")

# Set styling
sns.set(style="whitegrid")
plt.rcParams['figure.facecolor'] = 'white'

# Load and prepare data
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df["datetime"] = pd.to_datetime(df["datetime"])
    
    # Create new features
    df["year"] = df["datetime"].dt.year
    df["month"] = df["datetime"].dt.month
    df["dayofweek"] = df["datetime"].dt.dayofweek
    df["hour"] = df["datetime"].dt.hour
    
    # Map season names
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    df["season"] = df["season"].map(season_map)
    
    # Create day period
    def hour_to_period(hour):
        if 0 <= hour < 6:
            return "Night"
        elif 6 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 18:
            return "Afternoon"
        else:
            return "Evening"
    
    df["day_period"] = df["hour"].apply(hour_to_period)
    
    # Map day of week names
    day_map = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 
               4: "Friday", 5: "Saturday", 6: "Sunday"}
    df["dayofweek_name"] = df["dayofweek"].map(day_map)
    
    # Map weather descriptions
    weather_map = {
        1: "Clear/Partly Cloudy",
        2: "Mist/Cloudy",
        3: "Light Snow/Rain",
        4: "Heavy Rain/Snow"
    }
    df["weather_desc"] = df["weather"].map(weather_map)
    
    # Map working day
    df["working_status"] = df["workingday"].map({0: "Non-Working Day", 1: "Working Day"})
    
    return df

df = load_data()

# Sidebar for navigation and filters
st.sidebar.title("🚴 Dashboard Controls")
st.sidebar.markdown("---")

# Interactive widget 1: Year filter
years_available = sorted(df["year"].unique())
selected_years = st.sidebar.multiselect(
    "📅 Select Year(s):",
    options=years_available,
    default=years_available
)

# Interactive widget 2: Season filter
seasons = sorted(df["season"].unique())
selected_seasons = st.sidebar.multiselect(
    "🌤️ Select Season(s):",
    options=seasons,
    default=seasons
)

# Interactive widget 3: Working day filter
working_status_options = ["All", "Working Day", "Non-Working Day"]
selected_working_status = st.sidebar.selectbox(
    "🏢 Select Working Status:",
    options=working_status_options,
    index=0
)

# Apply filters
df_filtered = df[
    (df["year"].isin(selected_years)) & 
    (df["season"].isin(selected_seasons))
]

if selected_working_status != "All":
    df_filtered = df_filtered[df_filtered["working_status"] == selected_working_status]

# Main dashboard
st.title("🚴 Bike Rental Dashboard")
st.markdown("**Interactive dashboard summarizing bike rental trends from 2011-2012**")
st.markdown("---")

# Display key metrics
col1, col2, col3, col4 = st.columns(4)

total_rentals = df_filtered["count"].sum()
avg_hourly_rentals = df_filtered["count"].mean()
total_casual = df_filtered["casual"].sum()
total_registered = df_filtered["registered"].sum()

col1.metric("Total Rentals", f"{int(total_rentals):,}")
col2.metric("Avg Hourly Rentals", f"{avg_hourly_rentals:.0f}")
col3.metric("Total Casual Users", f"{int(total_casual):,}")
col4.metric("Total Registered Users", f"{int(total_registered):,}")

st.markdown("---")

# Row 1: Rentals by Hour and Working Status
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Mean Hourly Rentals by Hour of Day")
    mean_hour = df_filtered.groupby("hour")["count"].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(mean_hour["hour"], mean_hour["count"], marker="o", linewidth=2, markersize=6, color="#1f77b4")
    ax.set_xlabel("Hour of Day", fontsize=11)
    ax.set_ylabel("Mean Hourly Rentals", fontsize=11)
    ax.set_xticks(range(0, 24, 2))
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("📈 Working vs Non-Working Days")
    mean_working = df_filtered.groupby("working_status")["count"].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#ff7f0e", "#2ca02c"]
    ax.bar(mean_working["working_status"], mean_working["count"], color=colors)
    ax.set_ylabel("Mean Hourly Rentals", fontsize=11)
    ax.set_title("Average Rentals: Working vs Non-Working Days", fontsize=12, fontweight="bold")
    ax.grid(True, alpha=0.3, axis="y")
    for i, v in enumerate(mean_working["count"]):
        ax.text(i, v + 2, f"{v:.0f}", ha="center", va="bottom", fontweight="bold")
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# Row 2: Seasonal Trends
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ Mean Rentals by Season")
    season_mean = df_filtered.groupby("season")["count"].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_season = ["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4"]
    ax.barh(season_mean.index, season_mean.values, color=colors_season)
    ax.set_xlabel("Mean Hourly Rentals", fontsize=11)
    ax.grid(True, alpha=0.3, axis="x")
    for i, v in enumerate(season_mean.values):
        ax.text(v + 2, i, f"{v:.0f}", va="center", fontweight="bold")
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("🌦️ Mean Rentals by Weather")
    weather_mean = df_filtered.groupby("weather_desc")["count"].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_weather = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    ax.bar(range(len(weather_mean)), weather_mean.values, color=colors_weather)
    ax.set_xticks(range(len(weather_mean)))
    ax.set_xticklabels(weather_mean.index, rotation=45, ha="right")
    ax.set_ylabel("Mean Hourly Rentals", fontsize=11)
    ax.grid(True, alpha=0.3, axis="y")
    for i, v in enumerate(weather_mean.values):
        ax.text(i, v + 2, f"{v:.0f}", ha="center", va="bottom", fontweight="bold")
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# Row 3: Day Period Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("⏰ Mean Rentals by Day Period")
    day_period_order = ["Night", "Morning", "Afternoon", "Evening"]
    day_period_data = df_filtered.groupby("day_period")["count"].mean().reindex(day_period_order)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_period = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    ax.bar(day_period_data.index, day_period_data.values, color=colors_period)
    ax.set_ylabel("Mean Hourly Rentals", fontsize=11)
    ax.grid(True, alpha=0.3, axis="y")
    for i, v in enumerate(day_period_data.values):
        ax.text(i, v + 2, f"{v:.0f}", ha="center", va="bottom", fontweight="bold")
    st.pyplot(fig)
    plt.close()

with col1:
    st.subheader("📅 Mean Rentals by Day of Week")
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_data = df_filtered.groupby("dayofweek_name")["count"].mean().reindex(day_order)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_days = ["#1f77b4"] * 5 + ["#ff7f0e", "#2ca02c"]  # Weekdays and weekends
    ax.bar(range(len(day_data)), day_data.values, color=colors_days)
    ax.set_xticks(range(len(day_data)))
    ax.set_xticklabels(day_data.index, rotation=45, ha="right")
    ax.set_ylabel("Mean Hourly Rentals", fontsize=11)
    ax.grid(True, alpha=0.3, axis="y")
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# Row 4: Correlation Heatmap
st.subheader("🔗 Correlation Matrix of Numerical Variables")
numeric_cols = df_filtered.select_dtypes(include=["int64", "float64"]).columns
corr_matrix = df_filtered[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0, 
            cbar_kws={"label": "Correlation"}, ax=ax)
ax.set_title("Correlation Heatmap", fontsize=12, fontweight="bold", pad=20)
st.pyplot(fig)
plt.close()

st.markdown("---")

# Footer
st.markdown("### 📊 Data Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Records Displayed", f"{len(df_filtered):,}")
col2.metric("Date Range", f"{df_filtered['datetime'].min().date()} to {df_filtered['datetime'].max().date()}")
col3.metric("Avg Temperature", f"{df_filtered['temp'].mean():.1f}°C")

st.markdown("---")
st.markdown("**Dashboard created for Data Visualization Assignment III**")
st.markdown("Dataset: Bike Rental Demand (2011-2012)")

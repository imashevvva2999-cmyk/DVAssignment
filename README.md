# 🚴 Bike Rental Interactive Dashboard

This is an interactive dashboard created with Streamlit that summarizes findings from exploratory data analysis and visualization of bike rental data (2011-2012).

## 📊 Dashboard Features

### Interactive Widgets (3+):
1. **Year Filter** - Select one or multiple years (2011, 2012)
2. **Season Filter** - Select one or multiple seasons (Spring, Summer, Fall, Winter)
3. **Working Status Filter** - Filter by Working Days, Non-Working Days, or All

### Visualizations (6 plots):
1. **Mean Hourly Rentals by Hour of Day** - Line plot showing rental patterns throughout the day
2. **Working vs Non-Working Days** - Bar chart comparing average rentals
3. **Mean Rentals by Season** - Horizontal bar chart showing seasonal trends
4. **Mean Rentals by Weather** - Bar chart showing weather impact on rentals
5. **Mean Rentals by Day Period** - Bar chart showing rentals across Night/Morning/Afternoon/Evening
6. **Mean Rentals by Day of Week** - Bar chart showing weekday vs weekend patterns
7. **Correlation Heatmap** - Shows correlations between all numerical variables

### Key Metrics:
- Total Rentals
- Average Hourly Rentals
- Total Casual Users
- Total Registered Users
- Record Count
- Date Range
- Average Temperature

## 🚀 Local Setup & Running

### Prerequisites:
- Python 3.8 or higher
- pip package manager

### Installation Steps:

1. Navigate to the project directory:
```bash
cd /Users/kalemaimasheva/Desktop/DV\ Assignment
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## 📤 Deploy to Streamlit Community Cloud

### Step 1: Prepare Your Repository
1. Create a GitHub repository for your project
2. Push the following files to your repository:
   - `app.py`
   - `requirements.txt`
   - `train.csv` (your dataset)
   - `.streamlit/config.toml` (optional, for custom styling)
   - `README.md` (this file)

```bash
# Example git commands
git init
git add .
git commit -m "Initial commit: Bike rental dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud
1. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
2. Sign up with your GitHub account (if you haven't already)
3. Click "New app" button
4. Select your repository, branch, and the file path (`app.py`)
5. Click "Deploy"

Your app will be deployed at: `https://YOUR_USERNAME-REPO_NAME.streamlit.app`

### Step 3: Share Your Dashboard
Once deployed, you can share the URL with others. The dashboard will automatically update when you push changes to your GitHub repository.

## 📊 Dashboard Insights

### Key Findings from the Data:

1. **Hourly Patterns**: Rentals peak during commute hours (8-9 AM and 5-6 PM) on working days
2. **Working Days Impact**: More bikes are rented by registered users on working days
3. **Seasonal Trends**: Fall has the highest average rentals, while Spring has the lowest
4. **Weather Effect**: Clear weather sees significantly higher rentals than heavy rain/snow
5. **Day Period**: Afternoon and Evening have the highest rental counts
6. **Weekend vs Weekday**: Different patterns emerge with more casual users on weekends

## 📁 File Structure

```
DV Assignment/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── train.csv             # Bike rental dataset
├── README.md             # This file
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

## 🎨 Customization

You can customize the dashboard by:
- Modifying colors in `.streamlit/config.toml`
- Adjusting plot sizes and styles in `app.py`
- Adding more filters or visualizations
- Changing the theme colors in the sidebar

## 📝 Notes

- The dataset contains hourly bike rental data from 2011-2012
- All data processing is cached for optimal performance
- Filters are applied in real-time for interactive exploration
- The dashboard is responsive and works on mobile devices

## 🔗 Data Source

The bike rental dataset includes features:
- `datetime`: Timestamp of the rental
- `season`: Spring, Summer, Fall, Winter
- `holiday`: Whether the day is a holiday
- `workingday`: Whether the day is a working day
- `weather`: Weather condition (1-4)
- `temp`: Temperature in Celsius
- `humidity`: Humidity level
- `windspeed`: Wind speed
- `casual`: Number of casual users
- `registered`: Number of registered users
- `count`: Total number of rentals

---

**Created for: Data Visualization Assignment III**  
**Last Updated:** January 2026

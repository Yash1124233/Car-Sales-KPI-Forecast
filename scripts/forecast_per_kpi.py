import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os

# Load dataset
df = pd.read_csv("data/FS-data-80475.csv")

# Step 1: Create proper datetime column
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str) + '-01')

# Step 2: Pick one KPI to forecast (example: "monthly_value")
# Filter for one dealer + KPI
dealer_code = 80475
kpi = "monthly_value"

df_filtered = df[df['dealer_code'] == dealer_code].copy()

# Aggregate by date
ts = df_filtered.groupby('date')[kpi].sum()

# Step 3: Fit ARIMA model
model = sm.tsa.arima.ARIMA(ts, order=(1,1,1))
results = model.fit()

# Step 4: Forecast next 3 months
forecast = results.forecast(steps=3)

print("Forecasted values:")
print(forecast)

# Step 5: Save forecast to CSV for Power BI
output = pd.DataFrame({
    "date": pd.date_range(start=ts.index.max() + pd.offsets.MonthBegin(1), periods=3, freq='MS'),
    "forecast_value": forecast
})

os.makedirs("output", exist_ok=True)
output.to_csv("output/forecast_result.csv", index=False)

print("✅ Forecast saved to output/forecast_result.csv")

# Step 6: Plot actual vs forecast
plt.figure(figsize=(10,5))
plt.plot(ts.index, ts.values, label="Actual")
plt.plot(output['date'], output['forecast_value'], label="Forecast", linestyle="--")
plt.legend()
plt.show()

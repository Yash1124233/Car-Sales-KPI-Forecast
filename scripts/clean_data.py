import pandas as pd

df = pd.read_csv("../data/FS-data-80475.csv")

df["date"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"].astype(str) + "-01")

# columns
df = df[["account_id", "english_name", "dealer_code", "date", "monthly_value"]]

df = df.drop_duplicates()

# Sort for time-series order
df = df.sort_values(["account_id", "date"])

# 
df.to_csv("../cleaned_data/kpi_cleaned.csv", index=False)

print(" Data cleaned and saved at cleaned_data/kpi_cleaned.csv")

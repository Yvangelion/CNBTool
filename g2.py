import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Load the JSON file
with open('cars.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame and clean
df = pd.DataFrame(data)

# Clean columns
df['Sold Price'] = df['Sold Price'].replace('[\$,]', '', regex=True).astype(float)
df['Sold Date'] = pd.to_datetime(df['Sold Date'])
df['Bids'] = df['Bids'].astype(int)
df['Comments'] = df['Comments'].astype(int)

# 1. Scatter Plot: Price over Time, colored by Trim
plt.figure(figsize=(12, 6))
for trim in df['Trim'].unique():
    subset = df[df['Trim'] == trim]
    plt.scatter(subset['Sold Date'], subset['Sold Price'], label=trim, alpha=0.7)

plt.title('Tesla Model 3 Sold Prices Over Time by Trim')
plt.xlabel('Sold Date')
plt.ylabel('Sold Price (USD)')
plt.legend(title="Trim", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig("price_over_time_by_trim.png")
plt.show()

# 2. Bar Chart: Average Price by Trim
avg_price_by_trim = df.groupby('Trim')['Sold Price'].mean().sort_values()

plt.figure(figsize=(10, 6))
avg_price_by_trim.plot(kind='barh', color='skyblue')
plt.title('Average Sold Price by Trim')
plt.xlabel('Average Price (USD)')
plt.ylabel('Trim')
plt.tight_layout()
plt.savefig("average_price_by_trim.png")
plt.show()

# 3. Line Chart: Average Sold Price Over Time by Trim
df['Sold Month'] = df['Sold Date'].dt.to_period('M')
avg_price_trend = df.groupby(['Trim', 'Sold Month'])['Sold Price'].mean().reset_index()
avg_price_trend['Sold Month'] = avg_price_trend['Sold Month'].dt.to_timestamp()

plt.figure(figsize=(12, 6))
for trim in avg_price_trend['Trim'].unique():
    subset = avg_price_trend[avg_price_trend['Trim'] == trim]
    plt.plot(subset['Sold Month'], subset['Sold Price'], label=trim)

plt.title('Average Tesla Model 3 Sold Prices Over Time by Trim')
plt.xlabel('Sold Month')
plt.ylabel('Average Sold Price (USD)')
plt.legend(title="Trim", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig("avg_price_trend_by_trim.png")
plt.show()

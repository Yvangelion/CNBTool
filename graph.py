import json
import plotly.express as px

# Load JSON data
with open("cars.json", "r") as f:
    cars = json.load(f)

# Normalize data
data = []
for car in cars:
    trim = car["Trim"].strip()
    if trim == "3":
        trim = "3 RWD"
    
    price_str = car["Sold Price"].replace("$", "").replace(",", "")
    price = int(price_str)

    date = car.get("Date Sold", "Unknown")
    year = car["Year"]

    data.append({
        "Trim": trim,
        "Sold Price": price,
        "Year": year,
        "Date": date
    })

# Create scatter plot with hover info
fig = px.scatter(
    data,
    x="Trim",
    y="Sold Price",
    color="Trim",
    hover_data=["Sold Price", "Date","Trim","Year"],
    title="Tesla Model 3 Sales: Price by Trim",
)

fig.update_traces(marker=dict(size=10), selector=dict(mode='markers'))
fig.update_layout(
    xaxis_title="Trim",
    yaxis_title="Sold Price ($)",
    hovermode="closest"
)

import plotly.offline as pyo

# Replace fig.show() with this:
pyo.plot(fig, filename='plot.html', auto_open=True)

import pandas as pd
import plotly.express as px
import country_converter as coco
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("corruptibility_scores.csv")

# Convert country names to ISO3 codes
data["iso_alpha"] = coco.convert(names=data["country"], to="ISO3")

# Create interactive map
fig = px.choropleth(
    data,
    locations="iso_alpha",
    color="corruptibility_percent",
    hover_name="country",
    color_continuous_scale="Reds",
    title="Corruption Percentage by Country"
)
fig.write_html("corruption_map_Stat.html")
print("Interactive map saved as corruption_map.html")

# Filter for selected countries
selected_countries = ["United States", "Russia", "China", "Saudi Arabia", "Venezuela"]
subset = data[data["country"].isin(selected_countries)]

# Create bar chart
sns.barplot(
    x="country",
    y="corruptibility_percent",
    data=subset,
    palette="Reds"
)
plt.title("Corruption Percentage for Selected Countries")
plt.ylabel("Corruptibility %")
plt.xlabel("Country")
plt.tight_layout()
plt.show()

# corruption_map.py
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

# load data
df = pd.read_csv("corruptibility_scores.csv")
df.rename(columns={"Country": "country"}, inplace=True)


# map (uses the 'country' column directly)
fig_map = px.choropleth(
    df,
    locations="country",
    locationmode="country names",
    color="corruptibility_percent",
    hover_name="country",
    color_continuous_scale="Reds",
    range_color=(0, 100),
    title="Corruptibility Percentage (%) by Country"
)

# selected countries
want = ["United States", "Russia", "China", "Saudi Arabia", "Venezuela"]
sub = df[df["country"].isin(want)].copy()

# bar chart and PNG export
plt.figure(figsize=(8, 5))
plt.bar(sub["country"], sub["corruptibility_percent"])
plt.ylabel("Corruptibility %")
plt.ylim(0, 100)
plt.title("Selected Countries")
for i, v in enumerate(sub["corruptibility_percent"].tolist()):
    plt.text(i, v + 1, f"{v:.2f}%", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("selected_countries_corruptibility.png", dpi=150)

# streamlit layout
st.title("Corruption Visualization")
st.plotly_chart(fig_map, use_container_width=True)
st.subheader("Selected Countries (PNG also saved)")
st.image("selected_countries_corruptibility.png")

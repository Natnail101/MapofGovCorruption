import pandas as pd
import plotly.express as px
import country_converter as coco

csv_path = "corruptibility_scores.csv"
df = pd.read_csv(csv_path)

df["country_original"] = df["country"]

cc = coco.CountryConverter()
df["iso3"] = cc.convert(names=df["country"], to="ISO3", not_found=None)

unmatched = df[df["iso3"].isna()]["country"].tolist()
if unmatched:
    print("Unmatched country names:")
    for name in unmatched:
        print(" -", name)

manual_map = {
    # "Example Country": "XXX"
}
if manual_map:
    df.loc[df["country"].isin(manual_map.keys()), "iso3"] = df["country"].map(manual_map)

mapped = df.dropna(subset=["iso3"]).copy()

fig = px.choropleth(
    mapped,
    locations="iso3",
    color="corruptibility_percent",
    color_continuous_scale="Reds",
    range_color=(0, 100),
    hover_name="country_original",
    labels={"corruptibility_percent": "Corruptibility %"},
    title="Government Corruptibility Percentage(%) by Country",
)

fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Corruptibility: %{z:.2f}%<extra></extra>")
fig.update_layout(margin=dict(l=10, r=10, t=50, b=10), geo=dict(showframe=False, showcoastlines=True))

fig.show()
fig.write_html("corruptibility_map.html", include_plotlyjs="cdn")
print("Saved: corruptibility_map.html")

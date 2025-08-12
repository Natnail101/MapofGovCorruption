import pandas as pd
from sklearn.linear_model import LinearRegression

# load the csv file
file_path = r"C:\Users\natna\Desktop\FinalProject\Fully_Mapped_Country_Data_with_Regions.csv"
data = pd.read_csv(file_path)

# make risk values (higher number = more corruptible)
data["cpi_risk"] = 100 - data["corruption_perceptions_index"]
data["trust_gov_risk"] = 100 - data["trust_in_government_index"]
data["trust_news_risk"] = 100 - data["trust_in_news_media_index"]
data["press_freedom_risk"] = ((5 - data["press_freedom_index"]) / 4) * 100

# train a regression model
X = data[["trust_gov_risk", "trust_news_risk", "press_freedom_risk"]]
y = data["cpi_risk"]
model = LinearRegression()
model.fit(X, y)

# get weights and normalize them
raw_weights = model.coef_
total = sum(raw_weights)
weights = raw_weights / total

# predict risk using weights
predicted_risk = (
    weights[0] * data["trust_gov_risk"] +
    weights[1] * data["trust_news_risk"] +
    weights[2] * data["press_freedom_risk"]
)

# final score is average of cpi risk and predicted risk
data["corruptibility_percent"] = (
    0.5 * data["cpi_risk"] + 0.5 * predicted_risk
).round(2)

# keep only Country and Corruptibility Percentage
final_data = data[["country", "corruptibility_percent"]]

# save to a new csv
output_file = "corruptibility_scores.csv"
final_data.to_csv(output_file, index=False)

print("Weights (normalized):", weights)
print("File saved as:", output_file)

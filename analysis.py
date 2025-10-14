import geopandas as gpd                                                                                      # type: ignore
import matplotlib.pyplot as plt                                                                               # type: ignore

gdf = gpd.read_file("data/Great_Crested_Newt_Risk_Zones_Norfolk_And_Suffolk.geojson")


gdf.columns = gdf.columns.str.lower()

# Drop unnecessary columns
gdf = gdf[['risk_zone', 'area_ha', 'geometry']]


# Remove any rows without a valid zone
gdf = gdf.dropna(subset=['risk_zone'])

summary = (
    gdf.groupby("risk_zone")["area_ha"]
    .sum()
    .reset_index()
    .sort_values(by="area_ha", ascending=False)
)

total_area = summary["area_ha"].sum()
summary["percent"] = (summary["area_ha"] / total_area * 100).round(2)

summary["area_ha_formatted"] = summary["area_ha"].round(2).map("{:,.2f}".format)
print(f"{'Risk Zone':<15}{'Area (ha)':>20}{'Percent':>12}")
print("-" * 50)
for _, row in summary.iterrows():
    print(f"{row['risk_zone']:<15}{row['area_ha_formatted']:>20}{row['percent']:>12.2f}%")


fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(column="risk_zone", legend=True, cmap="Set2", ax=ax, edgecolor="black")
plt.title("Great Crested Newt Risk Zones – Norfolk & Suffolk", fontsize=14)
plt.axis("off")
plt.show()

plt.figure(figsize=(8, 5))
bars = plt.bar(summary["risk_zone"], summary["percent"], color=["#4CAF50", "#FFC107", "#F44336", "#9E9E9E"])
plt.title("Great Crested Newt Risk Zones – Norfolk & Suffolk")
plt.ylabel("Percentage of Total Area (%)")
plt.xlabel("Risk Zone")
plt.tight_layout()
plt.show()

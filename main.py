import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ── 1. LOAD DATA ──────────────────────────────────────────────
data = pd.read_csv("superstore.csv", encoding="latin-1")

print("=" * 50)
print("SUPERSTORE SALES DATA ANALYSIS")
print("=" * 50)

# ── 2. DATA CLEANING ──────────────────────────────────────────
print(f"\nDataset Shape: {data.shape}")
print(f"Missing Values:\n{data.isnull().sum()[data.isnull().sum() > 0]}")
print(f"Duplicate Rows: {data.duplicated().sum()}")

data.drop_duplicates(inplace=True)
data.dropna(inplace=True)

print(f"\nCleaned Dataset Shape: {data.shape}")

# ── 3. BASIC STATS ────────────────────────────────────────────
print("\n── Key Statistics ──")
print(f"Total Sales    : ${data['Sales'].sum():,.2f}")
print(f"Total Profit   : ${data['Profit'].sum():,.2f}")
print(f"Average Sales  : ${data['Sales'].mean():,.2f}")
print(f"Total Orders   : {data.shape[0]:,}")

# ── 4. INSIGHTS ───────────────────────────────────────────────
print("\n── Insights ──")

# Best and worst category
cat_sales = data.groupby("Category")["Sales"].sum().sort_values(ascending=False)
print(f"Best Category  : {cat_sales.index[0]} (${cat_sales.iloc[0]:,.2f})")
print(f"Worst Category : {cat_sales.index[-1]} (${cat_sales.iloc[-1]:,.2f})")

# Best region
region_sales = data.groupby("Region")["Sales"].sum().sort_values(ascending=False)
print(f"Best Region    : {region_sales.index[0]} (${region_sales.iloc[0]:,.2f})")

# Most profitable sub-category
sub_profit = data.groupby("Sub-Category")["Profit"].sum().sort_values(ascending=False)
print(f"Most Profitable: {sub_profit.index[0]} (${sub_profit.iloc[0]:,.2f})")
print(f"Least Profitable: {sub_profit.index[-1]} (${sub_profit.iloc[-1]:,.2f})")

# ── 5. CHART 1 — Bar Chart: Sales by Category ─────────────────
plt.figure(figsize=(8, 5))
plt.bar(cat_sales.index, cat_sales.values, color=["#4C9BE8", "#F4A261", "#2A9D8F"])
plt.title("Total Sales by Category", fontsize=14)
plt.xlabel("Category")
plt.ylabel("Total Sales ($)")
plt.tight_layout()
plt.savefig("chart1_sales_by_category.png")
plt.show()
print("\nChart 1 saved: chart1_sales_by_category.png")

# ── 6. CHART 2 — Box Plot: Profit Distribution by Region ──────
plt.figure(figsize=(9, 5))
sns.boxplot(
    x="Region",
    y="Profit",
    hue="Region",
    data=data,
    palette="pastel",
    legend=False
)
plt.title("Profit Distribution by Region", fontsize=14)
plt.xlabel("Region")
plt.ylabel("Profit ($)")
plt.tight_layout()
plt.savefig("chart2_profit_by_region.png")
plt.show()
print("Chart 2 saved: chart2_profit_by_region.png")

# ── 7. CHART 3 — Interactive Scatter: Sales vs Profit ─────────
fig = px.scatter(
    data,
    x="Sales",
    y="Profit",
    color="Category",
    size="Sales",
    hover_data=["Sub-Category", "Region"],
    title="Sales vs Profit by Category (Interactive)"
)
fig.write_html("chart3_sales_vs_profit.html")
fig.show()
print("Chart 3 saved: chart3_sales_vs_profit.html")

# ── 8. CHART 4 — Bar Chart: Top 10 Sub-Categories by Sales ────
top10 = data.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 5))
plt.barh(top10.index[::-1], top10.values[::-1], color="steelblue")
plt.title("Top 10 Sub-Categories by Sales", fontsize=14)
plt.xlabel("Total Sales ($)")
plt.tight_layout()
plt.savefig("chart4_top10_subcategories.png")
plt.show()
print("Chart 4 saved: chart4_top10_subcategories.png")

# ── 9. EXPORT SUMMARY REPORT ──────────────────────────────────
summary = data.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Avg_Sales=("Sales", "mean"),
    Order_Count=("Sales", "count")
).round(2)

summary.to_csv("sales_summary_report.csv")
print("\nSummary report saved: sales_summary_report.csv")
print("\n── Summary by Category ──")
print(summary)

print("\n" + "=" * 50)
print("Analysis Complete!")
print("=" * 50)
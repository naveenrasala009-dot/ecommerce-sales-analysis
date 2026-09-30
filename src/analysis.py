import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ecommerce_sales.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["order_date"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)

# KPI summary
kpis = pd.DataFrame({
    "metric": ["Orders", "Customers", "Revenue", "Units Sold", "Average Order Value", "Return Rate"],
    "value": [
        df["order_id"].nunique(),
        df["customer_id"].nunique(),
        round(df["sales"].sum(), 2),
        int(df["quantity"].sum()),
        round(df["sales"].sum() / df["order_id"].nunique(), 2),
        round((df["order_status"].eq("Returned").mean()) * 100, 2),
    ],
})
kpis.to_csv(OUT/"kpi_summary.csv", index=False)

# Monthly sales
monthly = df.groupby("month", as_index=False).agg(
    revenue=("sales","sum"), orders=("order_id","nunique"), units=("quantity","sum")
)
monthly.to_csv(OUT/"monthly_sales.csv", index=False)

# Category performance
category = df.groupby("category", as_index=False).agg(
    revenue=("sales","sum"), orders=("order_id","nunique"), units=("quantity","sum")
).sort_values("revenue", ascending=False)
category.to_csv(OUT/"category_performance.csv", index=False)

# State performance
state = df.groupby("state", as_index=False).agg(
    revenue=("sales","sum"), orders=("order_id","nunique"), customers=("customer_id","nunique")
).sort_values("revenue", ascending=False)
state.to_csv(OUT/"state_performance.csv", index=False)

# Customer leaderboard
customer = df.groupby(["customer_id","customer_name"], as_index=False).agg(
    revenue=("sales","sum"), orders=("order_id","nunique"), units=("quantity","sum")
).sort_values("revenue", ascending=False)
customer.head(25).to_csv(OUT/"top_25_customers.csv", index=False)

# Product performance
product = df.groupby(["category","product"], as_index=False).agg(
    revenue=("sales","sum"), units=("quantity","sum"), orders=("order_id","nunique")
).sort_values("revenue", ascending=False)
product.to_csv(OUT/"product_performance.csv", index=False)

# Charts
plt.figure(figsize=(10,5))
plt.plot(monthly["month"], monthly["revenue"], marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month"); plt.ylabel("Revenue ($)")
plt.xticks(rotation=45); plt.tight_layout()
plt.savefig(OUT/"monthly_revenue.png", dpi=160); plt.close()

plt.figure(figsize=(9,5))
plt.bar(category["category"], category["revenue"])
plt.title("Revenue by Category")
plt.xlabel("Category"); plt.ylabel("Revenue ($)")
plt.xticks(rotation=30); plt.tight_layout()
plt.savefig(OUT/"category_revenue.png", dpi=160); plt.close()

print("Analysis complete. Results saved in outputs/.")
print(kpis.to_string(index=False))

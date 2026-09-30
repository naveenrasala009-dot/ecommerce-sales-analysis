# Power BI Dashboard Guide

## Data source
Load `data/ecommerce_sales.csv` into Power BI Desktop.

## Recommended model
For this single-table project, use the CSV as the fact table. Create a Date table for time intelligence if desired.

## Suggested measures
```DAX
Total Revenue = SUM(ecommerce_sales[sales])

Total Orders = DISTINCTCOUNT(ecommerce_sales[order_id])

Total Customers = DISTINCTCOUNT(ecommerce_sales[customer_id])

Units Sold = SUM(ecommerce_sales[quantity])

Average Order Value = DIVIDE([Total Revenue], [Total Orders])

Return Rate % =
DIVIDE(
    CALCULATE([Total Orders], ecommerce_sales[order_status] = "Returned"),
    [Total Orders]
)
```

## Dashboard layout
Top KPI cards:
- Total Revenue
- Total Orders
- Total Customers
- Units Sold
- Average Order Value
- Return Rate %

Charts:
1. Line chart: Revenue by Month
2. Bar chart: Revenue by Category
3. Bar chart: Revenue by State
4. Column chart: Orders by Channel
5. Table: Top 10 Products
6. Table: Top 10 Customers

## Slicers
- Date
- Category
- State
- Customer Segment
- Channel
- Payment Method

## Business questions
Use the dashboard to explain:
- What is driving revenue?
- Which categories/products should receive attention?
- Which regions generate the most revenue?
- Which channels have the highest order value?
- Where are return rates elevated?

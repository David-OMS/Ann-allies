# FreshDay Yoghurt - Sales & Production Analysis

## Project Purpose

Analysis of daily sales and production data for FreshDay Yoghurt (March–April 2024). Cleaned manual Excel logs, validated calculations, and produced reporting with clear documentation of data limitations.

## Data Cleaning Summary

**Sales Data:**
- Standardized product names (e.g., "Strawberry" → "Strawberry Yoghurt 500ml")
- Standardized date formats to YYYY-MM-DD
- Recalculated totals where quantity × price ≠ total
- Calculated missing values (unit_price from total/quantity, quantity from total/price)
- Added date column to all entries

**Production Data:**
- Standardized product names to match sales data
- Standardized date formats
- Validated numeric fields

**Output:** Cleaned CSVs and Excel files ready for analysis.

## KPIs Reported

- **Total Revenue:** ₦3.73M (from 42 recorded sales days)
- **Total Units Sold:** 3,474 units
- **Total Units Produced:** 6,016 units
- **Active Products:** 10 SKUs (5 flavors × 2 sizes)

## Key Insights

- Plain 250ml leads unit sales (highest volume SKU)
- Plain 500ml generates highest revenue despite lower unit volume than 250ml variants
- Production (6,016 units) exceeds sales (3,474 units) by 73%, consistent with 7-day shelf life inventory management
- 250ml products drive volume while 500ml products drive revenue
- Production occurs on 18 days over 2 months (max 2 days per week)
- Sales activity recorded on 42 days out of ~60 business days (10 days missing from logs)

## Data Limitations & Reporting Confidence

**High Confidence:**
- Total revenue: Exact from cleaned sales data (42 recorded days)
- Units sold: Exact counts from validated records

**Medium Confidence:**
- Production totals: Based on irregular logging (18 days), may be incomplete
- Monthly trends: Reliable within recorded days scope

**Known Gaps:**
- 10 sales days missing from logs (could be closures or data entry gaps)
- Production records irregular (not all SKUs logged every production day)
- No expiry, batch, or waste tracking data available
- Some sales may be unlogged (manual entry system)

**Analyses Not Performed:**
- Inventory turnover (stock data unavailable)
- Product expiry/waste analysis (no expiry data)
- Profit margins (no cost data)
- Seasonal trends (insufficient data period)

## Project Structure

```
FreshDay_Yoghurt_Analysis/
├── data/
│   ├── daily_sales_raw.xlsx
│   ├── production_stock_log_raw.xlsx
│   ├── daily_sales_clean.xlsx
│   └── production_stock_log_clean.xlsx
├── sql/
│   └── analysis_queries.sql
├── dashboard/
│   └── freshday_dashboard.png
└── README.md
```

## Files

- **Raw Data:** `data/daily_sales_raw.xlsx`, `data/production_stock_log_raw.xlsx`
- **Cleaned Data:** `data/daily_sales_clean.xlsx`, `data/production_stock_log_clean.xlsx`
- **SQL Queries:** `sql/analysis_queries.sql`
- **Dashboard:** `dashboard/freshday_dashboard.png`

# FreshDay Yoghurt Analysis

**Interactive Dashboard:** [View Dashboard](https://ann-allies.streamlit.app/)

## Project Purpose

This project analyzes daily sales and production records for a small yoghurt producer, covering March–April 2024. The work involved cleaning manually maintained Excel logs, validating calculations, and producing clear operational reporting with explicit documentation of data limitations.

## Data Cleaning Summary

### Sales Data
- Standardized product names to a consistent flavor + size format (e.g., "Strawberry" → "Strawberry Yoghurt 500ml")
- Standardized all date formats to YYYY-MM-DD
- Recalculated total sales values where quantity × unit_price did not match recorded totals
- Where either unit_price or quantity was missing and sufficient information existed, values were recalculated for consistency
- Rows with insufficient information were left unchanged
- Verified that all records contained valid dates

### Production Data
- Standardized product names to match cleaned sales data
- Standardized date formats
- Validated numeric fields for obvious entry errors

**Output:** Cleaned Excel and CSV files suitable for SQL analysis and reporting.

## KPIs Reported

- **Total Revenue:** ₦3.73M (Based on 42 recorded sales days; missing days may affect totals)
- **Total Units Sold:** 3,474 units (Exact count from available sales records)
- **Total Units Produced:** 6,016 units (Based on recorded production logs only)
- **Active Products:** 10 SKUs (5 flavors × 2 sizes)

## Key Insights

- Plain 250ml records the highest unit sales among all SKUs
- Plain 500ml generates the highest revenue despite lower unit volume than several 250ml variants
- Recorded production (6,016 units) exceeds recorded sales (3,474 units) by approximately 73%. Due to the absence of expiry, waste, and complete stock movement data, the cause of this gap cannot be fully validated
- 250ml products account for the majority of unit volume, while 500ml products contribute a larger share of revenue
- Production activity is logged on 18 days across the two-month period, aligning with a maximum of two production days per week
- Sales activity is recorded on 42 days out of approximately 60 calendar days, indicating possible missing logs or non-trading days

## Data Limitations & Reporting Confidence

### High Confidence
- Total revenue: Calculated directly from cleaned sales records. All totals were validated after correcting pricing and quantity errors.
- Units sold: Exact counts from recorded sales entries.
  
### Medium Confidence
- Production totals: Production quantities are reliable for the days recorded. However, the data does not indicate whether days or products with no entries reflect zero production or missing logs.
- Monthly trends: Reliable only within the scope of recorded sales days

### Known Gaps
- Sales activity is recorded on 42 days. The dataset does not specify whether days with no entries represent shop closures, zero sales, or missing records.
- On production days, not all products appear in the logs. It is unclear whether this reflects selective production or incomplete recording.
- No expiry dates, batch numbers, waste, or cost data are available.
- All data was entered manually, which increases the risk of unrecorded or duplicated transactions, although no systematic issues were identified during cleaning.

### Analyses Not Performed
- Inventory turnover (insufficient stock movement data)
- Product expiry or waste analysis (no expiry data)
- Profitability or margin analysis (no cost data)
- Seasonal trend analysis (data period too short)

## Project Structure

```
FreshDay_Yoghurt_Analysis/
├── data/
│   ├── daily_sales_raw.xlsx
│   ├── production_stock_log_raw.xlsx
│   ├── daily_sales_clean.xlsx
│   └── production_stock_log_clean.xlsx
├── cleaned_data/
│   ├── daily_sales_cleaned.csv
│   └── production_stock_cleaned.csv
├── sql/
│   └── analysis_queries.sql
├── dashboard/
│   └── freshday_dashboard.png
├── dashboard_app.py
├── requirements.txt
└── README.md
```

## Files

### Raw Data
- `data/daily_sales_raw.xlsx`
- `data/production_stock_log_raw.xlsx`

### Cleaned Data
- `data/daily_sales_clean.xlsx`
- `data/production_stock_log_clean.xlsx`
- `cleaned_data/daily_sales_cleaned.csv`
- `cleaned_data/production_stock_cleaned.csv`

### SQL Queries
- `sql/analysis_queries.sql`

### Dashboard
- `dashboard/freshday_dashboard.png` (static image)
- `dashboard_app.py` (interactive dashboard)

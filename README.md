# Retail-Performance-Analytics-Dashboard
![Dashboard Preview](dashboard_preview.png)
<img width="1302" height="735" alt="image" src="https://github.com/user-attachments/assets/25f73ab4-60c5-4120-bc5f-4b6273845451" />
# 📊 Corporate Retail Performance Dashboard

## 📌 Executive Summary
Developed a brand-consistent retail analytics dashboard tracking synthetic transaction logs across Canadian store networks. The solution transforms raw multi-category data into clean, role-based visual insights that empower regional managers to track performance metrics and evaluate year-over-year operational health.

---

## 🛠️ Tech Stack & Architecture
- **Data Generation:** Python (Pandas, NumPy) to simulate realistic retail logic, volume scaling, and promotional discounts.
- **Data Modeling:** Power BI Desktop Star Schema (1:Many relationships with single-direction cross-filtering).
- **Analytics Layer:** Advanced DAX (Time-intelligence and conditional performance metrics).
- **Design Philosophy:** Human-Centered UI/UX, strict adherence to a professional corporate color palette, and high scannability.

---

## 📐 Data Model Blueprint (Star Schema)
The dataset architecture optimizes query performance and ensures clean filtering pathways by separating transactional metrics from descriptive dimensions:

* **Fact_Sales:** Central transaction table mapping `SalesID`, `Quantity`, `GrossRevenue`, `DiscountApplied`, and `NetRevenue`.
* **Dim_Product:** Inventory catalog containing `ProductID`, `ProductName`, `Category` (*Lumber, Hardware, Paint, Garden*), and pricing tiers.
* **Dim_Location:** Regional store profiles mapping `LocationID`, `StoreName`, `Province` (*Ontario, Alberta, etc.*), and `StoreType`.
* **Dim_Customer:** Consumer demographics identifying `CustomerID`, `CustomerType` (*DIYer, Contractor, Commercial*), and loyalty status.
* **Dim_Date:** Continuous master calendar facilitating time-series analysis via custom `DateKey` mappings.

---

## 📈 Core Business Metrics (DAX)

### 1. Total Net Revenue
Calculates real top-line sales performance after deducting promotional markdowns and variable discounts.
```dax
Total Net Revenue = SUM(Fact_Sales[NetRevenue])
Average Basket Value = 
DIVIDE(
    [Total Net Revenue], 
    DISTINCTCOUNT(Fact_Sales[SalesID]), 
    0
)
YoY Sales Growth = 
VAR CurrentSales = [Total Net Revenue]
VAR PreviousSales = CALCULATE([Total Net Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))
RETURN 
DIVIDE(CurrentSales - PreviousSales, PreviousSales, 0)

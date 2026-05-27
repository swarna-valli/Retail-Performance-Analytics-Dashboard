import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# ==========================================
# 1. GENERATE DIM_LOCATION
# ==========================================
stores = {
    'LocationID': [1, 2, 3, 4],
    'StoreName': ['St. Jacobs Home Hardware', 'Stratford Home Building Centre', 'Kitchener Market Retail', 'Cambridge Logistics Hub'],
    'Province': ['Ontario', 'Ontario', 'Ontario', 'Ontario'],
    'StoreType': ['Home Hardware', 'Home Building Centre', 'Retail', 'Distribution Centre']
}
df_location = pd.DataFrame(stores)
df_location.to_csv('Dim_Location.csv', index=False)

# ==========================================
# 2. GENERATE DIM_PRODUCT
# ==========================================
products = {
    'ProductID': [101, 102, 103, 104, 105, 106],
    'ProductName': ['2x4 Spruce Stud', 'Outdoor Wood Deck Screws', '12V Cordless Drill', 'Premium Matte Acrylic Paint', 'Ergonomic Garden Trowel', 'Fibreglass Insulation Batt'],
    'Category': ['Lumber', 'Building Materials', 'Hardware', 'Paint', 'Garden', 'Building Materials'],
    'CostPrice': [3.20, 8.50, 42.00, 21.50, 6.00, 28.00],
    'RetailPrice': [6.99, 16.49, 89.99, 44.99, 14.99, 54.99]
}
df_product = pd.DataFrame(products)
df_product.to_csv('Dim_Product.csv', index=False)

# ==========================================
# 3. GENERATE DIM_CUSTOMER
# ==========================================
customer_types = ['DIYer', 'Contractor', 'Commercial']
df_customer = pd.DataFrame({
    'CustomerID': range(1001, 1151),  # 150 unique customers
    'CustomerType': [random.choice(customer_types) for _ in range(150)],
    'LoyaltyMember': [random.choice(['Yes', 'No']) for _ in range(150)]
})
df_customer.to_csv('Dim_Customer.csv', index=False)

# ==========================================
# 4. GENERATE DIM_DATE
# ==========================================
# Create a continuous calendar for the year 2025
start_date = datetime(2025, 1, 1)
date_list = [start_date + timedelta(days=x) for x in range(365)]

df_date = pd.DataFrame({'Date': date_list})
df_date['DateKey'] = df_date['Date'].dt.strftime('%Y%m%d').astype(int)
df_date['Year'] = df_date['Date'].dt.year
df_date['Quarter'] = df_date['Date'].dt.quarter
df_date['Month'] = df_date['Date'].dt.month
df_date['MonthName'] = df_date['Date'].dt.strftime('%B')
df_date['DayOfWeek'] = df_date['Date'].dt.strftime('%A')
# Save file (format date cleanly)
df_date.to_csv('Dim_Date.csv', index=False, date_format='%Y-%m-%d')

# ==========================================
# 5. GENERATE FACT_SALES (5,000 rows)
# ==========================================
num_rows = 5000

# Map products to their prices easily using dictionaries
prod_retail_map = dict(zip(df_product['ProductID'], df_product['RetailPrice']))
prod_cost_map = dict(zip(df_product['ProductID'], df_product['CostPrice']))

# Generate random base transactional columns
sales_ids = [f"TXN-{i:05d}" for i in range(1, num_rows + 1)]
rand_products = [random.choice(df_product['ProductID'].tolist()) for _ in range(num_rows)]
rand_qty = [random.randint(1, 15) if prod_retail_map[p] < 20 else random.randint(1, 3) for p in rand_products]

fact_data = {
    'SalesID': sales_ids,
    'DateKey': [random.choice(df_date['DateKey'].tolist()) for _ in range(num_rows)],
    'ProductID': rand_products,
    'LocationID': [random.choice(df_location['LocationID'].tolist()) for _ in range(num_rows)],
    'CustomerID': [random.choice(df_customer['CustomerID'].tolist()) for _ in range(num_rows)],
    'Quantity': rand_qty
}

df_sales = pd.DataFrame(fact_data)

# Calculate financial metrics using vectorized math operations
df_sales['GrossRevenue'] = df_sales.apply(lambda row: round(row['Quantity'] * prod_retail_map[row['ProductID']], 2), axis=1)
# 20% chance a random promotion or markdown markdown applies
df_sales['DiscountApplied'] = df_sales['GrossRevenue'].apply(lambda gross: round(gross * random.choice([0.05, 0.10, 0.15]), 2) if random.random() < 0.20 else 0.0)
df_sales['NetRevenue'] = df_sales['GrossRevenue'] - df_sales['DiscountApplied']
df_sales['TotalCost'] = df_sales.apply(lambda row: round(row['Quantity'] * prod_cost_map[row['ProductID']], 2), axis=1)

df_sales.to_csv('Fact_Sales.csv', index=False)

print("🚀 Data generation complete! 5 clean CSV files are ready for Power BI ingestion.")

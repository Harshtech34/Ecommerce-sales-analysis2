import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# ----------------------------
# 1. Load Dataset
# ----------------------------
try:
    df = pd.read_csv("data/sales_data.csv")
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: sales_data.csv not found inside data folder.")
    sys.exit()
except Exception as e:
    print("Unexpected error:", e)
    sys.exit()

# ----------------------------
# 2. Validate Dataset
# ----------------------------
if df.empty:
    print("Error: Dataset is empty.")
    sys.exit()

required_columns = ['Date','Product','Quantity','Price','Customer_ID','Region','Total_Sales']
for col in required_columns:
    if col not in df.columns:
        print(f"Error: Missing column {col}")
        sys.exit()

# ----------------------------
# 3. Data Cleaning
# ----------------------------
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df.dropna(inplace=True)

df = df[(df['Quantity'] > 0) & (df['Price'] > 0) & (df['Total_Sales'] > 0)]

# ----------------------------
# 4. Key Metrics
# ----------------------------
total_revenue = df['Total_Sales'].sum()
total_orders = len(df)
average_order_value = df['Total_Sales'].mean()

print("\n===== BUSINESS METRICS =====")
print("Total Revenue:", total_revenue)
print("Total Orders:", total_orders)
print("Average Order Value:", round(average_order_value, 2))

# Create visualization folder if not exists
if not os.path.exists("visualizations"):
    os.makedirs("visualizations")

# ----------------------------
# 5. Bar Chart - Sales by Region
# ----------------------------
region_sales = df.groupby('Region')['Total_Sales'].sum()

plt.figure()
region_sales.plot(kind='bar')
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visualizations/sales_by_region.png")
plt.close()

# ----------------------------
# 6. Pie Chart - Sales by Product
# ----------------------------
product_sales = df.groupby('Product')['Total_Sales'].sum()

plt.figure()
product_sales.plot(kind='pie', autopct='%1.1f%%')
plt.title("Sales Distribution by Product")
plt.ylabel("")
plt.tight_layout()
plt.savefig("visualizations/sales_by_product.png")
plt.close()

# ----------------------------
# 7. Line Chart - Sales Trend
# ----------------------------
daily_sales = df.groupby('Date')['Total_Sales'].sum()

plt.figure()
daily_sales.plot()
plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visualizations/sales_trend.png")
plt.close()

print("\nAll visualizations saved successfully!")

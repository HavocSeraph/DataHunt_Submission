import pandas as pd

# 1. Load and Clean
df = pd.read_csv('THE_DATA_HUNT_dataset.csv')
df = df.drop_duplicates()
df['shipping_days'] = df['shipping_days'].apply(lambda x: x if pd.notnull(x) and x >= 0 else None)
df['discount_pct'] = df['discount_pct'].apply(lambda x: x if pd.notnull(x) and 0 <= x <= 1 else None)
df['order_date'] = pd.to_datetime(df['order_date'])

print("\n=== Q1: REVENUE & PROFIT ===")
print("\nBy Category:")
print(df.groupby('category')[['revenue', 'profit']].sum().sort_values('revenue', ascending=False))
print("\nBy Region:")
print(df.groupby('region')[['revenue', 'profit']].sum().sort_values('revenue', ascending=False))

print("\n=== Q2: MONTHLY TREND ===")
df['month'] = df['order_date'].dt.strftime('%Y-%m')
print(df.groupby('month')[['revenue', 'profit']].sum())

print("\n=== Q3: PROBLEMS (RETURNS) ===")
# Assuming status column has 'Returned' or 'Cancelled'
bad_orders = df[df['order_status'].isin(['Returned', 'Cancelled'])]
print("\nReturns by Category:")
print(bad_orders['category'].value_counts())
print("\nCorrelation (Shipping, Discount, Rating):")
print(df[['shipping_days', 'discount_pct', 'rating']].corr())

print("\n=== Q4: TOP CUSTOMERS ===")
print("\nTop 5 Cities by Revenue:")
print(df.groupby('city')['revenue'].sum().sort_values(ascending=False).head(5))
print("\nTop 5 Customers by Revenue:")
print(df.groupby('customer_id')[['revenue', 'customer_age', 'segment']].sum(numeric_only=True).sort_values('revenue', ascending=False).head(5))
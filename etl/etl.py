import pandas as pd
from pathlib import Path

base = Path(__file__).resolve().parent.parent

orders = pd.read_csv(base / "data" / "Orders.csv")
details = pd.read_csv(base / "data" / "Details.csv")

orders.columns = orders.columns.str.strip()
details.columns = details.columns.str.strip()

orders = orders.drop_duplicates()
details = details.drop_duplicates()

orders["Order Date"] = pd.to_datetime(
    orders["Order Date"], dayfirst=True, errors="coerce"
)

orders["Order Year"] = orders["Order Date"].dt.year
orders["Order Month"] = orders["Order Date"].dt.month
orders["Order Month Name"] = orders["Order Date"].dt.strftime("%B")
orders["Order Quarter"] = "Q" + orders["Order Date"].dt.quarter.astype(str)
orders["Order Day"] = orders["Order Date"].dt.day
orders["Order Day Name"] = orders["Order Date"].dt.strftime("%A")

details["Amount"] = pd.to_numeric(details["Amount"], errors="coerce")
details["Profit"] = pd.to_numeric(details["Profit"], errors="coerce")
details["Quantity"] = pd.to_numeric(details["Quantity"], errors="coerce")

details["Profit Margin"] = (
    details["Profit"] / details["Amount"]
).fillna(0)
details = details.merge(orders[["Order ID", "Order Date"]],on="Order ID",how="left")

orders.to_csv(base / "data" / "Orders_ETL_Processed.csv", index=False)
details.to_csv(base / "data" / "Details_ETL_Processed.csv", index=False)

print("Orders:", orders.shape)
print("Details:", details.shape)
print("Missing Order Dates:", details["Order Date"].isna().sum())
print("ETL completed successfully")
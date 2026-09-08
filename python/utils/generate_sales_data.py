import random
import pandas as pd
from datetime import datetime, timedelta

products = [
    "Laptop",
    "Wireless Mouse",
    "Keyboard",
    "Monitor",
    "USB-C Cable",
    "Webcam",
    "Headphones",
    "External SSD",
    "USB Hub",
    "Laptop Stand"
]

product_categories = {
    "Laptop": "Computers",
    "Wireless Mouse": "Accessories",
    "Keyboard": "Accessories",
    "Monitor": "Electronics",
    "USB-C Cable": "Accessories",
    "Webcam": "Electronics",
    "Headphones": "Electronics",
    "External SSD": "Storage",
    "USB Hub": "Accessories",
    "Laptop Stand": "Accessories"
}

payment_methods = [
    "Credit Card",
    "Debit Card",
    "Cash",
    "Mobile Payment"
]

stores = [
    "S001",
    "S002",
    "S003",
    "S004",
    "S005"
]

customers = [f"C{i:04d}" for i in range(1, 2001)]

product_prices = {
    "Laptop": 899.99,
    "Wireless Mouse": 24.99,
    "Keyboard": 49.99,
    "Monitor": 249.99,
    "USB-C Cable": 14.99,
    "Webcam": 79.99,
    "Headphones": 99.99,
    "External SSD": 129.99,
    "USB Hub": 34.99,
    "Laptop Stand": 39.99
}

sales_data = []

for i in range(50000):

    product = random.choice(products)

    category = product_categories[product]
    price = product_prices[product]

    quantity = random.randint(1, 5)
    store_id = random.choices(
    stores,
    weights=[30, 25, 20, 15, 10],
    k=1
)[0]
    payment_method = random.choice(payment_methods)

    customer_id = random.choice(customers)
    sale_id = 10001 + i

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    sale_date = start_date + timedelta(days=random_days)
    sale = {
        "sale_id": sale_id,
        "sale_date": sale_date,
        "customer_id": customer_id,
        "product": product,
        "category": category,
        "quantity": quantity,
        "price": price,
        "store_id": store_id,
        "payment_method": payment_method
}
    sales_data.append(sale)

df = pd.DataFrame(sales_data)
print(df.head())
print("Total rows:", len(df))
df.to_csv("data/retail_sales.csv", index=False)



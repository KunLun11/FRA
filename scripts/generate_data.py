import numpy as np
import pandas as pd

np.random.seed(42)

# Товары

categories = {
    "Диваны": ["Прямые", "Угловые", "Модульные"],
    "Шкафы": ["Купе", "Распашные", "Гардеробные"],
    "Кухни": ["Классика", "Модерн", "Лофт"],
    "Кровати": ["Односпальные", "Двуспальные", "Детские"],
    "Столы": ["Обеденные", "Журнальные", "Компьютерные"],
    "Стулья": ["Офисные", "Барные", "Кухонные"],
    "Матрасы": ["Пружинные", "Беспружинные", "Пенные"],
    "Аксессуары": ["Зеркала", "Светильники", "Ковры"],
}

products = []

for i in range(1, 121):
    cat = np.random.choice(list(categories))
    sub = np.random.choice(categories[cat])
    cost = np.random.randint(3000, 80000)
    margin = np.random.uniform(1.25, 1.6)
    price = round(cost * margin / 100) * 100
    products.append(
        {
            "product_id": f"P{i:03d}",
            "product_name": f"{cat} {sub} {i}",
            "category": cat,
            "subcategory": sub,
            "cost": cost,
            "price": price,
            "launch_date": pd.Timestamp("2023-01-01")
            + pd.to_timedelta(np.random.randint(0, 365), unit="D"),
            "is_active": np.random.choice([True, False], p=[0.9, 0.1]),
        }
    )

products_df = pd.DataFrame(products)

# Магазины

cities = [
    "Калининград",
    "Советск",
    "Черняховск",
    "Гурьевск",
    "Светлогорск",
    "Зеленоградск",
]
stores = []
for i, city in enumerate(cities, 1):
    stores.append(
        {
            "store_id": f"S{i:02d}",
            "store_name": f"BOXX {city}",
            "city": city,
            "format": np.random.choice(["ТЦ", "отдельный", "шоурум"]),
            "open_date": pd.Timestamp("2015-01-01")
            + pd.to_timedelta(np.random.randint(0, 2000), unit="D"),
        }
    )
stores_df = pd.DataFrame(stores)

# Клиенты
segments = ["Новичок", "Постоянный", "VIP", "Спящий"]
customers = []
for i in range(1, 1501):
    customers.append(
        {
            "customer_id": f"C{i:04d}",
            "segment": np.random.choice(segments, p=[0.4, 0.35, 0.1, 0.15]),
            "reg_date": pd.Timestamp("2022-01-01")
            + pd.to_timedelta(np.random.randint(0, 1000), unit="D"),
            "region": np.random.choice(["Калининград", "Область", "Другой"]),
        }
    )
customers_df = pd.DataFrame(customers)

# Календарь
dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
calendar_df = pd.DataFrame({"date": dates})
calendar_df["year"] = calendar_df["date"].dt.year
calendar_df["month"] = calendar_df["date"].dt.month
calendar_df["month_name"] = calendar_df["date"].dt.month_name()
calendar_df["quarter"] = calendar_df["date"].dt.quarter
calendar_df["week"] = calendar_df["date"].dt.isocalendar().week
calendar_df["weekday"] = calendar_df["date"].dt.weekday
calendar_df["is_weekend"] = calendar_df["weekday"] >= 5

# Продажи
month_mult = {
    1: 0.8,
    2: 0.7,
    3: 1.1,
    4: 1.0,
    5: 1.0,
    6: 1.1,
    7: 1.1,
    8: 1.0,
    9: 1.1,
    10: 1.2,
    11: 1.3,
    12: 1.5,
}
channels = ["Розница", "E-com", "B2B"]
channel_probs = [0.6, 0.25, 0.15]

sales = []
order_id = 1
for date in dates:
    base_orders = 30
    seasonal = month_mult[date.month]
    trend = 1 + (date - pd.Timestamp("2024-01-01")).days / 730 * 0.15
    n_orders = int(np.random.poisson(base_orders * seasonal * trend))

    for _ in range(n_orders):
        channel = np.random.choice(channels, p=channel_probs)
        store = np.random.choice(stores_df["store_id"])
        customer = np.random.choice(customers_df["customer_id"])
        n_items = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])

        for _ in range(n_items):
            prod = products_df.sample(1).iloc[0]
            qty = np.random.choice([1, 2, 3, 5, 10], p=[0.6, 0.2, 0.1, 0.05, 0.05])

            if channel == "B2B":
                qty *= 3
                discount = np.random.uniform(0.1, 0.3)
            elif channel == "E-com":
                discount = np.random.uniform(0, 0.15)
            else:
                discount = np.random.uniform(0, 0.1)

            revenue = prod["price"] * qty * (1 - discount)
            cost = prod["cost"] * qty
            sales.append(
                {
                    "order_id": f"O{order_id:06d}",
                    "date": date,
                    "product_id": prod["product_id"],
                    "store_id": store,
                    "customer_id": customer,
                    "channel": channel,
                    "qty": qty,
                    "price": prod["price"],
                    "discount": round(discount, 4),
                    "revenue": round(revenue, 2),
                    "cost": round(cost, 2),
                }
            )
        order_id += 1

sales_df = pd.DataFrame(sales)

inventory = []
for date in pd.date_range("2024-01-01", "2025-12-31", freq="MS"):
    for store in stores_df["store_id"]:
        for prod in products_df["product_id"]:
            stock_qty = np.random.poisson(20)
            # искусственно создаём неликвид
            if np.random.rand() < 0.1:
                stock_qty += np.random.randint(50, 200)
            cost = products_df.loc[products_df["product_id"] == prod, "cost"].values[0]
            inventory.append(
                {
                    "date": date,
                    "product_id": prod,
                    "store_id": store,
                    "stock_qty": stock_qty,
                    "stock_value": round(stock_qty * cost, 2),
                }
            )
inventory_df = pd.DataFrame(inventory)

products_df.to_csv("products.csv", index=False)
stores_df.to_csv("stores.csv", index=False)
customers_df.to_csv("customers.csv", index=False)
calendar_df.to_csv("calendar.csv", index=False)
sales_df.to_csv("sales.csv", index=False)
inventory_df.to_csv("inventory.csv", index=False)

print("Готово. Строк в sales:", len(sales_df))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)
n = 8000

# order basics
ids = list(range(1, n+1))
d0 = datetime(2026, 1, 1)
dates = [d0 + timedelta(days=np.random.randint(0, 181)) for _ in range(n)]
cust = np.random.randint(1, 9001, n)
mode = np.random.choice(['COD', 'Prepaid'], n, p=[0.6, 0.4])

# order value — mostly small, some big
def pick_val():
    r = np.random.random()
    if r < 0.3:  return np.random.randint(300, 750)
    if r < 0.65: return np.random.randint(750, 1500)
    if r < 0.9:  return np.random.randint(1500, 3000)
    return np.random.randint(3000, 5000)

val = [pick_val() for _ in range(n)]
for i in range(20):
    val[i] = np.random.randint(10000, 25000)

tier = np.random.choice(['Metro', 'Tier-2', 'Tier-3', 'Remote'], n, p=[.3, .3, .25, .15])
cur = np.random.choice(['A', 'B', 'C'], n, p=[.4, .3, .3])
cat = np.random.choice(['Electronics', 'Fashion', 'Home', 'Beauty', 'Sports'], n)

df = pd.DataFrame({
    'order_id': ids, 'order_date': dates, 'customer_id': cust,
    'payment_mode': mode, 'order_value': val, 'product_category': cat,
    'pincode_tier': tier, 'courier': cur,
})

df = df.sort_values('order_date').reset_index(drop=True)

# first order in window = New, rest = Repeat
df['customer_type'] = df.groupby('customer_id').cumcount().apply(
    lambda x: 'New' if x == 0 else 'Repeat'
)

# rto probability as per rules
df['rto_prob'] = 0.02
df.loc[df.payment_mode == 'COD', 'rto_prob'] = 0.15
df.loc[(df.payment_mode == 'COD') & (df.customer_type == 'New'), 'rto_prob'] += 0.05
df.loc[(df.payment_mode == 'COD') & (df.order_value >= 1500), 'rto_prob'] += 0.05
df.loc[df.pincode_tier == 'Tier-3', 'rto_prob'] += 0.04
df.loc[df.pincode_tier == 'Remote', 'rto_prob'] += 0.08
df.loc[df.courier == 'B', 'rto_prob'] += 0.03
df['rto_prob'] = df['rto_prob'].clip(0.01, 0.5)

# exactly 400 cancelled before dispatch
cancel = np.random.choice(df.index, 400, replace=False)
df['delivery_status'] = 'Delivered'
for i, row in df.iterrows():
    if i in cancel:
        df.at[i, 'delivery_status'] = 'Cancelled Before Dispatch'
    elif np.random.random() < row.rto_prob:
        df.at[i, 'delivery_status'] = 'RTO'

# high risk flag
df['is_high_risk'] = (
    (df.payment_mode == 'COD') &
    (df.customer_type == 'New') &
    (df.order_value >= 1500) &
    (df.pincode_tier.isin(['Tier-3', 'Remote']))
)

# a/b split — 50/50 on high-risk orders
df['group'] = 'Not eligible'
hr = list(df[df.is_high_risk].index)
np.random.shuffle(hr)
half = len(hr) // 2
ctrl = hr[:half]
trt = hr[half:]

df.loc[ctrl, 'group'] = 'Control'
df.loc[trt, 'group'] = 'Treatment'

# treatment gets -5 pt reduction
for i in trt:
    if df.at[i, 'delivery_status'] == 'Cancelled Before Dispatch':
        continue
    p = max(0.01, df.at[i, 'rto_prob'] - 0.05)
    df.at[i, 'delivery_status'] = 'RTO' if np.random.random() < p else 'Delivered'

df['call_cost'] = 0
df.loc[trt, 'call_cost'] = 10

# costs
ship_map = {'Metro': 60, 'Tier-2': 80, 'Tier-3': 100, 'Remote': 130}
df['shipping_cost'] = df.pincode_tier.map(ship_map)
df.loc[df.delivery_status == 'Cancelled Before Dispatch', 'shipping_cost'] = 0

df['return_shipping_cost'] = 0
rto_rows = df.delivery_status == 'RTO'
df.loc[rto_rows, 'return_shipping_cost'] = df.loc[rto_rows, 'shipping_cost']

df['packaging_cost'] = 15
df.loc[df.delivery_status == 'Cancelled Before Dispatch', 'packaging_cost'] = 0

df['product_cost'] = df.order_value * np.random.uniform(0.4, 0.6, n)

# inject data-quality issues (raw file ke liye)
miss = np.random.choice(df.index, 160, replace=False)
df.loc[miss, 'pincode_tier'] = np.nan

var = np.random.choice(df.index, 80, replace=False)
for i in var:
    if df.at[i, 'payment_mode'] == 'COD':
        df.at[i, 'payment_mode'] = np.random.choice(['cod', 'Cod', 'C.O.D'])
    else:
        df.at[i, 'payment_mode'] = np.random.choice(['prepaid', 'Prepaid ', 'PREPAID'])

# add 80 duplicate rows
dup = df.sample(80, random_state=42)
df_raw = pd.concat([df, dup], ignore_index=True)

# save ONLY raw file
os.makedirs('../data/raw', exist_ok=True)
df_raw.to_csv('../data/raw/orders_raw.csv', index=False)

# quick check
print("Raw rows:", len(df_raw))
print()
print(df.delivery_status.value_counts())
print()

disp = df[df.delivery_status != 'Cancelled Before Dispatch']
rto = (disp.delivery_status == 'RTO').sum()
print("RTO overall:", round(rto / len(disp) * 100, 2), "%")

cod = disp[disp.payment_mode.isin(['COD', 'cod', 'Cod', 'C.O.D'])]
print("RTO COD:", round((cod.delivery_status == 'RTO').sum() / len(cod) * 100, 2), "%")

print()
print("High-risk:", df.is_high_risk.sum())
hr_df = df[df.is_high_risk]
for g in ['Control', 'Treatment']:
    s = hr_df[hr_df.group == g]
    r = (s.delivery_status == 'RTO').sum()
    print(g, ":", r, "/", len(s), "=", round(r / len(s) * 100, 2), "%")

rto_only = df[df.delivery_status == 'RTO']
loss = rto_only.shipping_cost + rto_only.return_shipping_cost + rto_only.packaging_cost
print()
print("Avg loss per RTO: Rs", round(loss.mean(), 2))

de = df[df.delivery_status == 'Delivered']
m = de.order_value - de.product_cost - de.shipping_cost - de.packaging_cost
print("Avg margin: Rs", round(m.mean(), 2))
print("Median margin: Rs", round(m.median(), 2))
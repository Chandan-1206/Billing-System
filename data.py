# data.py
import pandas as pd

INVENTORY_FILE = "inventory.csv"
inventory_data = pd.read_csv(INVENTORY_FILE)

def get_inventory():
    return inventory_data

def save_inventory():
    allowed_columns = ["Name", "Retail Price", "Wholesale Price", "Quantity"]
    cleaned_data = inventory_data[allowed_columns].copy()
    cleaned_data.to_csv(INVENTORY_FILE, index=False)

def update_stock(item_name, quantity):
    inventory_data.loc[inventory_data["Name"] == item_name, "Quantity"] -= quantity

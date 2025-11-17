# logic.py
import tkinter as tk
from data import get_inventory, update_stock, save_inventory
from state import add_to_bill, remove_from_bill, get_bill_items, calculate_total, clear_bill

inventory_data = get_inventory()

def setup_variables(root):
    return {
        "customer_name_var": tk.StringVar(root),
        "product_entry_var": tk.StringVar(root),
        "quantity_var": tk.StringVar(root, value="1"),
        "price_type": tk.StringVar(root, value="R"),
        "price_var": tk.StringVar(root),
        "product_list_var": tk.StringVar(root, value=inventory_data["Name"].tolist()),
        "unit_var": tk.StringVar(root, value="pcs"),  
    }

def filter_inventory(product_entry_var, product_list_var):
    search = product_entry_var.get().lower()
    filtered = inventory_data[inventory_data["Name"].str.lower().str.contains(search)] if search else inventory_data
    product_list_var.set(filtered["Name"].tolist())

def select_item(product_listbox, product_entry_var, price_var, price_type, stock_status_label):
    selected = product_listbox.curselection()
    if selected:
        name = product_listbox.get(selected)
        product_entry_var.set(name)
        update_price(name, price_type, price_var)

        # Show stock status
        item = inventory_data[inventory_data["Name"] == name]
        if not item.empty:
            qty_left = item.iloc[0]["Quantity"]
            if qty_left <= 5:
                stock_status_label.config(text=f"⚠️ Only {qty_left} left in stock")
            else:
                stock_status_label.config(text=f"{qty_left} in stock")


def update_price(name, price_type, price_var):
    item = inventory_data[inventory_data["Name"] == name]
    if not item.empty:
        price = item.iloc[0]["Retail Price"] if price_type.get() == "R" else item.iloc[0]["Wholesale Price"]
        price_var.set(f"{price:.2f}")

def add_item(product_entry_var, quantity_var, price_var, unit_var, bill_tree, total_label):
    try:
        name = product_entry_var.get()
        price = float(price_var.get())
        quantity = int(quantity_var.get())  # pure number
        unit = unit_var.get()                # pcs or dzns

        item = inventory_data[inventory_data["Name"] == name]
        if item.empty:
            total_label.config(text="Item not found.")
            return

        available_qty = item.iloc[0]["Quantity"]
        existing_qty = sum(int(i[2].split()[0]) for i in get_bill_items() if i[0] == name)
        if quantity + existing_qty > available_qty:
            total_label.config(text=f"Only {available_qty - existing_qty} more in stock.")
            return

        # Check if already in tree
        for child in bill_tree.get_children():
            values = bill_tree.item(child)["values"]
            if values[0] == name:
                new_qty_number = int(values[2].split()[0]) + quantity
                new_qty_display = f"{new_qty_number} {unit}"
                new_total = round(price * new_qty_number, 2)
                bill_tree.item(child, values=(name, price, new_qty_display, new_total))

                remove_from_bill((values[0], float(values[1]), values[2], float(values[3])))
                add_to_bill((name, price, new_qty_display, new_total))

                update_total(total_label)
                return

        total = round(price * quantity, 2)
        display_quantity = f"{quantity} {unit}"
        bill_tree.insert("", "end", values=(name, price, display_quantity, total))
        add_to_bill((name, price, display_quantity, total))
        update_total(total_label)

    except Exception as e:
        total_label.config(text=f"Error: {e}")



def update_total(total_label):
    total_amount = calculate_total()
    total_label.config(text=f"Total: {total_amount:.2f}")

def delete_item(bill_tree, total_label):
    try:
        for item in bill_tree.selection():
            values = bill_tree.item(item, "values")
            
            # extract numeric quantity safely from "2 dzns" or "5 pcs"
            quantity_str = values[2]
            if isinstance(quantity_str, str) and " " in quantity_str:
                quantity = int(quantity_str.split(" ")[0])
            else:
                quantity = int(quantity_str)
            remove_from_bill((values[0], float(values[1]), quantity, float(values[3])))

            bill_tree.delete(item)
        update_total(total_label)
    except Exception as e:
        total_label.config(text=f"Error: {e}")

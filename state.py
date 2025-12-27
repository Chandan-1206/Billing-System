# state.py
bill_items = []

def add_to_bill(item):
    bill_items.append(item)

def remove_from_bill(item_to_remove):
    for item in bill_items:
        if (
            item[0] == item_to_remove[0] and  # name
            float(item[1]) == float(item_to_remove[1]) and  # price
            float(item[3]) == float(item_to_remove[3])  # total
        ):
            bill_items.remove(item)
            break

def clear_bill():
    bill_items.clear()

def get_bill_items():
    return bill_items

def calculate_total():
    return sum(item[3] for item in bill_items)

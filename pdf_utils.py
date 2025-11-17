#pdf_utils.py
from fpdf import FPDF
import os
from datetime import datetime
from datetime import timedelta
from data import update_stock, save_inventory
from state import calculate_total


def delete_old_bills(folder="bills2025", days=2):
    cutoff_time = datetime.now() - timedelta(days=days)

    if not os.path.exists(folder):
        return

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if modified_time < cutoff_time:
                try:
                    os.remove(file_path)  # Permanently delete
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

def save_bill_as_pdf(vars, items, total_label, reset_func, deduct_stock=True):
    try:
        if not items:
            total_label.config(text="No items in the bill to save.")
            return
        
        customer_name = vars["customer_name_var"].get().strip()

        folder = "bills2025"
        os.makedirs(folder, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if customer_name:
            safe_customer_name = customer_name.replace(" ", "_")
            pdf_filename = f"{safe_customer_name}_{timestamp}.pdf"
        else:
            pdf_filename = f"Bill_{timestamp}.pdf"

        pdf_path = os.path.join(folder, pdf_filename)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Heading
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Estimate - BILL", ln=True, align="C")
        pdf.set_font("Arial", size=12)

        # Date
        pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", ln=True, align="C")
        if customer_name:
            pdf.cell(200, 10, txt=f"Customer Name: {customer_name}", ln=True, align="C")
        pdf.ln(10)

        # Find longest product name length
        max_name_length = max(len(str(item[0])) for item in items)

        # Set Item column width based on name length
        if max_name_length >= 25:
            item_col_width = 80  # Wider if names are very long
        elif max_name_length >= 15:
            item_col_width = 60  # Medium
        else:
            item_col_width = 50  # Default

        pdf.set_font("Arial", 'B', 12)  # Bold, size 12
        pdf.set_line_width(0.35)  # Thicker lines for heading
        # Table Headers
        pdf.cell(20, 10, "S.No", border=1, align="C")
        pdf.cell(item_col_width, 10, "Item", border=1, align="C")
        pdf.cell(30, 10, "Price", border=1, align="C")
        pdf.cell(30, 10, "Quantity", border=1, align="C")
        pdf.cell(40, 10, "Total", border=1, align="C")
        pdf.ln(10)
        pdf.set_font("Arial","", 12)  
        pdf.set_line_width(0.2)  

        # Items with serial numbers
        for idx, item in enumerate(items, start=1):
            name, price, qty_with_unit, total = item
        
            # Separate quantity and unit
            if " " in str(qty_with_unit):
                qty, unit = str(qty_with_unit).split(" ", 1)
            else:
                qty, unit = str(qty_with_unit), "pcs"  # Default pcs
        
            pdf.cell(20, 10, str(idx), border=1, align="C")
            pdf.cell(item_col_width, 10, str(name), border=1, align="C")
            pdf.cell(30, 10, f"{price:.2f}", border=1, align="C")
            pdf.cell(30, 10, f"{qty} {unit}", border=1, align="C")
            pdf.cell(40, 10, f"{total:.2f}", border=1, align="C")
            pdf.ln(10)
            if deduct_stock:
                update_stock(name, int(qty))
            # IMPORTANT: Only update stock with number part

        # Total Amount
        total_amount = calculate_total()

        if deduct_stock:
            # Update daily sales total
            today_str = datetime.now().strftime("%Y-%m-%d")
            sales_file = f"{today_str}.txt"
            
            # Read current total
            if os.path.exists(sales_file):
                with open(sales_file, "r") as f:
                    try:
                        current_total = float(f.read().strip())
                    except:
                        current_total = 0.0
            else:
                current_total = 0.0
            
            # Add today's bill amount
            new_total = current_total + total_amount
            
            # Save back to file
            with open(sales_file, "w") as f:
                f.write(f"{new_total:.2f}")

        pdf.ln(10)
        pdf.cell(20, 10, "", border=0)
        pdf.cell(50, 10, "", border=0)
        pdf.cell(30, 10, "", border=0)
        pdf.cell(30, 10, "Grand Total:", border=1, align="C")
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(40, 10, f"Rs. {total_amount:.2f}", border=1, align="C")
        pdf.set_font("Arial", size=12)
        pdf.ln(10)

        pdf.output(pdf_path)

        save_inventory()
        total_label.config(text=f"Bill saved: {pdf_path}")
        reset_func()

        delete_old_bills()

        try:
            os.startfile(pdf_path)
        except Exception:
            pass

    except Exception as e:
        total_label.config(text=f"Error: {e}")

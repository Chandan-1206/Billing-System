# gui.py
import tkinter as tk
from tkinter import ttk
from logic import (
    setup_variables,
    filter_inventory,
    select_item,
    update_price,
    add_item,
    update_total,
    delete_item
)
from state import get_bill_items, clear_bill
from pdf_utils import save_bill_as_pdf

def create_gui(root):
    vars = setup_variables(root)

    root.title("Billing System")
    root.geometry("800x700")
    
    # ── Purple-Calm Light Theme ──
    light_theme = {
        "bg":               "#F3E8FF",   # very pale lavender
        "fg":               "#4B0082",   # deep indigo text
        "input_bg":         "#E7C6FF",   # entry background
        "input_fg":         "#4B0082",   # entry text
        "button_bg":        "#8A2BE2",   # blue-violet
        "button_fg":        "#FFFFFF",   # white on violet
        "button_active_bg": "#7A1ECC",   # slightly darker
        "tree_heading_bg":  "#DCC6E0",   # pale mauve
        "tree_heading_fg":  "#4B0082",   # indigo
        "row_even_bg":      "#FFFFFF",   # white
        "row_odd_bg":       "#F7E6FF",   # ultra-light purple
        "selection_bg":     "#E1BEE7",   # light orchid
        "selection_fg":     "#4B0082",   # indigo
    }

    # ── Purple-Night Dark Theme ──
    dark_theme = {
            "bg":               "#0A000A",   # nearly black with purple hint
            "fg":               "#FFFFFF",   # pure white text
            "input_bg":         "#E7C6FF",   # light purple
            "input_fg":         "#0A000A",   # white text
            "insert_bg":        "#FFFFFF",   # white cursor
            "button_bg":        "#BB00FF",   # neon magenta
            "button_fg":        "#0A000A",   # near-black text
            "button_active_bg": "#8800CC",   # darker magenta on press
            "tree_heading_bg":  "#100010",   # near-black purple
            "tree_heading_fg":  "#FF99FF",   # bright pink
            "row_even_bg":      "#1A001A",   # match input_bg
            "row_odd_bg":       "#0A000A",   # main bg
            "selection_bg":     "#550055",   # deep purple
            "selection_fg":     "#FFFFFF",   # white text on selection
        }
    
    current_theme = {"theme": light_theme}

    # Fonts
    label_font = ("Arial", 12)
    entry_font = ("Arial", 12)
    button_font = ("Arial", 14, "bold")

    # Layout frames
    form_frame = tk.Frame(root)
    tree_frame = tk.Frame(root)
    button_frame = tk.Frame(root)

    form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    tree_frame.grid(row=1, column=0, sticky="nsew", padx=10)
    button_frame.grid(row=2, column=0, pady=10)

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Variable trace logic
    vars["product_entry_var"].trace("w", lambda *args: filter_inventory(vars["product_entry_var"], vars["product_list_var"]))
    vars["price_type"].trace("w", lambda *args: update_price(vars["product_entry_var"].get(), vars["price_type"], vars["price_var"]))

    # Styled widget helpers
    def styled_label(text, row):
        lbl = tk.Label(form_frame, text=text, font=label_font)
        lbl.grid(row=row, column=0, sticky="w", pady=5)
        return lbl

    def styled_entry(var, row):
        entry = ttk.Entry(form_frame, textvariable=var, font=entry_font, width=30)
        entry.grid(row=row, column=1, sticky="w", pady=5)
        return entry

    # Labels
    labels = [
        styled_label("Customer Name:", 0),
        styled_label("Product Name:", 1),
        styled_label("Price Type:", 3),
        styled_label("Price:", 4),
        styled_label("Quantity:", 5),
        styled_label("Unit:", 6)
    ]

    # Entries and comboboxes
    styled_entry(vars["customer_name_var"], 0)
 #  styled_entry(vars["product_entry_var"], 1)
    product_entry = styled_entry(vars["product_entry_var"], 1)

    clear_btn = tk.Button(
        form_frame,
        text="✕",
        font=("Arial", 10, "bold"),
        bd=0,
        relief="flat",
        cursor="hand2",
        command=lambda: vars["product_entry_var"].set("")
    )
    # overlay the clear button inside the entry at right edge
    clear_btn.place(in_=product_entry, relx=1.0, x=-18, rely=0.5, anchor="w")

    ttk.Combobox(form_frame, textvariable=vars["price_type"], values=["R", "W"], font=entry_font, width=28).grid(row=3, column=1, sticky="w", pady=5)
    ttk.Entry(form_frame, textvariable=vars["price_var"], font=entry_font, width=30).grid(row=4, column=1, sticky="w", pady=5)
    tk.Spinbox(form_frame, from_=1, to=1000, textvariable=vars["quantity_var"], font=entry_font, width=28).grid(row=5, column=1, sticky="w", pady=5)
    ttk.Combobox(form_frame, textvariable=vars["unit_var"], values=["pcs", "dzns"], font=entry_font, width=28).grid(row=6, column=1, sticky="w", pady=5)


    # Product list
    product_listbox = tk.Listbox(form_frame, listvariable=vars["product_list_var"], height=5, font=entry_font, width=30)
    product_listbox.grid(row=2, column=1, sticky="w", pady=5)

    # Stock status label
    stock_status_label = tk.Label(form_frame, text="", font=("Arial", 10, "italic"), fg="red")
    stock_status_label.grid(row=2, column=2, sticky="w", padx=10)

    product_listbox.bind("<<ListboxSelect>>", lambda e: select_item(
        product_listbox,
        vars["product_entry_var"],
        vars["price_var"],
        vars["price_type"],
        stock_status_label
    ))

    # Treeview for bill
    columns = ("Name", "Price", "Quantity", "Total")
    style = ttk.Style()
    style.theme_use("default")

    bill_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
    for col in columns:
        bill_tree.heading(col, text=col)
        bill_tree.column(col, anchor="center", width=150)
    bill_tree.pack(fill="both", expand=True)

    # Total label
    total_label = tk.Label(root, text="Total: 0.00", font=("Arial", 14, "bold"))
    total_label.grid(row=3, column=0, pady=(5, 20))

    # Reset function
    def reset():
        for item in bill_tree.get_children():
            bill_tree.delete(item)
        vars["product_entry_var"].set("")
        vars["quantity_var"].set("1")
        vars["price_type"].set("R")
        vars["price_var"].set("")
        vars["customer_name_var"].set("")
        vars["product_list_var"].set([])
        stock_status_label.config(text="")
        clear_bill()
        update_total(total_label)

    # Buttons
    def themed_button(text, command, col):
        btn = tk.Button(button_frame, text=text, font=button_font, width=18, command=command)
        btn.grid(row=0, column=col, padx=10)
        return btn

    buttons = [
        themed_button("Add Item to Bill", lambda: add_item(vars["product_entry_var"], vars["quantity_var"], vars["price_var"], vars["unit_var"], bill_tree, total_label), 0),
        themed_button("Delete Selected Item", lambda: delete_item(bill_tree, total_label), 1),
        themed_button("Save Bill as PDF", lambda: save_bill_as_pdf(vars, get_bill_items(), total_label, reset), 2)
    ]

    # Theme toggle
    def toggle_theme():
        current_theme["theme"] = dark_theme if current_theme["theme"] == light_theme else light_theme
        apply_theme()
    
    # Create the button to switch themes
    theme_toggle_btn = tk.Button(root, text="Switch Theme", font=("Arial", 12, "bold"), command=toggle_theme)
    theme_toggle_btn.grid(row=4, column=0, pady=(0, 20))

    # Theme application
    def apply_theme():
        t = current_theme["theme"]

        # Frames & root
        root.configure(bg=t["bg"])
        form_frame.configure(bg=t["bg"])
        tree_frame.configure(bg=t["bg"])
        button_frame.configure(bg=t["bg"])
        total_label.configure(bg=t["bg"], fg=t["fg"])
        theme_toggle_btn.configure(
            bg=t["button_bg"], fg=t["button_fg"],
            activebackground=t["button_active_bg"])

        # Labels
        for lbl in labels:
            lbl.configure(bg=t["bg"], fg=t["fg"])

        # Entry & Combobox & Spinbox
        for widget in form_frame.winfo_children():
            if isinstance(widget, (ttk.Entry, tk.Spinbox, ttk.Combobox)):
                widget.configure(
                    background=t["input_bg"], foreground=t["input_fg"])
        # clear-button stays same

        # Buttons
        for btn in buttons:
            btn.configure(
                bg=t["button_bg"], fg=t["button_fg"],
                activebackground=t["button_active_bg"], relief="flat")

        # Listbox
        product_listbox.configure(
            bg=t["input_bg"], fg=t["input_fg"],
            selectbackground=t["selection_bg"], selectforeground=t["selection_fg"])

        # Treeview headings
        style.configure("Treeview.Heading",
                        font=("Arial", 12, "bold"),
                        background=t["tree_heading_bg"],
                        foreground=t["tree_heading_fg"],
                        relief="flat")
        # Treeview rows
        style.configure("Treeview",
                        font=("Arial", 11),
                        background=t["row_odd_bg"],
                        fieldbackground=t["row_odd_bg"],
                        foreground=t["fg"],
                        rowheight=24)
        style.map("Treeview",
                  background=[("selected", t["selection_bg"])],
                  foreground=[("selected", t["selection_fg"])])

        # Row striping
        for i, row in enumerate(bill_tree.get_children()):
            bill_tree.tag_configure(
                row,
                background=(t["row_even_bg"] if i % 2 == 0 else t["row_odd_bg"])
            )

    apply_theme()

# Billing System 

A **Python-based desktop billing application** built using **Tkinter**, focused on fast bill creation, inventory tracking, and PDF bill generation.  
This README reflects the **current working state** of the project.

---

## Features (Current)

- 🧾 GUI-based billing system (Tkinter)
- 📦 Inventory management via CSV
- 🔍 Live product search & filter
- ⚠️ Low-stock warnings
- 🧮 Automatic total calculation
- 📄 PDF bill generation
- 🌓 Light / Dark theme toggle
- 🧑 Customer name on bills
- 📉 Stock auto-updated after bill save

---

## Project Structure
```bash
Billing-System/
│
├── main.py # App entry point
├── gui.py # GUI layout & theming
├── logic.py # Billing & inventory logic
├── data.py # Inventory CSV handling
├── state.py # Bill state management
├── pdf_utils.py # PDF bill generation
├── Inventory.csv # Sample inventory file
├── inventory_viewer.ipynb
```
---

## How It Works

1. Launch app via `main.py`
2. Inventory loads from `Inventory.csv`
3. User selects product, price type (Retail/Wholesale), quantity & unit
4. Items added to bill table
5. Total auto-calculated
6. Bill saved as PDF
7. Inventory stock updates automatically

---

## Inventory CSV Format

Required columns:
- `Name`
- `Quantity`
- `Retail Price`
- `Wholesale Price`

---

## Tech Stack

- Python 3
- Tkinter
- Pandas
- FPDF

---

## Known Limitations

- No voice input yet
- CSV-based storage (no DB)
- Minimal error handling
- UI still under refinement

---

## Status

🚧 **Active Development**  
This is a **temporary README**. Will be expanded after refactoring, automation, and voice-assisted billing integration.


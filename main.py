# main.py
import tkinter as tk
from gui import create_gui

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Billing System")
    root.geometry("600x800")
    create_gui(root)
    root.mainloop()

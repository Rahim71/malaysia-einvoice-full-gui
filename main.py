import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import os
from datetime import datetime

from utils.xml_generator import generate_invoice_xml
from utils.pdf_export import export_invoice_pdf
from utils.excel_export import export_invoice_excel



# --- Setup Window ---
root = tk.Tk()
root.title("Malaysia e-Invoice System")
root.geometry("1000x800")

canvas = tk.Canvas(root)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)

canvas.configure(yscrollcommand=scroll_y.set)

canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")
canvas.create_window((0, 0), window=frame, anchor='nw')

# Enable 2-finger scroll on macOS and wheel scroll on Windows/Linux
def _on_mousewheel(event):
    if event.num == 4 or event.delta > 0:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5 or event.delta < 0:
        canvas.yview_scroll(1, "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)       # Windows
canvas.bind_all("<Button-4>", _on_mousewheel)          # macOS Up
canvas.bind_all("<Button-5>", _on_mousewheel)          # macOS Down


def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

fields = {}  # Stores all user inputs

# --- Helper to Add Labeled Field ---
def add_field(label, row, col=0, width=40, field_name=None):
    lbl = tk.Label(frame, text=label)
    lbl.grid(row=row, column=col, padx=10, pady=5, sticky='e')
    entry = tk.Entry(frame, width=width)
    entry.grid(row=row, column=col + 1, pady=5, sticky='w')
    if field_name:
        fields[field_name] = entry
    return entry

# --- Supplier Section ---
tk.Label(frame, text="--- Supplier Details ---", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
add_field("Supplier Name", 1, field_name="supplier_name")
add_field("Supplier TIN", 2, field_name="supplier_tin")
add_field("Supplier ID/Passport", 3, field_name="supplier_id")
add_field("SST Reg. Number", 4, field_name="supplier_sst")
add_field("Tourism Tax Reg. Number", 5, field_name="supplier_tourism_tax")
add_field("Supplier Email", 6, field_name="supplier_email")
add_field("MSIC Code", 7, field_name="supplier_msic")
add_field("Business Activity", 8, field_name="supplier_activity")
add_field("Supplier Address", 9, field_name="supplier_address")
add_field("Supplier Phone", 10, field_name="supplier_phone")

# --- Buyer Section ---
tk.Label(frame, text="--- Buyer Details ---", font=("Arial", 14, "bold")).grid(row=12, column=0, columnspan=2, pady=10)
add_field("Buyer Name", 13, field_name="buyer_name")
add_field("Buyer TIN", 14, field_name="buyer_tin")
add_field("Buyer ID/Passport", 15, field_name="buyer_id")
add_field("Buyer SST Reg. Number", 16, field_name="buyer_sst")
add_field("Buyer Email", 17, field_name="buyer_email")
add_field("Buyer Address", 18, field_name="buyer_address")
add_field("Buyer Phone", 19, field_name="buyer_phone")

# --- Invoice Section ---
tk.Label(frame, text="--- Invoice Details ---", font=("Arial", 14, "bold")).grid(row=21, column=0, columnspan=2, pady=10)
add_field("Invoice Version", 22, field_name="version")
add_field("Invoice Type", 23, field_name="type")
add_field("Invoice Number", 24, field_name="invoice_number")
add_field("Original Ref Number (if any)", 25, field_name="original_ref")
add_field("Date & Time", 26, field_name="datetime")
add_field("Currency Code", 27, field_name="currency")
add_field("Exchange Rate", 28, field_name="exchange_rate")
add_field("Billing Frequency", 29, field_name="billing_frequency")
add_field("Billing Period", 30, field_name="billing_period")

# --- Product/Service Section ---
tk.Label(frame, text="--- Product/Service ---", font=("Arial", 14, "bold")).grid(row=32, column=0, columnspan=2, pady=10)
add_field("Classification Code", 33, field_name="classification")
add_field("Product Description", 34, field_name="product_description")
add_field("Unit Price", 35, field_name="unit_price")
add_field("Tax Type", 36, field_name="tax_type")
add_field("Tax Rate", 37, field_name="tax_rate")
add_field("Tax Amount", 38, field_name="tax_amount")
add_field("Exemption Details", 39, field_name="tax_exemption")
add_field("Amount Exempted", 40, field_name="amount_exempted")
add_field("Subtotal", 41, field_name="subtotal")
add_field("Total Excl. Tax", 42, field_name="total_excl_tax")
add_field("Total Incl. Tax", 43, field_name="total_incl_tax")
add_field("Total Net Amount", 44, field_name="total_net")
add_field("Total Payable", 45, field_name="total_payable")
add_field("Rounding Amount", 46, field_name="rounding")
add_field("Total Taxable Amount (per type)", 47, field_name="taxable_per_type")
add_field("Quantity", 48, field_name="quantity")
add_field("Measurement", 49, field_name="measurement")
add_field("Discount Rate", 50, field_name="discount_rate")
add_field("Discount Amount", 51, field_name="discount_amount")
add_field("Fee/Charge Rate", 52, field_name="fee_rate")

# --- Payment Info ---
tk.Label(frame, text="--- Payment Info ---", font=("Arial", 14, "bold")).grid(row=54, column=0, columnspan=2, pady=10)
add_field("Payment Mode", 55, field_name="payment_mode")
add_field("Bank Account", 56, field_name="bank_account")
add_field("Payment Terms", 57, field_name="payment_terms")
add_field("Prepayment Amount", 58, field_name="prepayment_amount")
add_field("Prepayment Date", 59, field_name="prepayment_date")
add_field("Prepayment Ref", 60, field_name="prepayment_ref")
add_field("Bill Ref Number", 61, field_name="bill_ref")

# --- Actions ---

def save_invoice():
    data = {k: v.get() for k, v in fields.items()}
    filename = f"invoices/invoice-{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    os.makedirs("invoices", exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo("Saved", f"Invoice saved to {filename}")

def submit_invoice():
    messagebox.showinfo("Submit", "This would POST to IRBM or dummy server.")

#def export_xml():
#    messagebox.showinfo("Export", "This will export invoice as XML (to be implemented).")
def export_xml():
    data = {k: v.get() for k, v in fields.items()}
    xml = generate_invoice_xml(data)
    filename = f"exports/xml/invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.xml"
    os.makedirs("exports/xml", exist_ok=True)
    with open(filename, "w") as f:
        f.write(xml)
    messagebox.showinfo("Exported", f"XML invoice saved to:\n{filename}")

#def export_pdf():
#    messagebox.showinfo("Export", "This will export invoice as PDF (to be implemented).")
def export_pdf():
    data = {k: v.get() for k, v in fields.items()}
    filename = export_invoice_pdf(data)
    messagebox.showinfo("Exported", f"PDF invoice saved to:\n{filename}")
    
def export_excel():
    data = {k: v.get() for k, v in fields.items()}
    filename = export_invoice_excel(data)
    messagebox.showinfo("Exported", f"Excel invoice saved to:\n{filename}")


# --- Buttons ---
tk.Button(frame, text="💾 Save Invoice", command=save_invoice, width=20).grid(row=62, column=0, pady=20)
tk.Button(frame, text="📤 Submit Invoice", command=submit_invoice, width=20).grid(row=62, column=1)
tk.Button(frame, text="🧾 Export XML", command=export_xml, width=20).grid(row=63, column=0)
tk.Button(frame, text="🖨️ Export PDF", command=export_pdf, width=20).grid(row=63, column=1)
tk.Button(frame, text="📊 Export Excel", command=export_excel, width=20).grid(row=64, column=0)


root.mainloop()

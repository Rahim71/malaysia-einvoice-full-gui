import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import requests

from utils.xml_generator import generate_invoice_xml
from utils.pdf_export import export_invoice_pdf
from utils.excel_export import export_invoice_excel
from utils.validation import (
    is_valid_tin, is_valid_email, is_valid_msic, is_valid_currency,
    is_valid_invoice_type, is_valid_tax_type, is_required,
    is_valid_decimal, is_valid_phone, is_valid_passport, is_valid_date
)
from auth import get_token

# --- Main Window ---
root = tk.Tk()
root.title("Malaysia e-Invoice System (MyInvois)")
root.geometry("1600x900")

canvas = tk.Canvas(root)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)
canvas.configure(yscrollcommand=scroll_y.set)
canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")
canvas.create_window((0, 0), window=frame, anchor='nw')

def _on_mousewheel(event):
    canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)
frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

fields = {}

def add_field(parent, label, row, col=0, width=30, field_name=None, options=None, tooltip=None, required=False):
    font_style = ("Arial", 10, "bold italic") if required else ("Arial", 10)
    tk.Label(parent, text=label, font=font_style).grid(row=row, column=col, padx=5, pady=3, sticky='e')
    if options:
        var = tk.StringVar()
        entry = ttk.Combobox(parent, textvariable=var, values=options, width=width-2, state="readonly")
    else:
        entry = tk.Entry(parent, width=width)
    entry.grid(row=row, column=col + 1, pady=3, sticky='w')

    if tooltip:
        tk.Label(parent, text=tooltip, fg="gray", font=("Arial", 7)).grid(row=row + 1, column=col + 1, sticky='w')

    if field_name:
        fields[field_name] = entry
    return entry

# --- Column Frames ---
col1 = tk.Frame(frame)
col2 = tk.Frame(frame)
col3 = tk.Frame(frame)
col4 = tk.Frame(frame)
col1.grid(row=0, column=0, sticky="nw", padx=20, pady=10)
col2.grid(row=0, column=1, sticky="nw", padx=20, pady=10)
col3.grid(row=0, column=2, sticky="nw", padx=20, pady=10)
col4.grid(row=0, column=3, sticky="n", padx=20, pady=10)

# --- Column 1: Supplier & Buyer ---
tk.Label(col1, text="--- Supplier Details ---", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)
add_field(col1, "Supplier Name", 1, field_name="supplier_name", required=True)
add_field(col1, "Supplier TIN", 2, field_name="supplier_tin", tooltip="13-char TIN", required=True)
add_field(col1, "Supplier ID/Passport", 3, field_name="supplier_id")
add_field(col1, "SST Reg. Number", 4, field_name="supplier_sst")
add_field(col1, "Tourism Tax Reg. Number", 5, field_name="supplier_tourism_tax")
add_field(col1, "Supplier Email", 6, field_name="supplier_email", tooltip="e.g. name@domain.com", required=True)
add_field(col1, "MSIC Code", 7, field_name="supplier_msic", required=True)
add_field(col1, "Business Activity", 8, field_name="supplier_activity")
add_field(col1, "Supplier Address", 9, field_name="supplier_address")
add_field(col1, "Supplier Phone", 10, field_name="supplier_phone")

tk.Label(col1, text="--- Buyer Details ---", font=("Arial", 12, "bold")).grid(row=12, column=0, columnspan=2, pady=10)
add_field(col1, "Buyer Name", 13, field_name="buyer_name", required=True)
add_field(col1, "Buyer TIN", 14, field_name="buyer_tin", required=True)
add_field(col1, "Buyer ID/Passport", 15, field_name="buyer_id")
add_field(col1, "Buyer SST Reg. Number", 16, field_name="buyer_sst")
add_field(col1, "Buyer Email", 17, field_name="buyer_email")
add_field(col1, "Buyer Address", 18, field_name="buyer_address")
add_field(col1, "Buyer Phone", 19, field_name="buyer_phone")

# --- Column 2: Product/Service ---
tk.Label(col2, text="--- Product/Service ---", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)
add_field(col2, "Classification Code", 1, field_name="classification")
add_field(col2, "Product Description", 2, field_name="product_description", required=True)
add_field(col2, "Quantity", 3, field_name="quantity")
add_field(col2, "Measurement", 4, field_name="measurement")
add_field(col2, "Unit Price", 5, field_name="unit_price", required=True)
add_field(col2, "Discount Rate", 6, field_name="discount_rate")
add_field(col2, "Discount Amount", 7, field_name="discount_amount")
add_field(col2, "Fee/Charge Rate", 8, field_name="fee_rate")
add_field(col2, "Tax Type", 9, field_name="tax_type", options=["01", "02", "03"], required=True)
add_field(col2, "Tax Rate", 10, field_name="tax_rate")
add_field(col2, "Tax Amount", 11, field_name="tax_amount")
add_field(col2, "Exemption Details", 12, field_name="tax_exemption")
add_field(col2, "Amount Exempted", 13, field_name="amount_exempted")
add_field(col2, "Subtotal", 14, field_name="subtotal")
add_field(col2, "Total Excl. Tax", 15, field_name="total_excl_tax")
add_field(col2, "Total Incl. Tax", 16, field_name="total_incl_tax")
add_field(col2, "Total Net Amount", 17, field_name="total_net")
add_field(col2, "Total Payable", 18, field_name="total_payable")
add_field(col2, "Rounding Amount", 19, field_name="rounding")
add_field(col2, "Taxable Amt (per type)", 20, field_name="taxable_per_type")

# --- Column 3: Invoice + Payment ---
tk.Label(col3, text="--- Invoice Details ---", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)
add_field(col3, "Invoice Version", 1, field_name="version", required=True)
add_field(col3, "Invoice Type", 2, field_name="type", options=["01", "02", "03", "04"], required=True)
add_field(col3, "Invoice Number", 3, field_name="invoice_number", required=True)
add_field(col3, "Original Ref Number", 4, field_name="original_ref")
add_field(col3, "Date & Time", 5, field_name="datetime", tooltip="dd/mm/yyyy HH:MM:SS", required=True)
add_field(col3, "Currency Code", 6, field_name="currency", options=["MYR", "USD", "EUR", "JPY"], required=True)
add_field(col3, "Exchange Rate", 7, field_name="exchange_rate")
add_field(col3, "Billing Frequency", 8, field_name="billing_frequency", options=["01", "02", "03", "04", "05", "06", "07", "08", "09"])
add_field(col3, "Billing Period", 9, field_name="billing_period")

tk.Label(col3, text="--- Payment Info ---", font=("Arial", 12, "bold")).grid(row=11, column=0, columnspan=2, pady=10)
add_field(col3, "Payment Mode", 12, field_name="payment_mode")
add_field(col3, "Bank Account", 13, field_name="bank_account")
add_field(col3, "Payment Terms", 14, field_name="payment_terms")
add_field(col3, "Prepayment Amount", 15, field_name="prepayment_amount")
add_field(col3, "Prepayment Date", 16, field_name="prepayment_date")
add_field(col3, "Prepayment Ref", 17, field_name="prepayment_ref")
add_field(col3, "Bill Ref Number", 18, field_name="bill_ref")

# --- Column 4: Action Buttons ---
tk.Label(col4, text="--- Actions ---", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=10)
tk.Button(col4, text="💾 Save Invoice", command=lambda: save_invoice(), width=25).grid(row=1, column=0, pady=5)
tk.Button(col4, text="📤 Submit Invoice", command=lambda: submit_invoice(), width=25).grid(row=2, column=0, pady=5)
tk.Button(col4, text="🧾 Export XML", command=lambda: export_xml(), width=25).grid(row=3, column=0, pady=5)
tk.Button(col4, text="🖨️ Export PDF", command=lambda: export_pdf(), width=25).grid(row=4, column=0, pady=5)
tk.Button(col4, text="📊 Export Excel", command=lambda: export_excel(), width=25).grid(row=5, column=0, pady=5)

# --- Validation ---
def validate_fields():
    errors = []
    required_keys = [k for k, v in fields.items() if v.cget("font") == "Arial 10 bold italic"]
    for k in required_keys:
        if not is_required(fields[k].get()):
            errors.append(f"{k.replace('_', ' ').title()} is required")
    if "supplier_email" in fields and not is_valid_email(fields["supplier_email"].get()):
        errors.append("Invalid supplier email format.")
    return errors

# --- Actions ---
def save_invoice():
    errors = validate_fields()
    if errors:
        messagebox.showerror("Validation Error", "\n".join(errors))
        return
    data = {k: v.get() for k, v in fields.items()}
    os.makedirs("invoices", exist_ok=True)
    file_path = f"invoices/invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    messagebox.showinfo("Saved", f"Saved to {file_path}")

def submit_invoice():
    errors = validate_fields()
    if errors:
        messagebox.showerror("Validation Error", "\n".join(errors))
        return
    try:
        token = get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {
            "documents": [{
                "format": "JSON",
                "document": "base64encoded...",  # Use actual base64 content
                "documentHash": "samplehash",    # Provide valid hash
                "codeNumber": fields["invoice_number"].get()
            }]
        }
        url = os.getenv("API_BASE_URL") + "/api/v1.0/documentsubmissions/"
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 202:
            messagebox.showinfo("Submitted", "Invoice submitted successfully!")
        else:
            messagebox.showerror("Error", f"{response.status_code}: {response.text}")
    except Exception as e:
        messagebox.showerror("Submission Failed", str(e))

def export_xml():
    data = {k: v.get() for k, v in fields.items()}
    xml = generate_invoice_xml(data)
    os.makedirs("exports/xml", exist_ok=True)
    file_path = f"exports/xml/invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.xml"
    with open(file_path, "w") as f:
        f.write(xml)
    messagebox.showinfo("Exported", f"XML saved to {file_path}")

def export_pdf():
    data = {k: v.get() for k, v in fields.items()}
    file_path = export_invoice_pdf(data)
    messagebox.showinfo("Exported", f"PDF saved to {file_path}")

def export_excel():
    data = {k: v.get() for k, v in fields.items()}
    file_path = export_invoice_excel(data)
    messagebox.showinfo("Exported", f"Excel saved to {file_path}")

# --- Run App ---
root.mainloop()

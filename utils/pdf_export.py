from fpdf import FPDF
import os
from datetime import datetime

def export_invoice_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Malaysia e-Invoice", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, txt="Supplier Info", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt=f"Name: {data.get('supplier_name')}", ln=True)
    pdf.cell(200, 10, txt=f"TIN: {data.get('supplier_tin')}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, txt="Buyer Info", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt=f"Name: {data.get('buyer_name')}", ln=True)
    pdf.cell(200, 10, txt=f"TIN: {data.get('buyer_tin')}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, txt="Invoice Details", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt=f"Invoice Number: {data.get('invoice_number')}", ln=True)
    pdf.cell(200, 10, txt=f"Total: {data.get('total_payable')}", ln=True)

    filename = f"exports/pdf/invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    os.makedirs("exports/pdf", exist_ok=True)
    pdf.output(filename)
    return filename


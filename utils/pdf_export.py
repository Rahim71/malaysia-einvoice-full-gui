from fpdf import FPDF
import os
from datetime import datetime

def export_invoice_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    for k, v in data.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)
    os.makedirs("exports/pdf", exist_ok=True)
    filename = f"exports/pdf/invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

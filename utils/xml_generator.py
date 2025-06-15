import xml.etree.ElementTree as ET
from datetime import datetime

def generate_invoice_xml(data):
    root = ET.Element("Invoice")

    supplier = ET.SubElement(root, "Supplier")
    ET.SubElement(supplier, "Name").text = data.get("supplier_name")
    ET.SubElement(supplier, "TIN").text = data.get("supplier_tin")
    ET.SubElement(supplier, "ID").text = data.get("supplier_id")

    buyer = ET.SubElement(root, "Buyer")
    ET.SubElement(buyer, "Name").text = data.get("buyer_name")
    ET.SubElement(buyer, "TIN").text = data.get("buyer_tin")
    ET.SubElement(buyer, "ID").text = data.get("buyer_id")

    invoice = ET.SubElement(root, "InvoiceDetails")
    ET.SubElement(invoice, "InvoiceNumber").text = data.get("invoice_number")
    ET.SubElement(invoice, "DateTime").text = data.get("datetime") or datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    ET.SubElement(invoice, "Currency").text = data.get("currency")
    ET.SubElement(invoice, "TotalAmount").text = data.get("total_payable")

    tax = ET.SubElement(root, "TaxDetails")
    ET.SubElement(tax, "TaxType").text = data.get("tax_type")
    ET.SubElement(tax, "TaxRate").text = data.get("tax_rate")
    ET.SubElement(tax, "TaxAmount").text = data.get("tax_amount")

    return ET.tostring(root, encoding="utf-8", method="xml").decode()


def generate_invoice_xml(data):
    from xml.etree.ElementTree import Element, tostring, SubElement

    invoice = Element("Invoice")
    for key, value in data.items():
        SubElement(invoice, key).text = value
    return tostring(invoice, encoding='unicode')

import xlsxwriter
import os
from datetime import datetime

def export_invoice_excel(data):
    os.makedirs("exports/excel", exist_ok=True)
    filename = f"exports/excel/invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    workbook = xlsxwriter.Workbook(filename)
    sheet = workbook.add_worksheet()

    row = 0
    for key, value in data.items():
        sheet.write(row, 0, key)
        sheet.write(row, 1, value)
        row += 1
    workbook.close()
    return filename

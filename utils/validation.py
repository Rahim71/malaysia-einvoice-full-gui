import re
from datetime import datetime

# --- Required Field ---
def is_required(value: str) -> bool:
    return bool(value and value.strip())

# --- Email ---
def is_valid_email(email: str) -> bool:
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email or "") is not None

# --- TIN: 13 Alphanumeric ---
def is_valid_tin(tin: str) -> bool:
    return bool(tin) and len(tin) == 13 and tin.isalnum()

# --- MSIC: 5 digits ---
def is_valid_msic(msic: str) -> bool:
    return msic.isdigit() and len(msic) == 5

# --- Currency ---
def is_valid_currency(code: str) -> bool:
    return code in ["MYR", "USD", "EUR", "JPY"]

# --- Invoice Type: "01" to "04" ---
def is_valid_invoice_type(code: str) -> bool:
    return code in ["01", "02", "03", "04"]

# --- Tax Type: "01" to "03" ---
def is_valid_tax_type(code: str) -> bool:
    return code in ["01", "02", "03"]

# --- Decimal Value (e.g. 1.23) ---
def is_valid_decimal(value: str, precision=2) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False

# --- Phone Number (international format) ---
def is_valid_phone(phone: str) -> bool:
    return bool(re.match(r'^\+?\d{7,15}$', phone or ""))

# --- Date Format: "dd/mm/yyyy HH:MM:SS" ---
def is_valid_date(date_str: str, format="%d/%m/%Y %H:%M:%S") -> bool:
    try:
        datetime.strptime(date_str, format)
        return True
    except:
        return False

# --- Passport Number: Alphanumeric 6-12 chars ---
def is_valid_passport(value: str) -> bool:
    return bool(re.match(r'^[A-Z0-9]{6,12}$', value or ""))

# --- Optional: LHDN field length constraints ---
MAX_LENGTHS = {
    "supplier_name": 200,
    "supplier_email": 100,
    "supplier_phone": 20,
    "invoice_number": 20,
    "currency": 3,
    "product_description": 255,
    "bank_account": 50,
    "payment_terms": 100,
    "prepayment_ref": 20,
    "buyer_name": 200,
    "buyer_email": 100,
    "buyer_phone": 20,
    "discount_rate": 10,
    "fee_rate": 10
}

def is_valid_length(field: str, value: str) -> bool:
    return len(value) <= MAX_LENGTHS.get(field, 9999)

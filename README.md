# 🇲🇾 Malaysia e-Invoice GUI (MyInvois Integration)

A powerful and user-friendly desktop application built in Python with Tkinter to help taxpayers and intermediaries interact with the official **MyInvois e-Invoicing API** by **LHDN Malaysia**.

This tool simplifies creating, validating, saving, and submitting e-Invoices in compliance with Malaysian digital tax reporting standards.

---

## 🚀 Features

- ✅ GUI-based e-Invoice form with real-time validation
- ✅ Supports both **Taxpayer** and **Intermediary** login flows
- ✅ Save and export invoices to:
  - JSON (ERP integration)
  - XML (MyInvois submission)
  - PDF & Excel (Human-readable backups)
- ✅ Submit invoice directly to LHDN MyInvois API
- ✅ Token management using OAuth 2.0
- ✅ Field validation for:
  - TIN, Email, MSIC, Currency, Tax Type, Invoice Type
  - Passport number, Phone number, Date/Time format
  - LHDN field length restrictions

---

## 🛠️ Requirements

Install dependencies with:

```bash
pip install -r requirements.txt

Main packages:

requests
python-dotenv
xlsxwriter
reportlab
tkinter (usually bundled with Python)

⚙️ Setup
Create a .env file at the root:

env

CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
TOKEN_URL=https://identity.myinvois.hasil.gov.my/connect/token
API_BASE_URL=https://api.myinvois.hasil.gov.my
ON_BEHALF_OF=C25845632020  # Required if intermediary

🧾 How to Use
Run the GUI:

python main.py
From the interface, you can:

Fill in Supplier, Buyer, Product, and Invoice details

Save invoice locally

Export to XML, PDF, Excel

Submit to LHDN's MyInvois system directly

📤 Invoice Submission
Invoice data is posted to:

POST /api/v1.0/documentsubmissions/
Authorization is handled via JWT access token from:

POST /connect/token
🛡️ Security
Keep your .env file secure

Never commit credentials to version control

Always use HTTPS for API requests

📚 References
LHDN MyInvois SDK Docs

Official e-Invoice Guidelines

🤝 Contributions
Pull requests are welcome. Please ensure code follows LHDN SDK specifications.

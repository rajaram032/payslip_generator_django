# Payslip Generator (Django)

A simple payslip generator inspired by your screenshot. Create a company, employee, and a payslip with earnings & deductions, preview it, and export to PDF (via xhtml2pdf).

## Quickstart

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

### PDF Export
Export uses `xhtml2pdf`. If it isn't installed, the app will return an HTML page indicating that PDF isn't available.

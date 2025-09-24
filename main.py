import os
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

app = FastAPI(title="Invoice Generator API")

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class InvoiceItem(BaseModel):
    item: str
    qty: int
    price: float

class InvoiceRequest(BaseModel):
    client_name: str
    client_email: str
    items: list[InvoiceItem]
    currency: str = "$"

@app.get("/")
def root():
    return {"message": "Invoice Generator API is running"}

@app.post("/invoices")
def create_invoice(invoice: InvoiceRequest):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"invoice_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    LEFT, RIGHT = 50, width - 50

    # 1️⃣ INVOICE title at the very top
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 50, "INVOICE")

    # 2️⃣ Company header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(LEFT, height - 100, "My Company Name")
    c.setFont("Helvetica", 10)
    c.drawString(LEFT, height - 115, "1358 Business Street, Amsterdam, NL")
    c.drawString(LEFT, height - 130, "Email: info@mycompany.com | Phone: +31-020-0000000")
    c.line(LEFT, height - 140, RIGHT, height - 140)

    # 3️⃣ Invoice metadata block (pulled further down)
    issue_date = datetime.now().strftime("%b %d, %Y")
    due_date = (datetime.now() + timedelta(days=14)).strftime("%b %d, %Y")
    invoice_number = f"INV-{timestamp}"

    header_data = [
        ["Invoice #:", invoice_number],
        ["Issue Date:", issue_date],
        ["Due Date:", due_date],
    ]
    header_table = Table(header_data, colWidths=[100, 200])
    header_table.setStyle(TableStyle([
        ("FONT", (0,0), (0,-1), "Helvetica-Bold", 12),
        ("FONT", (1,0), (1,-1), "Helvetica", 12),
        ("ALIGN", (1,0), (1,-1), "LEFT"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    header_table.wrapOn(c, 0, 0)
    header_table.drawOn(c, LEFT, height - 220)  # moved down

    # 4️⃣ Client info (also moved down to avoid overlap)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(LEFT, height - 260, "Bill To:")
    c.setFont("Helvetica", 10)
    c.drawString(LEFT, height - 275, invoice.client_name)
    c.drawString(LEFT, height - 290, invoice.client_email)

    # 5️⃣ Items table
    items_data = [["Item", "Qty", "Price", "Total"]]
    total = 0.0
    for it in invoice.items:
        line_total = it.qty * it.price
        items_data.append([
            it.item,
            str(it.qty),
            f"{invoice.currency}{it.price:.2f}",
            f"{invoice.currency}{line_total:.2f}",
        ])
        total += line_total

    items_table = Table(items_data, colWidths=[200, 60, 100, 100])
    items_table.setStyle(TableStyle([
        ("FONT", (0,0), (-1,0), "Helvetica-Bold", 12),
        ("FONT", (0,1), (-1,-1), "Helvetica", 10),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("ALIGN", (1,1), (-1,-1), "RIGHT"),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
    ]))
    items_table.wrapOn(c, 0, 0)
    items_table.drawOn(c, LEFT, height - 360)

    # 6️⃣ Grand total
    total_data = [["Grand Total:", f"{invoice.currency}{total:.2f}"]]
    total_table = Table(total_data, colWidths=[360, 100])
    total_table.setStyle(TableStyle([
        ("FONT", (0,0), (-1,-1), "Helvetica-Bold", 12),
        ("ALIGN", (1,0), (1,0), "RIGHT"),
        ("LINEABOVE", (0,0), (-1,0), 1, colors.black),
    ]))
    total_table.wrapOn(c, 0, 0)
    total_table.drawOn(c, LEFT, height - 410)

    # 7️⃣ Footer
    footer_data = [
        ["Payment due within 14 days"],
        ["Bank: Example Bank | IBAN: NL00BANK0123456789 | SWIFT: EXAMPBANK"],
        ["Thank you for your business!"],
    ]
    footer_table = Table(footer_data, colWidths=[450])
    footer_table.setStyle(TableStyle([
        ("FONT", (0,0), (-1,-1), "Helvetica-Oblique", 10),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
    ]))
    footer_table.wrapOn(c, 0, 0)
    footer_table.drawOn(c, LEFT, 100)

    c.save()
    return {"filename": filename}

@app.get("/invoices/{filename}")
def get_invoice(filename: str):
    filepath = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Invoice not found")
    return FileResponse(filepath, media_type="application/pdf", filename=filename)

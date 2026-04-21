from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
from datetime import date

def generate_cover_letter_pdf(text_path, output_pdf, user_name="Dilendra Barman"):
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    today = date.today().strftime("%d %B %Y")

    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 1*inch, user_name)
    c.setFont("Helvetica", 11)
    c.drawString(1*inch, height - 1.2*inch, f"Date: {today}")
    c.line(1*inch, height - 1.3*inch, width - 1*inch, height - 1.3*inch)

    # Body
    y = height - 1.8*inch
    c.setFont("Helvetica", 11)
    with open(text_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        for subline in line.split("\n"):
            if y < 1*inch:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = height - 1*inch
            c.drawString(1*inch, y, subline.strip())
            y -= 14

    # Signature
    y -= 20
    c.drawString(1*inch, y, "Sincerely,")
    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, user_name)

    c.save()
    print(f"📄 Cover letter PDF saved to: {output_pdf}")
    return output_pdf

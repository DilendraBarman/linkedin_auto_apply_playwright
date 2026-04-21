# ai/pdf_generator.py

from docx import Document
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
import os

def text_to_pdf(text, output_path):
    c = canvas.Canvas(output_path)
    text_object = c.beginText(40, 800)
    text_object.setFont("Helvetica", 11)

    for line in text.split("\n"):
        text_object.textLine(line)

    c.drawText(text_object)
    c.save()

def generate_resume_pdf(resume_text, filename="custom_resume.pdf"):
    text_to_pdf(resume_text, filename)
    return filename

def generate_cover_letter_pdf(cover_letter_text, filename="cover_letter.pdf"):
    text_to_pdf(cover_letter_text, filename)
    return filename

import pdfplumber
import re

def extract_text_from_pdf(file):
    text = ''
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text

def extract_email(text: str):
    match = re.search(r'\S+@\S+', text)
    return match.group(0) if match else None


def extract_phone(text: str):
    match = re.search(r'\b\d{10}\b', text)
    return match.group(0) if match else None


def extract_name(text: str):
    lines = text.split("\n")
    for line in lines:
        if line.strip():
            return line.strip()
    return None


def parse_resume(text: str):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
    }


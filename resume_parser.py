import os
from PyPDF2 import PdfReader
from docx import Document


def extract_text(filepath):

    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":

        reader = PdfReader(filepath)

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    elif ext == ".docx":

        doc = Document(filepath)

        return "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )

    elif ext == ".txt":

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    return ""
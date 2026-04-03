from pypdf import PdfReader
from docx import Document

def parse_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def parse_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def parse_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_text(file_path: str) -> str:

    if file_path.endswith(".pdf"):
        return parse_pdf(file_path)

    if file_path.endswith(".docx"):
        return parse_docx(file_path)

    if file_path.endswith(".txt"):
        return parse_txt(file_path)

    raise ValueError("Unsupported file format")
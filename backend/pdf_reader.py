import fitz
from pathlib import Path


def read_pdf(file_path):
    """
    Reads a PDF file and returns all extracted text as a single string.
    """

    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    print("\n========== PDF READER ==========")
    print(f"Reading: {pdf_path.name}")

    document = fitz.open(pdf_path)

    full_text = ""

    print(f"Total Pages: {document.page_count}\n")

    for page_number in range(document.page_count):
        print(f"Extracting Page {page_number + 1}...")

        page = document.load_page(page_number)
        full_text += page.get_text()

    document.close()

    print("\nPDF extraction completed successfully.\n")

    return full_text
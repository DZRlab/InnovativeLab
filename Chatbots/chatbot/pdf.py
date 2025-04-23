__all__ = ["parse_pdf_file"]

from pypdf import PdfReader


def parse_pdf_file(file):
    raw = PdfReader(file)
    npages = raw.get_num_pages()
    # Initialize empty text string
    text = ""
    # Loop through all pages in PDF file and extract the text
    for i in range(npages):
        text += raw.get_page(i).extract_text()

    # We need to cap the text length to avoid hitting the Azure API limit
    return text[: 1024 * 64]

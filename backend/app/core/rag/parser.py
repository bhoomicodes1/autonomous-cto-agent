import re

from pypdf import PdfReader


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.
    """

    # Multiple spaces -> single space
    text = re.sub(r"[ \t]+", " ", text)

    # Multiple newlines -> max 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces between individual characters
    # Example:
    # B H O O M I  -> BHOOMI
    text = re.sub(r'(?<=\b[A-Za-z]) (?=[A-Za-z]\b)', '', text)

    return text.strip()


def read_pdf(path: str) -> str:

    reader = PdfReader(path)

    pages = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            pages.append(page_text)

    text = "\n".join(pages)

    return clean_text(text)
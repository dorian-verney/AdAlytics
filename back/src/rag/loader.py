from pypdf import PdfReader
from back.config.config import DATA_PATH
import os

def load_pdf(path: str) -> list[str]:
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages):
        pages.append(f"Page {i+1}: {page.extract_text()}")
    return pages

def load_md(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()




if __name__ == "__main__":
    pages = load_pdf(os.path.join(DATA_PATH, "shampoo-ad.pdf"))
    print(pages)
    # # md = load_md("data/ad.md")
    # # print(md)
import fitz  # PyMuPDF
from langdetect import detect

class DocumentExtractor:
    def __init__(self, path):
        self.path = path
        self.doc = fitz.open(path)

    def extract_sections(self):
        sections = []

        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text()
            lines = text.split('\n')

            for line in lines:
                if line.strip() and line.strip().istitle():  # crude way to guess "heading-like" lines
                    section = {
                        "document": self.path.split('/')[-1],
                        "page_number": page_num + 1,
                        "section_title": line.strip(),
                        "text": text,
                        "language": detect(text[:100])  # detect language from a sample
                    }
                    sections.append(section)

        return sections

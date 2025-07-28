import os
import fitz  # PyMuPDF
from langdetect import detect
import re


class DocumentExtractor:
    def __init__(self, path):
        self.path = path
        self.doc = fitz.open(path)

    def extract_sections(self):
        sections = []
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            blocks = page.get_text("dict")["blocks"]
            lines = []
            
            # Collect all lines with their positions
            for block in blocks:
                for line in block.get("lines", []):
                    line_text = " ".join([span["text"].strip() for span in line.get("spans", [])])
                    if line_text:
                        lines.append(line_text)

            # Heuristic: Lines that look like section titles (capitalized or numbered)
            heading_indices = []
            for i, line in enumerate(lines):
                if self._is_heading(line):
                    heading_indices.append(i)

            # Extract section info between heading indices
            for idx, start_idx in enumerate(heading_indices):
                end_idx = heading_indices[idx + 1] if idx + 1 < len(heading_indices) else len(lines)
                section_title = lines[start_idx].strip()
                section_text = " ".join(lines[start_idx + 1:end_idx]).strip()

                if section_title not in [s["section_title"] for s in sections]:  # deduplicate
                    section = {
                        "document": os.path.basename(self.path),
                        "page_number": page_num + 1,
                        "section_title": section_title,
                        "text": section_text[:500],  # limit text length for scoring
                        "language": detect(section_title) if len(section_title) > 3 else "unknown"
                    }
                    sections.append(section)

        return sections

    def _is_heading(self, text):
        """
        Heuristic to detect headings:
        - Starts with number (e.g., "1.", "2.1") or is title-cased and short
        - Not too long, not too short
        """
        return (
            re.match(r"^\d+(\.\d+)*[\).]?\s+", text) or
            (text.istitle() and 4 < len(text) < 80)
        )

import io
from pypdf import PdfReader

class PDFParser:
    @staticmethod
    def parse_pdf(file_bytes: bytes) -> str:
        """
        Reads syllabus PDF from bytes, extracts all text, and cleans the formatting.
        """
        try:
            pdf_file = io.BytesIO(file_bytes)
            reader = PdfReader(pdf_file)
            extracted_text = []
            
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    extracted_text.append(page_text)
            
            raw_text = "\n".join(extracted_text)
            return PDFParser.clean_text(raw_text)
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans redundant whitespace, blank lines, and normalizes formatting.
        """
        lines = text.split("\n")
        cleaned_lines = []
        for line in lines:
            # Strip trailing/leading spaces
            stripped = line.strip()
            if stripped:
                # Remove multiple consecutive spaces
                cleaned_line = " ".join(stripped.split())
                cleaned_lines.append(cleaned_line)
        
        return "\n".join(cleaned_lines)

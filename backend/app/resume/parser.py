"""PDF resume text extraction."""

from pypdf import PdfReader

MAX_PDF_PAGES = 10
MAX_TEXT_CHARS = 60_000


class ResumeParser:
    def parse_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        chunks: list = []
        for page in reader.pages[:MAX_PDF_PAGES]:
            try:
                extracted = page.extract_text() or ""
            except Exception:
                extracted = ""
            if extracted:
                chunks.append(extracted)
            if sum(len(part) for part in chunks) >= MAX_TEXT_CHARS:
                break
        return "\n".join(chunks)[:MAX_TEXT_CHARS]

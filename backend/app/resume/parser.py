from pypdf import PdfReader


class ResumeParser:

    def parse_pdf(
        self,
        file_path: str
    ):

        reader = PdfReader(
            file_path
        )

        text = ""

        for page in reader.pages:

            extracted = (
                page.extract_text()
            )

            if extracted:

                text += extracted

        return text
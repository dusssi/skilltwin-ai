from app.resume.parser import (
    ResumeParser
)

from app.resume.analyzer import (
    ResumeAnalyzer
)


class ResumeService:

    def __init__(self):

        self.parser = (
            ResumeParser()
        )

        self.analyzer = (
            ResumeAnalyzer()
        )

    def analyze_pdf(
        self,
        file_path: str
    ):

        text = (
            self.parser.parse_pdf(
                file_path
            )
        )

        return (
            self.analyzer.analyze(
                text
            )
        )
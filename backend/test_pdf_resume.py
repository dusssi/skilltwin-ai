from app.resume.parser import (
    ResumeParser
)

parser = (
    ResumeParser()
)

text = parser.parse_pdf(
    "resume.pdf"
)

print()

print(
    "EXTRACTED TEXT:"
)

print()

safe_text = text.encode(
    "ascii",
    errors="ignore"
).decode()

print(
    safe_text
)
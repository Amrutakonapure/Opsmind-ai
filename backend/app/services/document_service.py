from pathlib import Path

from pypdf import PdfReader


def extract_text_from_file(file_path: str, file_extension: str) -> str:
    """
    Extract text from TXT, Markdown, and PDF files.
    """

    extension = file_extension.lower()

    if extension in [".txt", ".md"]:
        return Path(file_path).read_text(
            encoding="utf-8",
            errors="ignore"
        )

    if extension == ".pdf":
        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    raise ValueError(
        "Unsupported file type. Only .txt, .md and .pdf are supported."
    )


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[str]:
    """
    Split text into overlapping chunks.
    """

    text = text.strip()

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError(
            "Overlap must be smaller than chunk size."
        )

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
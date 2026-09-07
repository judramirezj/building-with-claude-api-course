from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path

from pydantic import Field

SUPPORTED_EXTENSIONS = {"pdf", "docx"}


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(
        description="Absolute or relative path to a .pdf or .docx file on the local filesystem"
    ),
) -> str:
    """Read a PDF or DOCX file from disk and return its contents as markdown.

    Opens the file at the given path, reads its bytes, and converts the document
    to markdown-formatted text (headers, lists, tables, etc.) using markitdown.

    When to use:
    - When you have a path to a .pdf or .docx file and need its text content
    - When you want document structure preserved as markdown

    When not to use:
    - When the document is already in memory as bytes: use
      `binary_document_to_markdown` instead
    - For formats other than PDF or DOCX

    Examples:
    >>> document_path_to_markdown("tests/fixtures/mcp_docs.docx")
    '# MCP Documentation\\n...'
    >>> document_path_to_markdown("/tmp/report.pdf")
    'The report details the state of a 20m condenser tower.\\n...'
    """
    path = Path(file_path)

    if not path.is_file():
        raise ValueError(f"No file found at path: {file_path}")

    file_type = path.suffix.lower().lstrip(".")
    if file_type not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{path.suffix}'. "
            f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    return binary_document_to_markdown(path.read_bytes(), file_type)

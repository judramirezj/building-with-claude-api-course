import os
import pytest
from tools.document import binary_document_to_markdown, document_path_to_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathToMarkdown:
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_converts_docx_path(self):
        """Reads a DOCX file from disk and converts it to markdown."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "#" in result or "-" in result or "*" in result

    def test_converts_pdf_path(self):
        """Reads a PDF file from disk and converts it to markdown."""
        result = document_path_to_markdown(self.PDF_FIXTURE)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_missing_file_raises_value_error(self):
        """A path that does not exist raises ValueError."""
        with pytest.raises(ValueError, match="No file found"):
            document_path_to_markdown(os.path.join(self.FIXTURES_DIR, "nope.pdf"))

    def test_unsupported_extension_raises_value_error(self, tmp_path):
        """A file with an unsupported extension raises ValueError."""
        txt_file = tmp_path / "notes.txt"
        txt_file.write_text("plain text")

        with pytest.raises(ValueError, match="Unsupported file type"):
            document_path_to_markdown(str(txt_file))

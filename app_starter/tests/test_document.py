import os
import shutil
from pathlib import Path

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

    # 1. DOCX path -> markdown
    def test_converts_docx_path(self):
        """Reads a DOCX file from disk and converts it to markdown."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "#" in result or "-" in result or "*" in result

    # 2. PDF path -> markdown
    def test_converts_pdf_path(self):
        """Reads a PDF file from disk and converts it to markdown."""
        result = document_path_to_markdown(self.PDF_FIXTURE)

        assert isinstance(result, str)
        assert len(result) > 0

    # 3. Parity with binary_document_to_markdown (no drift from the path wrapper)
    @pytest.mark.parametrize(
        "fixture,ext", [("DOCX_FIXTURE", "docx"), ("PDF_FIXTURE", "pdf")]
    )
    def test_matches_binary_conversion(self, fixture: str, ext: str):
        """The path wrapper returns exactly what the bytes helper returns."""
        path = getattr(self, fixture)
        with open(path, "rb") as f:
            expected = binary_document_to_markdown(f.read(), ext)

        assert document_path_to_markdown(path) == expected

    # 4. Known-content assertion
    def test_extracts_known_content(self):
        """Converted output contains text known to be in the fixtures."""
        for path in (self.DOCX_FIXTURE, self.PDF_FIXTURE):
            result = document_path_to_markdown(path)
            assert "Model Context Protocol" in result
            assert "Key Features of this Python SDK" in result

    # 5. Relative path (resolved against the current working directory)
    def test_accepts_relative_path(self, monkeypatch: pytest.MonkeyPatch):
        """A path relative to the cwd is resolved and converted."""
        monkeypatch.chdir(self.FIXTURES_DIR)
        result = document_path_to_markdown("mcp_docs.docx")

        assert "Model Context Protocol" in result

    # 6. Path starting with '~' is expanded to the home directory
    def test_expands_user_home(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """A '~/...' path is expanded against $HOME before reading."""
        home = tmp_path / "home"
        home.mkdir()
        shutil.copy(self.PDF_FIXTURE, home / "mcp_docs.pdf")
        monkeypatch.setenv("HOME", str(home))
        monkeypatch.setenv("USERPROFILE", str(home))  # Windows equivalent

        result = document_path_to_markdown("~/mcp_docs.pdf")

        assert "Model Context Protocol" in result

    # 7. Extension inference is case-insensitive
    def test_extension_is_case_insensitive(self, tmp_path: Path):
        """An uppercased extension (.PDF / .DOCX) is still recognized."""
        upper = tmp_path / "mcp_docs.PDF"
        shutil.copy(self.PDF_FIXTURE, upper)

        result = document_path_to_markdown(str(upper))

        assert "Model Context Protocol" in result

    # 8. Accepts a pathlib.Path, not just a str
    def test_accepts_path_object(self):
        """A pathlib.Path argument works the same as a string path."""
        result = document_path_to_markdown(Path(self.DOCX_FIXTURE))

        assert "Model Context Protocol" in result

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv venv && source .venv/bin/activate   # create/activate virtualenv
uv pip install -e .                     # install package in editable mode

uv run main.py                          # start the MCP server (stdio transport)
uv run pytest                           # run all tests
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx  # single test
```

`uv run main.py` produces no output and appears to hang — that is correct. The server
communicates over stdio (JSON-RPC on stdin/stdout) and is meant to be launched by an MCP
client (Claude Desktop, MCP Inspector, or `../cli_project/mcp_client.py`), not run
interactively. Use `npx @modelcontextprotocol/inspector uv run main.py` to exercise it.

Python 3.10–3.13. This is the starter project for a "building with the Claude API" course;
`../cli_project/` holds a fuller MCP server + client example (tools, resources, prompts).

## Architecture

An MCP server built on `FastMCP` (from the `mcp` package). Two layers, kept separate:

- **Tool implementations** live in `tools/` as plain functions with no MCP import —
  pydantic `Field`-annotated parameters in, plain values out. This keeps them
  unit-testable in isolation (`tests/test_document.py` calls the function directly, never
  through the server).
- **Registration** happens in `main.py`: `mcp = FastMCP("docs")`, then one
  `mcp.tool()(function_name)` line per tool.

`tools/document.py` wraps `markitdown` to convert in-memory document bytes (docx, pdf) to
markdown, via `BytesIO` + `StreamInfo(extension=...)`. Test fixtures
(`tests/fixtures/mcp_docs.{docx,pdf}`) are real sample documents used to verify conversion
end to end.

## Defining MCP tools

**Two registration styles, both valid:**

1. This repo's style — keep the function MCP-free in `tools/`, register separately:
   ```python
   # tools/math.py — no mcp import
   from pydantic import Field
   def add(a: float = Field(description="First number"),
           b: float = Field(description="Second number")) -> float:
       """..."""
       return a + b

   # main.py
   from tools.math import add
   mcp.tool()(add)
   ```
2. Decorator style (see `../cli_project/mcp_server.py`) — inline, with explicit metadata:
   ```python
   @mcp.tool(name="read_doc_contents",
             description="Read the content of a document and return it as a string.")
   def read_document(doc_id: str = Field(description="Id of the document to read")):
       ...
   ```
   With `@mcp.tool()` and no args, the tool name is the function name and the description
   is the docstring. Passing `name=`/`description=` overrides both. Prefer style 1 here so
   logic stays testable without a server.

**Parameters:**
- Every parameter gets `Field(description=...)` from pydantic — this text is what the model
  sees when choosing arguments. Bare type hints alone are not enough.
- Type hints drive the generated JSON schema. Use precise types (`float`, `list[str]`,
  `Literal[...]`, pydantic models); avoid bare `dict`/`Any`.
- Keep the signature flat — primitives and simple lists are easier for the model than
  deeply nested objects.

**Docstring = tool description the model reads.** Structure it (per README):
- One-line summary first.
- Then detailed behavior.
- Then "When to use" *and* when **not** to use it — this most reduces wrong tool calls.
- Then usage examples with expected input/output (doctest-style, as in `tools/math.py`).

**Return values:** return a plain string or JSON-serializable value. A raw `str` return is
delivered as text content. Don't print to stdout — stdout is the JSON-RPC channel and any
stray write corrupts the protocol (`../cli_project` sets `FastMCP(log_level="ERROR")` to
keep the transport quiet).

**Errors:** raise a normal exception (e.g. `raise ValueError(f"Doc {doc_id} not found")`);
FastMCP converts it into a proper MCP tool error for the client. Don't catch-and-return
error strings — the model can't distinguish those from success.

**Adding a tool:** write and test the function in `tools/`, import it in `main.py`,
register with one line, add a test that calls it directly.

**Related primitives** (`FastMCP` also exposes, see `../cli_project/mcp_server.py`):
`@mcp.resource("scheme://path/{param}", mime_type=...)` for readable data the client pulls
in as context, and `@mcp.prompt(name=..., description=...)` returning
`list[mcp.server.fastmcp.prompts.base.Message]` for reusable prompt templates. Tools are
for model-invoked actions; resources for client-controlled context; prompts for
user-initiated workflows.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal workspace for Anthropic's "Building with the Claude API" course. It is **not one
application** — it is three independent parts plus lesson notebooks. Treat each subdirectory
as its own project with its own virtualenv, `pyproject.toml`, and Python version.

| Path | What it is |
|------|------------|
| `building_with_claude_api*.ipynb` | The course lessons — runnable notebooks covering messages, streaming, structured output, prompt evaluation/grading, prompt engineering, tool use, the text-editor & web-search tools, and (in `_features`) images/PDF/citations/prompt caching/Files API, and (in `_rag`) VoyageAI embeddings + a BM25 / multi-index RAG pipeline. |
| `cli_project/` | A working MCP chat CLI: an Anthropic agentic loop wired to MCP servers over stdio. See below. |
| `app_starter/` | A `FastMCP` server scaffold (course exercise). Has its own `CLAUDE.md` with detailed MCP-tool authoring guidance — read that before touching `app_starter/`. |
| `main.py`, `test.py` | Throwaway pi-calculation demo, unrelated to the course. Ignore unless asked. |

The notebooks and root files share the **root** virtualenv (`.venv/`, Python >=3.14,
`anthropic` + `voyageai` + `ipykernel`). `cli_project/` and `app_starter/` each have their own.

## Commands

Root / notebooks:
```bash
uv sync                       # install root deps into .venv/
uv run pytest test.py         # run the pi demo's tests (pytest collects test_* functions)
```

`cli_project/` (run from inside `cli_project/`):
```bash
uv venv && source .venv/bin/activate
uv pip install -e .
uv run main.py                # start the interactive MCP chat CLI
uv run main.py path/to/other_server.py   # attach extra MCP servers as positional args
```

`app_starter/` — see `app_starter/CLAUDE.md` (`uv run main.py` to serve, `uv run pytest`,
single test: `uv run pytest tests/test_document.py::TestClass::test_name`).

## Environment variables

Copy `.env.example` to `.env` in whichever subproject you are running.
- Root notebooks: `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY` (RAG notebook only).
- `cli_project/`: `ANTHROPIC_API_KEY` **and** `CLAUDE_MODEL` (both asserted non-empty at
  startup in `cli_project/main.py`); optional `USE_UV=1` to launch the bundled MCP server
  with `uv run` instead of `python`.

## cli_project architecture

An agentic loop over MCP, split so the Anthropic call and the MCP transport never touch
each other directly:

- `core/claude.py` — thin `Anthropic` SDK wrapper. `Claude.chat()` builds the params dict
  (model, 8k max tokens, optional `tools`/`system`/`thinking`) and returns the raw `Message`.
- `core/chat.py` — `Chat.run()` is the loop: append query → `claude.chat(tools=…)` →
  if `stop_reason == "tool_use"`, execute the tools and feed results back as a user message,
  else return the text. `Chat` is transport-agnostic.
- `core/cli_chat.py` — `CliChat` subclass adds course-specific query preprocessing:
  `@doc_id` mentions are expanded inline from MCP **resources** (`docs://documents/{id}`);
  `/command arg` lines are turned into MCP **prompts** via `get_prompt()` and spliced into
  the message history (`convert_prompt_messages_to_message_params`). A plain query is
  wrapped in a context-injection template.
- `core/cli.py` — `prompt-toolkit` REPL: tab-completion and autosuggest for `/commands`
  (from `list_prompts()`) and `@documents` (from the `docs://documents` resource).
- `mcp_client.py` — `MCPClient`, one per server: an async-context-managed `ClientSession`
  over `stdio_client`, exposing `list_tools` / `call_tool` / `list_prompts` / `get_prompt` /
  `read_resource`.
- `core/tools.py` — `ToolManager` aggregates tools across all connected clients, routes
  each `tool_use` block to the client that owns that tool, and formats `tool_result` blocks.
- `mcp_server.py` — the default bundled `FastMCP` server (`DocumentMCP`): an in-memory
  `docs` dict exposed as `read_doc_contents`/`edit_document` tools, `docs://documents[/{id}]`
  resources, and a `format` prompt. Contains intentional course TODOs (e.g. a `summarize`
  prompt to implement).

`main.py` wires it together: always starts `mcp_server.py` as `doc_client`, plus one
`MCPClient` per server script passed on the argv, all under one `AsyncExitStack`.

### The three MCP primitives, as used here
- **Tools** — model-invoked actions (`read_doc_contents`, `edit_document`).
- **Resources** — client-pulled context, addressed by URI (`docs://documents/{id}`);
  surfaced to the user as `@mentions`.
- **Prompts** — user-initiated templates returning a message list (`/format`); expanded
  into the conversation before the next Claude call.

## Conventions

- Always apply type annotations to function arguments and return types.
- MCP tool functions: pydantic `Field(description=...)` on every parameter, structured
  docstring (summary → behavior → when to use / when not to use → examples), raise
  exceptions rather than returning error strings, never `print` (stdout is the JSON-RPC
  channel). Full rationale in `app_starter/CLAUDE.md`.
- `cli_project/` has no linter or type checker configured.

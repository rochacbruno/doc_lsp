import logging
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlparse

from lsprotocol import types
from pygls.lsp.server import LanguageServer

from .parser import parse_document

server = LanguageServer("doc-lsp", "v1")

# Cache for parsed markdown documents
_doc_cache = {}

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    ".py",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".conf",
    ".properties",
}


def get_word_at_position(text: str, line: int, character: int) -> Optional[str]:
    """Extract the word/variable at the given position."""
    lines = text.split("\n")
    if line >= len(lines):
        return None

    line_text = lines[line]
    if character > len(line_text):
        return None

    # Find word boundaries (alphanumeric and underscore)
    # Also include dots for nested variables like DATABASES.default.NAME
    start = character
    end = character

    # Find start of word
    while start > 0 and (
        line_text[start - 1].isalnum() or line_text[start - 1] in "_."
    ):
        start -= 1

    # Find end of word
    while end < len(line_text) and (line_text[end].isalnum() or line_text[end] in "_."):
        end += 1

    word = line_text[start:end].strip()

    # Remove leading/trailing dots
    word = word.strip(".")

    return word if word else None


def get_doc_file_path(file_uri: str) -> Optional[Path]:
    """Get the corresponding .md documentation file path."""
    # Parse the file URI
    parsed = urlparse(file_uri)
    file_path = Path(unquote(parsed.path))

    # Check if file extension is supported
    if file_path.suffix not in SUPPORTED_EXTENSIONS:
        # Check if it's a plain text file (no extension or .txt)
        if file_path.suffix not in ("", ".txt"):
            return None

    # Construct the markdown file path
    doc_file = file_path.parent / f"{file_path.name}.md"

    if doc_file.exists():
        return doc_file

    return None


def load_documentation(doc_file: Path) -> Optional[dict]:
    """Load and parse the documentation file."""
    # Check cache first
    file_key = str(doc_file)
    mtime = doc_file.stat().st_mtime

    if file_key in _doc_cache:
        cached_mtime, cached_doc = _doc_cache[file_key]
        if cached_mtime == mtime:
            return cached_doc

    # Parse the markdown file
    try:
        content = doc_file.read_text(encoding="utf-8")
        document = parse_document(content)

        # Cache the parsed document
        _doc_cache[file_key] = (mtime, document)

        return document
    except Exception as e:
        logging.error(f"Error parsing {doc_file}: {e}")
        return None


@server.feature(types.TEXT_DOCUMENT_HOVER)
def hover(ls: LanguageServer, params: types.HoverParams):
    """Handle hover requests."""
    pos = params.position
    document_uri = params.text_document.uri
    document = ls.workspace.get_text_document(document_uri)

    # Get the word at the cursor position
    word = get_word_at_position(document.source, pos.line, pos.character)

    if not word:
        return None

    # Get the documentation file path
    doc_file = get_doc_file_path(document_uri)

    if not doc_file:
        return None

    # Load the documentation
    doc = load_documentation(doc_file)

    if not doc:
        return None

    # Look up the variable in the documentation
    variable = doc.get_variable(word)

    if not variable:
        return None

    # Format the hover content
    hover_content = (
        f"## {variable.name}\n\n{variable.doc}"
        if variable.doc
        else f"## {variable.name}"
    )

    return types.Hover(
        contents=types.MarkupContent(
            kind=types.MarkupKind.Markdown,
            value=hover_content,
        ),
        range=types.Range(
            start=types.Position(line=pos.line, character=0),
            end=types.Position(line=pos.line + 1, character=0),
        ),
    )


@server.feature(types.WORKSPACE_DID_CHANGE_WATCHED_FILES)
def did_change_watched_files(
    ls: LanguageServer, params: types.DidChangeWatchedFilesParams
):
    """Handle file change notifications to invalidate cache."""
    for change in params.changes:
        # Parse the file URI
        parsed = urlparse(change.uri)
        file_path = Path(unquote(parsed.path))

        # If it's a markdown file, invalidate its cache
        if file_path.suffix == ".md":
            file_key = str(file_path)
            if file_key in _doc_cache:
                del _doc_cache[file_key]
                logging.info(f"Cache invalidated for {file_path.name}")


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    server.start_io()

import logging
from datetime import datetime

from lsprotocol import types

from pygls.lsp.server import LanguageServer


DATE_FORMATS = [
    "%H:%M:%S",
    "%d/%m/%y",
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S",
]
server = LanguageServer("doc-lsp", "v1")


@server.feature(types.TEXT_DOCUMENT_HOVER)
def hover(ls: LanguageServer, params: types.HoverParams):
    """Right now this is just an example.
    The actual implementation will perform the lookup for the variable
    and return the documentation for it.
    """
    pos = params.position
    document_uri = params.text_document.uri
    document = ls.workspace.get_text_document(document_uri)

    # Will have to detect document type and then parse the AST for the document
    # using the parser.py module

    try:
        line = document.lines[pos.line]

        server.window_log_message(
            types.LogMessageParams(
                message=f"Line: {line}",
                type=types.MessageType.Info,
            )
        )
    except IndexError:
        return None

    for fmt in DATE_FORMATS:
        try:
            value = datetime.strptime(line.strip(), fmt)
            break
        except ValueError:
            pass

    else:
        # No valid datetime found.
        return None

    hover_content = [
        f"# {value.strftime('%a %d %b %Y')}",
        "",
        "| Format | Value |",
        "|:-|-:|",
        *[f"| `{fmt}` | {value.strftime(fmt)} |" for fmt in DATE_FORMATS],
    ]

    return types.Hover(
        contents=types.MarkupContent(
            kind=types.MarkupKind.Markdown,
            value="\n".join(hover_content),
        ),
        range=types.Range(
            start=types.Position(line=pos.line, character=0),
            end=types.Position(line=pos.line + 1, character=0),
        ),
    )


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    server.start_io()

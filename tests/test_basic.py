import pytest
from lsprotocol import types
from pytest_lsp import LanguageClient


@pytest.mark.asyncio(loop_scope="module")
async def test_server_info(client: LanguageClient):
    """Test that the LSP server provides correct server info."""
    # The server info is available in the initialization response
    response = client.initialization_response
    assert response.server_info is not None
    assert response.server_info.name == "doc-lsp"
    assert response.server_info.version == "v1"


@pytest.mark.asyncio(loop_scope="module")
async def test_hover_without_documentation(client: LanguageClient):
    """Test hover functionality on a file without corresponding .md documentation."""

    test_uri = "file:///test.txt"
    test_content = "SOME_VARIABLE = 'value'\nOTHER_VAR = 123"

    client.text_document_did_open(
        types.DidOpenTextDocumentParams(
            text_document=types.TextDocumentItem(
                uri=test_uri, language_id="text", version=1, text=test_content
            )
        )
    )

    # Test hover on a variable without documentation file
    hover_response = await client.text_document_hover_async(
        types.HoverParams(
            text_document=types.TextDocumentIdentifier(uri=test_uri),
            position=types.Position(line=0, character=5),
        )
    )

    # Should return None when no documentation file exists
    assert hover_response is None


@pytest.mark.asyncio(loop_scope="module")
async def test_hover_on_non_datetime(client: LanguageClient):
    """Test that hover returns None for non-datetime text."""

    test_uri = "file:///test2.txt"
    test_content = "This is not a datetime\nJust regular text"

    client.text_document_did_open(
        types.DidOpenTextDocumentParams(
            text_document=types.TextDocumentItem(
                uri=test_uri, language_id="text", version=1, text=test_content
            )
        )
    )

    hover_response = await client.text_document_hover_async(
        types.HoverParams(
            text_document=types.TextDocumentIdentifier(uri=test_uri),
            position=types.Position(line=0, character=5),
        )
    )

    assert hover_response is None

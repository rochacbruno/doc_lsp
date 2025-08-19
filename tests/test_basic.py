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
async def test_hover_on_datetime(client: LanguageClient):
    """Test hover functionality on a datetime string."""
    
    test_uri = "file:///test.txt"
    test_content = "2024-01-15\nSome other text\n12:30:45"
    
    client.text_document_did_open(
        types.DidOpenTextDocumentParams(
            text_document=types.TextDocumentItem(
                uri=test_uri,
                language_id="text",
                version=1,
                text=test_content
            )
        )
    )
    
    # Test hover on the date
    hover_response = await client.text_document_hover_async(
        types.HoverParams(
            text_document=types.TextDocumentIdentifier(uri=test_uri),
            position=types.Position(line=0, character=5)
        )
    )
    
    assert hover_response is not None
    assert hover_response.contents.kind == types.MarkupKind.Markdown
    assert "2024" in hover_response.contents.value
    assert "Mon 15 Jan 2024" in hover_response.contents.value
    
    # Test hover on the time
    hover_response_time = await client.text_document_hover_async(
        types.HoverParams(
            text_document=types.TextDocumentIdentifier(uri=test_uri),
            position=types.Position(line=2, character=3)
        )
    )
    
    assert hover_response_time is not None
    assert hover_response_time.contents.kind == types.MarkupKind.Markdown
    assert "12:30:45" in hover_response_time.contents.value


@pytest.mark.asyncio(loop_scope="module")
async def test_hover_on_non_datetime(client: LanguageClient):
    """Test that hover returns None for non-datetime text."""
    
    test_uri = "file:///test2.txt"
    test_content = "This is not a datetime\nJust regular text"
    
    client.text_document_did_open(
        types.DidOpenTextDocumentParams(
            text_document=types.TextDocumentItem(
                uri=test_uri,
                language_id="text",
                version=1,
                text=test_content
            )
        )
    )
    
    hover_response = await client.text_document_hover_async(
        types.HoverParams(
            text_document=types.TextDocumentIdentifier(uri=test_uri),
            position=types.Position(line=0, character=5)
        )
    )
    
    assert hover_response is None
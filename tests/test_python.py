import os
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
async def test_hover_on_settings(client: LanguageClient):
    """Test hover functionality on a datetime string."""
    
    test_path = os.path.join(os.path.dirname(__file__), "..", "examples", "settings.py")
    test_uri = "file://" + test_path
    test_content = open(test_path).read()
    
    client.text_document_did_open(
        types.DidOpenTextDocumentParams(
            text_document=types.TextDocumentItem(
                uri=test_uri,
                language_id="python",
                version=1,
                text=test_content
            )
        )
    )
    
    # Test hover on the date
    hover_response = await client.text_document_hover_async(
        types.HoverParams(
            text_document=types.TextDocumentIdentifier(uri=test_uri),
            position=types.Position(line=1, character=3)  # the SERVER variable
        )
    )
    
    assert hover_response is not None
    assert hover_response.contents.kind == types.MarkupKind.Markdown
    assert "SERVER" in hover_response.contents.value
    assert "This variable defines which server the system is connected to" in hover_response.contents.value


@pytest.mark.asyncio(loop_scope="module")
async def test_hover_on_non_settings(client: LanguageClient):
    """Test that hover returns None for non-datetime text."""
    
    test_path = os.path.join(os.path.dirname(__file__), "..", "examples", "settings.py")
    test_uri = "file://" + test_path
    test_content = open(test_path).read()
    
    client.text_document_did_open(
        types.DidOpenTextDocumentParams(
            text_document=types.TextDocumentItem(
                uri=test_uri,
                language_id="python",
                version=1,
                text=test_content
            )
        )
    )
    
    hover_response = await client.text_document_hover_async(
        types.HoverParams(
            text_document=types.TextDocumentIdentifier(uri=test_uri),
            position=types.Position(line=0, character=7)  # the docstring of the python file
        )
    )
    
    assert hover_response is None
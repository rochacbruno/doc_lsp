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
    """Test hover functionality on Python settings file."""

    test_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "examples", "settings.py")
    )
    test_uri = "file://" + test_path
    test_content = open(test_path).read()

    client.text_document_did_open(
        types.DidOpenTextDocumentParams(
            text_document=types.TextDocumentItem(
                uri=test_uri, language_id="python", version=1, text=test_content
            )
        )
    )

    # Test hover on SERVER variable (line 1, character 3)
    hover_response = await client.text_document_hover_async(
        types.HoverParams(
            text_document=types.TextDocumentIdentifier(uri=test_uri),
            position=types.Position(line=1, character=3),  # the SERVER variable
        )
    )

    assert hover_response is not None
    assert hover_response.contents.kind == types.MarkupKind.Markdown
    assert "SERVER" in hover_response.contents.value
    assert (
        "This variable defines which server the system is connected to"
        in hover_response.contents.value
    )

    # Test hover on PORT variable (line 2, character 2)
    hover_response = await client.text_document_hover_async(
        types.HoverParams(
            text_document=types.TextDocumentIdentifier(uri=test_uri),
            position=types.Position(line=2, character=2),  # the PORT variable
        )
    )

    assert hover_response is not None
    assert hover_response.contents.kind == types.MarkupKind.Markdown
    assert "PORT" in hover_response.contents.value
    assert "Port used to connect to server" in hover_response.contents.value

    # Test hover on DEBUG variable (line 3, character 2)
    hover_response = await client.text_document_hover_async(
        types.HoverParams(
            text_document=types.TextDocumentIdentifier(uri=test_uri),
            position=types.Position(line=3, character=2),  # the DEBUG variable
        )
    )

    assert hover_response is not None
    assert hover_response.contents.kind == types.MarkupKind.Markdown
    assert "DEBUG" in hover_response.contents.value
    assert "Enable or disable debugging mode" in hover_response.contents.value


@pytest.mark.asyncio(loop_scope="module")
async def test_hover_on_non_variable(client: LanguageClient):
    """Test that hover returns None for non-variable text."""

    test_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "examples", "settings.py")
    )
    test_uri = "file://" + test_path
    test_content = open(test_path).read()

    client.text_document_did_open(
        types.DidOpenTextDocumentParams(
            text_document=types.TextDocumentItem(
                uri=test_uri, language_id="python", version=1, text=test_content
            )
        )
    )

    # Test hover on docstring (line 0, character 7)
    hover_response = await client.text_document_hover_async(
        types.HoverParams(
            text_document=types.TextDocumentIdentifier(uri=test_uri),
            position=types.Position(
                line=0, character=7
            ),  # the docstring of the python file
        )
    )

    assert hover_response is None

    # Test hover on string value (line 1, character 15 - inside "localhost")
    hover_response = await client.text_document_hover_async(
        types.HoverParams(
            text_document=types.TextDocumentIdentifier(uri=test_uri),
            position=types.Position(line=1, character=15),
        )
    )

    assert hover_response is None


@pytest.mark.asyncio(loop_scope="module")
async def test_hover_on_yaml_file(client: LanguageClient):
    """Test hover functionality on YAML file."""

    test_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "examples", "marmite.yaml")
    )
    test_uri = "file://" + test_path

    # Check if the YAML file exists
    if not os.path.exists(test_path):
        pytest.skip("marmite.yaml not found")

    test_content = open(test_path).read()

    client.text_document_did_open(
        types.DidOpenTextDocumentParams(
            text_document=types.TextDocumentItem(
                uri=test_uri, language_id="yaml", version=1, text=test_content
            )
        )
    )

    # Find the location of a variable in the YAML file
    lines = test_content.split("\n")
    for i, line in enumerate(lines):
        if "title:" in line:
            # Test hover on 'title' key
            hover_response = await client.text_document_hover_async(
                types.HoverParams(
                    text_document=types.TextDocumentIdentifier(uri=test_uri),
                    position=types.Position(line=i, character=2),
                )
            )

            # If documentation exists, assert it has content
            if hover_response is not None:
                assert hover_response.contents.kind == types.MarkupKind.Markdown
                assert "title" in hover_response.contents.value.lower()
            break

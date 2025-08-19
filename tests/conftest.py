import pytest_lsp
from lsprotocol import types
from pytest_lsp import (
    ClientServerConfig,
    LanguageClient,
    client_capabilities,
)


@pytest_lsp.fixture(
    scope="module",
    config=ClientServerConfig(
        server_command=["uv", "run", "doc-lsp"],
    ),
)
async def client(lsp_client: LanguageClient):
    # Setup - Initialize the LSP session
    response = await lsp_client.initialize_session(
        types.InitializeParams(
            capabilities=client_capabilities("visual-studio-code"),
        )
    )

    # Store the initialization response for tests to access
    lsp_client.initialization_response = response

    yield lsp_client

    # Teardown - Shutdown the LSP session
    await lsp_client.shutdown_session()

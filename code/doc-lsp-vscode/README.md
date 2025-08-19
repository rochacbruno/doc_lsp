# Doc LSP - VS Code Extension

This is the Visual Studio Code extension for [Doc LSP](https://github.com/rochacbruno/doc_lsp), a Language Server Protocol implementation that loads documentation from separate markdown files.

## Features

- 🔍 **Hover Documentation**: Hover over variables to see their documentation from corresponding `.md` files
- 📝 **Multi-Language Support**: Works with Python, YAML, JSON, TOML, INI, and configuration files
- ⚡ **Automatic Activation**: Automatically activates when documentation files are detected
- 🔄 **Live Reload**: Documentation updates when markdown files change
- 🎯 **Configurable**: Customize server path and add additional file extensions

## Prerequisites

Before installing the extension, you need to have the `doc-lsp` server installed:

### Option 1: Install with pip
```bash
pip install doc-lsp
```

### Option 2: Install with uv
```bash
uv tool install doc-lsp
```

### Option 3: Install from source
```bash
# Clone the repository
git clone https://github.com/rochacbruno/doc_lsp.git
cd doc_lsp

# Install with uv
uv pip install -e .

# Or with pip
pip install -e .
```

## Building and Installing the Extension

### Quick Install (Pre-built)

If you have a pre-built `.vsix` file:

```bash
code --install-extension doc-lsp-*.vsix
```

### Building from Source

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/rochacbruno/doc_lsp.git
   cd doc_lsp/code/doc-lsp-vscode
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Build the extension**:
   ```bash
   # Using the build script (recommended)
   ./build.sh
   
   # Or manually:
   npm run compile
   npm run package
   ```

4. **Install the extension**:
   ```bash
   code --install-extension doc-lsp-*.vsix
   ```

### Development Mode

For development and testing:

1. Open the extension folder in VS Code:
   ```bash
   code /path/to/doc_lsp/code/doc-lsp-vscode
   ```

2. Press `F5` to run the extension in a new Extension Development Host window

3. Make changes and reload the window to test

## Configuration

The extension can be configured through VS Code settings:

### Settings

- `docLsp.enabled`: Enable/disable the Doc LSP extension (default: `true`)
- `docLsp.serverPath`: Path to the doc-lsp executable (default: `"doc-lsp"`)
- `docLsp.trace.server`: Trace server communication for debugging (default: `"off"`)
- `docLsp.additionalFileExtensions`: Additional file extensions to support (default: `[]`)

### Example Configuration

Add to your VS Code settings (`settings.json`):

```json
{
  "docLsp.enabled": true,
  "docLsp.serverPath": "doc-lsp",
  "docLsp.additionalFileExtensions": [".cfg", ".env"],
  "docLsp.trace.server": "messages"
}
```

## Usage

1. Create a documentation file alongside your code file:
   - For `settings.py`, create `settings.py.md`
   - For `config.yaml`, create `config.yaml.md`

2. Write documentation using markdown format:
   ```markdown
   ## VARIABLE_NAME
   > Documentation for the variable goes here
   > Can be multiple lines
   
   ## ANOTHER_VARIABLE
   > Documentation for another variable
   ```

3. Hover over variables in your code to see the documentation!

## Using with Generic LSP Proxy Extension

If you prefer to use the [Generic LSP Proxy](https://marketplace.visualstudio.com/items?itemName=statiolake.vscode-generic-lsp-proxy) extension instead:

1. Install the Generic LSP Proxy extension:
   ```bash
   code --install-extension statiolake.vscode-generic-lsp-proxy
   ```

2. Create `.vscode/lsp-proxy.json` in your workspace:
   ```json
   [
     {
       "languageId": "python",
       "command": "doc-lsp",
       "fileExtensions": [".py"]
     },
     {
       "languageId": "yaml",
       "command": "doc-lsp",
       "fileExtensions": [".yaml", ".yml"]
     },
     {
       "languageId": "json",
       "command": "doc-lsp",
       "fileExtensions": [".json"]
     },
     {
       "languageId": "toml",
       "command": "doc-lsp",
       "fileExtensions": [".toml"]
     },
     {
       "languageId": "ini",
       "command": "doc-lsp",
       "fileExtensions": [".ini", ".conf"]
     },
     {
       "languageId": "properties",
       "command": "doc-lsp",
       "fileExtensions": [".properties"]
     }
   ]
   ```

3. Reload VS Code window or restart VS Code

## Commands

The extension provides the following commands:

- **Doc LSP: Restart Language Server** - Restarts the doc-lsp server
- **Doc LSP: Show Output Channel** - Shows the extension output for debugging

## Troubleshooting

### Server not found

If you get "Doc LSP server not found" error:

1. Ensure `doc-lsp` is installed:
   ```bash
   which doc-lsp  # On Unix-like systems
   where doc-lsp  # On Windows
   ```

2. If installed in a virtual environment, provide the full path in settings:
   ```json
   {
     "docLsp.serverPath": "/path/to/venv/bin/doc-lsp"
   }
   ```

### Extension not activating

The extension activates when:
- You open a supported file type (Python, YAML, JSON, etc.)
- Documentation files (`.md`) exist in the workspace

### No hover documentation

Check that:
1. The documentation file exists (e.g., `file.py.md` for `file.py`)
2. The documentation follows the correct format
3. The variable name in the documentation matches the code

### Debugging

Enable trace logging to see server communication:
```json
{
  "docLsp.trace.server": "verbose"
}
```

Then check the output channel: `View > Output > Doc LSP`

## License

This extension is licensed under the AGPL-3.0-or-later license. See [LICENSE](../../LICENSE) for details.

## Contributing

Contributions are welcome! Please see the [main repository](https://github.com/rochacbruno/doc_lsp) for contribution guidelines.

## Links

- [Main Repository](https://github.com/rochacbruno/doc_lsp)
- [Issue Tracker](https://github.com/rochacbruno/doc_lsp/issues)
- [PyPI Package](https://pypi.org/project/doc-lsp/)
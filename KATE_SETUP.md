# Configuring doc-lsp with Kate Editor

This guide provides step-by-step instructions to set up the doc-lsp Language Server with Kate editor.

## Prerequisites

- Kate editor installed (version 21.12 or later recommended for better LSP support)
- Python 3.11+ installed
- pip or uv package manager

## Step 1: Install doc-lsp

First, install the doc-lsp server on your system:

```bash
# Using pip (system-wide)
pip install doc-lsp

# Or using uv (recommended)
uv tool install doc-lsp

# Or from source
git clone https://github.com/rochacbruno/doc_lsp.git
cd doc_lsp
pip install -e .
```

After installation, verify it's available:

```bash
# Check if doc-lsp is in your PATH
which doc-lsp

# Test that it runs
doc-lsp --version
```

## Step 2: Enable LSP Client Plugin in Kate

1. **Open Kate editor**

2. **Navigate to Settings**:
   - Click on `Settings` menu
   - Select `Configure Kate...`

3. **Enable the LSP Client plugin**:
   - In the configuration window, click on `Plugins` in the left sidebar
   - Find `LSP Client` in the list
   - Check the checkbox next to `LSP Client` to enable it
   - Click `Apply` button

4. **Restart Kate** for the plugin to take effect

## Step 3: Configure doc-lsp Server

1. **Open Kate Settings again**:
   - `Settings` → `Configure Kate...`

2. **Navigate to LSP Client**:
   - In the left sidebar, expand `Application`
   - Click on `LSP Client`

3. **Configure Client Settings** (optional but recommended):
   - In the `Client Settings` tab, check these options:
     - ✅ Show hover information
     - ✅ Enable code completion
     - ✅ Enable semantic highlighting
     - ✅ Show diagnostic messages
   - You may want to uncheck:
     - ❌ Format on typing (doc-lsp doesn't provide formatting)
     - ❌ Add parentheses upon function completion

4. **Add doc-lsp Server Configuration**:
   - Click on the `User Server Settings` tab
   - Copy and paste the following JSON configuration:

```json
{
  "servers": {
    "doc-lsp-python": {
      "command": ["doc-lsp"],
      "rootIndicationFileNames": ["pyproject.toml", "setup.py", "requirements.txt", ".git"],
      "url": "https://github.com/rochacbruno/doc_lsp",
      "highlightingModeRegex": "^Python$"
    },
    "doc-lsp-yaml": {
      "command": ["doc-lsp"],
      "rootIndicationFileNames": [".git"],
      "url": "https://github.com/rochacbruno/doc_lsp",
      "highlightingModeRegex": "^YAML$"
    },
    "doc-lsp-json": {
      "command": ["doc-lsp"],
      "rootIndicationFileNames": ["package.json", ".git"],
      "url": "https://github.com/rochacbruno/doc_lsp",
      "highlightingModeRegex": "^JSON$"
    },
    "doc-lsp-toml": {
      "command": ["doc-lsp"],
      "rootIndicationFileNames": ["pyproject.toml", "Cargo.toml", ".git"],
      "url": "https://github.com/rochacbruno/doc_lsp",
      "highlightingModeRegex": "^TOML$"
    },
    "doc-lsp-ini": {
      "command": ["doc-lsp"],
      "rootIndicationFileNames": [".git"],
      "url": "https://github.com/rochacbruno/doc_lsp",
      "highlightingModeRegex": "^INI Files$"
    },
    "doc-lsp-properties": {
      "command": ["doc-lsp"],
      "rootIndicationFileNames": [".git"],
      "url": "https://github.com/rochacbruno/doc_lsp",
      "highlightingModeRegex": "^Java Properties$"
    },
    "doc-lsp-conf": {
      "command": ["doc-lsp"],
      "rootIndicationFileNames": [".git"],
      "url": "https://github.com/rochacbruno/doc_lsp",
      "highlightingModeRegex": "^Config$"
    }
  }
}
```

5. **Apply the settings**:
   - Click `Apply`
   - Click `OK` to close the configuration dialog

## Step 4: Alternative - Single Server Configuration

If you prefer a simpler setup that works for all file types, you can use this configuration instead:

```json
{
  "servers": {
    "doc-lsp": {
      "command": ["doc-lsp"],
      "rootIndicationFileNames": [".git", "pyproject.toml", "package.json"],
      "url": "https://github.com/rochacbruno/doc_lsp",
      "highlightingModeRegex": "^(Python|YAML|JSON|TOML|INI Files|Java Properties|Config)$"
    }
  }
}
```

## Step 5: Test the Configuration

1. **Create a test file** (e.g., `test_settings.py`):
```python
# test_settings.py
SERVER = "localhost"
PORT = 8080
DEBUG = True
DATABASE_URL = "sqlite:///app.db"
```

2. **Create the documentation file** (`test_settings.py.md`):
```markdown
## SERVER
> The hostname or IP address of the server.
> Default: "localhost"
> Example: "192.168.1.100" or "api.example.com"

## PORT
> The port number the server listens on.
> Must be between 1024 and 65535.
> Default: 8080

## DEBUG
> Enable debug mode for development.
> **Warning**: Never enable in production!
> Default: False

## DATABASE_URL
> Database connection string.
> Supports: PostgreSQL, MySQL, SQLite
> Format: "dialect://user:password@host/database"
```

3. **Open the Python file in Kate**

4. **Test the features**:
   - **Hover**: Move your mouse over a variable (e.g., `SERVER`) - you should see a tooltip with the documentation
   - **Completion**: Start typing a variable name (e.g., type `DAT`) and press `Ctrl+Space` - you should see `DATABASE_URL` in the completion list with documentation

## Step 6: Check LSP Client Logs

If something isn't working:

1. **Open the LSP Client output**:
   - In Kate, look for the bottom panel
   - Click on the `LSP Client` tab
   - You should see logs showing the server starting and any errors

2. **Common issues and solutions**:

   - **"Command not found"**: Make sure `doc-lsp` is in your PATH
     ```bash
     echo $PATH
     which doc-lsp
     ```

   - **Server not starting**: Check if the command works manually
     ```bash
     doc-lsp
     ```

   - **No hover/completion**: Ensure you have both the source file and `.md` documentation file in the same directory

## Step 7: Configure for .env Files (Optional)

For `.env` files and other plain text files without standard highlighting modes:

```json
{
  "servers": {
    "doc-lsp-env": {
      "command": ["doc-lsp"],
      "rootIndicationFileNames": [".git", ".env"],
      "url": "https://github.com/rochacbruno/doc_lsp",
      "highlightingModeRegex": "^(Plain Text|None)$",
      "fileExtensions": [".env", ".env.example", ".env.local"]
    }
  }
}
```

## Troubleshooting

### LSP Server Not Starting

1. Check if doc-lsp is installed correctly:
   ```bash
   doc-lsp --help
   ```

2. Try running doc-lsp manually to see any error messages:
   ```bash
   doc-lsp
   ```

3. Check Kate's LSP Client logs for error messages

### No Documentation Showing

1. Verify the documentation file exists:
   - For `config.py`, you need `config.py.md`
   - For `settings.yaml`, you need `settings.yaml.md`

2. Check the documentation file format:
   - Headers should be `## VARIABLE_NAME`
   - Documentation text follows the header

3. Ensure the LSP server is running (check LSP Client tab)

### Completion Not Working

1. Make sure you're using the latest version of doc-lsp with the completion fix
2. Try manually triggering completion with `Ctrl+Space`
3. Check that the variable is documented in the `.md` file

## Additional Tips

- **File watching**: doc-lsp watches for changes in `.md` files and updates documentation automatically
- **Multiple projects**: Each project/folder can have its own documentation files
- **Nested variables**: doc-lsp supports nested variable documentation (e.g., `DATABASE.HOST`)

## References

- [doc-lsp GitHub Repository](https://github.com/rochacbruno/doc_lsp)
- [Kate Editor LSP Documentation](https://docs.kde.org/stable5/en/kate/kate/kate-application-plugin-lspclient.html)
- [Language Server Protocol Specification](https://microsoft.github.io/language-server-protocol/)

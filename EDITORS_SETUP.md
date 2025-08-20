# Editor Configuration Guide for doc-lsp

This guide provides setup instructions for configuring doc-lsp with various popular editors.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Helix](#helix)
- [Neovim](#neovim)
- [Zed](#zed)
- [Emacs](#emacs)
- [VS Code](#vs-code)
- [Kate](#kate)
- [Sublime Text](#sublime-text)

## Prerequisites

Before configuring any editor, ensure doc-lsp is installed and accessible:

```bash
# Install using pip
pip install doc-lsp

# Or using uv
uv tool install doc-lsp

# Or from source
git clone https://github.com/rochacbruno/doc_lsp.git
cd doc_lsp
pip install -e .

# Verify installation
doc-lsp --version
which doc-lsp
```

---

## Helix

Helix has built-in LSP support and requires configuration through `languages.toml`.

### Configuration

1. **Create/edit the configuration file**:
   ```bash
   mkdir -p ~/.config/helix
   touch ~/.config/helix/languages.toml
   ```

2. **Add doc-lsp configuration**:

   ```toml
   # ~/.config/helix/languages.toml
   
   # Define the doc-lsp server
   [language-server.doc-lsp]
   command = "doc-lsp"
   
   # Python configuration
   [[language]]
   name = "python"
   language-servers = [{ name = "doc-lsp" }, { name = "pylsp" }]  # Can chain with other LSPs
   
   # YAML configuration
   [[language]]
   name = "yaml"
   language-servers = ["doc-lsp"]
   
   # JSON configuration
   [[language]]
   name = "json"
   language-servers = ["doc-lsp"]
   
   # TOML configuration
   [[language]]
   name = "toml"
   language-servers = ["doc-lsp"]
   
   # INI configuration
   [[language]]
   name = "ini"
   language-servers = ["doc-lsp"]
   file-types = ["ini", "conf", "cfg", "properties"]
   ```

3. **Verify configuration**:
   ```bash
   hx --health python
   hx --health yaml
   ```

### Usage in Helix

- **Hover**: Press `K` (uppercase) while cursor is on a variable
- **Completion**: Start typing and completions will appear automatically
- **Documentation**: Navigate completions with `Tab`/`Shift+Tab`

---

## Neovim

Neovim requires the `nvim-lspconfig` plugin for LSP management.

### Installation

1. **Install nvim-lspconfig** (using your preferred plugin manager):

   **Using packer.nvim**:
   ```lua
   use 'neovim/nvim-lspconfig'
   ```

   **Using lazy.nvim**:
   ```lua
   { 'neovim/nvim-lspconfig' }
   ```

   **Using vim-plug**:
   ```vim
   Plug 'neovim/nvim-lspconfig'
   ```

### Configuration

2. **Create doc-lsp configuration**:

   Create a file `~/.config/nvim/lua/lsp/doc_lsp.lua`:

   ```lua
   -- ~/.config/nvim/lua/lsp/doc_lsp.lua
   local lspconfig = require('lspconfig')
   local configs = require('lspconfig.configs')
   
   -- Define doc-lsp if not already defined
   if not configs.doc_lsp then
     configs.doc_lsp = {
       default_config = {
         cmd = { 'doc-lsp' },
         filetypes = { 
           'python', 'yaml', 'json', 'toml', 'ini', 'conf', 
           'cfg', 'properties', 'sh', 'bash', 'zsh'
         },
         root_dir = lspconfig.util.root_pattern(
           '.git', 'pyproject.toml', 'setup.py', 'package.json'
         ),
         settings = {},
       },
     }
   end
   
   -- Setup doc-lsp
   lspconfig.doc_lsp.setup{
     on_attach = function(client, bufnr)
       -- Enable completion triggered by <c-x><c-o>
       vim.api.nvim_buf_set_option(bufnr, 'omnifunc', 'v:lua.vim.lsp.omnifunc')
       
       -- Mappings
       local opts = { noremap=true, silent=true, buffer=bufnr }
       vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)
       vim.keymap.set('n', '<C-k>', vim.lsp.buf.signature_help, opts)
       vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
       vim.keymap.set('n', 'gr', vim.lsp.buf.references, opts)
       
       -- Enable autocompletion
       vim.api.nvim_create_autocmd("InsertEnter", {
         buffer = bufnr,
         callback = function()
           vim.lsp.buf.completion()
         end,
       })
     end,
     capabilities = require('cmp_nvim_lsp').default_capabilities(),
   }
   ```

3. **Add to your init.lua**:

   ```lua
   -- ~/.config/nvim/init.lua
   require('lsp.doc_lsp')
   ```

### Enhanced Setup with nvim-cmp (Recommended)

For better completion experience, use nvim-cmp:

```lua
-- Install plugins (using lazy.nvim)
{
  'hrsh7th/nvim-cmp',
  dependencies = {
    'hrsh7th/cmp-nvim-lsp',
    'hrsh7th/cmp-buffer',
    'hrsh7th/cmp-path',
    'L3MON4D3/LuaSnip',
  },
  config = function()
    local cmp = require('cmp')
    cmp.setup({
      snippet = {
        expand = function(args)
          require('luasnip').lsp_expand(args.body)
        end,
      },
      mapping = cmp.mapping.preset.insert({
        ['<C-Space>'] = cmp.mapping.complete(),
        ['<CR>'] = cmp.mapping.confirm({ select = true }),
        ['<Tab>'] = cmp.mapping.select_next_item(),
        ['<S-Tab>'] = cmp.mapping.select_prev_item(),
      }),
      sources = cmp.config.sources({
        { name = 'nvim_lsp' },  -- LSP completions (including doc-lsp)
        { name = 'buffer' },
        { name = 'path' },
      }),
      -- Show documentation window
      window = {
        documentation = cmp.config.window.bordered(),
      },
    })
  end
}
```

### Usage in Neovim

- **Hover**: Press `K` in normal mode
- **Completion**: Press `Ctrl+Space` in insert mode
- **Navigate completions**: Use `Tab`/`Shift+Tab`

---

## Zed

Zed has built-in LSP support and can be configured through settings.json.

### Configuration

1. **Open Zed settings**:
   - Press `Cmd+,` (macOS) or `Ctrl+,` (Linux)
   - Or open `~/.config/zed/settings.json`

2. **Add doc-lsp configuration**:

   ```json
   {
     "languages": {
       "Python": {
         "language_servers": ["doc-lsp", "pyright"],
         "format_on_save": "on"
       },
       "YAML": {
         "language_servers": ["doc-lsp", "yaml-language-server"]
       },
       "JSON": {
         "language_servers": ["doc-lsp", "json-language-server"]
       },
       "TOML": {
         "language_servers": ["doc-lsp"]
       }
     },
     "lsp": {
       "doc-lsp": {
         "binary": {
           "path": "doc-lsp"
         },
         "initialization_options": {},
         "settings": {}
       }
     }
   }
   ```

3. **Alternative: Project-specific configuration**:

   Create `.zed/settings.json` in your project root:

   ```json
   {
     "lsp": {
       "doc-lsp": {
         "binary": {
           "path": "doc-lsp"
         }
       }
     },
     "languages": {
       "Python": {
         "language_servers": ["doc-lsp", "pyright"]
       }
     }
   }
   ```

### Usage in Zed

- **Hover**: Hold `Cmd` (macOS) or `Ctrl` (Linux) and hover over variable
- **Completion**: Completions appear automatically as you type
- **Documentation**: Shows in completion popup and hover

---

## Emacs

Emacs supports LSP through either `lsp-mode` or `eglot`. We'll cover both.

### Option 1: Using lsp-mode

1. **Install lsp-mode**:

   ```elisp
   ;; Using use-package
   (use-package lsp-mode
     :ensure t
     :commands (lsp lsp-deferred)
     :init
     (setq lsp-keymap-prefix "C-c l"))
   
   (use-package lsp-ui
     :ensure t
     :commands lsp-ui-mode)
   ```

2. **Configure doc-lsp**:

   ```elisp
   ;; ~/.emacs.d/init.el or ~/.emacs
   
   (use-package lsp-mode
     :ensure t
     :hook ((python-mode . lsp-deferred)
            (yaml-mode . lsp-deferred)
            (json-mode . lsp-deferred)
            (conf-mode . lsp-deferred))
     :commands (lsp lsp-deferred)
     :init
     (setq lsp-keymap-prefix "C-c l")
     :config
     ;; Register doc-lsp
     (lsp-register-client
      (make-lsp-client
       :new-connection (lsp-stdio-connection "doc-lsp")
       :major-modes '(python-mode yaml-mode json-mode conf-mode)
       :priority -1  ; Lower priority so it works alongside other servers
       :server-id 'doc-lsp)))
   
   ;; Enable nice UI features
   (use-package lsp-ui
     :ensure t
     :hook (lsp-mode . lsp-ui-mode)
     :config
     (setq lsp-ui-doc-enable t
           lsp-ui-doc-show-with-hover t
           lsp-ui-doc-delay 0.5
           lsp-ui-sideline-enable t
           lsp-ui-sideline-show-hover t))
   
   ;; Better completion
   (use-package company
     :ensure t
     :hook (lsp-mode . company-mode)
     :config
     (setq company-minimum-prefix-length 1
           company-idle-delay 0.0))
   ```

### Option 2: Using eglot (Built-in for Emacs 29+)

1. **Configure eglot**:

   ```elisp
   ;; ~/.emacs.d/init.el or ~/.emacs
   
   (require 'eglot)
   
   ;; Add doc-lsp to eglot server programs
   (add-to-list 'eglot-server-programs
                '((python-mode python-ts-mode) . ("doc-lsp")))
   (add-to-list 'eglot-server-programs
                '((yaml-mode yaml-ts-mode) . ("doc-lsp")))
   (add-to-list 'eglot-server-programs
                '((json-mode json-ts-mode) . ("doc-lsp")))
   (add-to-list 'eglot-server-programs
                '(conf-mode . ("doc-lsp")))
   
   ;; Auto-start eglot for supported modes
   (add-hook 'python-mode-hook 'eglot-ensure)
   (add-hook 'yaml-mode-hook 'eglot-ensure)
   (add-hook 'json-mode-hook 'eglot-ensure)
   (add-hook 'conf-mode-hook 'eglot-ensure)
   
   ;; Keybindings
   (define-key eglot-mode-map (kbd "C-c h") 'eldoc)
   (define-key eglot-mode-map (kbd "C-c a") 'eglot-code-actions)
   (define-key eglot-mode-map (kbd "C-c r") 'eglot-rename)
   ```

2. **Enhanced completion with corfu (for eglot)**:

   ```elisp
   (use-package corfu
     :ensure t
     :custom
     (corfu-auto t)
     (corfu-quit-no-match 'separator)
     :init
     (global-corfu-mode))
   
   (use-package cape
     :ensure t
     :init
     (add-to-list 'completion-at-point-functions #'cape-file)
     (add-to-list 'completion-at-point-functions #'cape-dabbrev))
   ```

### Usage in Emacs

**With lsp-mode**:
- **Hover**: `M-x lsp-describe-thing-at-point` or hover with mouse
- **Completion**: Automatic with company-mode
- **Documentation**: `C-c l g h` for hover

**With eglot**:
- **Hover**: `M-x eldoc` or `C-c h`
- **Completion**: Automatic with corfu or company
- **Documentation**: Shows in minibuffer or eldoc buffer

---

## VS Code

See the dedicated [VS Code extension README](code/doc-lsp-vscode/README.md) for detailed instructions.

Quick setup:
```bash
cd code/doc-lsp-vscode
npm install
npm run package
code --install-extension doc-lsp-*.vsix
```

---

## Kate

See the dedicated [Kate setup guide](KATE_SETUP.md) for detailed instructions.

Quick configuration in User Server Settings:
```json
{
  "servers": {
    "doc-lsp": {
      "command": ["doc-lsp"],
      "rootIndicationFileNames": [".git"],
      "highlightingModeRegex": "^(Python|YAML|JSON|TOML|INI Files)$"
    }
  }
}
```

---

## Sublime Text

Sublime Text uses the LSP package for Language Server Protocol support.

### Installation

1. **Install Package Control** (if not already installed)

2. **Install LSP package**:
   - Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
   - Type "Package Control: Install Package"
   - Search for "LSP" and install it

### Configuration

3. **Configure doc-lsp**:
   - Open LSP Settings: `Preferences → Package Settings → LSP → Settings`
   - Add the following configuration:

   ```json
   {
     "clients": {
       "doc-lsp": {
         "enabled": true,
         "command": ["doc-lsp"],
         "selector": "source.python | source.yaml | source.json | source.toml | source.ini",
         "schemes": ["file", "buffer"],
         "initializationOptions": {},
         "settings": {}
       }
     }
   }
   ```

4. **Project-specific configuration**:

   Create `.sublime-project` file:
   ```json
   {
     "folders": [
       {
         "path": "."
       }
     ],
     "settings": {
       "LSP": {
         "doc-lsp": {
           "enabled": true
         }
       }
     }
   }
   ```

### Usage in Sublime Text

- **Hover**: Move mouse over variable or press `F1`
- **Completion**: Press `Ctrl+Space`
- **Documentation**: Shows in popup when hovering

---

## Testing Your Setup

Regardless of your editor, test the configuration with these files:

1. **Create a test file** (`test_config.py`):
   ```python
   # Database configuration
   DATABASE_HOST = "localhost"
   DATABASE_PORT = 5432
   DATABASE_NAME = "myapp"
   
   # API settings
   API_KEY = "secret-key-here"
   API_TIMEOUT = 30
   
   # Feature flags
   ENABLE_CACHE = True
   DEBUG_MODE = False
   ```

2. **Create documentation** (`test_config.py.md`):
   ```markdown
   ## DATABASE_HOST
   > The hostname or IP address of the database server.
   > Use "localhost" for local development.
   > Example: "db.example.com" or "192.168.1.100"
   
   ## DATABASE_PORT
   > The port number for the database connection.
   > Default: 5432 (PostgreSQL), 3306 (MySQL)
   
   ## DATABASE_NAME
   > The name of the database to connect to.
   > Must exist on the database server.
   
   ## API_KEY
   > Secret key for API authentication.
   > **Security**: Store in environment variables in production!
   > Generate with: `openssl rand -hex 32`
   
   ## API_TIMEOUT
   > Maximum time in seconds to wait for API responses.
   > Increase for slow connections or large payloads.
   > Range: 10-300 seconds
   
   ## ENABLE_CACHE
   > Enable caching to improve performance.
   > Recommended: True for production, False for development
   
   ## DEBUG_MODE
   > Enable debug mode for detailed error messages.
   > **Warning**: Never enable in production!
   ```

3. **Test features**:
   - Open the Python file in your configured editor
   - Hover over variables to see documentation
   - Start typing a variable name to test completion
   - Verify documentation appears in completion popups

---

## Troubleshooting

### Common Issues

1. **LSP server not starting**:
   ```bash
   # Check if doc-lsp is in PATH
   which doc-lsp
   
   # Test manually
   echo "" | doc-lsp
   ```

2. **No hover/completion**:
   - Ensure `.md` documentation file exists
   - Check file is in same directory
   - Verify file naming: `file.ext` → `file.ext.md`

3. **Editor-specific logs**:
   - **Helix**: Check `~/.cache/helix/helix.log`
   - **Neovim**: `:LspLog` or `:messages`
   - **Zed**: View → Debug → Language Server Logs
   - **Emacs (lsp-mode)**: `M-x lsp-workspace-show-log`
   - **Emacs (eglot)**: Check `*EGLOT (mode) events*` buffer
   - **VS Code**: Output panel → doc-lsp
   - **Kate**: View → Tool Views → LSP Client
   - **Sublime**: View → Show Console

4. **Permission issues**:
   ```bash
   # Make doc-lsp executable
   chmod +x $(which doc-lsp)
   ```

---

## Additional Resources

- [doc-lsp GitHub Repository](https://github.com/rochacbruno/doc_lsp)
- [Language Server Protocol Specification](https://microsoft.github.io/language-server-protocol/)
- [LSP implementations list](https://langserver.org/)

## Contributing

If you've successfully configured doc-lsp with another editor, please contribute your configuration to this guide!

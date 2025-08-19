#!/bin/bash

# Build script for Doc LSP VS Code extension

echo "Building Doc LSP VS Code extension..."

# Install dependencies
echo "Installing dependencies..."
npm install

# Compile TypeScript
echo "Compiling TypeScript..."
npm run compile

# Package the extension
echo "Packaging extension..."
npm run package

echo "Build complete! Extension package created: doc-lsp-*.vsix"
echo ""
echo "To install locally, run:"
echo "  code --install-extension doc-lsp-*.vsix"
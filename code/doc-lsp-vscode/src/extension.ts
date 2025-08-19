import * as vscode from 'vscode';
import * as path from 'path';
import { spawn } from 'child_process';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    TransportKind,
    RevealOutputChannelOn
} from 'vscode-languageclient/node';

let client: LanguageClient | undefined;
let outputChannel: vscode.OutputChannel;

export async function activate(context: vscode.ExtensionContext) {
    outputChannel = vscode.window.createOutputChannel('Doc LSP');
    
    const config = vscode.workspace.getConfiguration('docLsp');
    const enabled = config.get<boolean>('enabled', true);
    
    if (!enabled) {
        outputChannel.appendLine('Doc LSP is disabled in settings');
        return;
    }

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('docLsp.restart', async () => {
            await restartLanguageServer(context);
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('docLsp.showOutputChannel', () => {
            outputChannel.show();
        })
    );

    // Start the language server
    await startLanguageServer(context);
}

async function startLanguageServer(context: vscode.ExtensionContext) {
    const config = vscode.workspace.getConfiguration('docLsp');
    const serverPath = config.get<string>('serverPath', 'doc-lsp');
    const additionalExtensions = config.get<string[]>('additionalFileExtensions', []);

    // Check if doc-lsp is available
    const isServerAvailable = await checkServerAvailable(serverPath);
    if (!isServerAvailable) {
        const message = `Doc LSP server not found at '${serverPath}'. Please install it with: pip install doc-lsp or uv tool install doc-lsp`;
        vscode.window.showErrorMessage(message);
        outputChannel.appendLine(message);
        return;
    }

    // Define supported document selectors
    const documentSelectors = [
        { scheme: 'file', language: 'python' },
        { scheme: 'file', language: 'yaml' },
        { scheme: 'file', language: 'json' },
        { scheme: 'file', language: 'toml' },
        { scheme: 'file', language: 'ini' },
        { scheme: 'file', language: 'properties' },
        { scheme: 'file', pattern: '**/*.conf' },
        { scheme: 'file', pattern: '**/*.cfg' },
    ];

    // Add additional extensions from settings
    for (const ext of additionalExtensions) {
        documentSelectors.push({ scheme: 'file', pattern: `**/*${ext}` });
    }

    // Server options
    const serverOptions: ServerOptions = {
        run: {
            command: serverPath,
            transport: TransportKind.stdio
        },
        debug: {
            command: serverPath,
            transport: TransportKind.stdio,
            options: {
                env: { ...process.env, 'PYTHONDONTWRITEBYTECODE': '1' }
            }
        }
    };

    // Client options
    const clientOptions: LanguageClientOptions = {
        documentSelector: documentSelectors,
        synchronize: {
            // Synchronize the setting section 'docLsp' to the server
            configurationSection: 'docLsp',
            // Notify the server about file changes to markdown files
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.md')
        },
        outputChannel: outputChannel,
        revealOutputChannelOn: RevealOutputChannelOn.Error
    };

    // Create and start the language client
    client = new LanguageClient(
        'docLsp',
        'Doc LSP',
        serverOptions,
        clientOptions
    );

    outputChannel.appendLine('Starting Doc LSP server...');
    
    try {
        await client.start();
        outputChannel.appendLine('Doc LSP server started successfully');
        
        // Show status bar item
        const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
        statusBarItem.text = '$(book) Doc LSP';
        statusBarItem.tooltip = 'Doc LSP is active';
        statusBarItem.command = 'docLsp.showOutputChannel';
        statusBarItem.show();
        context.subscriptions.push(statusBarItem);
        
    } catch (error) {
        outputChannel.appendLine(`Failed to start Doc LSP server: ${error}`);
        vscode.window.showErrorMessage(`Failed to start Doc LSP: ${error}`);
    }
}

async function restartLanguageServer(context: vscode.ExtensionContext) {
    outputChannel.appendLine('Restarting Doc LSP server...');
    
    if (client) {
        await client.stop();
        client = undefined;
    }
    
    await startLanguageServer(context);
}

async function checkServerAvailable(serverPath: string): Promise<boolean> {
    return new Promise((resolve) => {
        const process = spawn(serverPath, ['--version'], {
            shell: true,
            windowsHide: true
        });

        process.on('error', () => {
            resolve(false);
        });

        process.on('exit', (code) => {
            resolve(code === 0);
        });

        // Timeout after 3 seconds
        setTimeout(() => {
            process.kill();
            resolve(false);
        }, 3000);
    });
}

export async function deactivate() {
    if (client) {
        outputChannel.appendLine('Stopping Doc LSP server...');
        await client.stop();
        outputChannel.appendLine('Doc LSP server stopped');
    }
}
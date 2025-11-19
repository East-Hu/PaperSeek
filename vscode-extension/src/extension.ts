import * as vscode from 'vscode';
import { PaperPanel } from './webview/PaperPanel';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export function activate(context: vscode.ExtensionContext) {
    console.log('Paper-to-Action extension is now active!');

    // 注册命令
    context.subscriptions.push(
        vscode.commands.registerCommand('paperRobot.openPanel', () => {
            PaperPanel.render(context.extensionUri);
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('paperRobot.search', async () => {
            PaperPanel.render(context.extensionUri);
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('paperRobot.config', async () => {
            await configureAPI();
        })
    );

    // 注册 Webview View Provider
    const provider = new PaperViewProvider(context.extensionUri);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('paperRobotView', provider)
    );
}

export function deactivate() { }

// Webview View Provider
class PaperViewProvider implements vscode.WebviewViewProvider {
    constructor(private readonly _extensionUri: vscode.Uri) { }

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        // 处理来自 webview 的消息
        webviewView.webview.onDidReceiveMessage(async (data) => {
            switch (data.type) {
                case 'search':
                    await handleSearch(data.payload, webviewView.webview);
                    break;
                case 'config':
                    await configureAPI();
                    break;
                case 'getConfig':
                    const config = getConfiguration();
                    webviewView.webview.postMessage({
                        type: 'configLoaded',
                        payload: config
                    });
                    break;
            }
        });
    }

    private _getHtmlForWebview(webview: vscode.Webview) {
        const config = getConfiguration();
        const isConfigured = config.apiKey && config.apiKey.length > 0;

        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Paper Robot</title>
    <style>
        body {
            padding: 20px;
            color: var(--vscode-foreground);
            font-family: var(--vscode-font-family);
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .header h2 {
            margin: 10px 0;
            color: var(--vscode-button-background);
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
        }
        input, select {
            width: 100%;
            padding: 8px;
            background: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
            border: 1px solid var(--vscode-input-border);
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 10px;
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            margin-top: 10px;
        }
        button:hover {
            background: var(--vscode-button-hoverBackground);
        }
        .config-button {
            background: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
        }
        .status {
            margin-top: 20px;
            padding: 10px;
            border-radius: 4px;
            display: none;
        }
        .status.success {
            background: var(--vscode-testing-iconPassed);
            color: white;
            display: block;
        }
        .status.error {
            background: var(--vscode-testing-iconFailed);
            color: white;
            display: block;
        }
        .status.info {
            background: var(--vscode-button-background);
            color: white;
            display: block;
        }
        .config-status {
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 4px;
            text-align: center;
        }
        .config-status.configured {
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid rgba(0, 255, 0, 0.3);
        }
        .config-status.not-configured {
            background: rgba(255, 165, 0, 0.1);
            border: 1px solid rgba(255, 165, 0, 0.3);
        }
        .results {
            margin-top: 20px;
        }
        .paper-card {
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid var(--vscode-panel-border);
            border-radius: 4px;
            background: var(--vscode-editor-background);
        }
        .paper-title {
            font-weight: 600;
            margin-bottom: 10px;
            color: var(--vscode-textLink-foreground);
        }
        .paper-meta {
            font-size: 0.9em;
            color: var(--vscode-descriptionForeground);
            margin-bottom: 10px;
        }
        .paper-summary {
            margin-top: 10px;
            padding: 10px;
            background: var(--vscode-textCodeBlock-background);
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h2>📚 Paper Robot</h2>
        <p>自动化论文爬取与智能摘要</p>
    </div>

    <div class="config-status ${isConfigured ? 'configured' : 'not-configured'}" id="configStatus">
        ${isConfigured ? '✓ API 已配置' : '⚠️ 请先配置 API'}
    </div>

    ${!isConfigured ? `
        <button class="config-button" onclick="configureAPI()">⚙️ 配置 API</button>
        <div class="status info" style="display: block; margin-top: 15px;">
            首次使用需要配置 LLM API 密钥。请点击上方按钮进行配置。
        </div>
    ` : `
        <div class="form-group">
            <label for="keywords">🔍 搜索关键词</label>
            <input type="text" id="keywords" placeholder="例如: AI Security, RAG" />
        </div>

        <div class="form-group">
            <label for="startDate">📅 开始日期</label>
            <input type="date" id="startDate" />
        </div>

        <div class="form-group">
            <label for="endDate">📅 结束日期</label>
            <input type="date" id="endDate" />
        </div>

        <div class="form-group">
            <label for="maxResults">📊 最大结果数</label>
            <input type="number" id="maxResults" value="${config.maxResults}" min="1" max="100" />
        </div>

        <div class="form-group">
            <label>📝 生成 AI 摘要</label>
            <input type="checkbox" id="generateSummary" checked />
            <label for="generateSummary" style="display: inline; margin-left: 5px;">是</label>
        </div>

        <button onclick="searchPapers()">🚀 搜索论文</button>
        <button class="config-button" onclick="configureAPI()">⚙️ 重新配置 API</button>

        <div class="status" id="status"></div>
        <div class="results" id="results"></div>
    `}

    <script>
        const vscode = acquireVsCodeApi();

        function configureAPI() {
            vscode.postMessage({ type: 'config' });
        }

        function searchPapers() {
            const keywords = document.getElementById('keywords').value;
            if (!keywords) {
                showStatus('请输入搜索关键词', 'error');
                return;
            }

            const payload = {
                keywords: keywords,
                startDate: document.getElementById('startDate').value,
                endDate: document.getElementById('endDate').value,
                maxResults: parseInt(document.getElementById('maxResults').value),
                generateSummary: document.getElementById('generateSummary').checked
            };

            showStatus('正在搜索论文...', 'info');
            vscode.postMessage({ type: 'search', payload: payload });
        }

        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + type;
        }

        function displayResults(papers) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<h3>搜索结果 (' + papers.length + ' 篇论文)</h3>';

            papers.forEach((paper, index) => {
                const card = document.createElement('div');
                card.className = 'paper-card';
                
                const authors = paper.authors.slice(0, 3).join(', ') + 
                               (paper.authors.length > 3 ? ' et al.' : '');
                
                card.innerHTML = \`
                    <div class="paper-title">\${index + 1}. \${paper.title}</div>
                    <div class="paper-meta">
                        <div>👤 \${authors}</div>
                        <div>📅 \${paper.published}</div>
                        <div>📄 <a href="\${paper.pdf_url}">\${paper.arxiv_id}</a></div>
                    </div>
                    \${paper.ai_summary ? \`
                        <div class="paper-summary">
                            <strong>🤖 AI 摘要：</strong><br/>
                            \${paper.ai_summary}
                        </div>
                    \` : ''}
                \`;
                
                resultsDiv.appendChild(card);
            });
        }

        // 接收来自扩展的消息
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.type) {
                case 'searchComplete':
                    showStatus('搜索完成！', 'success');
                    displayResults(message.payload.papers);
                    break;
                case 'searchError':
                    showStatus('搜索失败: ' + message.payload.error, 'error');
                    break;
            }
        });
    </script>
</body>
</html>`;
    }
}

// 配置 API
async function configureAPI() {
    const config = vscode.workspace.getConfiguration('paperRobot');

    const apiKey = await vscode.window.showInputBox({
        prompt: '请输入 API Key',
        password: true,
        value: config.get('apiKey') || ''
    });

    if (!apiKey) {
        return;
    }

    const baseUrl = await vscode.window.showInputBox({
        prompt: '请输入 API Base URL',
        value: config.get('baseUrl') || 'https://api.openai.com/v1'
    });

    const model = await vscode.window.showInputBox({
        prompt: '请输入模型名称',
        value: config.get('model') || 'gpt-4o-mini'
    });

    await config.update('apiKey', apiKey, vscode.ConfigurationTarget.Global);
    await config.update('baseUrl', baseUrl, vscode.ConfigurationTarget.Global);
    await config.update('model', model, vscode.ConfigurationTarget.Global);

    vscode.window.showInformationMessage('✓ API 配置已保存！');

    // 重新加载窗口
    vscode.commands.executeCommand('workbench.action.reloadWindow');
}

// 获取配置
function getConfiguration() {
    const config = vscode.workspace.getConfiguration('paperRobot');
    return {
        apiKey: config.get('apiKey') || '',
        baseUrl: config.get('baseUrl') || 'https://api.openai.com/v1',
        model: config.get('model') || 'gpt-4o-mini',
        maxResults: config.get('maxResults') || 20,
        outputDir: config.get('outputDir') || 'papers'
    };
}

// 处理搜索
async function handleSearch(payload: any, webview: vscode.Webview) {
    try {
        const config = getConfiguration();

        // 构建 Python 命令
        let cmd = `paper-robot search "${payload.keywords}"`;

        if (payload.startDate) {
            cmd += ` --start-date ${payload.startDate}`;
        }
        if (payload.endDate) {
            cmd += ` --end-date ${payload.endDate}`;
        }
        cmd += ` --max-results ${payload.maxResults}`;
        cmd += payload.generateSummary ? ' --summarize' : ' --no-summarize';
        cmd += ' --format json';

        // 执行命令
        webview.postMessage({
            type: 'searchComplete',
            payload: {
                papers: [],
                message: '搜索功能已触发，请查看输出目录'
            }
        });

        const { stdout, stderr } = await execAsync(cmd);

        vscode.window.showInformationMessage('论文搜索完成！');

    } catch (error: any) {
        webview.postMessage({
            type: 'searchError',
            payload: { error: error.message }
        });
        vscode.window.showErrorMessage('搜索失败: ' + error.message);
    }
}

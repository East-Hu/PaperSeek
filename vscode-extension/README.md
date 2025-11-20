# Paper-to-Action VSCode Extension

Automated academic paper delivery for researchers - right in your VSCode editor!

## Features

- **📚 ArXiv Search** - Search for papers directly from VSCode
- **🤖 AI Summarization** - Get AI-generated summaries of paper innovations
- **⚙️ Easy Configuration** - Simple API setup within VSCode
- **💾 Local Storage** - Papers saved to your local directory
- **🌍 Multi-language** - Chinese and English support

## Installation

### From VSCode Marketplace (Recommended)

1. Open VSCode
2. Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on Mac)
3. Search for "Paper-to-Action"
4. Click "Install"

### From VSIX File

1. Download the `.vsix` file from releases
2. Open VSCode
3. Press `Ctrl+Shift+P` → "Extensions: Install from VSIX"
4. Select the downloaded file

## Quick Start

1. **Click the 📚 icon** in the Activity Bar (left sidebar)
2. **Configure API** on first use:
   - Click "Configure API"
   - Enter your LLM API key
   - Enter API base URL (default: OpenAI)
   - Enter model name (default: gpt-4o-mini)
3. **Search Papers**:
   - Enter keywords
   - Select date range (optional)
   - Click "Search Papers"
4. **View Results** with AI summaries in the sidebar

## Configuration

Open VSCode Settings (`Ctrl+,`) and search for "Paper Robot":

- **API Key**: Your LLM service API key
- **Base URL**: API endpoint (default: `https://api.openai.com/v1`)
- **Model**: Model to use (default: `gpt-4o-mini`)
- **Max Results**: Maximum papers to fetch (default: 20)
- **Output Directory**: Where to save papers (default: `papers`)

## Supported LLM Providers

- OpenAI (GPT-4, GPT-4o-mini, etc.)
- Azure OpenAI
- Any OpenAI-compatible API service

## Usage

### Search Papers

1. Enter search keywords (e.g., "AI Security", "RAG")
2. Optionally set date range
3. Choose number of results
4. Toggle AI summary generation
5. Click "Search Papers"

### View Results

Results appear in the sidebar with:
- Paper title and authors
- Publication date
- ArXiv ID and PDF link
- AI-generated summary (if enabled)

## Requirements

- VSCode 1.80.0 or higher
- LLM API access (OpenAI, Azure, or compatible)
- Internet connection

## Extension Commands

- `Paper Robot: Search Papers` - Open search interface
- `Paper Robot: Configure API` - Set up API credentials
- `Paper Robot: Open Panel` - Show Paper Robot panel

## Privacy

- All API keys stored locally in VSCode settings
- No data sent to third parties except your configured LLM provider
- Papers saved to your local machine

## Support

- [GitHub Issues](https://github.com/East-Hu/paper-to-action/issues)
- [Documentation](https://github.com/East-Hu/paper-to-action#readme)

## License

MIT License - see [LICENSE](https://github.com/East-Hu/paper-to-action/blob/main/LICENSE)

---

**Made with ❤️ for researchers worldwide**

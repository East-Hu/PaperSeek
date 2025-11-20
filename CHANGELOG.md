# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-19

### Added
- ✨ Initial release of Paper-to-Action
- 🔍 ArXiv paper crawler with keyword and date range filtering
- 🤖 AI-powered paper summarization using LLM APIs (GPT-4o-mini, etc.)
- 🎨 Beautiful interactive CLI with Rich library
- 🌍 Multi-language support (Chinese and English)
- 📚 Language selection screen on first launch
- 💾 Multiple output formats (Markdown, JSON)
- ⚙️ Configurable settings via YAML file
- 🎯 Customizable robot name
- 📊 Progress indicators and loading animations
- 🎨 Gradient colored welcome banner
- 📦 Paper preview cards in CLI
- 💻 Basic VSCode extension
- 🔧 Command-line interface with multiple subcommands
- 📖 Comprehensive documentation (README in Chinese and English)
- 🤝 Contributing guidelines
- 📄 MIT License

### Features
- **Interactive Mode**: Beautiful menu-driven interface for easy navigation
- **Command Mode**: Direct command-line access for automation
- **API Management**: Easy API key configuration and testing
- **History Viewing**: Browse previously saved papers
- **Batch Processing**: Process multiple papers with progress tracking

### Technical
- Python 3.8+ support
- Rich terminal UI library
- Typer CLI framework
- ArXiv API integration
- OpenAI-compatible LLM API support
- YAML-based configuration
- Internationalization (i18n) system

### Known Issues
- VSCode extension webview needs further enhancement
- PDF download feature not yet implemented
- PyPI package not yet published
- VSCode Marketplace listing pending

### Coming Soon
- 📦 PyPI package publication
- 🔗 Direct PDF download support
- 📱 Enhanced VSCode extension UI
- 🧪 Unit test coverage
- 📊 More output formats (HTML, PDF)
- 🔄 Paper update notifications
- 🏷️ Paper tagging and categorization system

---

## Release Notes

### Version 0.1.0 Highlights

This is the first public release of Paper-to-Action! 🎉

**What's Special:**
- **Fancy CLI**: Unlike traditional academic tools, Paper-to-Action features a stunning command-line interface with animations, colors, and modern design
- **Multi-language**: Full support for both Chinese and English interfaces
- **AI-Powered**: Leverage LLM technology to generate concise summaries of academic papers
- **Fork & Use**: Designed for easy deployment and customization

**Target Users:**
- Researchers tracking latest papers in their field
- Students doing literature reviews
- Academic labs maintaining paper collections
- Anyone who reads ArXiv papers regularly

**Why Paper-to-Action?**
- Saves time by auto-summarizing papers
- Beautiful interface makes daily paper checks enjoyable
- Highly customizable for different research areas
- Open source and free to use

---

## Future Roadmap

### Version 0.2.0 (Planned)
- Enhanced VSCode extension with React-based UI
- Paper management features (favorites, tags, notes)
- Export to reference managers (Zotero, Mendeley)
- Citation format generation

### Version 0.3.0 (Planned)
- Multi-source support (beyond ArXiv)
- Collaborative features (shared collections)
- Paper recommendation system
- Advanced search filters

---

For detailed commit history, see [GitHub Commits](https://github.com/East-Hu/paper-to-action/commits/main)

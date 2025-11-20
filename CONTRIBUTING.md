# Contributing to Paper-to-Action

Thank you for your interest in contributing to Paper-to-Action! This document provides guidelines for contributing to the project.

## 🌟 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:

- **Bug Description**: Clear and concise description of the bug
- **Steps to Reproduce**: Detailed steps to reproduce the behavior
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: 
  - OS (macOS, Linux, Windows)
  - Python version
  - Paper-to-Action version
- **Screenshots**: If applicable, add screenshots

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

- **Feature Description**: Clear description of the proposed feature
- **Use Case**: Why this feature would be useful
- **Possible Implementation**: If you have ideas on how to implement it

### Pull Requests

1. **Fork the Repository**
   ```bash
   git clone https://github.com/East-Hu/paper-to-action.git
   cd paper-to-action
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the code style guidelines below
   - Add/update tests if applicable
   - Update documentation if needed

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```
   
   **Commit Message Guidelines:**
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation changes
   - `Refactor:` for code refactoring

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template with details

## 📝 Code Style Guidelines

### Python Code

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where applicable
- Write docstrings for all public functions and classes
- Keep functions focused and small (< 50 lines ideally)
- Use meaningful variable and function names

**Example:**

```python
def search_papers(
    keywords: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Search for papers on ArXiv
    
    Args:
        keywords: Search keywords
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        List of paper dictionaries
    """
    # Implementation here
    pass
```

### TypeScript Code (VSCode Extension)

- Follow the existing code style
- Use TypeScript types, avoid `any` when possible
- Add JSDoc comments for public functions

### Documentation

- Use clear, concise language
- Add code examples where helpful
- Keep line length < 100 characters for readability
- Use Markdown formatting consistently

## 🧪 Testing

Before submitting a PR, please test your changes:

```bash
# Activate virtual environment
source venv/bin/activate

# Install in development mode
pip install -e .

# Test the CLI
paper-seek

# Test specific features you modified
paper-seek search "test" --max-results 5
```

For VSCode extension:

```bash
cd vscode-extension
npm install
npm run compile
# Press F5 in VSCode to test
```

## 🌍 Internationalization (i18n)

When adding new UI text:

1. Add the text key to `paper_to_action/i18n.py`
2. Provide both Chinese (`zh`) and English (`en`) translations
3. Use `self.i18n.get("key_name")` in the code

**Example:**

```python
# In i18n.py
TEXTS = {
    "zh": {
        "new_feature": "新功能描述"
    },
    "en": {
        "new_feature": "New feature description"
    }
}

# In your code
console.print(self.i18n.get("new_feature"))
```

## 📁 Project Structure

```
paper_robot/
├── paper_to_action/          # Core Python package
│   ├── __init__.py
│   ├── arxiv_crawler.py      # ArXiv crawler
│   ├── llm_client.py         # LLM API client
│   ├── config.py             # Configuration management
│   ├── storage.py            # Data storage
│   ├── i18n.py               # Internationalization
│   └── cli/                  # CLI components
│       ├── interface.py      # Interactive UI
│       └── commands.py       # Command handlers
├── vscode-extension/         # VSCode extension
│   ├── src/
│   │   └── extension.ts
│   └── package.json
├── tests/                    # Test files
├── docs/                     # Documentation
└── README.md
```

## ✅ Checklist Before Submitting PR

- [ ] Code follows style guidelines
- [ ] Code has been tested locally
- [ ] Documentation has been updated (if needed)
- [ ] Commit messages follow the guidelines
- [ ] No unnecessary files included (check .gitignore)
- [ ] i18n texts added for both languages (if applicable)

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## 💬 Getting Help

If you have questions:

- Create an issue with the "question" label
- Check existing issues and documentation first
- Provide as much context as possible

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Paper-to-Action! 🚀

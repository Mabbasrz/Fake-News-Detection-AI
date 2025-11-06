# 🤝 Contributing to Fake News Detection System

Thank you for considering contributing to this project! This document will guide you through the contribution process.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## 🎯 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**Good Bug Report Includes:**
- Clear, descriptive title
- Exact steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Python version, OS details
- Error messages (full stack trace)

**Example:**
```markdown
**Bug**: App crashes when analyzing empty text

**Steps to Reproduce:**
1. Launch clean_app.py
2. Click "Analyze" without entering text
3. App freezes

**Expected**: Should show warning message
**Actual**: Application crashes
**OS**: Windows 11
**Python**: 3.9.7
**Error**: [paste error message]
```

### 💡 Suggesting Enhancements

Feature requests are welcome! Please include:

- **Use Case**: Why this feature is needed
- **Description**: What it should do
- **Examples**: How it would work
- **Benefits**: Who would benefit and how

### 🔧 Pull Requests

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Make** your changes
4. **Test** thoroughly
5. **Commit** with clear messages (`git commit -m 'Add some AmazingFeature'`)
6. **Push** to your fork (`git push origin feature/AmazingFeature`)
7. **Open** a Pull Request

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- Git
- Text editor (VS Code recommended)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/fake-news-detection.git
cd "github fake news detection by Muzammil Abbas"

# Install dependencies
pip install -r requirements.txt

# Set up config
# Edit config.json with your Groq API key

# Run tests (if available)
python -m pytest tests/

# Run application
python clean_app.py
```

## 📝 Coding Standards

### Python Style

- Follow **PEP 8** style guide
- Use **4 spaces** for indentation (no tabs)
- **Max line length**: 120 characters
- Use **meaningful variable names**

### Example:

```python
# Good
def analyze_news_article(text, use_cache=True):
    """
    Analyzes news article for authenticity.
    
    Args:
        text (str): News article text
        use_cache (bool): Whether to check cache first
        
    Returns:
        dict: Analysis results with verdict and confidence
    """
    if not text or len(text) < 5:
        raise ValueError("Text too short for analysis")
    
    # Implementation...
    return results

# Bad
def a(t,c=1):
    if not t:return None
    return r
```

### Code Documentation

- **Docstrings** for all functions/classes
- **Inline comments** for complex logic
- **Type hints** where helpful

### Commit Messages

Use clear, descriptive commit messages:

```
# Good
✅ Add caching system for API responses
✅ Fix crash when config.json is missing
✅ Improve UI responsiveness during analysis

# Bad
❌ update
❌ fix bug
❌ changes
```

## 🧪 Testing

Before submitting PR:

- [ ] Test all modified features
- [ ] Verify no new bugs introduced
- [ ] Check both dark/light themes
- [ ] Test with various text lengths
- [ ] Ensure API key config works
- [ ] Run on clean Python environment

## 📂 Project Structure

Understanding the codebase:

```python
clean_app.py
├── ML Functions (train_model, predict_news)
├── AI Integration (search_gemini)
├── Database (add_to_learning_database, find_stored_analysis)
├── UI Class (App)
│   ├── __init__: Setup
│   ├── setup_ui: Build interface
│   ├── analyze: Main analysis logic
│   ├── toggle_theme: Theme switching
│   └── view_database: DB viewer
└── Main: Entry point
```

## 🎨 UI Contributions

If modifying UI:

- Test in **both themes** (dark/light)
- Ensure **responsive** layout
- Use **consistent** color scheme
- Keep **performance** smooth
- Test on different **screen sizes**

## 🤖 AI/ML Contributions

For model improvements:

- Document **accuracy changes**
- Provide **test results**
- Explain **methodology**
- Consider **API cost** impact
- Maintain **backward compatibility**

## 📊 Database Schema

If modifying database structure:

```python
# Current learning_db.json format
{
    "text": "News article content",
    "label": 0 or 1,  # 0=fake, 1=real
    "source": "ml/ai",
    "confidence": 0.0-1.0,
    "ai_analysis": "Reasoning text",
    "timestamp": "ISO format"
}
```

Ensure migrations for existing users!

## 🔐 Security

- **Never commit** API keys
- **Sanitize** user inputs
- **Validate** all external data
- **Handle** errors gracefully
- **Test** edge cases

## 📞 Questions?

- **GitHub Issues**: Technical questions
- **Discussions**: General questions
- **Email**: Muzammil Abbas (see profile)

## 🌟 Recognition

Contributors will be:
- Listed in README
- Mentioned in release notes
- Part of project history

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making this project better! 🙏**

**Happy Coding! 💻**

Created by Muzammil Abbas | November 2025

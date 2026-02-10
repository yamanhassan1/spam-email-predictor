# 🤝 Contributing to Email Spam Detector

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Getting Started

### 1. Fork the Repository
```bash
# Click "Fork" on GitHub
git clone https://github.com/your-username/Email-Spam-Detector.git
cd Email\ Spam\ Detector
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Set Up Development Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### 4. Make Your Changes
- Write clean, readable code
- Follow PEP 8 style guide
- Add docstrings to functions
- Include type hints where possible

### 5. Test Your Changes
```bash
# Run tests
pytest tests/

# Run linting
flake8 src/
black src/

# Run type checking
mypy src/
```

### 6. Commit Your Changes
```bash
git add .
git commit -m "feat: add new feature" -m "Detailed description of changes"
```

### 7. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 8. Create a Pull Request
- Go to GitHub and create a PR
- Provide clear description of changes
- Reference any related issues
- Wait for review and feedback

## Commit Message Guidelines

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Build process, dependencies, etc.

### Examples
```
feat(model): add support for multiple classifiers
fix(nlp): handle unicode characters in preprocessing
docs(readme): update installation instructions
refactor(design): simplify CSS structure
```

## Code Style

### Python Style Guide (PEP 8)

```python
# Good
def analyze_message(text: str, model: Any) -> Dict[str, Any]:
    """Analyze message for spam indicators.
    
    Args:
        text: Message text to analyze
        model: Trained ML model
        
    Returns:
        Dictionary with analysis results
    """
    result = {}
    # Implementation
    return result

# Bad
def analyze_message(text,model):
    result={}
    # Implementation
    return result
```

### Naming Conventions
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

### Documentation

```python
def function_name(param1: str, param2: int) -> bool:
    """One-line summary of function.
    
    Longer description if needed. Explain what the function does,
    any important behavior, and edge cases.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is invalid
        
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
    pass
```

## Testing

### Writing Tests

```python
# tests/test_nlp.py
import pytest
from src.nlp import transformed_text

def test_transformed_text_basic():
    """Test basic text transformation."""
    result = transformed_text("Hello World")
    assert isinstance(result, str)
    assert len(result) > 0

def test_transformed_text_empty():
    """Test with empty string."""
    result = transformed_text("")
    assert result == ""

@pytest.mark.parametrize("text,expected", [
    ("HELLO", "hello"),
    ("Hello123", "hello"),
])
def test_transformed_text_cases(text, expected):
    """Test various text cases."""
    result = transformed_text(text)
    assert expected in result.lower()
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_nlp.py

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_nlp.py::test_transformed_text_basic
```

## Documentation

### Updating README
- Keep it concise and up-to-date
- Include examples
- Update table of contents
- Add new features to feature list

### Adding Docstrings
- Use Google-style docstrings
- Include type hints
- Provide examples
- Document exceptions

### Creating New Pages
1. Create file in `src/pages/`
2. Add render function
3. Update `app.py` navigation
4. Document in README

## Pull Request Process

1. **Before Submitting**
   - Run tests: `pytest`
   - Check linting: `flake8 src/`
   - Format code: `black src/`
   - Update documentation

2. **PR Description**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Related Issues
   Fixes #123
   
   ## Testing
   - [ ] Added tests
   - [ ] All tests pass
   - [ ] Manual testing done
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] No new warnings generated
   ```

3. **Review Process**
   - Maintainers will review code
   - Provide feedback if needed
   - Make requested changes
   - Rebase if necessary

4. **Merging**
   - Squash commits if needed
   - Merge to main branch
   - Delete feature branch

## Areas for Contribution

### High Priority
- [ ] Multi-language support
- [ ] API endpoint development
- [ ] Performance optimization
- [ ] Additional test coverage
- [ ] Documentation improvements

### Medium Priority
- [ ] Browser extension
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Custom model training UI
- [ ] Email integration

### Low Priority
- [ ] UI/UX improvements
- [ ] Additional visualizations
- [ ] Example datasets
- [ ] Tutorial videos

## Development Tools

### Recommended IDE
- VS Code with Python extension
- PyCharm Professional/Community
- Vim/Neovim with Python plugins

### Useful Extensions
- Python (Microsoft)
- Pylance
- Black Formatter
- Flake8
- Pytest

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
EOF

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Reporting Issues

### Bug Report Template
```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Windows/Mac/Linux
- Python: 3.x
- Streamlit: 1.x

## Screenshots
If applicable, add screenshots

## Additional Context
Any other relevant information
```

### Feature Request Template
```markdown
## Description
Clear description of the feature

## Use Case
Why this feature is needed

## Proposed Solution
How it should work

## Alternatives
Other possible approaches

## Additional Context
Any other relevant information
```

## Performance Guidelines

### Code Performance
- Avoid nested loops where possible
- Use list comprehensions
- Cache expensive operations
- Profile before optimizing

### Memory Usage
- Don't load entire datasets into memory
- Use generators for large data
- Clean up resources properly
- Monitor memory usage

### API Performance
- Implement caching
- Use pagination
- Compress responses
- Optimize database queries

## Security Guidelines

- Never commit secrets or API keys
- Validate all user inputs
- Use parameterized queries
- Keep dependencies updated
- Report security issues privately

## Questions?

- Open an issue for questions
- Check existing issues first
- Join our community discussions
- Contact maintainers directly

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

---

**Thank you for contributing! 🎉**

Your contributions make this project better for everyone.

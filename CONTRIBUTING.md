# Contributing to Atlas AI

Thank you for your interest in contributing to Atlas AI! This document provides guidelines and instructions for contributing.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Atlas-AI.git
   cd Atlas-AI
   ```
3. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and commit with clear messages
5. **Push to your fork** and submit a Pull Request

## 📋 Before You Start

- Read the [COMPREHENSIVE_ANALYSIS_REPORT.md](COMPREHENSIVE_ANALYSIS_REPORT.md) to understand the project structure
- Check [existing issues](https://github.com/YOUR_USERNAME/Atlas-AI/issues) to avoid duplicate work
- For major changes, open an issue first to discuss your approach

## 🐛 Reporting Bugs

**Before submitting a bug report:**
- Check if the bug has already been reported
- Ensure you're using the latest version
- Collect relevant information (error messages, logs, screenshots)

**Bug Report Template:**
```markdown
**Description:** Clear description of the bug

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. ...

**Expected Behavior:** What should happen

**Actual Behavior:** What actually happens

**Environment:**
- OS: [e.g., Windows 11, Ubuntu 22.04]
- Python Version: [e.g., 3.10.5]
- Node Version: [e.g., 18.16.0]
- Browser: [e.g., Chrome 120]

**Additional Context:** Screenshots, logs, etc.
```

## 💡 Suggesting Features

We welcome feature suggestions! Please:
1. Check if the feature has been suggested before
2. Open an issue with the `enhancement` label
3. Clearly describe the feature and its benefits
4. Provide use cases and examples

## 🔧 Development Setup

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Run the server
python start_server.py
```

### Frontend Setup
```bash
cd frontend/vite-react-app
npm install
npm run dev
```

## 📝 Coding Standards

### Python (Backend)
- Follow **PEP 8** style guide
- Use **type hints** for function parameters and return values
- Write **docstrings** for all public functions/classes
- Maximum line length: 120 characters
- Use **Black** for formatting:
  ```bash
  pip install black
  black backend/
  ```

**Example:**
```python
from typing import List, Dict, Optional

def get_career_recommendations(
    skills: List[str],
    target_role: Optional[str] = None
) -> Dict[str, any]:
    """
    Generate career recommendations based on user skills.
    
    Args:
        skills: List of user's current skills
        target_role: Optional target career role
    
    Returns:
        Dictionary containing recommendations and match scores
    """
    # Implementation
    pass
```

### TypeScript/React (Frontend)
- Use **functional components** with hooks
- Use **TypeScript** for all new code
- Follow **React best practices**
- Use **ESLint** and **Prettier**:
  ```bash
  npm run lint
  npm run format
  ```

**Example:**
```tsx
import React from 'react';

interface ProfileProps {
    userId: number;
    onUpdate?: () => void;
}

export const Profile: React.FC<ProfileProps> = ({ userId, onUpdate }) => {
    // Component implementation
    return <div>Profile Content</div>;
};
```

### Commit Messages
Follow **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(auth): add password reset functionality

Add endpoint for password reset email and token validation.
Includes rate limiting to prevent abuse.

Closes #123

---

fix(roadmap): correct double /api prefix bug

Remove duplicate /api prefix in roadmap router that was
causing 404 errors on all roadmap endpoints.

Fixes #456

---

docs(readme): update installation instructions

Add troubleshooting section for common setup issues.
```

## 🧪 Testing

### Running Tests

**Backend:**
```bash
cd backend
pytest
pytest --cov=. --cov-report=html  # With coverage
```

**Frontend:**
```bash
cd frontend/vite-react-app
npm test
npm run test:coverage
```

### Writing Tests

**Backend (pytest):**
```python
import pytest
from api.routes.auth import create_user

def test_create_user_success(db_session):
    """Test successful user creation."""
    user = create_user(
        email="test@example.com",
        password="SecurePass123",
        db=db_session
    )
    assert user.email == "test@example.com"
    assert user.hashed_password != "SecurePass123"
```

**Frontend (Vitest + Testing Library):**
```tsx
import { render, screen } from '@testing-library/react';
import { Login } from './Login';

test('renders login form', () => {
    render(<Login />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
});
```

## 🔀 Pull Request Process

1. **Ensure your code:**
   - Passes all tests
   - Follows coding standards
   - Is well-documented
   - Doesn't break existing functionality

2. **Update documentation** if needed:
   - README.md
   - API documentation
   - Inline code comments

3. **PR Title Format:**
   ```
   [Type] Brief description
   
   Examples:
   [Feature] Add mock interview functionality
   [Fix] Correct login error handling
   [Docs] Update API documentation
   ```

4. **PR Description Template:**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Related Issues
   Closes #123

   ## Testing
   - [ ] All tests pass
   - [ ] Added new tests for changes
   - [ ] Manually tested the feature

   ## Screenshots (if applicable)
   [Add screenshots here]

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-reviewed my code
   - [ ] Commented complex sections
   - [ ] Updated documentation
   - [ ] No new warnings generated
   - [ ] Added tests that prove fix/feature works
   ```

5. **Review Process:**
   - At least 1 approval required
   - Address all review comments
   - Maintainers will merge when ready

## 🎯 Priority Areas for Contribution

See [COMPREHENSIVE_ANALYSIS_REPORT.md](COMPREHENSIVE_ANALYSIS_REPORT.md) for detailed areas needing attention:

### 🔴 High Priority (Bugs)
1. Login error handling mismatch
2. Experience translator signature fix
3. Roadmap double-prefix bug
4. Postman documentation updates

### 🟡 Medium Priority (Features)
1. ESCO API integration
2. Milestone tracking for roadmaps
3. Side hustle finder backend
4. Scholarship database seeding
5. Mock interview AI

### 🟢 Good First Issues
1. Add missing docstrings
2. Improve error messages
3. Add frontend component tests
4. Update documentation with examples
5. Add health check endpoint

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Project Architecture](architecture/)

## 💬 Communication

- **Issues:** For bug reports and feature requests
- **Discussions:** For questions and general discussion
- **Pull Requests:** For code contributions

## 🏆 Recognition

Contributors will be acknowledged in:
- README.md Contributors section
- Release notes
- Project documentation

Thank you for contributing to Atlas AI! 🚀✨

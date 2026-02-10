# Atlas AI - Intelligent Career Development Platform 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-61dafb.svg)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/typescript-4.0+-3178c6.svg)](https://www.typescriptlang.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Atlas AI is a comprehensive career development platform that uses Artificial Intelligence to guide users through their professional journey. From personalized career recommendations and skill gap analysis to roadmap generation and job simulation, Atlas AI provides a holistic approach to career growth.

> ⚠️ **Note:** This is a pre-release version. See [COMPREHENSIVE_ANALYSIS_REPORT.md](COMPREHENSIVE_ANALYSIS_REPORT.md) for known issues and roadmap.

## 🌟 Features

- **Smart Dashboard**: personalized stats, career path tracking, and daily goals.
- **AI Career Guidance**: specialized algorithms to recommend careers based on skills and interests.
- **Dynamic Roadmaps**: step-by-step learning paths generated for your target role.
- **Skill Assessment**: track and verify your proficiency in key technologies.
- **Mock Interviews**: AI-powered interview practice with real-time feedback.
- **Tools Suite**: Scholarship finder, Side Hustle generator, Ghost Job detector.
- **Settings**: Fully customizable experience with Dark/Light themes and privacy controls.

## 🛠️ Technology Stack

**Frontend:**
- React 18 (Vite)
- TypeScript
- React Query & Context API
- Vanilla CSS Variables (Theming)

**Backend:**
- FastAPI (Python 3.10+)
- SQLAlchemy ORM
- PostgreSQL / SQLite
- OpenAI API Integration

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- Docker & Docker Compose (Optional, for containerized run)

### Local Development (Manual)

1.  **Backend Setup**:
    ```bash
    cd backend
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    # source venv/bin/activate
    
    pip install -r requirements.txt
    
    # Configure environment
    # Copy .env.example to .env and add your OPENAI_API_KEY
    
    python start_server.py
    ```

2.  **Frontend Setup**:
    ```bash
    cd frontend/vite-react-app
    npm install
    npm run dev
    ```

    Access the app at `http://localhost:5173`.

### 🐳 Deployment with Docker

We provide a production-ready Docker setup.

1.  **Build and Run**:
    ```bash
    docker-compose up --build -d
    ```

2.  **Access**:
    - Frontend: `http://localhost:3000`
    - Backend API: `http://localhost:8000`
    - API Docs: `http://localhost:8000/docs`

## 📁 Project Structure

```
atlas-ai/
├── backend/                 # FastAPI application
│   ├── api/                 # Route handlers
│   ├── core/                # Config and security
│   ├── models/              # Database schemas
│   └── services/            # Business logic & AI
├── frontend/vite-react-app/ # React application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── contexts/        # Global state
│   │   ├── pages/           # Application views
│   │   └── services/        # API client
└── docker-compose.yml       # Container orchestration
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [COMPREHENSIVE_ANALYSIS_REPORT.md](COMPREHENSIVE_ANALYSIS_REPORT.md) for priority areas and known issues.

## 🐛 Bug Reports & Feature Requests

- **Bugs:** Open an issue with the `bug` label
- **Features:** Open an issue with the `enhancement` label
- **Security:** Email security concerns privately (see SECURITY.md)

## 📊 Project Status

**Current Version:** 0.9.0-beta (MVP)  
**Status:** ⭐⭐⭐⚫⚫ (3/5 - Functional with known issues)

**Next Milestones:**
- ✅ Fix critical bugs (5 identified)
- 🔄 Add comprehensive testing
- 🔄 Security hardening
- 🔄 Complete missing features
- 🔄 Production deployment

See [COMPREHENSIVE_ANALYSIS_REPORT.md](COMPREHENSIVE_ANALYSIS_REPORT.md) for detailed analysis.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Acknowledgments

- OpenAI for GPT-4o-mini API
- ESCO for occupation and skill data
- FastAPI and React communities
- All contributors and testers

## 📧 Contact

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/Atlas-AI/issues)
- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/Atlas-AI/discussions)
- **Documentation:** [Project Wiki](https://github.com/YOUR_USERNAME/Atlas-AI/wiki)

---

**Made with ❤️ by the Atlas AI Team**

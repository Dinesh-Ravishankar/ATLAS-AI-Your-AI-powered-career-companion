# Changelog

All notable changes to the Atlas AI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔄 In Progress
- Comprehensive testing infrastructure
- ESCO API integration for career data
- Milestone tracking for roadmaps
- Rate limiting for API endpoints
- Security hardening

### 🐛 Known Issues
See [COMPREHENSIVE_ANALYSIS_REPORT.md](COMPREHENSIVE_ANALYSIS_REPORT.md) for detailed bug list:
1. Login error handling mismatch (frontend/src/pages/Login.tsx:31)
2. Experience translator signature mismatch (backend/api/routes/skills.py)
3. Roadmap double /api prefix (backend/api/routes/roadmap.py:14)
4. 401 auto-redirect masks errors (frontend/src/services/api.ts)
5. Postman documentation path drift (backend/POSTMAN_TESTING_GUIDE.md)

## [0.9.0-beta] - 2026-02-10

### 🎉 Initial Beta Release

### ✨ Added
#### Backend Features
- FastAPI REST API with 9 route modules (43 endpoints)
- JWT authentication with bcrypt password hashing
- SQLAlchemy ORM with PostgreSQL/SQLite support
- OpenAI GPT-4o-mini integration for AI features
- LangChain orchestrator for conversation management
- 13 AI modules including:
  - Career recommendations
  - Skill gap analysis
  - Learning pathway generation
  - Roadmap generator (587 lines)
  - Resume parser (PDF/DOCX support)
  - Resume generator (PDF export)
  - Ghost job detector (scam detection)
  - Experience translator
  - Project recommender
  - Platform guide (RAG chatbot)
  - ESCO API client
- Gamification system (XP, levels, badges)
- Onboarding wizard (multi-step)
- Origin Story stream selector (8 majors)

#### Frontend Features
- React 18 + TypeScript + Vite
- 14 full pages including:
  - Dashboard with Bento grid layout
  - Profile management (Atlas Card)
  - Career exploration
  - Skills management
  - Learning roadmap visualization
  - Projects portfolio
  - Clarity Coach (AI counselor)
  - Mock interview practice
  - Job verifier
  - Scholarships finder
  - Side hustles
  - Settings
- React Query for server state management
- AuthContext for global auth state
- Protected routes with auth guard
- Custom UI components (Card, Button, Modal)
- Responsive design with CSS variables

#### Infrastructure
- Docker + Docker Compose setup
- Multi-stage Dockerfile for frontend
- Backend Dockerfile with Python 3.10
- Environment-based configuration
- Supabase integration support

### 📚 Documentation
- Comprehensive README with quick start
- COMPREHENSIVE_ANALYSIS_REPORT.md (700+ lines)
- IMPLEMENTATION_PLAN.md
- SUPABASE_INTEGRATION.md
- SUPABASE_SETUP.md
- DATABASE_CONNECTION_STEPS.md
- POSTMAN_TESTING_GUIDE.md
- BUG_FIX_SUMMARY.md
- Multiple session reports

### 🛠️ Technical Details
- **Backend:** FastAPI 0.115.0, SQLAlchemy 2.0.36, OpenAI, LangChain 0.1.20
- **Frontend:** React 18, TypeScript 4+, Vite 4, React Router v7, React Query v5
- **Database:** PostgreSQL/SQLite with 6 tables
- **AI:** GPT-4o-mini, Sentence Transformers (all-MiniLM-L6-v2)
- **Auth:** JWT tokens, bcrypt hashing

### ⚠️ Limitations
- No production deployment yet
- Minimal test coverage (15% backend, 0% frontend)
- Mock data in some features (career recommender, skill gap analyzer)
- Missing features:
  - Side hustle finder backend
  - Scholarship database seeding
  - Mock interview AI backend
  - Mentorship matching backend
- Security considerations:
  - No rate limiting
  - Limited file upload validation
  - Missing health check endpoints

### 📊 Project Metrics
- ~14,000 lines of code
- 80+ files
- 43 API endpoints (36 working, 7 broken)
- 13 AI modules
- 6 database tables
- 14 frontend pages
- 40+ reusable components

---

## Version History

### Version Numbering
- **Major (X.0.0):** Breaking changes, major rewrites
- **Minor (0.X.0):** New features, non-breaking changes
- **Patch (0.0.X):** Bug fixes, small improvements

### Upcoming Versions
- **v0.9.1** - Critical bug fixes (45 min development time)
- **v0.9.5** - Security + quick wins (1 week)
- **v1.0.0** - Production-ready with full testing (3 months)

---

## Links
- [Changelog Guidelines](https://keepachangelog.com/en/1.0.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- [Project Analysis](COMPREHENSIVE_ANALYSIS_REPORT.md)
- [Contributing Guide](CONTRIBUTING.md)

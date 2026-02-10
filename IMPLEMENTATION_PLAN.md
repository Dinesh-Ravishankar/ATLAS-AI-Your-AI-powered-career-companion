# Atlas AI — Complete Implementation Plan

**Generated:** February 9, 2026  
**Current State:** ~65-70% MVP complete | ~40-45% of full vision  
**Remaining Effort Estimate:** ~60-80 hours of focused development

---

## Phase 0: Critical Blockers (Fix Before Anything Else)

> These are production-stopping bugs. Nothing else works until these are resolved.

### 0.1 — Backend Cannot Start (bcrypt issue)
- **Problem:** `python main.py` exits with code 1. `pip install bcrypt==3.1.7` also fails.
- **Root Cause:** `passlib[bcrypt]` depends on a bcrypt version incompatible with the installed Python 3.11. The `bcrypt` 4.x API changed — `bcrypt.hashpw()` now returns `bytes`, and `passlib` hasn't adapted.
- **Fix:**
  1. Remove `passlib` dependency entirely (it's imported nowhere — `jwt_handler.py` uses `bcrypt` directly).
  2. `pip install bcrypt>=4.0` (works with Python 3.11).
  3. Ensure `jwt_handler.py` handles bytes↔str conversion (it already does).
- **Files:** `backend/requirements.txt`, verify `backend/auth/jwt_handler.py`
- **Time:** 15 min
- **Priority:** 🔴 BLOCKER

### 0.2 — Frontend Cannot Start (`npm run dev` fails)
- **Problem:** Exit code 1 on `npm run dev`.
- **Likely Cause:** `node_modules` not installed, or Next.js 16 + React 19 version conflict.
- **Fix:**
  1. `cd frontend && rm -rf node_modules .next && npm install`
  2. If that fails, check for Node.js version (Next 16 needs Node 18+).
  3. Verify `next.config.ts` has valid config (currently may be empty/minimal).
- **Files:** `frontend/package.json`, `frontend/next.config.ts`
- **Time:** 15 min
- **Priority:** 🔴 BLOCKER

### 0.3 — Login Endpoint Encoding Mismatch
- **Problem:** Frontend sends JSON `{ username, password }` but FastAPI's `OAuth2PasswordRequestForm` expects `application/x-www-form-urlencoded`.
- **Fix:** Change `api-client.ts` login method to send form-encoded data:
  ```ts
  const params = new URLSearchParams();
  params.append('username', email);
  params.append('password', password);
  const response = await this.client.post('/api/auth/login', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });
  ```
- **Files:** `frontend/lib/api-client.ts`
- **Time:** 10 min
- **Priority:** 🔴 BLOCKER

### 0.4 — Scholarships Page Import Error
- **Problem:** `scholarships/page.tsx` uses `import apiClient from "@/lib/api-client"` (default import) while all other pages use `import { apiClient } from "@/lib/api-client"` (named import). Both exist, but this inconsistency may cause issues with tree-shaking or bundling.
- **Fix:** Standardize to named import: `import { apiClient } from "@/lib/api-client"`.
- **Files:** `frontend/app/dashboard/scholarships/page.tsx`
- **Time:** 2 min
- **Priority:** 🟡 Bug

---

## Phase 1: Stabilize & Polish Existing MVP (Sprint 1)

> Goal: Make everything that exists actually work reliably end-to-end.  
> **Estimated time: 8-10 hours**

### 1.1 — End-to-End Auth Flow Testing & Fixes
- Test: Register → Auto-login → Dashboard → Logout → Login
- Add proper error messages for duplicate email, weak password
- Add `auth/refresh` endpoint for token refresh
- Files: `backend/api/routes/auth.py`, `frontend/lib/api-client.ts`, `frontend/app/login/page.tsx`
- **Time:** 2 hrs

### 1.2 — Protected Route Middleware (Frontend)
- Create auth guard: redirect to `/login` if no token on dashboard pages
- Add `AuthProvider` context wrapping the dashboard layout
- Files: NEW `frontend/lib/auth-context.tsx`, modify `frontend/app/dashboard/layout.tsx`
- **Time:** 1.5 hrs

### 1.3 — Mobile Responsive Sidebar
- Currently `hidden md:flex` — no navigation on mobile
- Add hamburger menu toggle for screens < 768px
- Files: `frontend/components/sidebar.tsx`, `frontend/app/dashboard/layout.tsx`
- **Time:** 1.5 hrs

### 1.4 — Loading States & Error Boundaries
- Add skeleton loaders for dashboard, profile, and all feature pages
- Create a reusable `<ErrorBoundary>` component
- Files: NEW `frontend/components/ui/skeleton.tsx`, NEW `frontend/components/error-boundary.tsx`, update all dashboard pages
- **Time:** 2 hrs

### 1.5 — Framer Motion Page Transitions
- Already installed but unused. Add `<AnimatePresence>` and fade/slide transitions.
- Files: `frontend/app/dashboard/layout.tsx`, all page.tsx files
- **Time:** 1 hr

### 1.6 — Next.js Image Optimization
- Landing page uses raw `<img>` tags with Unsplash URLs
- Switch to `next/image` with proper domains config
- Files: `frontend/next.config.ts`, `frontend/app/page.tsx`
- **Time:** 30 min

### 1.7 — Dark Mode Support
- Add dark mode CSS variables in `globals.css`
- Create theme toggle button in Header
- Use `prefers-color-scheme` or localStorage persistence
- Files: `frontend/app/globals.css`, `frontend/components/header.tsx`, NEW `frontend/lib/theme-context.tsx`
- **Time:** 1.5 hrs

---

## Phase 2: Complete Core Backend Intelligence (Sprint 2)

> Goal: Replace all mock/hardcoded data with real intelligence.  
> **Estimated time: 12-15 hours**

### 2.1 — ESCO API Integration
- Connect to `https://ec.europa.eu/esco/api` for occupations and skills
- Map target roles to ESCO occupation URIs
- Fetch "essential" and "optional" skills per occupation
- Replace hardcoded `role_skills` dict in `skill_gap_analyzer.py`
- Files: NEW `backend/ai/esco_client.py`, modify `backend/ai/skill_gap_analyzer.py`
- **Time:** 3 hrs

### 2.2 — Semantic Skill Matching (NLP)
- Use `sentence-transformers` (already in requirements) for skill normalization
- Encode user skills and ESCO skills → cosine similarity matching
- Handle synonyms: "JS" → "JavaScript", "ML" → "Machine Learning"
- Files: `backend/ai/skill_gap_analyzer.py`
- **Time:** 2 hrs

### 2.3 — Alembic Migration Setup
- Initialize Alembic, generate initial migration from existing models
- Create migration scripts for any future schema changes
- Files: NEW `backend/alembic/`, NEW `backend/alembic.ini`, modify `backend/README.md`
- **Time:** 1.5 hrs

### 2.4 — Resume Upload & Parsing
- POST `/api/profile/upload-resume` endpoint accepting PDF/DOCX
- Extract text using PyPDF2 + python-docx (already in requirements)
- Use GPT to extract structured data: name, skills, education, experience
- Auto-populate Atlas Card fields
- Files: NEW `backend/ai/resume_parser.py`, modify `backend/api/routes/profile.py`
- **Time:** 3 hrs

### 2.5 — GitHub Integration
- OAuth flow or token-based GitHub API access
- Import user repositories: titles, descriptions, languages, stars
- Extract skills from repo languages and package files
- Files: NEW `backend/ai/github_integration.py`, modify `backend/api/routes/profile.py`, modify `backend/config.py`
- **Time:** 2.5 hrs

### 2.6 — Database Seed Data
- Create seed script with sample careers, skills, and scholarship data
- Populate `careers` and `scholarships` tables with real data
- Files: NEW `backend/seed_data.py`
- **Time:** 1.5 hrs

### 2.7 — Comprehensive Logging
- Add Python `logging` module across all routes and AI modules
- Log API requests, errors, AI response times
- Files: NEW `backend/utils/logger.py`, modify all route files and AI modules
- **Time:** 1.5 hrs

---

## Phase 3: Missing Core Feature Pages (Sprint 3)

> Goal: Build the 9 unimplemented core features from the spec.  
> **Estimated time: 20-25 hours**

### 3.1 — Onboarding Wizard
- **Backend:** POST `/api/onboarding/complete` — saves initial assessment to profile
- **Frontend:** Multi-step wizard after first registration: interests, skills, education, goals
- Gamified progress bar (10 steps), auto-creates Atlas Card skeleton
- Files: NEW `backend/api/routes/onboarding.py`, NEW `frontend/app/onboarding/page.tsx`
- **Time:** 3 hrs

### 3.2 — Interactive Career Maps (Skill Trees)
- **Backend:** GET `/api/career/skill-tree/{role}` — returns hierarchical skill progression
- **Frontend:** D3.js or react-flow tree visualization: Student → Junior → Mid → Senior
- Show which skills unlock which roles
- Files: NEW `frontend/app/dashboard/career-map/page.tsx`, modify `backend/api/routes/career.py`
- **Dependencies:** ESCO integration (2.1)
- **Time:** 4 hrs

### 3.3 — Career Comparator Tool
- **Backend:** POST `/api/career/compare` — compares 2-3 career paths side-by-side
- **Frontend:** Side-by-side cards: salary, growth rate, work-life balance, skill overlap, demand
- Files: NEW `frontend/app/dashboard/career-compare/page.tsx`, modify `backend/api/routes/career.py`
- **Time:** 2.5 hrs

### 3.4 — Mock Interview Simulator
- **Backend:** POST `/api/career/mock-interview` — GPT-powered interviewer for a specific role
- **Frontend:** Chat-style interface with role selection, timer, and feedback summary
- Uses orchestrator's LangChain for contextual follow-up questions
- Files: NEW `frontend/app/dashboard/mock-interview/page.tsx`, modify `backend/ai/orchestrator.py`, modify `backend/api/routes/career.py`
- **Time:** 3.5 hrs

### 3.5 — Personalized Learning Pathways
- **Backend:** POST `/api/career/learning-path` — curated course recommendations per missing skill
- Integrate free course APIs (Coursera, Udemy affiliate links) or static curated list
- **Frontend:** Step-by-step learning roadmap with progress checkboxes
- Files: NEW `frontend/app/dashboard/learning-path/page.tsx`, NEW `backend/ai/learning_pathway.py`, modify `backend/api/routes/career.py`
- **Time:** 3 hrs

### 3.6 — Coursework Relevance Mapper
- **Backend:** POST `/api/academic/relevance` — AI explains why each course matters for target career
- **Frontend:** Input current courses → get relevance scores and explanations per career
- Files: NEW `frontend/app/dashboard/coursework/page.tsx`, modify `backend/api/routes/career.py`
- **Time:** 2 hrs

### 3.7 — Internship Matcher
- **Backend:** POST `/api/career/internships` — matches profile to internship opportunities
- GPT-generated recommendations based on skills + location + availability
- **Frontend:** Filterable card grid with match scores
- Files: NEW `frontend/app/dashboard/internships/page.tsx`, modify `backend/api/routes/career.py`
- **Time:** 2 hrs

### 3.8 — "Future Self" Projector
- **Backend:** POST `/api/career/future-projection` — simulates career trajectory at 5/10/15 years
- **Frontend:** Timeline visualization with salary, role progression, skill accumulation
- Files: NEW `frontend/app/dashboard/future-self/page.tsx`, modify `backend/api/routes/career.py`
- **Time:** 2.5 hrs

### 3.9 — Pivot Simulator
- **Backend:** POST `/api/career/pivot-analysis` — "What if I switch to X?" transferable skills analysis
- **Frontend:** From-To career selector, transferable skills Venn diagram, new gaps
- Files: NEW `frontend/app/dashboard/pivot/page.tsx`, modify `backend/api/routes/career.py`
- **Time:** 2 hrs

> **After Phase 3:** Update sidebar navigation to include all new pages.

---

## Phase 4: Complete "Winning" Features (Sprint 4)

> Goal: Build the remaining 3 high-impact differentiation features.  
> **Estimated time: 10-12 hours**

### 4.1 — Soft Skills Bootcamp with AI Role-Play
- **Backend:** POST `/api/skills/roleplay/start` and `/api/skills/roleplay/respond`
- Use existing `orchestrator.start_soft_skills_roleplay()` method
- Scenarios: "Tell your manager you missed a deadline", "Mediate a team conflict", "Salary negotiation"
- Track rounds, provide a score + feedback after 3-4 exchanges
- **Frontend:** Chat-like roleplay interface with scenario selector, performance scorecard
- Files: NEW `frontend/app/dashboard/soft-skills/page.tsx`, NEW `backend/api/routes/skills.py`
- **Time:** 4 hrs

### 4.2 — AI-Powered Experience Translator
- **Backend:** POST `/api/profile/translate-experience`
- Input: free-text non-traditional experience ("Ran a YouTube channel with 10K subs")
- Output: professional skill tags, resume bullet points, matching job roles
- **Frontend:** Text area input → bullet points + skill badges + role suggestions
- Files: NEW `frontend/app/dashboard/experience-translator/page.tsx`, NEW `backend/ai/experience_translator.py`, modify `backend/api/routes/profile.py`
- **Time:** 3 hrs

### 4.3 — Industry Trend Radar (Full Page)
- **Backend:** Endpoint already exists (`GET /api/career/trending-skills`) but returns mock data
- Enhance with real data: scrape/aggregate from job posting APIs, BLS data, or use GPT
- Add historical trending data (weekly snapshots stored in DB)
- **Frontend:** Line charts (Recharts) for skill demand over time, rising/declining lists
- Table: NEW `trend_snapshots` in DB
- Files: NEW `frontend/app/dashboard/trends/page.tsx`, modify `backend/api/routes/career.py`, modify `backend/models/database.py`
- **Time:** 3.5 hrs

---

## Phase 5: XAI, Privacy, and Skill Verification (Sprint 5)

> Goal: Trust, transparency, and validation features.  
> **Estimated time: 8-10 hours**

### 5.1 — XAI "Why This?" Explainer (Complete)
- Enhance all recommendation endpoints to include explanatory fields
- Career recommendations already have `reasons[]` — extend to skill gap, projects, scholarships
- Add expandable "Why?" tooltip/drawer on all recommendation cards in frontend
- Files: All recommendation-producing AI modules, corresponding frontend components
- **Time:** 2.5 hrs

### 5.2 — Data Privacy & Ethics Hub
- **Frontend:** `/dashboard/privacy` — shows what data is stored, what AI sees
- Options: download all data (GDPR export), delete account, toggle AI features
- **Backend:** GET `/api/profile/export-data` (JSON dump), DELETE `/api/auth/delete-account`
- Files: NEW `frontend/app/dashboard/privacy/page.tsx`, modify `backend/api/routes/auth.py`, modify `backend/api/routes/profile.py`
- **Time:** 2.5 hrs

### 5.3 — Skill Verification System
- Upload project/certificate as proof of skill
- AI reviews submission and assigns verified badge
- **Backend:** POST `/api/profile/verify-skill` with file upload
- **Frontend:** "Verify" button next to each skill on profile page
- Files: modify `frontend/app/dashboard/profile/page.tsx`, modify `backend/api/routes/profile.py`, modify `backend/models/database.py` (add `verified` column to user_skills)
- **Time:** 3 hrs

### 5.4 — Confidence Scores on All AI Outputs
- Add `confidence: "low" | "medium" | "high"` to all AI response schemas
- Display as colored badges next to recommendations
- Files: modify `backend/models/schemas.py`, all AI modules, all frontend recommendation cards
- **Time:** 2 hrs

---

## Phase 6: Testing, Performance & Deployment (Sprint 6)

> Goal: Production readiness.  
> **Estimated time: 10-12 hours**

### 6.1 — Backend Unit & Integration Tests
- Set up `pytest` + `httpx` for FastAPI testing
- Write tests for: auth flow, profile CRUD, all AI endpoints
- Target: 80%+ route coverage
- Files: NEW `backend/tests/`, NEW `backend/tests/conftest.py`, NEW `backend/tests/test_auth.py`, `test_profile.py`, `test_career.py`
- **Time:** 4 hrs

### 6.2 — Frontend Component Tests
- Set up Vitest + React Testing Library
- Test: Login form, Register form, API client, Dashboard rendering
- Files: NEW `frontend/__tests__/`, update `frontend/package.json`
- **Time:** 2 hrs

### 6.3 — Rate Limiting & Security
- Add `slowapi` rate limiter to FastAPI
- Configure CORS with specific origins (not `*`)
- Add input sanitization to all text fields
- Files: `backend/main.py`, `backend/requirements.txt`
- **Time:** 1.5 hrs

### 6.4 — Environment Configs (Dev/Staging/Prod)
- Separate `.env.development`, `.env.production`
- Add `NEXT_PUBLIC_API_URL` for frontend environment switching
- Files: `backend/.env.example`, `frontend/.env.local`, `frontend/.env.production`
- **Time:** 30 min

### 6.5 — Deployment Setup
- **Backend:** Dockerfile + deploy to Railway/Render
- **Frontend:** Vercel deployment config
- Add health check endpoint (already exists at `/health`)
- Files: NEW `backend/Dockerfile`, NEW `backend/.dockerignore`, NEW `vercel.json`
- **Time:** 2 hrs

### 6.6 — CI/CD Pipeline
- GitHub Actions: lint + test on PR, deploy on merge to main
- Files: NEW `.github/workflows/ci.yml`, NEW `.github/workflows/deploy.yml`
- **Time:** 1.5 hrs

### 6.7 — Error Monitoring
- Integrate Sentry for both frontend and backend
- Files: `backend/main.py`, `frontend/app/layout.tsx`, both `requirements.txt`/`package.json`
- **Time:** 1 hr

---

## Phase 7: Gamification & Engagement (Sprint 7 — Stretch)

> Goal: User stickiness and retention features.  
> **Estimated time: 8-10 hours**  
> **Dependency:** All Phases 1-6 complete.

### 7.1 — XP and Leveling System
- Award XP for: completing profile (+100), adding skills (+20), running skill gap (+50), chatting with counselor (+10)
- Level thresholds: Novice (0), Explorer (200), Strategist (500), Master (1000)
- Backend tracking in `profiles.xp` and `profiles.level` (columns already exist!)
- Trigger XP awards in route handlers, return updated XP in responses
- Files: NEW `backend/utils/gamification.py`, modify all relevant route handlers, modify dashboard to show XP bar
- **Time:** 3 hrs

### 7.2 — Badge System
- Define badge criteria: "First Skill Gap Analysis", "Profile Complete", "5 Projects Added", etc.
- Store in `profiles.badges` (JSON column — already exists!)
- Show badges on profile page and dashboard
- Files: modify `backend/utils/gamification.py`, modify `frontend/app/dashboard/profile/page.tsx`
- **Time:** 2 hrs

### 7.3 — Weekly Skill Challenges
- AI generates weekly mini-challenges based on user's target role
- Track completions, award XP
- Files: NEW `frontend/app/dashboard/challenges/page.tsx`, modify `backend/api/routes/career.py`
- **Time:** 2.5 hrs

### 7.4 — Notification System
- Bell icon in header already exists (non-functional)
- Backend: store notifications table (skill reminders, new challenges, deadline alerts)
- Frontend: dropdown notification panel
- Files: modify `backend/models/database.py`, NEW `backend/api/routes/notifications.py`, modify `frontend/components/header.tsx`
- **Time:** 2.5 hrs

---

## Summary: Effort by Phase

| Phase | Description | Hours | Priority |
|-------|-------------|-------|----------|
| **0** | Critical Blockers | 0.5 | 🔴 Do first |
| **1** | Stabilize & Polish MVP | 8-10 | 🔴 Essential |
| **2** | Core Backend Intelligence | 12-15 | 🔴 Essential |
| **3** | Missing Core Feature Pages | 20-25 | 🟡 High |
| **4** | Complete "Winning" Features | 10-12 | 🟡 High |
| **5** | XAI, Privacy, Verification | 8-10 | 🟡 Medium |
| **6** | Testing & Deployment | 10-12 | 🟢 Medium |
| **7** | Gamification (Stretch) | 8-10 | 🟢 Low |
| | **TOTAL** | **~77-94 hrs** | |

---

## Recommended Execution Order

```
Week 1 (Day 1):      Phase 0 → blockers fixed, both servers running
Week 1 (Days 1-3):   Phase 1 → stable, polished MVP demo-able
Week 1 (Days 3-5):   Phase 2 → real intelligence replacing mocks
Week 2 (Days 1-4):   Phase 3 → all 19 core features have pages
Week 2 (Days 4-5):   Phase 4 → all 7 "winning" features complete
Week 3 (Days 1-2):   Phase 5 → trust & transparency layer
Week 3 (Days 3-5):   Phase 6 → tested & deployed
Week 4 (if time):    Phase 7 → gamification polish
```

---

## Files to Create (New Files Needed)

### Backend (15 new files)
```
backend/ai/esco_client.py
backend/ai/resume_parser.py
backend/ai/github_integration.py
backend/ai/experience_translator.py
backend/ai/learning_pathway.py
backend/api/routes/onboarding.py
backend/api/routes/skills.py
backend/api/routes/notifications.py
backend/utils/logger.py
backend/utils/gamification.py
backend/seed_data.py
backend/alembic.ini
backend/alembic/env.py
backend/Dockerfile
backend/tests/conftest.py  (+ test files)
```

### Frontend (14 new pages + 4 utilities)
```
frontend/lib/auth-context.tsx
frontend/lib/theme-context.tsx
frontend/components/ui/skeleton.tsx
frontend/components/error-boundary.tsx
frontend/app/onboarding/page.tsx
frontend/app/dashboard/career-map/page.tsx
frontend/app/dashboard/career-compare/page.tsx
frontend/app/dashboard/mock-interview/page.tsx
frontend/app/dashboard/learning-path/page.tsx
frontend/app/dashboard/coursework/page.tsx
frontend/app/dashboard/internships/page.tsx
frontend/app/dashboard/future-self/page.tsx
frontend/app/dashboard/pivot/page.tsx
frontend/app/dashboard/soft-skills/page.tsx
frontend/app/dashboard/experience-translator/page.tsx
frontend/app/dashboard/trends/page.tsx
frontend/app/dashboard/privacy/page.tsx
frontend/app/dashboard/challenges/page.tsx
```

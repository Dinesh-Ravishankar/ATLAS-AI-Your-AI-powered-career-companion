# 🚀 Atlas AI — Demo Guide

## Quick Start (One Command)

### Option A: Double-click
> Double-click **`start.bat`** in the project root.

### Option B: PowerShell
```powershell
cd D:\Atlas-AI
.\start.ps1
```

### Option C: Manual
```powershell
# Terminal 1 — Backend
cd D:\Atlas-AI\backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 — Frontend
cd D:\Atlas-AI\frontend
npm run dev
```

Both servers will start and the browser opens automatically.

| Service  | URL |
|----------|-----|
| Frontend | http://localhost:3000 |
| Backend  | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 🎯 Demo Walkthrough (5 Minutes)

### Step 1 — Register & Login (30 sec)
1. Open **http://localhost:3000**
2. Click **Register** → enter name, email, password → Submit
3. You're now on the Dashboard

### Step 2 — Set Up Profile / Atlas Card (1 min)
1. Sidebar → **Atlas Card**
2. Fill in: **Full Name**, Major, University, GPA, Target Roles
3. Add **Skills** (e.g. Python, JavaScript, React, SQL)
4. Click **Save Profile**

### Step 3 — Skill Gap Analysis (30 sec)
1. Sidebar → **Skill Gap**
2. Select a target role (e.g. *Software Engineer*)
3. Click **Analyze Skill Gap**
4. View radar chart + missing skills with priority badges

### Step 4 — Career Compare (30 sec)
1. Sidebar → **Career Compare**
2. Enter 2-3 careers (e.g. *Frontend*, *Backend*, *Data Scientist*)
3. Click **Compare Careers**
4. See side-by-side cards with salary, skill match %, pros/cons

### Step 5 — Learning Path (30 sec)
1. Sidebar → **Learning Path**
2. Enter target role + weekly hours
3. Click **Generate Path**
4. View step-by-step learning roadmap with resources

### Step 6 — Mock Interview (30 sec)
1. Sidebar → **Mock Interview**
2. Select role, difficulty, question count
3. Click **Generate Questions**
4. Review questions with tips and sample answers

### Step 7 — Side Hustle Incubator (30 sec)
1. Sidebar → **Side Hustle**
2. Click **Get Ideas**
3. Browse 5 side hustle ideas with income estimates & steps

### Step 8 — Scholarships (30 sec)
1. Sidebar → **Scholarships**
2. Click **Find Scholarships**
3. Browse scholarship cards with amounts, deadlines, and links

---

## 📋 All 17 Features

| # | Feature | Sidebar Link | What It Does |
|---|---------|-------------|--------------|
| 1 | **Dashboard** | Dashboard | Overview with stats and quick actions |
| 2 | **Atlas Card** | Atlas Card | Your digital profile — skills, goals, education |
| 3 | **Career Quiz** | Career Quiz | Discover careers matching your personality |
| 4 | **Skill Gap** | Skill Gap | Radar chart comparing your skills vs. role requirements |
| 5 | **Career Map** | Career Map | Visual graph of career paths and growth trajectories |
| 6 | **Career Compare** | Career Compare | Side-by-side comparison of 2-3 career paths |
| 7 | **Learning Path** | Learning Path | Personalized roadmap with courses and milestones |
| 8 | **Mock Interview** | Mock Interview | AI-generated interview questions with tips |
| 9 | **Projects** | Projects | Recommended portfolio projects for your target role |
| 10 | **Side Hustle** | Side Hustle | Income ideas based on your skills |
| 11 | **Scholarships** | Scholarships | Financial aid finder with deadlines and amounts |
| 12 | **Soft Skills** | Soft Skills | Role-play scenarios for communication practice |
| 13 | **Trends** | Trends | Trending skills in the job market |
| 14 | **Experience Translator** | Experience Translator | Convert non-tech experience into tech skills |
| 15 | **GitHub Import** | GitHub Import | Pull skills from your GitHub profile |
| 16 | **Verify Job** | Verify Job | Ghost job / scam detector |
| 17 | **Privacy** | Privacy | Privacy settings and data controls |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind v4 |
| Backend | FastAPI, Python 3.11, SQLAlchemy |
| AI | OpenAI GPT-4o-mini, LangChain (with full offline fallbacks) |
| Database | Supabase PostgreSQL |
| Auth | JWT + bcrypt |

---

## ⚠ Troubleshooting

| Problem | Fix |
|---------|-----|
| Port 8000 in use | `Get-Process -Name python \| Stop-Process -Force` |
| Port 3000 in use | `npx kill-port 3000` |
| Backend import error | Make sure you `cd backend` before running uvicorn |
| npm not found | Install Node.js from https://nodejs.org |
| Python not found | Adjust path in `start.ps1` or install via `uv` |

# ATLAS AI Backend

FastAPI backend for the ATLAS AI career guidance platform.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your database credentials and API keys
```

3. **Run database migrations:**
```bash
# The database tables will be created automatically on first run
```

4. **Start the server:**
```bash
python main.py
# Or use uvicorn directly:
uvicorn main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py               # Database and settings configuration
├── requirements.txt        # Python dependencies
├── models/
│   ├── database.py        # SQLAlchemy models
│   └── schemas.py         # Pydantic schemas
├── auth/
│   └── jwt_handler.py     # Authentication utilities
├── api/
│   └── routes/
│       ├── auth.py        # Authentication endpoints
│       ├── profile.py     # Profile management
│       └── career.py      # Career guidance features
├── ai/
│   ├── skill_gap_analyzer.py    # Skill gap analysis
│   └── career_recommender.py    # Career recommendations
├── knowledge/
│   ├── esco_client.py     # ESCO API integration
│   └── onet_client.py     # O*NET API integration
└── utils/
    └── helpers.py         # Utility functions
```

## Core Features Implemented

### ✅ Authentication
- User registration
- JWT-based login
- Protected routes

### ✅ Profile Management (Atlas Card)
- Create/update user profile
- Add/remove skills with proficiency levels
- Manage projects
- Education and experience tracking

### ✅ Career Guidance
- **Skill Gap Analysis**: Compare user skills against target roles
- **Career Recommendations**: AI-powered career path suggestions
- **Trending Skills**: Market intelligence on skill demand

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Profile
- `GET /profile/` - Get user profile
- `PUT /profile/` - Update profile
- `POST /profile/skills` - Add skill
- `GET /profile/skills` - Get all user skills
- `DELETE /profile/skills/{id}` - Remove skill
- `POST /profile/projects` - Add project
- `GET /profile/projects` - Get all projects

### Career Guidance
- `POST /career/skill-gap` - Analyze skill gap for target role
- `GET /career/recommendations` - Get personalized career recommendations
- `GET /career/trending-skills` - Get trending skills data

## Database Schema

### Users
- Email, password (hashed)
- Full name
- Timestamps

### Profiles (Atlas Card)
- Bio, location, contact info
- Education (JSON array)
- Academic info (GPA, major, university)
- Career targets and interests
- Gamification (level, XP, badges)

### Skills
- Name, category
- ESCO URI (for ontology linking)
- Many-to-many with Users (includes proficiency)

### Projects
- Title, description
- GitHub/live URLs
- Tech stack
- Featured flag

### Careers (Reference Data)
- Title, description
- Required skills
- Salary, growth rate
- ESCO/O*NET codes

## Next Steps

1. **Connect Real APIs:**
   - Integrate ESCO API for skill taxonomy
   - Integrate O*NET API for career data
   - Connect to job market APIs

2. **Add More Features:**
   - Resume parser
   - GitHub integration
   - Scholarship finder
   - Chatbot with RAG

3. **Production Setup:**
   - Configure production database
   - Set up proper secret management
   - Add rate limiting
   - Implement caching (Redis)

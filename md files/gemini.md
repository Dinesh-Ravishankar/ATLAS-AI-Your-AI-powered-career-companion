# Project Constitution

## Data Schemas
### Atlas Card (Unified Portfolio Profile)
```json
{
  "profile_id": "string",
  "basics": {
    "name": "string",
    "contact": {
      "email": "string",
      "linkedin": "url",
      "github": "url"
    },
    "summary": "string"
  },
  "academic": [
    {
      "institution": "string",
      "degree": "string",
      "status": "completed|current",
      "courses": [
        {
          "name": "string",
          "grade": "string",
          "relevance": "string (mapped to skills)"
        }
      ]
    }
  ],
  "skills": {
    "hard": [{"name": "string", "proficiency": "0-1", "source": "ESCO|GitHub|Self"}],
    "soft": [{"name": "string", "proficiency": "0-1"}]
  },
  "projects": [
    {
      "title": "string",
      "repository": "url",
      "tech_stack": ["string"],
      "deliverable": "url",
      "ai_analysis": "string (extracted contribution)"
    }
  ],
  "career_path": {
    "target_roles": ["string"],
    "preferences": ["string"],
    "gap_analysis": {
      "missing_skills": ["string"],
      "recommended_actions": ["string"]
    }
  },
  "gamification": {
    "level": "integer",
    "badges": ["string"]
  }
}
```

## Behavioral Rules
1. **Privacy First:** Never store PII (Personally Identifiable Information) in plain text logs. Encrypt or anonymize Atlas Card data at rest.
2. **Explainability:** Every career recommendation MUST be accompanied by a "Why this?" factor.
3. **Proactive Guidance:** If a student's grades in a core subject (e.g., Math) drop, the system should flag it as a risk to related career goals (e.g., Data Science).
4. **Ethical AI:** Recommendations must avoid gender or ethnic bias by focusing on performance and expressed interest.
5. **No Guessing:** If the system cannot find a high-confidence match for a role, it must state "Insufficient Data" and ask for more information.

## Architectural Invariants
- **Layer 1: UI Layer** (Interactive Web + Chatbot)
- **Layer 2: Orchestration** (Decision routing & User context)
- **Layer 3: AI Intelligence** (ML Models & Reasoning)
- **Layer 4: Career Knowledge** (ESCO/O*NET Knowledge Graph)
- **Layer 5: Data/Profile** (Atlas Card Persistence)
- **Data-First Rule:** Coding only begins once the "Payload" shape is confirmed.
- **Self-Annealing:** Analyze -> Patch -> Test -> Update Architecture.
- **Protocol:** B.L.A.S.T. (Blueprint, Link, Architect, Stylize, Trigger)

# Atlas AI - System Architecture Diagrams

## 1. High-Level System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Web Browser]
        Mobile[Mobile Browser]
    end
    
    subgraph "Frontend Layer - Vite + React"
        UI[React UI Components]
        State[State Management]
        Router[React Router]
        UI --> State
        State --> Router
    end
    
    subgraph "Backend Layer - FastAPI"
        API[FastAPI Server]
        Auth[Auth Middleware]
        Routes[API Routes]
        
        API --> Auth
        Auth --> Routes
        
        subgraph "AI Intelligence Layer"
            Orchestrator[LangChain Orchestrator]
            LLM[GPT-4o / Llama-3]
            Tools[AI Tools]
            
            Routes --> Orchestrator
            Orchestrator --> LLM
            Orchestrator --> Tools
        end
    end
    
    subgraph "Data Layer - Supabase"
        SupaAuth[Supabase Auth]
        PostgresDB[(PostgreSQL)]
        PGVector[(pgvector)]
        Storage[File Storage]
        
        PostgresDB --> PGVector
    end
    
    subgraph "External Services"
        ESCO[ESCO API]
        JobBoards[Job Boards APIs]
        GitHub[GitHub API]
        LinkedIn[LinkedIn API]
    end
    
    Browser --> UI
    Mobile --> UI
    UI <-->|REST API| API
    UI <-->|Auth & Data| SupaAuth
    
    Routes --> PostgresDB
    Routes --> PGVector
    Routes --> Storage
    
    Tools --> ESCO
    Tools --> JobBoards
    Tools --> GitHub
    Tools --> LinkedIn
    
    style UI fill:#3b82f6
    style API fill:#8b5cf6
    style PostgresDB fill:#10b981
    style LLM fill:#f59e0b
```

## 2. Detailed Component Architecture

```mermaid
graph LR
    subgraph "Frontend Components"
        Landing[Landing Page]
        Dashboard[Dashboard]
        AtlasCard[Atlas Card View]
        ChatUI[Clarity Coach Chat]
        SkillGap[Skill Gap Visualizer]
        
        Landing --> Dashboard
        Dashboard --> AtlasCard
        Dashboard --> ChatUI
        Dashboard --> SkillGap
    end
    
    subgraph "UI Component Library"
        Shadcn[Shadcn/UI]
        Tailwind[Tailwind CSS]
        Framer[Framer Motion]
        Lucide[Lucide Icons]
    end
    
    subgraph "Backend Services"
        UserService[User Service]
        ProfileService[Profile Service]
        CareerService[Career Service]
        SkillService[Skill Intelligence]
        ChatService[Chat Service]
    end
    
    AtlasCard --> ProfileService
    ChatUI --> ChatService
    SkillGap --> SkillService
    
    Landing -.uses.-> Shadcn
    Dashboard -.uses.-> Tailwind
    ChatUI -.uses.-> Framer
    
    style AtlasCard fill:#06b6d4
    style ChatUI fill:#8b5cf6
    style SkillGap fill:#10b981
```

## 3. Data Flow Architecture

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant FastAPI
    participant LangChain
    participant LLM
    participant Supabase
    
    User->>Frontend: Open Atlas Card
    Frontend->>Supabase: Authenticate User
    Supabase-->>Frontend: Auth Token
    
    Frontend->>FastAPI: GET /profile
    FastAPI->>Supabase: Query User Profile
    Supabase-->>FastAPI: Profile Data (JSONB)
    FastAPI-->>Frontend: Atlas Card JSON
    
    User->>Frontend: Ask Clarity Coach
    Frontend->>FastAPI: POST /chat
    FastAPI->>LangChain: Process Query
    LangChain->>Supabase: Fetch Context
    LangChain->>LLM: Generate Response
    LLM-->>LangChain: AI Response
    LangChain->>Supabase: Store Conversation
    LangChain-->>FastAPI: Response + Actions
    FastAPI-->>Frontend: Chat Message
    Frontend-->>User: Display Response
```

## 4. AI Intelligence Layer

```mermaid
graph TD
    subgraph "Clarity Coach (AI Counselor)"
        ChatInput[User Query]
        Intent[Intent Classification]
        Context[Context Retrieval]
        Memory[Long-term Memory]
        Response[Response Generation]
        
        ChatInput --> Intent
        Intent --> Context
        Context --> Memory
        Memory --> Response
    end
    
    subgraph "Skill Intelligence Engine"
        UserSkills[User Skills]
        TargetRole[Target Role]
        ESCO_API[ESCO Ontology]
        Embeddings[Skill Embeddings]
        GapAnalysis[Gap Analysis]
        
        UserSkills --> Embeddings
        TargetRole --> ESCO_API
        Embeddings --> GapAnalysis
        ESCO_API --> GapAnalysis
    end
    
    subgraph "Experience Translator"
        RawExp[Raw Experience]
        NLP[NLP Extraction]
        SkillMap[Skill Mapping]
        Resume[Resume Bullets]
        
        RawExp --> NLP
        NLP --> SkillMap
        SkillMap --> Resume
    end
    
    subgraph "LLM Core"
        GPT4[GPT-4o]
        Llama[Llama-3]
        
        Response --> GPT4
        Resume --> GPT4
        GapAnalysis -.fallback.-> Llama
    end
    
    style ChatInput fill:#3b82f6
    style GapAnalysis fill:#10b981
    style Resume fill:#f59e0b
```

## 5. Database Schema (Supabase PostgreSQL)

```mermaid
erDiagram
    USERS ||--o{ ATLAS_CARDS : has
    USERS ||--o{ CONVERSATIONS : has
    USERS ||--o{ SKILL_ASSESSMENTS : takes
    
    ATLAS_CARDS ||--o{ PROJECTS : contains
    ATLAS_CARDS ||--o{ EXPERIENCES : contains
    ATLAS_CARDS ||--o{ SKILLS : contains
    
    CONVERSATIONS ||--o{ MESSAGES : contains
    
    USERS {
        uuid id PK
        string email
        string name
        timestamp created_at
        jsonb preferences
    }
    
    ATLAS_CARDS {
        uuid id PK
        uuid user_id FK
        jsonb profile_data
        jsonb skills
        jsonb experiences
        jsonb projects
        timestamp updated_at
    }
    
    CONVERSATIONS {
        uuid id PK
        uuid user_id FK
        string title
        timestamp created_at
    }
    
    MESSAGES {
        uuid id PK
        uuid conversation_id FK
        string role
        text content
        jsonb metadata
        timestamp created_at
    }
    
    SKILLS {
        uuid id PK
        uuid atlas_card_id FK
        string skill_name
        string proficiency
        vector embedding
    }
    
    PROJECTS {
        uuid id PK
        uuid atlas_card_id FK
        string title
        text description
        string github_url
        jsonb technologies
    }
```

## 6. Authentication Flow

```mermaid
graph TD
    Start[User Visits Platform]
    
    Start --> CheckAuth{Authenticated?}
    
    CheckAuth -->|No| LoginPage[Login/Signup Page]
    CheckAuth -->|Yes| Dashboard[Dashboard]
    
    LoginPage --> AuthMethod{Auth Method}
    
    AuthMethod -->|Email/Password| EmailAuth[Supabase Email Auth]
    AuthMethod -->|Google| GoogleAuth[Google OAuth]
    AuthMethod -->|GitHub| GitHubAuth[GitHub OAuth]
    
    EmailAuth --> SupabaseAuth[Supabase Auth Service]
    GoogleAuth --> SupabaseAuth
    GitHubAuth --> SupabaseAuth
    
    SupabaseAuth --> CreateSession[Create Session]
    CreateSession --> StoreToken[Store JWT Token]
    StoreToken --> Dashboard
    
    Dashboard --> ProtectedRoutes[Protected Routes]
    ProtectedRoutes --> ValidateToken{Token Valid?}
    
    ValidateToken -->|Yes| AllowAccess[Allow Access]
    ValidateToken -->|No| LoginPage
    
    style SupabaseAuth fill:#10b981
    style Dashboard fill:#3b82f6
```

## 7. Deployment Architecture

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Frontend Hosting"
            Vercel[Vercel / Netlify]
            CDN[Global CDN]
            
            Vercel --> CDN
        end
        
        subgraph "Backend Hosting"
            Railway[Railway / Render]
            FastAPIApp[FastAPI Container]
            
            Railway --> FastAPIApp
        end
        
        subgraph "Database & Auth"
            SupabaseProd[Supabase Cloud]
            PostgresProd[(Production DB)]
            VectorProd[(Vector Store)]
            
            SupabaseProd --> PostgresProd
            SupabaseProd --> VectorProd
        end
        
        subgraph "AI Services"
            OpenAI[OpenAI API]
            Ollama[Ollama (Self-hosted)]
        end
    end
    
    Users[End Users] --> CDN
    CDN --> Vercel
    Vercel <-->|API Calls| FastAPIApp
    FastAPIApp <--> SupabaseProd
    FastAPIApp --> OpenAI
    FastAPIApp -.fallback.-> Ollama
    
    style Vercel fill:#3b82f6
    style Railway fill:#8b5cf6
    style SupabaseProd fill:#10b981
```

## 8. Feature Implementation Layers

```mermaid
graph TB
    subgraph "Layer 1: Core Platform"
        L1A[User Authentication]
        L1B[Atlas Card Profile]
        L1C[Data Privacy]
    end
    
    subgraph "Layer 2: Career Intelligence"
        L2A[Career Recommendation]
        L2B[Skill Gap Analysis]
        L2C[Learning Pathways]
    end
    
    subgraph "Layer 3: AI Features"
        L3A[Clarity Coach]
        L3B[Experience Translator]
        L3C[Resume Builder]
    end
    
    subgraph "Layer 4: Advanced Features"
        L4A[Soft Skills Bootcamp]
        L4B[Ghost Job Detector]
        L4C[Mental Health Pacing]
    end
    
    subgraph "Layer 5: Marketplace"
        L5A[Micro-Internships]
        L5B[Side Hustle Incubator]
        L5C[Mentorship Matching]
    end
    
    L1A --> L2A
    L1B --> L2B
    L1C --> L2C
    
    L2A --> L3A
    L2B --> L3B
    L2C --> L3C
    
    L3A --> L4A
    L3B --> L4B
    L3C --> L4C
    
    L4A --> L5A
    L4B --> L5B
    L4C --> L5C
    
    style L1A fill:#3b82f6
    style L2A fill:#8b5cf6
    style L3A fill:#10b981
    style L4A fill:#f59e0b
    style L5A fill:#ef4444
```

---

## Usage Notes

1. **Copy any diagram** and paste it into:
   - [Mermaid Live Editor](https://mermaid.live/)
   - GitHub Markdown (renders automatically)
   - NotebookLM or Obsidian (with Mermaid plugin)

2. **For Presentations**: Export diagrams as PNG/SVG from Mermaid Live Editor.

3. **Color Legend**:
   - Blue (#3b82f6): Frontend/UI
   - Purple (#8b5cf6): Backend/API
   - Green (#10b981): Database/Data
   - Orange (#f59e0b): AI/ML Components
   - Red (#ef4444): External/Advanced Features

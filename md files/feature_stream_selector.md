# Feature: "The Origin Story" – Intelligent Stream & Major Selector
**Target Audience:** High School Graduates (Pre-College)  
**Problem:** Paralysis by analysis. Students are overwhelmed by choices (Engineering vs. Arts vs. Medical) and lack insight into what those choices actually entail in the real world.

---

## 1. Brainstorming & Concept

### The Core Philosophy: "Reverse Engineering the Future"
Instead of asking "What do you want to study?", we ask "What problems do you want to solve?" and "What is your working style?", then map it backward to the right Stream/Department.

### Key Innovative Components:
1.  **The "Anti-Choice" Filter**:
    *   It's easier for teenagers to define what they *hate* than what they love.
    *   *Mechanism:* "Do you hate looking at blood?" (Filters out Medicine). "Do you hate sitting alone for hours?" (Filters out Research/backend coding).
2.  **The "Ikigai" Engine**:
    *   Overlaps 4 data points:
        *   **Academics:** Strong subjects (Physics = Mech/Civil).
        *   **Interests:** Hobbies (Gaming = CS/Game Design).
        *   **Market Reality:** Job trends (AI is booming).
        *   **Lifestyle:** Salary expectations vs. Work-life balance.
3.  **"Day in the Life" Simulations**:
    *   Don't just say "Mechanical Engineering". Show a 60-second video or interactive text scenario of a Mechanical Engineer on a shop floor.
4.  **The "Reality Check" (Honest AI)**:
    *   *Scenario:* Student wants CS but hates Math.
    *   *AI Response:* "CS requires Logic and Discrete Math. Your Math score is low. To succeed, you will need to put in 2x effort here. Are you ready?"

---

## 2. Implementation Plan

### Phase 1: Data Ingestion (The Gamified Onboarding)
*   **Format:** Chatbot conversational style (not a boring form).
*   **Inputs:**
    *   **Grade 10/12 Marks:** PDF Upload (OCR extracts subject strengths).
    *   **Interest Tags:** #Robots, #Writing, #Money, #Outdoors.
    *   **Constraint Inputs:** Budget, Location preferences.
    *   **Psychometric Mini-Game:** 5-question visual quiz to determine "Builder" vs. "Thinker" vs. "Communicator".

### Phase 2: The Matching Engine (The Logic)
We use a **Weighted Scoring Algorithm** combined with LLM reasoning.

**Entity Mapping (Simplified Example):**
*   *Stream:* **Computer Science**
    *   *Required Tags:* Logic, Math, Sitting, Problem Solving.
    *   *Anti-Tags:* Outdoors, Physical Labor.
    *   *Weight:* Math (0.4), Physics (0.2), Logic (0.4).

**Algorithm:**
1.  Extract User Profile Vector (Marks + Interests).
2.  Compute Cosine Similarity against Stream Vectors.
3.  Filter by "Anti-Tags" (Hard exclusions).
4.  Rank top 3 recommendations.

### Phase 3: The Presentation (The "Reveal")
Display results as "Career Cards" with 3 tabs:
1.  **The Pitch:** "Why this fits you." (e.g., "You love Physics and solving tactile problems -> Mechanical Engineering").
2.  **The ROI:** "Avg Starting Salary: $X. Job Growth: Y%."
3.  **The Roadmap:** "If you pick this: Year 1 (Basics) -> Year 2 (Thermodynamics) -> Job (Tesla Design Engineer)."

### Phase 4: Actionable Next Steps
*   **University Mapper:** "Here are the top colleges for [Selected Stream] based on your marks."
*   **Bridge Course:** "You picked CS, but you didn't do coding in high school. Here is a 'Intro to Python' module to start *before* college."

---

## 3. Technical Architecture

### Frontend (User Interface)
*   **Interactive Chat Interface:** (React/Next.js + Framer Motion) for the onboarding.
*   **Vis.js / D3.js:** For the "Skill Tree" visualization of where a major leads.

### Backend (Logic Layer)
*   **FastAPI Endpoint:** `/api/recommend/stream`
*   **LLM (GPT-4o/Llama-3):** To generate the "Why" explanation and "Reality Check" text.
*   **Vector Database (Supabase pgvector):** Storing Stream profiles to match against User embeddings.

### Data Requirements
*   **Stream Metadata:** Detailed JSON for each major (CS, EEE, Mech, BioTech, Arts, Commerce). Including: *Subjects, Career Outcomes, Salary range, Drop-out rates, Difficulty level.*

---

## 4. Development Roadmap (Sprint Plan)

*   **Sprint 1:** Define JSON schema for "Stream" and "User Profile". Create the "Anti-Choice" logic.
*   **Sprint 2:** Build the Chatbot Onboarding Flow (Frontend).
*   **Sprint 3:** Implement the Matching Algorithm (Backend).
*   **Sprint 4:** Generate the "Report Card" UI (The Reveal).
*   **Sprint 5:** Integrate University Mapper (Hard-coded list -> API).

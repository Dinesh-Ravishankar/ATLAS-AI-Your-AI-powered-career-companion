# Research Log: AI & ML-Based Career Guidance Platform

## Project Context
**Date:** 2026-02-09
**Status:** In Progress
**Overview:**  
An AI-powered, end-to-end career guidance platform designed to support students (pre-college & college) throughout their academic journey. It acts as a personalized career companion integrating AI/ML for continuous, adaptive, and explainable guidance.

### 1. Problem Statement
- **Core Issue:** Students lack clarity on career paths, skills, and industry expectations despite enrolling in higher education.
- **Current State:** Decisions rely on limited info, peer influence, or late-stage placement guidance.
- **Failures of Traditional Systems:** Manual, generic, reactive, and fragmented (silos of jobs, courses, assessments).
- **Need:** Scalable, intelligent, adaptive system bridging the gap between education and employability.

### 2. Existing System Analysis
- **Institutional Cells:** Low scalability, manual, late-stage.
- **Software Platforms:** Isolated features (jobs vs. courses), lack holistic integration.
- **Job Portals:** Assume prior clarity, don't guide undecided students.
- **Assessments:** Static, one-time, non-adaptive.
- **Informal Sources:** Unstructured, biased.

### 3. Proposed System Features
1.  **Intelligent Student Profiling:** Dynamic profiles updated via academic data, assessments, interactions.
2.  **AI Career Exploration:** ML-based recommendations ranked by suitability/feasibility.
3.  **Skill Mapping & Gap Analysis:** Identifies required skills vs. current skills; prioritizes gaps.
4.  **Academic Alignment:** Maps coursework/electives to career goals.
5.  **Experience Guidance:** Internships/projects readiness and recommendations.
6.  **Job Readiness:** Resume feedback, interview prep, job suitability.
7.  **Decision Support:** Trade-off analysis, career pivot simulation.
8.  **Feedback & Explainability:** Continuous improvement loop + XAI transparency.
9.  **Ethical Design:** Privacy, bias awareness, human-in-the-loop.

---

## Research Findings

### 1. Student Profiling & Data Modeling
To build dynamic, intelligent profiles, the system must ingest various data points (grades, interests, psychometrics).
*   **Key Data Standards:** IMS Learner Information Services (LIS) and HR-XML can standardize profile data.
*   **AI Models for Profiling:**
    *   **Classification Models (SVM, Random Forest):** Effective for categorizing students into "career archetypes" based on academic performance and interests.
    *   **Clustering (K-Means, KNN):** Useful for finding "similar students" to predict successful paths taken by peers with similar profiles.
    *   **Predictive Analytics:** Regression models to forecast academic performance and identifying "at-risk" phases where intervention is needed.

### 2. Career Recommendation Algorithms
The core engine requires a hybrid approach to balance accuracy and novelty.
*   **Content-Based Filtering:** Matches student attributes (skills, grades) directly to job requirements. Good for specific, hard-skill matching.
*   **Collaborative Filtering:** "Students like you also became Data Scientists." Good for discovering non-obvious paths but suffers from the "cold start" problem for new users.
*   **Hybrid Engineers:** The industry standard. Combines both above methods.
*   **Advanced Models:**
    *   **XGBoost:** Highly effective for structured data classification (e.g., "Probability of success in Career X").
    *   **Knowledge Graphs:** Mapping Students -> Skills -> Jobs allow for reasoning (e.g., "You have Skill A, which is a prerequisite for Job B").

### 3. Skill Ontologies & Gap Analysis
"Gap Analysis" requires a standardized vocabulary for skills.
*   **Open Standard Ontologies:**
    *   **ESCO (European Skills, Competences, Qualifications and Occupations):** High-quality, multilingual, open-source. Maps 13,500+ skills. Strongly recommended for its structured relationships (e.g., "Java is related to Programming").
    *   **O*NET (Occupational Information Network):** US-based, very detailed for job descriptions and "worker requirements."
*   **APIs for Extraction & Matching:**
    *   **Google Cloud Talent Solution:** Advanced "Job Search" and "Profile Search" APIs that handle vague queries and skill synonyms effectively.
    *   **Textkernel / RChilli:** Specialized in parsing resumes and job descriptions to extract structured data.
    *   **Open Source NLP:** Using BERT-based models (e.g., `SkillNER`) to extract skills from raw text (course descriptions, resumes) to map them to the ESCO ontology.

### 4. Explainable AI (XAI) for Trust
Students need to know *why* a career is recommended to trust the system.
*   **Post-Hoc Explanations (LIME / SHAP):** Can answer "Why was I recommended 'Data Science'?" by highlighting key factors (e.g., "Because your Math grades are high and you passed a Python course").
*   **Knowledge Graph Paths:** Visually intuitive. "You are here (Student) -> Connected to (Skill: Analysis) -> Connected to (Career: Analyst)."
*   **Counterfactuals:** "If you improve your 'Public Speaking' skill, your match score for 'Management' would increase by 15%."

### 5. Implementation Roadmap Recommendation
Based on research, a feasible implementation path is:
1.  **Data Layer:** Adopt **ESCO** as the central skill taxonomy.
2.  **Profiling:** Start with a structured input form + Resume Parser (using NLP) to build the initial profile.
3.  **Recommendation V1:** A **Rule-Based + Content-Processing** system. Match Student Skills to ESCO Job Skills.
4.  **Recommendation V2:** Collect user interaction data to train a **Collaborative Filtering** model.
5.  **Gap Analysis:** Simple set difference: `Job_Required_Skills - Student_Current_Skills`.

---

## Future Research Topics
### Topic E: Professional Network & Portfolio Integration
- **Question:** How to leverage the GitHub API for activity heatmaps and contribution analysis to verify "proof of work"?
- **Question:** What are the constraints for LinkedIn profile data extraction for academic use?

### Topic F: Dynamic Portfolio Generation
- **Question:** What are the best libraries/frameworks for generating high-fidelity web portfolios and PDF resumes from JSON profiles? (e.g., Puppeteer for PDF, React-based templates)

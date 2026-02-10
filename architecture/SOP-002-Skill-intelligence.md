# SOP-002: Skill Intelligence & Gap Analysis

## Purpose
Automate the identification of skill discrepancies between a user's Atlas Card and a target career role using ESCO/O*NET ontologies.

## Inputs
- **User Skills:** List of strings from Atlas Card.
- **Target Role:** Desired occupation string.

## Logic Flow
1. **Ontology Retrieval:**
   - Query ESCO API for "Essential Skills" and "Optional Skills" associated with the Target Role.
2. **Normalization:**
   - Use NLP (BERT/Sentence Transformers) to map User Skills to ESCO skill nodes to handle synonyms.
3. **Set Difference:**
   - `Missing_Skills = Required_ESCO_Skills - Normalized_User_Skills`.
4. **Prioritization:**
   - Rank missing skills based on "Essential" status vs "Optional".
5. **Recommendation:**
   - Map missing skills to learning resources (Phase 4).

## Success Metrics
- **Accuracy:** Match rate between extracted user skills and ontology.
- **Actionability:** Percentage of missing skills that have a direct learning roadmap.

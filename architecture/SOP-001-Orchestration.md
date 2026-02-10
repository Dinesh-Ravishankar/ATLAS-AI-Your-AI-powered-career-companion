# SOP-001: Orchestration Layer Logic

## Purpose
The Orchestration Layer acts as the "Navigation" layer of the system. It receives user input, maintains context from the Atlas Card, and routes tasks to the appropriate Intelligence or Tool modules.

## Inputs
- **User Message:** Natural language string.
- **Atlas Card (JSON):** The current state of the user's profile.
- **Session Context:** History of the current conversation.

## Logic Flow
1. **Intent Extraction:** Determine the user's goal (e.g., "Analyze skill gap", "Find internships", "Update profile").
2. **Context Enrichment:** Fetch relevant sections of the Atlas Card (e.g., if analyzing gaps, fetch target roles and current skills).
3. **Execution Routing:**
   - If profile update -> Route to `.tools/profile_manager.py`
   - If career exploration -> Route to Layer 4 (Career Knowledge) via Intelligence modules.
   - If job readiness -> Route to Mock Interview or Resume tools.
4. **Response Synthesis:** Combine tool outputs with conversational tone defined in `gemini.md`.

## Edge Cases
- **Incomplete Profile:** If the required data is missing in Atlas Card, the Orchestrator must prompt the user to provide it before proceeding.
- **Ambiguous Intent:** Ask clarifying questions before calling expensive APIs.

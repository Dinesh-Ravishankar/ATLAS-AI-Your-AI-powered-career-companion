# ATLAS AI - 13-Hour Accelerated Sprint Plan

This plan is optimized for a **13-hour sprint** to deliver a functional MVP of the entire ATLAS AI platform.

**Strategy:**
- **Stub Everything First**: Build UI skeletons before connecting backend.
- **Mock ML Intelligence**: Use hardcoded/simulated AI responses initially, then connect to real APIs if time permits.
- **Focus on Flow**: User must be able to click through the entire specific journey.
- **Prioritize "Visuals"**: High-fidelity UI for demo purposes (Chart.js, beautiful forms).

---

## 🕒 Hour-by-Hour Breakdown

### **Phase 1: Foundation Setup (Hours 0-2)**
- **Hour 0-1: Project Skeleton & Config**
  - Initialize Next.js (Frontend) + FastAPI (Backend).
  - Setup PostgreSQL (Supabase) + Database Schema (Users, Profiles, Skills).
  - Configure basic Authentication (Clerk/Auth0/Supabase Auth).
- **Hour 1-2: Core Navigation & Layout**
  - Build responsive Navbar, Sidebar, Footer.
  - Implement basic "Dashboard" layout structure.
  - Setup Theme (Tailwind CSS/Chakra UI/Mantine).

### **Phase 2: Core Profile & Data Entry (Hours 2-4)**
- **Hour 2-3: The "Atlas Card" (Profile)**
  - Build editable Profile Form (Personal Info, Education, Experience).
  - Implement Skill Input (Tags + Proficiency Sliders).
  - Simple "Resume Export" button (generates basic PDF).
- **Hour 3-4: Dashboard Widgets**
  - Implement "Skill Gap" placeholder widget.
  - Implement "Recommended Careers" placeholder list.
  - Implement "Progress Tracker" chart (using Chart.js/Recharts with dummy data).

### **Phase 3: The "Winning" Features (Hours 4-7)**
- **Hour 4-5: Career Path Chooser (Mocked Logic)**
  - Simple "Quiz" interface (5 questions on interests).
  - Hardcoded recommendation logic (if 'tech' -> suggest 'Software Engineer').
  - Display career cards with salary/growth stats (static data).
- **Hour 5-6: Skill Gap Analysis (Visuals)**
  - Interactive Radar Chart (User Skills vs. Target Role).
  - List of "Missing Skills" with direct links to mock courses.
- **Hour 6-7: Chatbot Interface (Skeleton)**
  - Floating Chat Widget (UI only).
  - Basic rule-based responses ("Hello", "Show me jobs").
  - Connect to simple LLM API endpoint (optional, else stub response).

### **Phase 4: Advanced Features - Rapid Prototyping (Hours 7-10)**
- **Hour 7-8: Job & Market Tools**
  - **Ghost Job Detector:** UI showing a "Trust Score" on job cards.
  - **Industry Trend Radar:** Line chart showing "Trending Skills" (fake data for demo).
- **Hour 8-9: Student Success Tools**
  - **Soft Skills Bootcamp:** A single "Role Play" scenario screen (text-based).
  - **Financial Aid Finder:** A searchable list/table of scholarships.
- **Hour 9-10: Networking & Social**
  - **Mentor Marketplace:** Grid of mentor profile cards.
  - **Study Groups:** Simple list of active groups to "join".

### **Phase 5: Polish & Integration (Hours 10-13)**
- **Hour 10-11: UI Polish & Animations**
  - Add hover effects, transitions, loading states.
  - Ensure consistent color palette and typography.
- **Hour 11-12: Data Connections (Where possible)**
  - Connect Profile form to Supabase.
  - Ensure "Save" functionality works.
- **Hour 12-13: Final Review & Deployment**
  - Walkthrough of user journey.
  - Deploy to Vercel (Frontend) + Render/Railway (Backend).
  - Fix critical bugs preventing demo flow.

---

## ⚠️ Critical Constraints
1.  **NO Complex ML Training:** We will mock all ML outputs (recommendations, gap analysis scores) for the demo.
2.  **NO Real-Time Data Scraping:** Job listings and trends will use static JSON datasets.
3.  **NO Complex Auth Flows:** Simple email/password or "Guest Mode" for demo speed.
4.  **UI First:** If backend logic breaks, fallback to hardcoded data on frontend immediately.

**Goal:** A "Clickable, Beautiful, High-Fidelity Prototype" that looks and feels like a finished product.

# Atlas AI - Frontend Design Prompt (v2)

## 🎨 FOR LOVABLE AI / GOOGLE AI STUDIO / V0

---

# MASTER PROMPT: Atlas AI - The Narrative Career Platform

**Objective:** Create a sophisticated, storytelling-driven web application for **Atlas AI**, a platform that guides students from career confusion to clarity. The design must be **gorgeous, editorial, and immersive**, using a modular grid layout to showcase complex information clearly.

**Design Philosophy:**
> "Innovative, energetic, forward-thinking."
> Focus on visual impact and project showcases through high-contrast, editorial storytelling.

---

## 🎨 DESIGN SYSTEM (STRICT REQUIREMENTS)

### Color Palette (High Contrast & Professional)
```css
/* Base Colors */
--primary: #6366F1;      /* Indigo (Brand Identity) */
--cta: #10B981;          /* Emerald (Calls to Action/Success) */
--background: #FFFFFF;   /* Pure White (Canvas) */
--text: #1E293B;         /* Slate (Primary Text) */
--accent: #F59E0B;       /* Amber (Highlights/Warnings) */

/* Usage Rules */
--text-secondary: #64748B; /* Slate-500 for subtitles */
--border: #E2E8F0;       /* Slate-200 for subtle borders */
--surface: #F8FAFC;      /* Slate-50 for cards/sections */
```

### Typography (Editorial & Modern)
```css
/* Headings (Sophisticated) */
font-family: 'Playfair Display', serif;
font-weight: 700 (Bold) for H1, H2
font-weight: 400 (Regular) for H3

/* Body Copy (Clean & Readable) */
font-family: 'Montserrat', sans-serif;
font-weight: 300 (Light) for large paragraphs
font-weight: 400 (Regular) for standard text

/* Accents/Labels (Elegant) */
font-family: 'Cormorant Garamond', serif;
font-style: italic;
```

### Layout & Spacing (Modular & Organized)
- **Grid System:** CSS Grid with 12 columns
- **Gaps:** Consistent 16px-24px spacing
- **Card Sizes:** Varied (bento box style) for visual interest
- **Sections:** Full-screen immersive sections
- **Scroll:** Horizontal scroll galleries for projects/skills

---

## 🚫 ANTI-PATTERNS (DO NOT IMPLEMENT)

**❌ Flash Over Function:**
- NO animations blocking user action (>300ms)
- NO auto-playing videos with sound
- NO infinite scroll without pagination

**❌ Low Contrast Crimes:**
- NO light grey text on white
- NO pure white text on pure black (use #F8FAFC on #0F172A)
- **MUST** pass WCAG AA (4.5:1 contrast)

**❌ Over-Cluttered Chaos:**
- MAX 3 primary colors
- MAX 2 font families (plus accent)
- MAX 5 font sizes per view

**❌ UX Frustrations:**
- NO hamburger menus on desktop
- NO hidden navigation
- NO tiny touch targets (<44px)
- NO horizontal scroll on mobile (except carousels)

---

## 📱 CORE PAGES & FEATURES

### 1. Landing Page (The Story)
**Layout:** Full-screen vertical sections
**Vibe:** Immersive, Editorial, Case Study

- **Hero:**
  - Headline (Playfair, 64px): "From Confusion to Clarity."
  - Subhead (Montserrat, 300, 24px): "The AI-powered career companion for the future of work."
  - CTA (Emerald, #10B981): "Start Your Journey" (Solid, 44px height)
  - Visual: Split screen or full-width abstract 3D visualization of a "career path"

- **Problem/Solution:**
  - High-contrast section (Indigo bg, White text)
  - Bento grid layout showing:
    - "The Crisis" (Stat card)
    - "The Solution" (Text card)
    - "The Result" (Success metrics)

- **Feature Showcase (Horizontal Scroll):**
  - "Clarity Coach"
  - "Atlas Card"
  - "Skill DNA"
  - Large, high-res screenshots/mockups with Cormorant Garamond captions

### 2. Dashboard (The Command Center)
**Layout:** Modular "Bento Box" Grid
**Vibe:** Organized, Information-Dense, Clean

- **Top Bar:**
  - Logo (Playfair)
  - Global Search (Prominent, centered)
  - User Profile (Avatar + Name)

- **Grid Widgets:**
  1. **My Journey (Large, 2x2):** Timeline visualization of career progress
  2. **Next Steps (Tall, 1x2):** AI-recommended actions (Emerald accents)
  3. **Skill Health (1x1):** Radar chart of current skills
  4. **Job Market (1x1):** Live trend indicator (Amber accent)
  5. **Recent Activity (Wide, 2x1):** List of recent modules/chats

### 3. Atlas Card (The Modern Resume)
**Layout:** Asymmetric Two-Column
**Vibe:** Portfolio, Case Study, Personal Brand

- **Left Column (Sticky Info):**
  - Photo (High quality, rounded rect)
  - Name (Playfair, H1)
  - "Open to Work" badge (Emerald border)
  - Core Stats: "Years Exp", "Projects", "Skill Score"

- **Right Column (Scrollable Content):**
  - **About:** Editorial-style bio (Montserrat light)
  - **Projects:** Large visuals, minimal text, tech stack tags
  - **Skills:** Visual bars (Indigo fill), not just lists
  - **Experience:** Timeline with "Outcome" focus (not just tasks)

### 4. Clarity Coach (The AI Interface)
**Layout:** Split View (Context + Chat)
**Vibe:** Focused, Intelligent, Human

- **Left Panel (Context):**
  - "Current Focus" card
  - "Relevant Documents" list
  - "Memory Bank" (saved insights)

- **Right Panel (Chat):**
  - Minimal interface
  - Message bubbles:
    - User: Indigo background, White text
    - AI: Slate-50 background, Slate-900 text
  - Typing indicator: Subtle pulse (Emerald)
  - Input: Large, labeled text area (no tiny inputs)

### 5. Authentication (The Entry)
**Layout:** Split Screen (Visual + Form)
**Vibe:** Secure, Welcoming, Premium

- **Left:** High-quality editorial image or brand pattern (Indigo)
- **Right:** Clean form
  - Inputs: Labeled *outside* the box (Montserrat bold)
  - Validation: Inline error messages (Red/Amber)
  - Submit: Full-width Emerald button
  - Social Auth: Branded buttons (Google, GitHub)

---

## ⚡ INTERACTION DESIGN (The Feel)

- **Hover Effects:**
  - Cards: Slight lift (transform: translateY(-4px)), shadow deepens
  - Buttons: Brightness increase (filter: brightness(110%))
  - Links: Underline expands from center

- **Transitions:**
  - Page Load: Elements stagger in (fade-up, 50ms delay)
  - Modals: Scale up from 95% opacity
  - Tab Switch: Cross-fade (opacity + x-axis slide)

- **Micro-interactions:**
  - Checkboxes: Satisfying "bounce" animation
  - Search: Expands on focus
  - Success: Emerald checkmark animate-in

---

## 🛠 TECHNICAL SPECIFICATIONS

- **Framework:** React 18 + TypeScript
- **Styling:** Tailwind CSS (Custom config for colors/fonts)
- **Icons:** Lucide React (Clean, consistent strokes)
- **Motion:** Framer Motion (for staggered entrances)
- **Charts:** Recharts (Customized colors: Indigo/Emerald)
- **Grid:** CSS Grid (Gap-4, Gap-6, Gap-8 responsive)

---

## ✅ ACCEPTANCE CRITERIA FOR GENERATION

1. **Design System Adherence:**
   - [ ] Primary color is #6366F1
   - [ ] Headings are Playfair Display
   - [ ] Body is Montserrat
   - [ ] Layout is grid-based and modular

2. **UX Compliance:**
   - [ ] No low-contrast text
   - [ ] Navigation is labeled and visible
   - [ ] Touch targets are >44px
   - [ ] Focus states are visible

3. **Feature Completeness:**
   - [ ] Landing Page
   - [ ] Dashboard
   - [ ] Atlas Card
   - [ ] Chat Interface
   - [ ] Login/Register

---

**Generate the code structure, Tailwind config, and key components for this application now.**

# ATLAS AI - Frontend Implementation Plan

## Goal Description
Build a "gorgeous", high-fidelity frontend for **ATLAS AI** that covers the end-to-end user journey from login to core features. The design must strictly adhere to the "Storytelling + Case Studies" pattern, use specific typography (Playfair Display, Montserrat, Cormorant Garamond), and follow defined color/layout constraints.

## User Review Required
> [!IMPORTANT]
> **Tech Stack**
> - **Framework**: Next.js 14 (App Router) + TypeScript
> - **Styling**: Tailwind CSS + Framer Motion (for immersive transitions)
> - **Icons**: Lucide React
> - **State Management**: React Context / Zustand
> - **Backend Integration**: Connecting to existing Python FastAPI backend

> [!NOTE]
> **Design Specifications**
> - **Fonts**: Playfair Display (Headings), Montserrat (Body), Cormorant Garamond (Accents) through `next/font/google`.
> - **Colors**: Indigo Primary (#6366F1), Emerald CTA (#10B981), Amber Accent (#F59E0B).
> - **Layout**: Full-screen sections, CSS Grid "bento" layouts, horizontal scroll galleries.

## Proposed Changes

### Phase 1: Foundation & Design System
#### [NEW] `frontend/`
- Initialize Next.js project.
- Configure `tailwind.config.ts` with:
  - Custom colors (`--primary`, `--cta`, etc.)
  - Font families
  - Animation keyframes
- Set up `globals.css` for base typography weights (300, 400, 700).

#### [NEW] `frontend/components/ui/`
- **Button**: High-contrast, accessible, proper hover states.
- **Card**: Glassmorphism or clean white with subtle shadows, varying sizes.
- **Input/Form**: Floating labels or clear top labels, validation states.
- **Typography**: Reusable components for `H1` (Playfair), `P` (Montserrat), `Caption` (Cormorant).

### Phase 2: Core Architecture & Navigation
#### [NEW] `frontend/app/layout.tsx`
- Root layout with font optimization.
- Global navigation (Responsive, no hamburger on desktop).
- Assessment/Onboarding check provider.

#### [NEW] `frontend/components/layout/`
- **Navbar**: Sticky, glass effect.
- **Sidebar**: (If applicable for Dashboard) Collapsible, labelled icons.
- **Footer**: Minimal, clean.

### Phase 3: Feature Implementation (Storytelling Flow)

#### 1. Landing & Authentication
- **`frontend/app/page.tsx`**: Immersive "Case Study" style intro. Full-screen scrolling sections.
- **`frontend/app/login/page.tsx`**: Split screen layout. "Join the Network" storytelling approach.

#### 2. Intelligence Hub (Dashboard)
- **`frontend/app/dashboard/page.tsx`**:
  - **Layout**: CSS Grid (Bento Box).
  - **Module**: "Today's Briefing" (Editorial style updates).
  - **Module**: Skill Gap Radar (Recharts).
  - **Module**: "Next Steps" Horizontal Gallery.

#### 3. The Atlas Card (Profile)
- **`frontend/app/profile/page.tsx`**:
  - **Header**: Large typography, impact numbers (Level, XP).
  - **Timeline**: Vertical flow of experience/education.
  - **Portfolio**: Grid of project cards with "View Case Study" actions.

#### 4. Career Guidance (Core Features)
- **`frontend/app/career/exploration/page.tsx`**:
  - Comparison Cards for Career Paths.
- **`frontend/app/career/skill-gap/page.tsx`**:
  - Detailed "Analysis" view with actionable steps.

### Phase 4: Polish & Integration
- **Transitions**: Page transitions using Framer Motion.
- **Micro-interactions**: Hover effects on cards, buttons.
- **API integration**: Connect forms and dashboards to backend endpoints.

## Verification Plan
### Automated Tests
- `npm run lint`: Ensure no code style violations.
- `npm run build`: Verify production build succeeds.

### Manual Verification
- **Design Check**:
  - Confirm fonts load correctly.
  - Validate contrast ratios (WCAG AA).
  - Test responsive behavior (Mobile <-> Desktop).
- **Flow Check**:
  - Login -> Dashboard -> Profile -> Career Exploration.
  - Verify "Storytelling" feel (smooth scrolling, logical content flow).

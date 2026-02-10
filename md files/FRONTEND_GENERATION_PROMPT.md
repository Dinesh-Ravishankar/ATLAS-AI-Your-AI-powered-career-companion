# Atlas AI - Frontend Generation Prompt

## 🎨 FOR LOVABLE AI / GOOGLE AI STUDIO

---

# MASTER PROMPT: Atlas AI Career Guidance Platform

Create a stunning, modern web application for **Atlas AI** - an intelligent career guidance platform for students. This is a premium, AI-powered career companion that helps students navigate from confusion to clarity.

---

## 🎯 CORE CONCEPT

Atlas AI is the "Netflix of Career Guidance" - a personalized, AI-driven platform that combines:
- **Career Discovery** (like LinkedIn meets ChatGPT)
- **Skill Development** (like Coursera meets GitHub)
- **Mental Health Support** (career guidance with empathy)
- **Portfolio Building** (dynamic resume + project showcase)

**Target Audience:** Gen Z students (18-25), tech-savvy, seeking career clarity

---

## 🎨 DESIGN SYSTEM (STRICT REQUIREMENTS)

### Color Palette
```
Primary (Brand): #FF4F00 (Vibrant Orange-Red)
Accent: #FF4F00 (Same as primary for consistency)
Background: #FFFDF9 (Warm Off-White)
Text Primary: #201515 (Deep Brown-Black)
Text Secondary/Links: #C5C0B1 (Warm Gray)
```

**Color Usage Rules:**
- Primary (#FF4F00): CTAs, active states, highlights, progress indicators
- Background (#FFFDF9): Main canvas, cards, modals
- Text (#201515): Headings, body text, labels
- Links (#C5C0B1): Secondary text, disabled states, subtle elements

### Typography
```
Display Font: "Degular Display" (for headings, hero text)
Body Font: "Inter" (for all body text, UI elements)

Sizes:
- H1: 40px (Hero headlines)
- H2: 14px (Section titles - intentionally small for modern look)
- Body: 14px (Paragraphs, labels)
```

**Typography Rules:**
- Use Degular Display ONLY for large display text (hero, major headings)
- Use Inter for everything else (navigation, body, buttons, forms)
- Maintain 14px as base size for clean, modern aesthetic

### Spacing & Layout
```
Base Unit: 4px (all spacing should be multiples of 4)
Border Radius: 4px (subtle, modern corners)
Grid: 12-column responsive grid
Padding: 16px, 24px, 32px (4px multiples)
```

### Personality
```
Tone: Modern, Professional, Approachable
Energy: High (vibrant, dynamic, engaging)
Vibe: "Startup meets Premium SaaS"
```

---

## 📱 REQUIRED PAGES & COMPONENTS

### 1. **Landing Page / Hero**

**Layout:**
- Full-screen hero section with gradient overlay
- Large headline (Degular Display, 40px): "Your AI Career Companion"
- Subheadline (Inter, 14px): "From Confusion to Clarity in 30 Days"
- Primary CTA button: "Start Your Journey" (#FF4F00, white text)
- Secondary CTA: "See How It Works" (outline style)

**Visual Elements:**
- Animated background: Subtle particle effect or gradient mesh
- 3D illustration or abstract shapes representing career paths
- Social proof: "Trusted by 10,000+ students"
- Feature highlights (3 cards):
  1. AI Clarity Coach (24/7 guidance)
  2. Skill Gap Analysis (Know what to learn)
  3. Atlas Card (Your dynamic portfolio)

**Inspiration:** Clean, spacious, high-energy startup landing page

---

### 2. **Login / Authentication Page**

**Layout (Inspired by reference image):**
- Split screen OR centered card design
- Left side: Branding, welcome message
- Right side: Login form

**Form Elements:**
- Email input (clean, minimal border)
- Password input (with show/hide toggle)
- "Continue with Twitter" button (outline, icon + text)
- "Continue with Apple" button (outline, icon + text)
- "Don't have an account? Sign up" link at bottom

**Styling:**
- Soft shadows on form card
- Rounded corners (4px)
- Hover states on buttons (subtle scale or color shift)
- Error states (red border, helper text)

**Copy:**
- Headline: "Welcome back" (Degular Display)
- Subtext: "Log in to your account" (Inter, gray)

---

### 3. **Dashboard (Atlas Card View)**

**Layout (Inspired by reference dashboard):**
- **Left Sidebar:** Vertical navigation (dark background, white icons)
  - Dashboard
  - Atlas Card (Profile)
  - Skills
  - Projects
  - Career Paths
  - Clarity Coach (Chat)
  - Settings

- **Main Content Area:**
  - **Top Bar:** Search, notifications, user avatar
  - **Stats Cards (4 across):**
    1. Skills Mastered (number + icon)
    2. Active Projects (number + icon)
    3. Learning Progress (number + icon)
    4. Career Matches (number + icon)
  
  - **Primary Card:** "Atlas Card Preview"
    - User photo
    - Name, bio
    - Target roles (tags)
    - Skills visualization (circular progress or bar chart)
    - "Edit Profile" button
  
  - **Activity Feed:**
    - Recent skill additions
    - Project updates
    - Career recommendations
    - AI coach suggestions

**Visual Style:**
- Cards with subtle shadows
- Green accent for positive metrics (#00C853 or similar)
- Progress bars with #FF4F00 fill
- Clean, grid-based layout

---

### 4. **Atlas Card (Profile Page)**

**Sections:**
1. **Header:**
   - Profile photo (large, circular)
   - Name (Degular Display, 40px)
   - Tagline/Bio (Inter, 14px)
   - Location, GitHub, LinkedIn icons

2. **Target Careers:**
   - Horizontal scrollable cards
   - Each card: Career title, match percentage, icon
   - "Add Career" button

3. **Skills Matrix:**
   - Visual grid or radar chart
   - Skills grouped by category (Technical, Soft, Domain)
   - Proficiency levels (Beginner, Intermediate, Advanced)
   - Color-coded by strength

4. **Projects Showcase:**
   - Grid of project cards (3 columns)
   - Each card: Thumbnail, title, tech stack tags, GitHub link
   - Hover effect: Lift + shadow

5. **Education & Experience:**
   - Timeline view
   - University, degree, GPA
   - Internships, work experience

6. **Achievements:**
   - Badge collection
   - Certifications
   - Hackathon wins

**Interaction:**
- "Edit" button on each section
- Inline editing for quick updates
- "Export as PDF" button (top right)

---

### 5. **Clarity Coach (AI Chat Interface)**

**Layout:**
- **Left Panel (30%):** Conversation history
  - List of past chats
  - "New Conversation" button
  - Search conversations

- **Main Chat Area (70%):**
  - Messages (user vs. AI)
  - User messages: Right-aligned, #FF4F00 background, white text
  - AI messages: Left-aligned, light gray background, dark text
  - Typing indicator (3 animated dots)
  - Input box at bottom:
    - Text area (auto-expand)
    - Send button (icon, #FF4F00)
    - Attachment icon (for resume upload)

**Quick Actions (Chips above input):**
- "Analyze my resume"
- "Suggest career paths"
- "Find skill gaps"
- "Mock interview"

**Visual Style:**
- Clean, WhatsApp/ChatGPT-inspired
- Smooth scroll
- Message timestamps
- Avatar for AI (robot icon or logo)

---

### 6. **Skill Gap Analysis Page**

**Layout:**
- **Header:** "Your Skill Gap Analysis"
- **Target Role Selector:** Dropdown or search bar

**Visualization:**
- **Venn Diagram or Bar Chart:**
  - Your Skills (green)
  - Required Skills (orange)
  - Gap (red)

- **Gap List:**
  - Table or cards showing missing skills
  - Priority level (High, Medium, Low)
  - Estimated time to learn
  - "Add to Learning Path" button

**Recommendations:**
- Course suggestions (Coursera, Udemy links)
- Project ideas to practice
- Mentors to connect with

---

### 7. **Vertical Navigation Sidebar** (Inspired by reference)

**Design:**
- Dark background (#1A1A1A or #201515)
- White icons + text
- Active state: #FF4F00 background or left border
- Hover state: Subtle highlight
- Collapsed mode: Icons only
- Expanded mode: Icons + labels

**Menu Items:**
- Dashboard (home icon)
- Atlas Card (user icon)
- Skills (chart icon)
- Projects (folder icon)
- Careers (compass icon)
- Clarity Coach (chat icon)
- Settings (gear icon)
- Logout (exit icon)

**Bottom Section:**
- User profile mini-card
- Upgrade to Pro (if freemium)

---

## 🎭 COMPONENT LIBRARY REQUIREMENTS

### Buttons
```css
Primary Button:
- Background: #FF4F00
- Text: White
- Border Radius: 4px
- Padding: 12px 24px
- Hover: Darken 10%
- Active: Scale 0.98

Secondary Button:
- Background: Transparent
- Border: 1px solid #FF4F00
- Text: #FF4F00
- Hover: Background #FF4F00, Text White

Ghost Button:
- Background: Transparent
- Text: #201515
- Hover: Background #FFFDF9
```

### Cards
```css
Standard Card:
- Background: #FFFDF9
- Border: 1px solid #C5C0B1 (optional)
- Border Radius: 4px
- Padding: 24px
- Shadow: 0 2px 8px rgba(0,0,0,0.08)
- Hover: Shadow 0 4px 16px rgba(0,0,0,0.12)
```

### Inputs
```css
Text Input:
- Background: White
- Border: 1px solid #C5C0B1
- Border Radius: 4px
- Padding: 12px 16px
- Focus: Border #FF4F00, Shadow 0 0 0 3px rgba(255,79,0,0.1)
- Error: Border red
```

### Tags/Chips
```css
Skill Tag:
- Background: #FF4F00 (10% opacity)
- Text: #FF4F00
- Border Radius: 4px
- Padding: 4px 12px
- Font Size: 12px
```

---

## 🌟 ADVANCED FEATURES TO INCLUDE

### Micro-Interactions
1. **Button Hover:** Subtle scale (1.02) + shadow increase
2. **Card Hover:** Lift effect (translateY -4px)
3. **Input Focus:** Smooth border color transition
4. **Loading States:** Skeleton screens (not spinners)
5. **Success Feedback:** Checkmark animation
6. **Progress Bars:** Animated fill on load

### Animations
- **Page Transitions:** Fade + slide (300ms ease-out)
- **Modal Open:** Scale from 0.9 to 1 + fade in
- **List Items:** Stagger animation (50ms delay each)
- **Skill Chart:** Animate bars/circles on scroll into view
- **Typing Indicator:** Bouncing dots for AI chat

### Responsive Design
- **Desktop (1440px+):** Full sidebar, 3-column grids
- **Tablet (768px-1439px):** Collapsed sidebar, 2-column grids
- **Mobile (< 768px):** Bottom nav bar, single column, full-width cards

---

## 🚀 TECHNICAL REQUIREMENTS

### Framework & Libraries
```
- React 18+ with TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Shadcn/UI (component library)
- Framer Motion (animations)
- Recharts or Chart.js (data visualization)
- React Router (navigation)
- Axios (API calls)
- React Hook Form (forms)
- Zod (validation)
```

### File Structure
```
src/
├── components/
│   ├── ui/ (Shadcn components)
│   ├── layout/ (Sidebar, Header, Footer)
│   ├── cards/ (ProfileCard, SkillCard, ProjectCard)
│   └── forms/ (LoginForm, ProfileForm)
├── pages/
│   ├── Landing.tsx
│   ├── Login.tsx
│   ├── Dashboard.tsx
│   ├── AtlasCard.tsx
│   ├── ClarityCoach.tsx
│   └── SkillGap.tsx
├── hooks/ (custom React hooks)
├── lib/ (utilities, API client)
├── styles/ (global CSS, Tailwind config)
└── types/ (TypeScript interfaces)
```

### API Integration
```typescript
// Example API endpoints to integrate
const API_BASE = "http://localhost:8000";

endpoints:
- POST /auth/register
- POST /auth/login
- GET /auth/me
- GET /profile/me
- PUT /profile/me
- GET /career/recommendations
```

---

## 🎨 DESIGN INSPIRATION SUMMARY

**From Reference Image:**
1. **Login Page:** Clean, centered form with social login options
2. **Dashboard:** Card-based layout with stats, activity feed, progress tracking
3. **Vertical Sidebar:** Dark theme, icon-based navigation, collapsible
4. **File Upload:** Simple drag-and-drop area for resume upload

**Additional Inspiration:**
- **Linear.app:** Clean, fast, keyboard-first navigation
- **Notion:** Flexible, card-based layouts
- **Stripe Dashboard:** Data visualization, clean metrics
- **ChatGPT:** Conversational UI for Clarity Coach

---

## ✅ ACCEPTANCE CRITERIA

The generated frontend MUST:
1. ✅ Use EXACT color scheme (#FF4F00, #FFFDF9, #201515, #C5C0B1)
2. ✅ Use Degular Display for headings, Inter for body
3. ✅ Include all 7 pages (Landing, Login, Dashboard, Atlas Card, Chat, Skill Gap, Sidebar)
4. ✅ Be fully responsive (mobile, tablet, desktop)
5. ✅ Have smooth animations and micro-interactions
6. ✅ Use 4px spacing system and 4px border radius
7. ✅ Include working navigation between pages
8. ✅ Have form validation and error states
9. ✅ Show loading states (skeleton screens)
10. ✅ Be accessible (ARIA labels, keyboard navigation)

---

## 🎯 FINAL INSTRUCTIONS FOR AI

**Generate a complete, production-ready React + TypeScript + Tailwind CSS web application** that:
- Looks like a premium SaaS product (think Linear, Notion, Stripe)
- Uses the EXACT design system specified above
- Includes all 7 pages with proper routing
- Has smooth animations and delightful micro-interactions
- Is fully responsive and accessible
- Follows modern React best practices (hooks, composition, TypeScript)
- Uses Shadcn/UI for base components
- Includes placeholder data for demonstration
- Has clean, well-commented code

**Prioritize:**
1. Visual polish and attention to detail
2. Smooth user experience
3. Modern, trendy design patterns
4. Performance (lazy loading, code splitting)
5. Accessibility and responsiveness

**Deliver:**
- Complete source code with all components
- README with setup instructions
- Package.json with all dependencies
- Tailwind config with custom colors
- Example data/mock API responses

---

## 🌈 BONUS POINTS

If possible, include:
- Dark mode toggle (using same color scheme with inverted backgrounds)
- Keyboard shortcuts (e.g., Cmd+K for search)
- Onboarding tour (first-time user guide)
- Empty states (when no data exists)
- Error boundaries (graceful error handling)
- Toast notifications (success/error feedback)
- Drag-and-drop for file uploads
- Real-time typing indicators in chat
- Animated skill charts (on scroll into view)
- Export Atlas Card as PDF (using jsPDF or similar)

---

**START BUILDING THE MOST BEAUTIFUL CAREER GUIDANCE PLATFORM EVER CREATED!** 🚀

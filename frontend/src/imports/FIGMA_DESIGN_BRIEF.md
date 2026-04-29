# SWACH AI CARBON ACCOUNTING - COMPREHENSIVE DESIGN BRIEF FOR FIGMA

## PROJECT OVERVIEW

**Project Name:** Swach AI Carbon Footprint Calculator  
**Target Users:** Indian enterprises (mid to large companies)  
**Purpose:** Calculate and track corporate carbon emissions with AI-powered insights  
**Platform:** Web-based SaaS application  
**Tech Stack:** React, TypeScript, Tailwind CSS, Recharts  
**Launch Date:** October 2026 (India's CCTS compliance deadline)  

---

## APPLICATION STRUCTURE & PAGES

### PAGE 1: LANDING / FORM ENTRY (Multi-Step Form)

#### Layout Overview:
- **Header Section** (Sticky)
  - Logo + Brand name "Swach AI"
  - Tagline: "Calculate your company's carbon footprint with AI-powered insights"
  - Background: Green gradient (primary brand color)
  - Height: 120px

- **Main Content Area**
  - Maximum width: 900px, centered on larger screens
  - Padding: 2rem on desktop, 1rem on mobile

#### Step Indicator (Visual Progress)
```
┌─────────────────────────────────────────┐
│  Step 1          Step 2          Step 3 │
│  ✓ Company      🔋 Energy       💨 Other │
│  Info            & Fuel          Sources │
│                                          │
│  Progress: ████░░░░░░░░░░░░ 33%       │
└─────────────────────────────────────────┘
```

- 3 circular indicators (50px diameter)
- Active step: Green gradient fill + scale up slightly
- Completed steps: Green checkmark icon
- Inactive steps: Light gray border
- Connected by a horizontal line
- Labels below each circle
- Spacing between circles: Auto-distributed

#### Form Cards (Per Step)
```
┌────────────────────────────────────────────┐
│ 🏢  STEP 1: COMPANY INFORMATION            │
│     Tell us about your company             │
├────────────────────────────────────────────┤
│                                            │
│  Company Name *                            │
│  [________________ placeholder text____] │
│                                            │
│  Industry Type *                           │
│  [▼ Select industry________▼]             │
│  Industries: Technology, Manufacturing,    │
│  Retail, Healthcare, Finance, etc.        │
│                                            │
│  Number of Employees *                     │
│  [_________]  (employees)                 │
│                                            │
│  💡 Tip: If you don't have exact figures, │
│     use annual estimates or monthly avg.   │
│                                            │
├────────────────────────────────────────────┤
│  [◀ Previous]              [Next ▶]        │
│  (disabled)                (enabled)       │
└────────────────────────────────────────────┘
```

**Form Field Specifications:**
- Input fields: 100% width, 44px height
- Padding: 12px left/right, 10px top/bottom
- Border: 2px solid #e5e7eb (light gray)
- Border-radius: 8px
- Font: 16px, regular weight
- Focus state: Border becomes #10b981 (green), with subtle shadow
- Placeholder text: #9ca3af (light gray)
- Error state: Border becomes #ef4444 (red), error message in red below

**Step 1 Fields:**
1. Company Name (Text Input)
2. Industry Type (Dropdown Select)
3. Employee Count (Number Input)

**Step 2 Fields:**
1. Annual Electricity Consumption (kWh)
2. Diesel Consumption (liters)
3. Petrol Consumption (liters)
4. Natural Gas Consumption (MMBtu)
5. LPG Consumption (kg)

**Step 3 Fields:**
1. Coal Consumption (tonnes)
2. Water Consumption (m³)
3. Waste Generated (tonnes)
4. Business Travel Distance (km)

#### Buttons

**Primary Button (Next/Submit)**
- Background: Linear gradient (135deg) #10b981 → #059669
- Text: White, 16px, bold
- Padding: 12px 24px
- Border-radius: 8px
- Height: 44px
- Icon on right: Chevron or checkmark
- Hover: Shadow increases, subtle translate up
- Disabled: Opacity 0.5, cursor not-allowed

**Secondary Button (Previous)**
- Background: White
- Border: 2px solid #10b981
- Text: #10b981, 16px, bold
- Same sizing as primary
- Hover: Background becomes green, text becomes white
- Disabled: Border gray, text gray, cursor not-allowed

**Button Layout:**
- Space between buttons: 16px
- Button width: ~150px each
- On mobile: Stack vertically, full width

#### Info Box
```
┌─────────────────────────────────────────┐
│ 💡 Tip: If you don't have exact       │
│    figures, use annual estimates or    │
│    monthly averages × 12.              │
└─────────────────────────────────────────┘
```
- Background: Light green #f0fdf4
- Border-left: 4px solid #10b981
- Padding: 16px
- Border-radius: 8px
- Text: #065f46 (dark green)
- Icon: 💡 (24px)

---

### PAGE 2: STREAMING PANEL (Real-Time Agent Processing)

#### Layout Overview:
- Full-width container with max-width 900px
- Header section (130px)
- Timeline content area (scrollable, min 300px, max 600px)
- Footer with stats (70px)

#### Header Section
```
┌──────────────────────────────────────────┐
│ 💡 AI AGENT THINKING                    │
│ Real-time reasoning and analysis        │
│                        [🟢 Analyzing...] │
└──────────────────────────────────────────┘
```

- Icon: Light bulb (32px, #10b981)
- Title: "AI Agent Thinking" (24px, bold)
- Subtitle: "Real-time reasoning and analysis" (14px, gray)
- Status badge on right:
  - **Calculating:** Blue background, pulsing dot
  - **Complete:** Green background, checkmark icon

#### Timeline Events

Each event in the timeline shows:
```
        ●─────── Event Node (36px diameter)
       /│ 
      / │
     /  └─→ [Event Card]
    /
   ●
```

**Timeline Event Card:**
```
    💭  Thought  #1
    ────────────────────
    "Starting carbon footprint 
    calculation for the company..."
    
    10:35:42 AM
```

**Event Card Specifications:**
- Width: Fill container minus margins
- Padding: 16px
- Border-radius: 8px
- Border-left: 4px solid (color varies by type)
- Margin-bottom: 24px
- Animation: Fade in + slide from left

**Event Types & Colors:**

1. **Thought** (Light Blue Background)
   - Icon: 💭
   - Border color: #3b82f6
   - Background: #dbeafe
   - Label color: #1e40af
   - Badge: "THOUGHT" (uppercase, 12px font)

2. **Action** (Light Yellow Background)
   - Icon: ⚙️
   - Border color: #eab308
   - Background: #fef3c7
   - Label color: #a16207
   - Badge: "ACTION"

3. **Observation** (Light Purple Background)
   - Icon: 👁️
   - Border color: #a855f7
   - Background: #f3e8ff
   - Label color: #6b21a8
   - Badge: "OBSERVATION"

4. **Complete** (Light Green Background)
   - Icon: ✅
   - Border color: #10b981
   - Background: #d1fae5
   - Label color: #047857
   - Badge: "COMPLETE"

5. **Error** (Light Red Background)
   - Icon: ❌
   - Border color: #ef4444
   - Background: #fee2e2
   - Label color: #991b1b
   - Badge: "ERROR"

#### Timeline Nodes (Circle Indicators)
- Diameter: 36px
- Border: None
- Gradient fill based on event type
- Icon inside: 20px
- Positioned on left side of timeline
- Box shadow: 0 2px 8px rgba(0,0,0,0.1)
- Animation: Scale in from 0 to 1

#### Timeline Connecting Line
- Width: 2px
- Height: Dynamic (distance to next event)
- Gradient: Color fades from event color to transparent
- Positioned on left side, connecting nodes

#### Loading State (When Processing Starts)
```
        ↻
      ↻   ↻
    ↻       ↻
    
    Starting AI analysis...
```
- Animated spinning circles (3 circles, rotating)
- Color: #10b981
- Animation: 1.5s rotation, staggered delays
- Text below: "Starting AI analysis..." (14px, gray)

#### Completion Message
```
    🎉
    
    Analysis complete!
    Results ready for download.
```
- Icon: 🎉 (48px)
- Title: "Analysis complete!" (20px, bold)
- Message: Subtitle (14px, gray)
- Background: Light green gradient
- Border: 2px solid #d1fae5
- Padding: 24px
- Border-radius: 8px

#### Stats Footer
```
┌─────────────────────────────────────────┐
│ Total Steps: 8    Time: 12s    Status: Done │
└─────────────────────────────────────────┘
```
- Display 3 stats in flexbox
- Each stat: Label + Value
- Separator between stats
- Background: #f9fafb
- Padding: 16px
- Border-top: 2px solid #e5e7eb

#### Action Buttons (Below Timeline)
- **When Complete:** "View Results & Charts →" (Primary button)
- **When Error:** "Try Again" (Secondary button)
- Centered alignment
- Margin-top: 24px

---

### PAGE 3: RESULTS DASHBOARD (Charts & Metrics)

#### Header Section
```
┌────────────────────────────────────────┐
│ Your Carbon Footprint Analysis         │
│ Detailed breakdown and recommendations │
└────────────────────────────────────────┘
```
- Title: 24px, bold, dark gray
- Subtitle: 14px, regular, light gray
- Background: White card
- Padding: 24px
- Border-radius: 16px
- Margin-bottom: 24px

#### Summary Cards (3 Cards in Row)

**Card 1: Total Emissions**
```
    🌿
    Total Emissions
    13,190 tCO2e
    Annual carbon footprint
```

**Card 2: vs. Benchmark**
```
    🎯
    vs. Benchmark
    87.9%
    Below industry average (green) / Above (red)
```

**Card 3: Reduction Potential**
```
    📉
    Reduction Potential
    2,850 tCO2e
    21.6% reduction possible
```

**Summary Card Specifications:**
- Background: White
- Border-left: 4px solid (green for card 1, blue for card 2, purple for card 3)
- Padding: 24px
- Border-radius: 16px
- Box-shadow: 0 4px 12px rgba(0,0,0,0.08)
- Display: Flex (icon on left, content on right)
- Gap: 24px
- Hover: Translate up 4px, shadow increases

**Icon Box:**
- Width/Height: 56px
- Background: Light gradient based on card type
- Border-radius: 8px
- Icon: 32px (white)

**Content Section:**
- Label: 14px, medium weight, #6b7280
- Value: 28px, bold, #1f2937
- Subtitle: 14px, regular, varies by card

**Layout:**
- 3 columns on desktop
- 2 columns on tablet
- 1 column on mobile
- Gap between cards: 24px

#### Charts Section (2 Charts in Row)

**Chart 1: Emissions Breakdown (Pie Chart)**
```
        ╱ Scope 1 (Direct): 11.7%
       ╱  Scope 2 (Indirect): 62.1%
      ╱   Scope 3 (Value Chain): 26.2%
```

- Title: "Emission Sources Breakdown" (18px, bold)
- Subtitle: "Distribution by emission scope" (12px, gray)
- Pie Chart: Donut style, 300px diameter
- Colors:
  - Scope 1: #ef4444 (red)
  - Scope 2: #3b82f6 (blue)
  - Scope 3: #a855f7 (purple)
- Labels: Positioned outside with lines
- Tooltip: Show exact values on hover
- Legend: Below chart with colored squares + text

**Chart 2: Company vs. Industry (Bar Chart)**
```
    |
16K |       ▓▓▓
    |       ▓▓▓  ░░░
    | ░░░   ▓▓▓  ░░░
    |_░░░___▓▓▓__░░░____
      Your   Industry
      Company Benchmark
```

- Title: "Company vs. Industry" (18px, bold)
- Subtitle: "Comparison with benchmark" (12px, gray)
- Bar Chart: 2 bars
- Your Company: Green gradient
- Industry Benchmark: Light gray
- Values displayed on top of bars
- Tooltip: Show exact values on hover
- Y-axis label: tCO2e
- X-axis label: Category

**Chart Container:**
- Background: White card
- Padding: 24px
- Border-radius: 12px
- Box-shadow: 0 4px 12px rgba(0,0,0,0.08)
- Min-height: 350px

**Layout:**
- 2 columns on desktop
- 1 column on tablet/mobile
- Gap: 24px

#### Scope Details Breakdown
```
┌─────────────────────────────────────┐
│ Scope 1: 1,540 tCO2e  ■ Red        │
│ Scope 2: 8,200 tCO2e  ■ Blue       │
│ Scope 3: 3,450 tCO2e  ■ Purple     │
└─────────────────────────────────────┘
```

- 3 items in grid (1-3 columns responsive)
- Each item: Colored square + name + value
- Background: #f9fafb
- Padding: 12px
- Border-radius: 6px
- Margin: 12px gap

#### Reduction Roadmap (Bar Chart)
```
    |
    | Current  After Reduction
15K | ▓▓▓      
    | ▓▓▓      ░░░
 8K | ▓▓▓      ░░░
    |_▓▓▓______░░░____
      13,190    10,340 tCO2e
```

- Title: "Reduction Roadmap" (18px, bold)
- Subtitle: "Potential impact of sustainability initiatives"
- Show before & after emissions
- Reduction amount highlighted
- Percentage reduction shown above

#### Offset Recommendations Box
```
┌────────────────────────────────────┐
│ 🌿 Recommended Offsets             │
│    Carbon reduction strategies     │
├────────────────────────────────────┤
│ ✓ Renewable Energy Credits         │
│ ✓ Carbon Offset Programs           │
│ ✓ Reforestation Projects           │
├────────────────────────────────────┤
│ [Download Detailed Report (PDF)]   │
└────────────────────────────────────┘
```

- Background: White card
- Border-left: 4px solid #10b981
- Padding: 24px
- Border-radius: 12px
- Box-shadow: 0 4px 12px rgba(0,0,0,0.08)

**Offset Items:**
- Layout: Vertical list
- Each item: Checkmark icon + text
- Checkmark: Circle background #10b981, white check
- Text: 16px, #047857
- Padding: 12px per item
- Background: Light green #f0fdf4

**Download Button:**
- Full width (within card)
- Primary green button
- Icon: Download (20px)
- Text: "Download Detailed Report (PDF)"
- Height: 44px
- Margin-top: 16px

#### Info Box
```
┌────────────────────────────────────┐
│ 📊 Understanding Your Results:     │
│ Scope 1 covers direct emissions... │
└────────────────────────────────────┘
```

- Background: #f0fdf4 (light green)
- Border-left: 4px solid #10b981
- Padding: 16px
- Border-radius: 8px
- Text: #065f46 (dark green), 14px

#### Calculation ID (Footer)
```
Calculation ID: abc-123-def-456
```
- Centered text
- Background: #f9fafb
- Padding: 16px
- Border-radius: 8px
- Font: Monospace (Courier)
- Font-size: 12px

#### Action Buttons (Footer)
```
[Download PDF]    [Calculate Again]
```
- 2 buttons side by side
- Primary button on left (green)
- Secondary button on right
- Margin-top: 24px
- On mobile: Stack vertically

---

## OVERALL COLOR SCHEME

### Primary Colors
```
Green #10b981       - Main CTA, primary actions, success
Dark Green #059669  - Hover states, secondary text
Light Green #34d399 - Accents, highlights
```

### Secondary Colors
```
Blue #3b82f6        - Thought events, secondary info
Yellow #eab308      - Action events, warnings
Purple #a855f7      - Observation events, analytics
Red #ef4444         - Errors, dangerous actions
```

### Neutral Colors
```
Text Primary #1f2937      - Headlines, body text
Text Secondary #6b7280    - Labels, descriptions
Border #e5e7eb           - Dividers, borders
Background Light #f9fafb  - Card backgrounds
Background #f3f4f6       - Page background
White #ffffff            - Pure white for cards
```

---

## TYPOGRAPHY

### Font Stack
`-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif`

### Font Sizes & Weights

| Element | Size | Weight | Line Height |
|---------|------|--------|------------|
| H1 (Page Title) | 32px | 700 | 1.2 |
| H2 (Section Title) | 24px | 700 | 1.3 |
| H3 (Card Title) | 18px | 700 | 1.3 |
| Body Text | 16px | 400 | 1.5 |
| Small Text | 14px | 400 | 1.5 |
| Label | 12px | 500 | 1.4 |
| Badge | 11px | 700 | 1.2 |
| Button Text | 16px | 600 | 1 |
| Monospace (Code) | 12px | 400 | 1.5 |

---

## SPACING SYSTEM (8px Grid)

```
xs: 4px (0.5rem)
sm: 8px (1rem)
md: 16px (1.5rem)
lg: 24px (2rem)
xl: 32px (2.5rem)
2xl: 48px (3rem)
```

### Common Spacing Values:
- Component padding: 16px - 24px
- Element gaps: 8px - 16px
- Section margins: 24px - 32px
- Page margins: 2rem (desktop), 1rem (mobile)

---

## BUTTON SPECIFICATIONS

### Primary Button
```
Background: Linear gradient #10b981 → #059669 (135deg)
Text: White, 16px, 600 weight
Padding: 12px 24px
Height: 44px
Border-radius: 8px
Icon: 20px (optional, on right or left)
Shadow: 0 4px 12px rgba(16,185,129,0.3)
Hover: Scale up slightly, shadow increases
Active: Return to normal size
Disabled: opacity 0.5, cursor not-allowed
```

### Secondary Button
```
Background: White
Border: 2px solid #10b981
Text: #10b981, 16px, 600 weight
Padding: 12px 24px
Height: 44px
Border-radius: 8px
Icon: 20px (optional)
Shadow: None
Hover: Background #10b981, text white
Active: Maintain hover state
Disabled: opacity 0.5, cursor not-allowed
```

### Icon Buttons
```
All buttons include icons from Lucide React:
- ChevronRight (next)
- ChevronLeft (previous)
- Download (PDF)
- RotateCcw (retry)
- Zap (logo)
- Building2 (company)
- Leaf (results)
- Target (goals)
etc.
```

---

## INPUT FIELD SPECIFICATIONS

### Text Input / Number Input
```
Width: 100%
Height: 44px
Padding: 12px 16px
Border: 2px solid #e5e7eb
Border-radius: 8px
Font: 16px, 400 weight
Background: White
Placeholder: #9ca3af

Focus State:
  Border: 2px solid #10b981
  Box-shadow: 0 0 0 3px rgba(16,185,129,0.1)
  Background: #f9fafb

Error State:
  Border: 2px solid #ef4444
  Text: #dc2626
  Error message: 12px, red, below field

Disabled State:
  Background: #f3f4f6
  Text: #9ca3af
  Cursor: not-allowed
```

### Select Dropdown
```
Same as text input, but with dropdown arrow on right:
Background-image: SVG arrow
Padding-right: 40px
Appearance: None (custom styling)
```

---

## ANIMATIONS

### Page Transitions
```
Fade In + Slide Up:
  From: opacity 0, transform translateY(20px)
  To: opacity 1, transform translateY(0)
  Duration: 0.4s
  Easing: ease-out
```

### Button Interactions
```
Hover (Desktop):
  Transform: translateY(-2px)
  Box-shadow: Increase
  Duration: 0.3s
  
Active/Click:
  Transform: translateY(0)
  Duration: 0.1s
```

### Form Field Focus
```
Border change: 0.3s ease
Shadow change: 0.3s ease
Background change: 0.2s ease
```

### Streaming Events
```
Fade In + Slide In (Left):
  From: opacity 0, transform translateX(-10px)
  To: opacity 1, transform translateX(0)
  Duration: 0.4s
  Easing: ease-out
  Stagger: 0.1s between events
```

### Loading Spinner (3 circles)
```
Circle 1: Rotate 360deg, 1.5s linear, delay 0s
Circle 2: Rotate 360deg, 1.5s linear, delay 0.5s
Circle 3: Rotate 360deg, 1.5s linear, delay 1s
Repeat: Infinite
```

### Pulse Animation
```
Status Indicator:
  Opacity: 1 → 0.5 → 1
  Duration: 1.5s
  Easing: ease-in-out
  Repeat: Infinite
```

### Float Animation (Header Icon)
```
Transform: translateY(0) → translateY(-8px) → translateY(0)
Duration: 3s
Easing: ease-in-out
Repeat: Infinite
```

### Bounce Animation (Completion)
```
Transform: translateY(0) → translateY(-10px) → translateY(0)
Duration: 0.6s
Easing: ease-out
Play: Once on completion
```

---

## RESPONSIVE DESIGN BREAKPOINTS

### Desktop (1024px+)
```
- 3-column grids for summary cards
- 2-column grids for charts
- Full-width forms with max-width 900px
- Sidebar layouts if needed
- All desktop features visible
```

### Tablet (768px - 1023px)
```
- 2-column grids for summary cards
- 1-column grids for charts
- Adjusted padding: 16px
- Stacked navigation if present
- Touch-friendly button sizing maintained
```

### Mobile (640px - 767px)
```
- 1-column layout for all elements
- Full-width cards and forms
- Padding: 12px left/right
- Buttons: Full width, 48px minimum height
- Text sizes: Maintain readability
- Touch targets: 44px minimum
```

### Small Mobile (<640px)
```
- 1-column layout
- Maximum padding: 1rem
- Font sizes: Slightly reduced if needed
- Charts: Simplified or stacked
- Navigation: Hamburger menu if needed
```

---

## INTERACTION PATTERNS

### Form Submission Flow
```
1. User fills field
   └─ Real-time validation (optional)
   └─ Visual feedback (green border if valid)

2. User clicks Next
   └─ Button shows loading state
   └─ Form animates out
   └─ Next step animates in

3. On last step, user clicks Submit
   └─ Button shows "Calculating..." with spinner
   └─ Form gets disabled
   └─ API call is made
   └─ Page transitions to streaming panel
```

### Streaming Event Display
```
1. First event appears
   └─ Slides in from left with fade
   └─ Node animation: scale in

2. Each subsequent event
   └─ Same animation as first
   └─ Staggered with 0.1s delay
   └─ Timeline line connects nodes

3. When "complete" event arrives
   └─ Celebration animation
   └─ Stats update
   └─ Action button appears
```

### Chart Interactions
```
1. On page load
   └─ Charts animate in
   └─ Bars/pie slices grow from 0

2. On hover
   └─ Tooltip appears
   └─ Highlight specific element
   └─ Show exact values

3. Legend interaction
   └─ Click to show/hide data
   └─ Visual feedback on legend item
```

---

## COMPONENT STATES

### Empty States
```
When no calculations exist yet:
- Icon: Chart/analytics icon (64px)
- Title: "No calculations yet"
- Message: "Start by filling the form above"
- Action: Link to form
```

### Loading States
```
Form loading:
- All inputs disabled
- Button shows spinner
- Cursor: not-allowed

Data loading:
- Skeleton screens with pulse animation
- Placeholder boxes same size as real content
```

### Error States
```
Form error:
- Red border on affected field
- Error message below (12px, red)
- All form disabled, showing error overlay

Calculation error:
- Red error card with ❌ icon
- Error message
- Retry button
- Back to form button
```

### Success States
```
Form submitted:
- Checkmark animation
- Page transition with fade

Calculation complete:
- Celebration emoji (🎉)
- Completion message
- Results page loads
- Charts animate in
```

---

## ACCESSIBILITY REQUIREMENTS

### Color
```
- No color used alone to convey information
- Text contrast: Minimum 4.5:1 for normal text
- Focus indicators: Clear and visible (2px, high contrast)
```

### Focus States
```
- All interactive elements focusable
- Focus visible with outline: 2px solid #10b981
- Outline offset: 2px
- Tab order: Logical flow left-to-right, top-to-bottom
```

### Text Alternatives
```
- All icons have aria-labels
- Images have alt text
- Form fields have associated labels
- Icons + text for actions (e.g., "⚙️ Action" not just icon)
```

### Keyboard Navigation
```
- Tab: Move to next element
- Shift+Tab: Move to previous element
- Enter: Activate button/submit form
- Space: Activate checkbox/button
- Arrow keys: Navigate within menus
```

---

## MOBILE-SPECIFIC DESIGN

### Touch Targets
```
- Minimum size: 44px × 44px
- Spacing between targets: 8px minimum
- All buttons easily tappable with thumb
```

### Mobile Navigation
```
- No hover states (use active/focus instead)
- Tap feedback: Visual change (color/shadow)
- Back button: Hardware back button works
- Swipe: Consider for mobile navigation
```

### Mobile Form
```
- Large touch fields
- Number input with numeric keyboard
- Select dropdown: Native picker
- Single column layout
- Progress visible at top
- One question per screen (optional)
```

### Mobile Charts
```
- Simplified pie chart labels (legend only)
- Single column bar charts
- Larger tap areas for legend items
- Tooltips on tap, not hover
```

---

## DARK MODE (Future Enhancement)

When implementing dark mode:

```
Primary Colors:
- Dark bg: #111827
- Card bg: #1f2937
- Text primary: #f3f4f6
- Green: #10b981 (same)
- Borders: #374151

Charts:
- Background: #1f2937
- Text labels: #d1d5db
- Grid: #374151
```

---

## DESIGN ASSETS NEEDED

### Icons (from Lucide React)
- Zap (logo)
- Building2 (company)
- Leaf (sustainability)
- Lightbulb (thoughts)
- Eye (observations)
- Target (goals)
- Download (PDF)
- RotateCcw (retry)
- ChevronRight/Left (navigation)
- CheckCircle2 (complete)
- AlertCircle (errors)
- TrendingDown (reduction)

### Graphics/Illustrations
- Header background (optional)
- Empty state illustrations
- Error state graphics
- Success illustrations

### Fonts
- System font stack (no external font needed)
- Monospace for code (can use system monospace)

---

## DESIGN TOKENS SUMMARY

```
COLORS:
Primary: #10b981
Dark Primary: #059669
Light Primary: #34d399
Text: #1f2937
Gray: #6b7280
Light Gray: #f3f4f6
Border: #e5e7eb

SPACING:
4, 8, 12, 16, 24, 32, 48px

BORDER RADIUS:
4px (small), 8px (medium), 12px (large), 16px (extra large)

SHADOWS:
Light: 0 1px 2px rgba(0,0,0,0.05)
Medium: 0 4px 12px rgba(0,0,0,0.08)
Large: 0 10px 40px rgba(0,0,0,0.1)

ANIMATION TIMING:
Fast: 0.2s
Normal: 0.3-0.4s
Slow: 0.6-0.8s
```

---

## FIGMA SETUP RECOMMENDATIONS

### Layers Structure
```
Figma File Organization:

📄 Swach AI Design System
├── 🎨 Colors
│   ├── Palette
│   └── Gradients
├── 🔤 Typography
│   ├── Styles
│   └── Sizes
├── 🧩 Components
│   ├── Buttons
│   ├── Inputs
│   ├── Cards
│   ├── Timeline
│   └── Charts
├── 📄 Pages
│   ├── Form Entry
│   ├── Streaming Panel
│   └── Results Dashboard
└── 📐 Specs
    ├── Spacing Grid
    └── Breakpoints
```

### Components to Create
1. Button (primary, secondary, states)
2. Input Field (text, number, select)
3. Card (summary, chart container)
4. Timeline Event
5. Chart Container
6. Progress Indicator
7. Status Badge
8. Form Field Group
9. Info Box
10. Summary Card

---

## DESIGN FILE SPECIFICATIONS

### Artboard Sizes

**Desktop (1440px width)**
```
- Form Entry Page: 1440 × 2000px
- Streaming Panel: 1440 × 1600px
- Results Dashboard: 1440 × 2400px
```

**Tablet (768px width)**
```
- Form Entry Page: 768 × 2200px
- Streaming Panel: 768 × 1800px
- Results Dashboard: 768 × 2800px
```

**Mobile (375px width)**
```
- Form Entry Page: 375 × 2400px
- Streaming Panel: 375 × 2000px
- Results Dashboard: 375 × 3200px
```

---

## BRAND GUIDELINES

### Logo Placement
```
- Header: Left side, 32px × 32px icon
- Zap icon in green (#10b981)
- Text "Swach AI" next to icon, 18px bold
- Tagline below (optional)
```

### Color Usage
```
- Primary actions: Green (#10b981)
- Supporting actions: Secondary green (#059669)
- Backgrounds: Neutral grays
- Alerts: Red (#ef4444)
- Info: Blue (#3b82f6)
```

### Tone of Voice
```
- Friendly and approachable
- Clear and straightforward
- Action-oriented
- Trustworthy and professional
```

---

## SUCCESS METRICS & USABILITY TARGETS

### Performance
- Page load: < 2 seconds
- Form submission: < 100ms
- Streaming events: Real-time (<50ms)
- Chart rendering: < 1 second

### Usability
- Form completion rate: >80%
- Streaming understandability: 95%+
- Mobile responsiveness: 100% across devices
- Accessibility score: WCAG AA minimum

---

This comprehensive design brief provides all the specifications, measurements, colors, spacing, interactions, and layout details needed to create a professional Figma design for the Swach AI Carbon Accounting application. The design should prioritize clarity, engagement, and mobile responsiveness while maintaining a consistent green sustainability theme throughout.

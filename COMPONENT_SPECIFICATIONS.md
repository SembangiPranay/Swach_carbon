# DESIGN SYSTEM - DETAILED COMPONENT SPECIFICATIONS

## COMPONENT LIBRARY BREAKDOWN

### 1. BUTTONS

#### Primary Button
```
State: Default
├─ Background: Linear gradient #10b981 → #059669 (135deg)
├─ Width: Auto (min 150px)
├─ Height: 44px
├─ Padding: 12px 24px
├─ Border-radius: 8px
├─ Text: White, 16px, 600 weight
├─ Icon: 20px (optional)
├─ Box-shadow: 0 4px 12px rgba(16,185,129,0.3)
└─ Cursor: pointer

State: Hover
├─ Transform: translateY(-2px)
├─ Box-shadow: 0 6px 20px rgba(16,185,129,0.4)
└─ Duration: 0.3s ease

State: Active
├─ Transform: translateY(0)
└─ Duration: 0.1s ease

State: Disabled
├─ Opacity: 0.5
├─ Cursor: not-allowed
└─ No hover effects

State: Loading
├─ Text: "Calculating..."
├─ Icon: Spinning ⚙️
└─ Button: Disabled appearance
```

#### Secondary Button
```
State: Default
├─ Background: White
├─ Border: 2px solid #10b981
├─ Width: Auto (min 150px)
├─ Height: 44px
├─ Padding: 12px 24px
├─ Border-radius: 8px
├─ Text: #10b981, 16px, 600 weight
├─ Icon: 20px (optional)
├─ Box-shadow: None
└─ Cursor: pointer

State: Hover
├─ Background: #10b981
├─ Text: White
├─ Transform: translateY(-2px)
└─ Box-shadow: 0 4px 12px rgba(16,185,129,0.2)

State: Active
├─ Transform: translateY(0)
└─ Duration: 0.1s

State: Disabled
├─ Border: 2px solid #d1d5db
├─ Text: #9ca3af
├─ Opacity: 0.5
└─ Cursor: not-allowed
```

---

### 2. INPUT FIELDS

#### Text Input
```
Container
├─ Width: 100%
├─ Position: relative
└─ Margin-bottom: 16px

Input Element
├─ Width: 100%
├─ Height: 44px
├─ Padding: 12px 16px
├─ Border: 2px solid #e5e7eb
├─ Border-radius: 8px
├─ Font: 16px, 400 weight
├─ Background: #ffffff
├─ Color: #1f2937
├─ Placeholder-color: #9ca3af
└─ Transition: all 0.3s ease

State: Focus
├─ Border: 2px solid #10b981
├─ Box-shadow: 0 0 0 3px rgba(16,185,129,0.1)
├─ Background: #f9fafb
└─ Outline: none

State: Error
├─ Border: 2px solid #ef4444
├─ Box-shadow: 0 0 0 3px rgba(239,68,68,0.1)
└─ Color: #dc2626

State: Disabled
├─ Background: #f3f4f6
├─ Border: 2px solid #e5e7eb
├─ Color: #9ca3af
└─ Cursor: not-allowed

Label
├─ Font-size: 14px
├─ Font-weight: 600
├─ Color: #1f2937
├─ Margin-bottom: 8px
├─ Required asterisk: #ef4444
└─ Position: above input

Helper Text
├─ Font-size: 12px
├─ Color: #6b7280
├─ Margin-top: 6px
└─ Position: below input

Error Message
├─ Font-size: 12px
├─ Color: #ef4444
├─ Margin-top: 6px
├─ Icon: ❌
└─ Position: below input
```

#### Number Input
```
Same as Text Input, but:
├─ Input-type: number
├─ Right padding: 40px (for unit text)
├─ Unit display (right side):
│  ├─ Position: absolute right
│  ├─ Right: 16px
│  ├─ Top: 50%
│  ├─ Transform: translateY(-50%)
│  ├─ Font-size: 12px
│  ├─ Color: #9ca3af
│  └─ Pointer-events: none
└─ Example units: "kWh", "liters", "tonnes"
```

#### Select Dropdown
```
Same as Text Input, but:
├─ Appearance: none (custom styled)
├─ Background-image: SVG arrow down
├─ Background-position: right 16px center
├─ Background-repeat: no-repeat
├─ Padding-right: 40px
├─ Cursor: pointer
└─ Options:
   ├─ Style: Inherit from browser defaults
   ├─ Color: #1f2937
   └─ Background: White
```

---

### 3. FORM LAYOUT

#### Form Container
```
├─ Width: 100% (max-width: 900px on desktop)
├─ Background: White
├─ Border-radius: 24px
├─ Padding: 40px (desktop), 24px (tablet), 16px (mobile)
├─ Box-shadow: 0 10px 40px rgba(0,0,0,0.08)
└─ Animation: slide-up 0.8s ease-out 0.2s backwards
```

#### Step Header
```
├─ Display: flex
├─ Align-items: center
├─ Gap: 24px
├─ Margin-bottom: 32px
├─ Padding-bottom: 24px
└─ Border-bottom: 2px solid #f3f4f6

Icon
├─ Size: 40px
├─ Color: #10b981
└─ Flex-shrink: 0

Content
├─ Flex: 1
├─ Title: 28px, 700 weight, #1f2937
├─ Subtitle: 16px, 400 weight, #6b7280
└─ Margin (title→subtitle): 8px
```

#### Form Fields Grid
```
├─ Display: grid
├─ Grid-template-columns: 1fr (mobile), 1fr 1fr (desktop)
├─ Gap: 24px
├─ Margin-bottom: 32px
└─ Animation: fade-in 0.3s ease-in
```

#### Form Field Group
```
├─ Display: flex
├─ Flex-direction: column
├─ Gap: 8px

Label
├─ Font-size: 14px
├─ Font-weight: 600
├─ Color: #1f2937
├─ Display: flex
├─ Align-items: center
├─ Gap: 4px
└─ Required: Red asterisk

Input/Select
└─ Follows input field spec above

Helper Text
├─ Font-size: 12px
├─ Color: #6b7280
└─ Margin-top: 6px
```

---

### 4. PROGRESS BAR & STEP INDICATOR

#### Step Indicator (Top of Form)
```
Container
├─ Display: flex
├─ Justify-content: space-between
├─ Position: relative
├─ Margin: 48px 0
└─ Animation: slide-up 0.7s ease-out 0.1s backwards

Background Line
├─ Position: absolute
├─ Top: 24px
├─ Left: 0
├─ Right: 0
├─ Height: 2px
├─ Background: #e5e7eb
├─ Z-index: 0
└─ Before all circles

Step Item (3 total)
├─ Flex: 1
├─ Display: flex
├─ Flex-direction: column
├─ Align-items: center
├─ Position: relative
├─ Z-index: 1
└─ Gap: 16px

Circle
├─ Width: 50px
├─ Height: 50px
├─ Border-radius: 50%
├─ Background: White
├─ Border: 3px solid #e5e7eb
├─ Display: flex
├─ Align-items: center
├─ Justify-content: center
├─ Box-shadow: 0 2px 8px rgba(0,0,0,0.08)
├─ Color: #9ca3af
├─ Transition: all 0.3s ease
└─ Animation: scale-in 0.4s ease-out (staggered)

State: Active Step
├─ Background: Linear gradient #10b981 → #059669
├─ Border-color: #10b981
├─ Color: White
├─ Box-shadow: 0 4px 12px rgba(16,185,129,0.3)
├─ Transform: scale(1.1)
└─ Display: flex labels

State: Completed Step
├─ Background: Linear gradient #10b981 → #059669
├─ Border-color: #10b981
├─ Color: White
└─ Icon: CheckCircle2

Label (Active Step Only)
├─ Text-align: center
├─ Font-size: 14px
├─ Font-weight: 600
├─ Color: #10b981
├─ Step-name: "Company Info", "Energy & Fuel", "Other Sources"
└─ Margin-bottom: 8px

Step Number (Active)
├─ Font-size: 11px
├─ Color: #6b7280
├─ Font-weight: 500
└─ Example: "Step 1 of 3"
```

#### Progress Bar
```
Container
├─ Display: flex
├─ Align-items: center
├─ Gap: 16px
├─ Margin: 32px 0
└─ Padding: 16px 0

Bar
├─ Flex: 1
├─ Height: 4px
├─ Background: #e5e7eb
├─ Border-radius: 2px
├─ Overflow: hidden

Fill
├─ Height: 100%
├─ Background: Linear gradient #10b981 → #059669
├─ Border-radius: 2px
├─ Transition: width 0.4s ease
└─ Width: Calculated per step (33%, 66%, 100%)

Percentage
├─ Font-size: 12px
├─ Font-weight: 500
├─ Color: #6b7280
├─ Min-width: 50px
├─ Text-align: right
└─ Example: "1 of 3", "66%"
```

---

### 5. TIMELINE & STREAMING PANEL

#### Timeline Container
```
├─ Flex: 1
├─ Overflow-y: auto
├─ Overflow-x: hidden
├─ Padding: 32px
├─ Min-height: 300px
├─ Max-height: 600px
├─ Position: relative
└─ Scrollbar-width: thin (8px)

Scrollbar Style
├─ Track: #f3f4f6
├─ Thumb: #10b981
└─ Thumb-hover: #059669
```

#### Timeline Item
```
├─ Position: relative
├─ Margin-left: 50px
├─ Margin-bottom: 32px
├─ Animation: slide-up 0.4s ease-out (staggered)
└─ Z-index: Auto incrementing

Timeline Line
├─ Position: absolute
├─ Left: -25px
├─ Top: 40px
├─ Width: 2px
├─ Height: calc(100% + 32px)
├─ Background: Gradient (color to transparent)
└─ Animation: Grows from 0 to full height

Event Node (Circle)
├─ Position: absolute
├─ Left: -33px
├─ Top: 0
├─ Width: 36px
├─ Height: 36px
├─ Border-radius: 50%
├─ Display: flex
├─ Align-items: center
├─ Justify-content: center
├─ Color: White
├─ Icon-size: 20px
├─ Z-index: 10
├─ Box-shadow: 0 2px 8px rgba(0,0,0,0.1)
├─ Animation: scale-in 0.4s ease-out
└─ Background: Gradient based on event type

Event Card
├─ Padding: 16px
├─ Border: 2px solid (color varies)
├─ Border-left-width: 4px
├─ Border-radius: 8px
├─ Background: Light color (varies)
└─ Animation: slide-in-right 0.4s ease-out

Header
├─ Display: flex
├─ Justify-content: space-between
├─ Align-items: center
├─ Margin-bottom: 8px
├─ Font-size: 12px
├─ Font-weight: 600
└─ Color: Event color

Badge
├─ Background: Event color
├─ Color: White
├─ Padding: 4px 12px
├─ Border-radius: 6px
├─ Font-size: 10px
├─ Font-weight: 700
├─ Text-transform: uppercase
├─ Letter-spacing: 0.5px
└─ Min-width: 80px

Number
├─ Font-size: 12px
├─ Opacity: 0.6
└─ Example: "#1", "#2"

Message
├─ Font-size: 14px
├─ Line-height: 1.5
├─ Color: #374151
├─ Margin-bottom: 8px
├─ Word-break: break-word
└─ Max-width: 100%

Timestamp
├─ Font-size: 11px
├─ Opacity: 0.6
├─ Font-family: Monospace
├─ Margin-top: 8px
└─ Example: "10:35:42 AM"

Event Type Colors:
Thought:
├─ Border: #3b82f6
├─ Background: #dbeafe
├─ Node-gradient: #3b82f6 → #1e40af
└─ Label-color: #1e40af

Action:
├─ Border: #eab308
├─ Background: #fef3c7
├─ Node-gradient: #eab308 → #a16207
└─ Label-color: #a16207

Observation:
├─ Border: #a855f7
├─ Background: #f3e8ff
├─ Node-gradient: #a855f7 → #6b21a8
└─ Label-color: #6b21a8

Complete:
├─ Border: #10b981
├─ Background: #d1fae5
├─ Node-gradient: #10b981 → #047857
└─ Label-color: #047857

Error:
├─ Border: #ef4444
├─ Background: #fee2e2
├─ Node-gradient: #ef4444 → #991b1b
└─ Label-color: #991b1b
```

#### Loading Spinner
```
Container
├─ Position: relative
├─ Width: 60px
├─ Height: 60px
├─ Margin: 0 auto 24px

Ring 1
├─ Position: absolute
├─ Width: 60px
├─ Height: 60px
├─ Border: 3px solid transparent
├─ Border-top-color: #10b981
├─ Border-radius: 50%
├─ Animation: spin 1.5s linear infinite
└─ Delay: 0s

Ring 2
├─ Position: absolute
├─ Width: 48px
├─ Height: 48px
├─ Border: 3px solid transparent
├─ Border-top-color: #059669
├─ Border-radius: 50%
├─ Top: 6px
├─ Left: 6px
├─ Animation: spin 1.5s linear infinite
└─ Delay: 0.5s

Ring 3
├─ Position: absolute
├─ Width: 36px
├─ Height: 36px
├─ Border: 3px solid transparent
├─ Border-top-color: #34d399
├─ Border-radius: 50%
├─ Top: 12px
├─ Left: 12px
├─ Animation: spin 1.5s linear infinite
└─ Delay: 1s

Text Below Spinner
├─ Font-size: 14px
├─ Color: #6b7280
├─ Text-align: center
└─ Margin-top: 16px
```

---

### 6. CHARTS

#### Chart Container
```
├─ Background: White
├─ Border-radius: 12px
├─ Padding: 24px
├─ Box-shadow: 0 4px 12px rgba(0,0,0,0.08)
├─ Min-height: 350px
└─ Margin-bottom: 24px

Title
├─ Font-size: 18px
├─ Font-weight: 700
├─ Color: #1f2937
├─ Margin: 0 0 8px 0

Subtitle
├─ Font-size: 12px
├─ Color: #6b7280
├─ Margin: 0 0 24px 0
└─ Padding-bottom: 12px, border-bottom: 2px solid #f3f4f6
```

#### Pie Chart (Emissions Breakdown)
```
Size: 300px diameter
Colors:
├─ Scope 1: #ef4444 (Red)
├─ Scope 2: #3b82f6 (Blue)
└─ Scope 3: #a855f7 (Purple)

Animation: Slices grow from center
Duration: 0.8s per slice
Labels: Positioned outside with connector lines
Tooltip: Show on hover with value

Legend Below:
├─ 3 items in grid
├─ Each item: Colored square (12×12) + text
├─ Gap: 12px
├─ Alignment: Left-aligned
└─ Font: 12px, regular
```

#### Bar Chart (Company vs Benchmark)
```
Type: Vertical bars
Width: Full container
Height: 300px

Bars:
├─ Your Company: Gradient #10b981 → #059669
├─ Industry Benchmark: #d1d5db
├─ Width: 60px each
├─ Gap: 20px between pairs
├─ Border-radius: 8px top only

Axes:
├─ X-axis labels: Company | Industry
├─ Y-axis: tCO2e (0 to max value)
├─ Grid lines: Light gray (#f3f4f6)
└─ Font: 12px

Tooltip: Show exact values on hover
Animation: Bars grow from bottom on load
```

#### Reduction Roadmap Chart
```
Type: Horizontal or vertical bars
Shows: Before | After reduction

Bar 1 (Current):
├─ Color: #10b981
├─ Label: Current emissions
└─ Value: 13,190 tCO2e

Bar 2 (After):
├─ Color: #d1d5db
├─ Label: After reduction
└─ Value: 10,340 tCO2e

Highlight Reduction:
├─ Connector line between bars
├─ Reduction amount: 2,850 tCO2e
├─ Percentage: 21.6%
└─ Color: Green #10b981
```

---

### 7. SUMMARY CARDS

#### Summary Card Grid
```
Container
├─ Display: grid
├─ Grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))
├─ Gap: 24px
├─ Margin-bottom: 32px
└─ Animation: slide-up 0.5s ease-out
```

#### Individual Card
```
├─ Background: White
├─ Border-left: 4px solid (green/blue/purple)
├─ Border-radius: 12px
├─ Padding: 24px
├─ Box-shadow: 0 4px 12px rgba(0,0,0,0.08)
├─ Display: flex
├─ Gap: 24px
├─ Align-items: center
├─ Transition: all 0.3s ease
├─ Cursor: pointer
└─ Animation: slide-up 0.5s ease-out (staggered)

On Hover
├─ Transform: translateY(-4px)
└─ Box-shadow: 0 8px 24px rgba(0,0,0,0.12)

Icon Container
├─ Width: 56px
├─ Height: 56px
├─ Border-radius: 8px
├─ Display: flex
├─ Align-items: center
├─ Justify-content: center
├─ Flex-shrink: 0
├─ Icon-size: 32px
├─ Icon-color: White
└─ Background: Gradient (varies by card)

Card 1 (Total Emissions):
├─ Border-left: Green #10b981
├─ Icon-bg: Green gradient
└─ Icon: 🌿

Card 2 (vs Benchmark):
├─ Border-left: Blue #3b82f6
├─ Icon-bg: Blue gradient
└─ Icon: 🎯

Card 3 (Reduction Potential):
├─ Border-left: Purple #a855f7
├─ Icon-bg: Purple gradient
└─ Icon: 📉

Content Section
├─ Flex: 1
├─ Display: flex
├─ Flex-direction: column
└─ Gap: 4px

Label
├─ Font-size: 12px
├─ Font-weight: 500
├─ Color: #6b7280
├─ Text-transform: uppercase
├─ Letter-spacing: 0.5px
└─ Margin-bottom: 4px

Value
├─ Font-size: 28px
├─ Font-weight: 700
├─ Color: #1f2937
├─ Margin-bottom: 8px
└─ Line-height: 1.2

Subtitle/Status
├─ Font-size: 13px
├─ Font-weight: 500
├─ Color: Varies (green for positive, red for negative)
└─ Examples:
   ├─ "Annual carbon footprint"
   ├─ "Below industry average" (positive - green #059669)
   ├─ "Above industry average" (negative - red #dc2626)
   └─ "21.6% reduction possible"
```

---

### 8. OFFSET RECOMMENDATIONS BOX

#### Container
```
├─ Background: White
├─ Border-left: 4px solid #10b981
├─ Border-radius: 12px
├─ Padding: 24px
├─ Box-shadow: 0 4px 12px rgba(0,0,0,0.08)
├─ Display: flex
├─ Flex-direction: column
├─ Gap: 16px
└─ Animation: slide-up 0.5s ease-out
```

#### Header
```
├─ Display: flex
├─ Align-items: center
├─ Gap: 16px
├─ Padding-bottom: 12px
├─ Border-bottom: 2px solid #f3f4f6

Icon
├─ Size: 24px
├─ Color: #10b981
└─ Flex-shrink: 0

Title Area
├─ Flex: 1
├─ Title: 18px, 700 weight, #1f2937
├─ Subtitle: 12px, 400 weight, #6b7280
└─ Margin: 0
```

#### Offset Items List
```
├─ Display: flex
├─ Flex-direction: column
├─ Gap: 12px
└─ Padding: 12px 0

Offset Item
├─ Display: flex
├─ Align-items: center
├─ Gap: 12px
├─ Padding: 12px
├─ Background: #f0fdf4
├─ Border-left: 3px solid #10b981
├─ Border-radius: 6px

Checkmark Icon
├─ Width: 24px
├─ Height: 24px
├─ Border-radius: 50%
├─ Background: #10b981
├─ Color: White
├─ Display: flex
├─ Align-items: center
├─ Justify-content: center
├─ Font-size: 14px
├─ Font-weight: bold
├─ Flex-shrink: 0
└─ Content: "✓"

Item Text
├─ Font-size: 16px
├─ Font-weight: 500
├─ Color: #047857
└─ Flex: 1
```

#### Download Button
```
├─ Display: flex
├─ Align-items: center
├─ Justify-content: center
├─ Gap: 12px
├─ Width: 100%
├─ Height: 44px
├─ Background: Linear gradient #10b981 → #059669
├─ Color: White
├─ Border: None
├─ Border-radius: 8px
├─ Font: 16px, 600 weight
├─ Cursor: pointer
├─ Box-shadow: 0 4px 12px rgba(16,185,129,0.3)
├─ Transition: all 0.3s ease
├─ Margin-top: 12px
└─ Animation: slide-up 0.5s ease-out 0.1s backwards

On Hover
├─ Transform: translateY(-2px)
└─ Box-shadow: 0 6px 20px rgba(16,185,129,0.4)

Icon (Download)
├─ Size: 20px
└─ Color: White
```

---

This detailed component specification provides exact measurements, colors, spacing, and interactions for every component in the design. Use these specifications to create pixel-perfect designs in Figma.

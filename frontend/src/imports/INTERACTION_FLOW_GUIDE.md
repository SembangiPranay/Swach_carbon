# INTERACTION FLOW & USER JOURNEY MAP

## COMPLETE USER FLOW

### FLOW 1: SUCCESSFUL CALCULATION PATH

```
┌─ User Lands on App
│
├─ ✅ Sees attractive header with call-to-action
│
├─ ✅ Fills Multi-Step Form
│  ├─ Step 1: Company Details
│  ├─ Step 2: Energy & Fuel
│  └─ Step 3: Other Emissions
│
├─ ✅ Clicks "Calculate Emissions" Button
│  └─ Form validates & disables
│  └─ Loading spinner appears
│  └─ Button shows "Calculating..."
│
├─ ✅ Transitions to Streaming Panel
│  └─ Smooth fade/slide animation
│
├─ ✅ Watches Agent Thinking in Real-Time
│  ├─ Sees "Thought" events (blue)
│  ├─ Sees "Action" events (yellow)
│  ├─ Sees "Observation" events (purple)
│  ├─ Timeline animates smoothly
│  └─ Events appear with staggered timing
│
├─ ✅ Agent Completes Analysis
│  └─ Final "Complete" event appears (green)
│  └─ Completion message: "🎉 Analysis complete!"
│
├─ ✅ Clicks "View Results & Charts" Button
│  └─ Smooth transition to results page
│
├─ ✅ Sees Beautiful Results Dashboard
│  ├─ Summary cards animate in
│  ├─ Charts load with animations
│  ├─ Pie chart shows emissions breakdown
│  ├─ Bar chart shows company vs benchmark
│  ├─ Reduction roadmap visible
│  └─ Offset recommendations displayed
│
├─ ✅ Downloads PDF Report
│  └─ Clicks "Download Detailed Report"
│  └─ PDF file downloads to computer
│
└─ ✅ Can Calculate Again or Exit
   └─ "Calculate Again" button → back to form
```

---

### FLOW 2: ERROR HANDLING PATH

```
┌─ Form Submission Error
│  ├─ Invalid input detected
│  │  └─ Field highlights in red
│  │  └─ Error message appears below field
│  │  └─ "Submit" button remains disabled
│  │  └─ User corrects input
│  │  └─ Error clears, button enables
│  │
│  └─ Form submits successfully
│
├─ Network Error During Calculation
│  ├─ Streaming fails
│  └─ Error card appears:
│     ├─ ❌ Error icon
│     ├─ "Connection lost" message
│     └─ "Try Again" button
│
├─ User Clicks "Try Again"
│  ├─ Form resets
│  ├─ Page returns to form
│  └─ User can re-submit
│
└─ LLM Fallback (Silent)
   ├─ Groq API fails
   ├─ System automatically tries Gemini
   ├─ User continues without knowing
   └─ Results are still accurate
```

---

### FLOW 3: MOBILE USER EXPERIENCE

```
┌─ Mobile User Lands on App
│
├─ ✅ Sees Full-Screen Header
│  ├─ Logo centered (smaller)
│  ├─ Tagline visible
│  └─ All text readable
│
├─ ✅ Fills Form (Optimized for Mobile)
│  ├─ Step indicator at top
│  ├─ One step visible at a time
│  ├─ Large touch targets (44px+)
│  ├─ Full-width input fields
│  ├─ Numeric keyboard for numbers
│  ├─ Native select dropdown
│  └─ Previous/Next buttons full-width
│
├─ ✅ Transitions to Streaming Panel
│  ├─ Timeline fits in viewport
│  ├─ Scrollable for longer sequences
│  ├─ Text wraps properly
│  └─ Touch-friendly spacing
│
├─ ✅ Sees Results Dashboard
│  ├─ Cards stack vertically
│  ├─ Charts display at 100% width
│  ├─ No horizontal scrolling
│  ├─ Text remains readable
│  ├─ Download button full-width
│  └─ Bottom action buttons stacked
│
└─ ✅ Downloads PDF
   └─ Opens in native PDF viewer
```

---

## DETAILED INTERACTION SPECIFICATIONS

### INTERACTION 1: Form Field Validation

**Real-Time Validation (Optional Enhancement)**
```
When user types:
  ├─ Timer: 500ms after user stops typing
  ├─ Validate field
  ├─ Show success state (green border)
  │  └─ Small green checkmark icon
  ├─ OR show error state (red border)
  │  └─ Error message below field
  └─ Enable/disable Next button accordingly
```

**On Form Submit**
```
1. Check all fields are valid
2. If any invalid:
   ├─ Field highlights in red
   ├─ Error message shows below
   ├─ Focus moves to first invalid field
   └─ Button stays disabled
3. If all valid:
   ├─ Button shows loading state
   ├─ Form disabled (all inputs grayed out)
   └─ API call initiated
```

---

### INTERACTION 2: Multi-Step Form Navigation

**Moving Between Steps**
```
User clicks "Next":
  1. Validate current step fields
  2. If validation fails:
     ├─ Show error messages
     └─ Stay on current step
  3. If validation passes:
     ├─ Animate current step out (fade)
     ├─ Update step indicator
     ├─ Animate next step in (slide up)
     ├─ Scroll to top of form
     ├─ Focus first field of new step
     └─ "Previous" button now enabled

User clicks "Previous":
  1. No validation needed
  2. Animate current step out (fade)
  3. Update step indicator
  4. Animate previous step in (slide up)
  5. Scroll to top of form
  6. Focus first field of previous step
  7. On step 1: "Previous" button disabled

Step Indicator Animation:
  ├─ Active step circle: Scale up 1.1x
  ├─ Active step color: Green gradient
  ├─ Completed steps: Show checkmark
  ├─ Inactive steps: Gray
  └─ Line connecting steps: Highlight as you progress
```

---

### INTERACTION 3: Form Submission to Streaming

**Transition Animation**
```
1. User clicks "Calculate Emissions"
   ├─ Button shows spinner
   ├─ Button text changes to "Calculating..."
   ├─ All form inputs disabled

2. API call to POST /calculate
   ├─ Backend returns calculation_id
   ├─ Frontend transitions to streaming page

3. Page Transition:
   ├─ Current page (form) fades out
   ├─ New page (streaming) fades in
   ├─ Smooth duration: 0.3s
   ├─ Scroll to top automatically
   └─ All animations complete before user sees content
```

---

### INTERACTION 4: Real-Time Streaming Events

**Timeline Event Appearance**
```
Each event appears with sequence:

1. Timeline line grows (animation)
   ├─ Start: 0 height
   ├─ End: Full height to next event
   ├─ Duration: 0.3s with event
   └─ Color: Gradient fade

2. Event node animates in
   ├─ Start: Scale 0, opacity 0
   ├─ End: Scale 1, opacity 1
   ├─ Duration: 0.4s
   └─ Icon rotates slightly

3. Event card slides in
   ├─ Start: translateX(-10px), opacity 0
   ├─ End: translateX(0), opacity 1
   ├─ Duration: 0.4s
   ├─ Delay: 0.1s after node
   └─ Text gradually becomes visible

4. Scroll automatically
   ├─ New events scroll into view
   ├─ Smooth scroll behavior
   └─ User always sees latest event
```

**Event Styling (Interactive)**
```
When hovering over event (desktop):
  ├─ Card shadow increases
  ├─ Background slightly brightens
  └─ Text remains same (no hover text changes)

On mobile (no hover):
  ├─ Just display events
  └─ No hover effects
```

---

### INTERACTION 5: Chart Interactions

**Pie Chart (Emissions Breakdown)**
```
On Page Load:
  ├─ Chart animates in
  ├─ Slices grow from center
  ├─ Each slice animated sequentially
  ├─ Duration: 0.8s per slice
  └─ Stagger delay: 0.1s

On Hover (Desktop):
  ├─ Hovered slice highlights
  ├─ Tooltip appears with exact values
  ├─ Other slices slightly dim
  └─ Legend item corresponding to slice highlights

On Mobile:
  ├─ No hover effects
  ├─ Tap to see tooltip
  ├─ Legend always visible below
  └─ All slices visible
```

**Bar Chart (Company vs Benchmark)**
```
On Page Load:
  ├─ Bars animate in from bottom
  ├─ Grid lines animate in
  ├─ Labels fade in
  ├─ Duration: 0.8s
  └─ Stagger: 0.1s between bars

On Hover (Desktop):
  ├─ Bar highlights (shadow increases)
  ├─ Tooltip shows exact value
  ├─ Other bar slightly dims
  └─ Label becomes bolder

On Mobile:
  ├─ Tap to see value
  ├─ All labels visible
  └─ No dim effect
```

---

### INTERACTION 6: Button States & Feedback

**Primary Button States**

```
Default (Enabled):
├─ Color: Green gradient
├─ Cursor: pointer
├─ Opacity: 1
└─ Box-shadow: 0 4px 12px

Hover (Desktop):
├─ Transform: translateY(-2px)
├─ Box-shadow: 0 6px 20px (increased)
├─ Duration: 0.3s
└─ Slightly brighter gradient

Active/Pressed:
├─ Transform: translateY(0)
├─ Shadow returns to normal
├─ Duration: 0.1s
└─ User feels tactile feedback

Disabled:
├─ Opacity: 0.5
├─ Cursor: not-allowed
├─ No hover effects
└─ No shadow changes

Loading:
├─ Cursor: wait
├─ Button disabled
├─ Text: "Calculating..."
├─ Icon: Rotating spinner
└─ Button remains green but visually less interactive
```

---

### INTERACTION 7: Form Input Focus States

**Text Input Focus**
```
Normal State:
├─ Border: 2px solid #e5e7eb (light gray)
├─ Background: White
├─ Placeholder visible in light gray
└─ Shadow: Subtle

On Focus:
├─ Border: 2px solid #10b981 (green)
├─ Box-shadow: 0 0 0 3px rgba(16,185,129,0.1)
├─ Background: #f9fafb (very light)
├─ Placeholder: Fades out smoothly
├─ Text cursor: Visible
└─ Duration: 0.2s transition

On Type:
├─ Continue showing green border
├─ Show green checkmark if valid (optional)
├─ Clear placeholder
└─ Show typed text

On Error (While Focused):
├─ Border: 2px solid #ef4444 (red)
├─ Box-shadow: 0 0 0 3px rgba(239,68,68,0.1)
├─ Error message: Appears below
├─ Duration: 0.2s transition
└─ Continue showing error until corrected

On Blur (Leave Field):
├─ Show validation result (green or red)
├─ If error: Keep showing error message
├─ If valid: Show subtle success indicator
└─ Border returns to light gray if valid
```

---

### INTERACTION 8: Loading & Waiting States

**Loading Spinner (During Calculation)**
```
Container:
├─ Position: Centered in timeline
├─ Margin-bottom: 24px

Rings Animation:
├─ Ring 1: Rotate 360deg (1.5s linear) - Delay 0s
├─ Ring 2: Rotate 360deg (1.5s linear) - Delay 0.5s
├─ Ring 3: Rotate 360deg (1.5s linear) - Delay 1s
├─ Repeat: Infinite
└─ Colors: Green shades from dark to light

Text Below:
├─ "Starting AI analysis..."
├─ Font-size: 14px
├─ Color: #6b7280
├─ Fade in animation: 0.3s
└─ Stays visible until first event
```

**Progress Indication**
```
Form Submit:
├─ Button spinner: ⚙️ rotating
├─ Text: "Calculating..."
├─ Opacity: 1 (fully visible)

Streaming:
├─ Status badge (top right): Pulsing dot
├─ Text: "Analyzing..."
├─ Color: Blue background
└─ Badge updates when complete (green checkmark)
```

---

### INTERACTION 9: Success & Completion

**Form Submit Success**
```
1. Button shows success state
   ├─ Text changes to "✓ Submitted"
   ├─ Icon: CheckCircle (stays)
   ├─ Color: Remains green
   └─ Duration: 0.5s

2. Page transitions
   ├─ Form fades out
   ├─ Streaming panel fades in
   └─ Automatic scroll to top
```

**Streaming Complete**
```
1. Final "Complete" event appears
   ├─ Event type: complete (green)
   ├─ Icon: ✅
   ├─ Message: "Analysis complete"
   └─ Animation: Normal slide-in

2. Completion message appears
   ├─ Icon: 🎉 (bounces in)
   ├─ Title: "Analysis complete!"
   ├─ Message: "Results ready for download"
   └─ Background: Light green gradient

3. Action button appears
   ├─ Text: "View Results & Charts →"
   ├─ Animation: Slide up into view
   ├─ Fade in: 0.4s
   └─ Ready to click immediately
```

**Results Dashboard Complete**
```
1. Summary cards animate in
   ├─ Card 1: Slide up 0.5s, delay 0s
   ├─ Card 2: Slide up 0.5s, delay 0.1s
   └─ Card 3: Slide up 0.5s, delay 0.2s

2. Charts animate in
   ├─ Chart 1: Bars grow from bottom 0.8s
   ├─ Chart 2: Pie slices appear sequentially
   └─ Duration: 1.2s total

3. Offset box animates in
   ├─ Slide up: 0.5s
   ├─ Delay: 0.3s
   └─ Items appear sequentially within

4. User can immediately download PDF
   └─ Click "Download Detailed Report"
```

---

### INTERACTION 10: Error & Retry

**Network Error**
```
1. Error occurs during streaming
   ├─ Event stream stops
   ├─ Error event appears (red)
   ├─ Message: "Connection lost - Retrying..."
   └─ System attempts automatic reconnect

2. Automatic retry mechanism
   ├─ Wait: 2 seconds
   ├─ Attempt reconnection
   ├─ Show spinner during retry
   └─ Max 3 attempts

3. If reconnect fails
   ├─ Error card appears:
   │  ├─ ❌ Error icon
   │  ├─ Message: "Failed to calculate"
   │  ├─ Explanation: "Please try again"
   │  └─ "Try Again" button appears
   │
   └─ User clicks "Try Again"
      ├─ Returns to form
      ├─ Form fields preserved (optional)
      ├─ Can resubmit
      └─ New calculation starts
```

**Form Validation Error**
```
1. User submits form with missing fields
   ├─ Next button clicked but validation fails

2. Invalid fields highlight
   ├─ Border: Red #ef4444
   ├─ Icon: ❌
   └─ Message: "This field is required"

3. Focus management
   ├─ Focus moves to first invalid field
   ├─ Scroll to show field
   ├─ Keyboard ready for input
   └─ User can type to fix

4. As user corrects
   ├─ Invalid state clears
   ├─ Border returns to normal
   ├─ Error message disappears
   └─ Next button re-enables
```

---

## MICRO-INTERACTIONS & POLISH

### Subtle Hover Effects
```
Buttons:
├─ Slight scale: 1.02x (very subtle)
├─ Shadow increase: +2px
└─ Duration: 0.3s ease

Cards:
├─ Shadow increase: 0.08 → 0.12 rgba
├─ Slight lift: translateY(-4px)
└─ Duration: 0.3s ease

Links:
├─ Color change
├─ Underline appears
└─ Duration: 0.2s ease
```

### Scroll Behavior
```
Smooth scrolling:
├─ New timeline events: Auto-scroll into view
├─ Duration: 0.6s smooth
├─ Behavior: Smooth (not instant)
└─ Position: Center of viewport if possible

Page transitions:
├─ Auto-scroll to top
├─ Duration: 0.3s smooth
└─ Behavior: Smooth

Navigation:
├─ Next step: Scroll to top of form
├─ Duration: 0.3s smooth
└─ Behavior: Smooth
```

### Keyboard Navigation
```
Tab Order (Form):
1. Company Name field
2. Industry Type field
3. Employee Count field
4. Previous button
5. Next button

Tab Order (Results):
1. Summary Card 1
2. Summary Card 2
3. Summary Card 3
4. Offset items (each)
5. Download button
6. Calculate Again button

Focus Indicator:
├─ Outline: 2px solid #10b981
├─ Outline-offset: 2px
├─ Border-radius: Match element
└─ Visible on all interactive elements
```

---

## ANIMATION TIMING

### Standard Animation Durations

```
Fast: 0.2s
  └─ Focus states, small transitions

Normal: 0.3-0.4s
  └─ Button hover, form transitions

Slow: 0.6-0.8s
  └─ Page transitions, chart animations
```

### Easing Functions

```
ease-out:
  └─ Page load animations, user feels immediate response

ease-in-out:
  └─ Smooth transitions, natural movement

ease:
  └─ General transitions

linear:
  └─ Continuous animations (spinner, loading)
```

---

This interaction guide ensures smooth, delightful user experience with clear visual and interaction feedback throughout the application.

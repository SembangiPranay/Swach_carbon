# PROJECT ROADMAP — Swach AI Carbon Agent
## Current: Week 1 COMPLETE → Week 2 READY TO START

---

## 🗺️ 28-DAY JOURNEY

```
┌─────────────────────────────────────────────────────────────┐
│ WEEK 1: FOUNDATION (Days 1-7) ✅ COMPLETE                  │
├─────────────────────────────────────────────────────────────┤
│ ✅ Day 1-2:   GHG Calculator (700 lines, 42 tests)         │
│ ✅ Day 3-4:   Tavily Search + ChromaDB (tools working)      │
│ ✅ Day 5-6:   PDF Generator (ReportLab framework)           │
│ ✅ Day 7:     LangChain ReAct Agent (orchestration)         │
│                                                              │
│ 📦 Deliverable: Terminal-based agent running successfully   │
│ 📊 Code: 1,700+ lines | Tests: 42 passing | Tech debt: 0   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ WEEK 2: BACKEND API (Days 8-14) 🔨 YOU ARE HERE            │
├─────────────────────────────────────────────────────────────┤
│ 🔨 Day 8-9:   FastAPI Endpoints (/calculate, /stream,      │
│               /report, /health)                             │
│ 🔨 Day 10-11: SSE Streaming (real-time agent thoughts)     │
│ 🔨 Day 12-13: Error Handling + LLM Fallback                │
│ 🔨Day 14:     Integration Testing (all endpoints)          │
│                                                              │
│ 📦 Deliverable: REST API ready for frontend                │
│ 🎯 Focus: Server-Sent Events streaming (key feature!)      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ WEEK 3: REACT FRONTEND (Days 15-21) ⏳ READY WHEN DONE      │
├─────────────────────────────────────────────────────────────┤
│ ⏳ Day 15-16: Multi-step form + project setup              │
│ ⏳ Day 17-18: Live agent thinking panel (visual streaming) │
│ ⏳ Day 19:    Results dashboard + charts                   │
│ ⏳ Day 20:    PDF download integration                     │
│ ⏳ Day 21:    Full QA + polish                             │
│                                                              │
│ 📦 Deliverable: Deployed React app on Vercel              │
│ 🎯 Focus: User-friendly multi-step interface              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ WEEK 4: PRODUCTION (Days 22-28) ⏳ COMING SOON             │
├─────────────────────────────────────────────────────────────┤
│ ⏳ Day 22-23: Deploy backend to Render                     │
│ ⏳ Day 24:    Deploy frontend to Vercel                   │
│ ⏳ Day 25-26: GitHub README + architecture diagram        │
│ ⏳ Day 27:    Demo video (2 min)                           │
│ ⏳ Day 28:    LinkedIn post + portfolio                   │
│                                                              │
│ 📦 Deliverable: Live production app + portfolio assets    │
│ 🎯 Focus: Polish + storytelling                           │
└─────────────────────────────────────────────────────────────┘

Overall: [████████████░░░░░░░░░░░░] 50% COMPLETE
```

---

## 🎯 WHAT YOU'RE BUILDING IN PHASE 2

### The Problem Phase 2 Solves

**Week 1's Terminal Agent:**
```bash
$ python backend/agent.py
Thought: Calculating emissions...
Action: Call ghg_calculator...
Observation: Scope1=1540, Scope2=8200...
[output in terminal]
```

❌ **Problem:** Only you can run this. Not accessible to others. No web UI.

---

### Phase 2 Solution: Web API

```
┌──────────────────────┐
│   React Frontend     │
│   (Week 3)           │
└──────────┬───────────┘
           │ HTTP/SSE
           ↓
┌──────────────────────────────────────┐
│   FastAPI Backend (Phase 2) 🔨       │
│                                      │
│ POST /calculate                      │
│  ├─ Receives: {company_name, ...}   │
│  └─ Returns: {calculation_id: UUID} │
│                                      │
│ GET /stream?id=UUID                  │
│  ├─ Server-Sent Events              │
│  └─ Streams: Thought→Action→Obs      │
│                                      │
│ GET /report?id=UUID                  │
│  ├─ Serves: PDF binary               │
│  └─ Downloads: carbon_report.pdf     │
│                                      │
│ GET /health                          │
│  └─ Returns: {"status": "healthy"}   │
└──────────┬───────────────────────────┘
           │ Python function calls
           ↓
┌──────────────────────────────────────┐
│   LangChain ReAct Agent (Week 1) ✅   │
├──────────────────────────────────────┤
│ └─ All 4 Tools orchestrated          │
│    ├─ GHG Calculator                 │
│    ├─ Tavily Search                  │
│    ├─ ChromaDB Retriever             │
│    └─ PDF Generator                  │
└──────────────────────────────────────┘
```

✅ **Solution:** API is now web-accessible. React can call it. Multiple users can access simultaneously.

---

## 📋 PHASE 2 DELIVERABLES

### Day 8-9: 4 FastAPI Endpoints
```python
# Endpoint 1: Start calculation
POST /calculate
Request:  {"company_name": "TechCorp", "diesel_litres": 500, ...}
Response: {"calculation_id": "abc-123-def"}

# Endpoint 2: Stream agent thoughts (SSE)
GET /stream?id=abc-123-def
Response: [Server-Sent Events stream]
  data: {"type": "thought", "content": "Calculating..."}
  data: {"type": "action", "content": "Calling calculator..."}
  data: {"type": "observation", "content": "Scope1=1540..."}
  [continues for all agent steps]

# Endpoint 3: Download PDF report
GET /report?id=abc-123-def
Response: [Binary PDF file]
Browser: Triggers download of "carbon_report_abc-123-def.pdf"

# Endpoint 4: Health check
GET /health
Response: {"status": "healthy", "timestamp": "2026-04-23T10:15:30"}
```

### Day 10-11: SSE Streaming Magic

**What happens in real-time:**

```
User Action:
  [Click "Calculate Emissions" button]
           ↓
Frontend:
  POST /calculate with company data
  Receive: calculation_id = "xyz789"
           ↓
Frontend:
  Open EventSource to /stream?id=xyz789
           ↓
Backend (Background thread):
  1. Start agent execution
  2. Capture each reasoning step:
     - "Thought: Need to calculate..."
     - "Action: ghg_calculator(...)"
     - "Observation: Got results"
     - "Thought: Now search for offsets..."
     - "Action: search_carbon_offsets(...)"
     - [continues through all tools]
  3. Emit each step as SSE event
           ↓
Frontend (Real-time):
  Receives events in sequence
  Displays them in Agent Thinking Panel:
  
  "💭 Thought: I need to calculate emissions..."
  "⚙️ Action: Calling GHG calculator..."
  "👁️ Observation: Scope1=1540, Scope2=8200..."
  [etc. - user sees it happening in real-time!]
           ↓
Backend:
  Agent finishes
  PDF generated and saved
  Emits final "complete" event
           ↓
Frontend:
  Sees "complete" event
  Calls GET /report?id=xyz789
  Triggers PDF download
  Shows results dashboard
```

**Why this is impressive:**
- User sees the AI "thinking" step-by-step
- Builds trust (not a black box)
- Differentiator from other tools
- Interview talking point: "Built streaming agent reasoning UI"

### Day 12-13: Production Resilience

```python
# Error Handling Examples:

# 1. Invalid input → Pydantic validates automatically
POST /calculate with {"electricity_kwh": "abc"}
Response: 422 Unprocessable Entity
{
  "detail": [
    {
      "loc": ["body", "electricity_kwh"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}

# 2. LLM fallback (automatic)
Groq API is down
  → System tries Groq (fails)
  → Automatically switches to Gemini
  → User never sees downtime!
  → Agent completes successfully

# 3. Rate limiting
Same IP makes >1 request per 5 seconds
Response: 429 Too Many Requests
{"detail": "Rate limit exceeded. Try again in 5 seconds"}

# 4. Missing calculation
GET /report?id=nonexistent-id
Response: 404 Not Found
{"detail": "Calculation not found"}
```

### Day 14: Integration Testing

```bash
# Run full end-to-end test
pytest backend/tests/test_api.py -v

# Output:
test_calculate_endpoint PASSED           ✓
test_stream_endpoint PASSED              ✓
test_report_download PASSED              ✓
test_health_check PASSED                 ✓
test_invalid_input PASSED                ✓
test_llm_fallback PASSED                 ✓
test_rate_limiting PASSED                ✓
test_concurrent_calculations PASSED      ✓
test_error_handling PASSED               ✓
test_cors_headers PASSED                 ✓

=============== 10 passed in 2.34s ===============
```

---

## 🔑 KEY ARCHITECTURAL DECISIONS

### 1. Why SSE Instead of WebSocket?
| Feature | SSE | WebSocket |
|---------|-----|-----------|
| Complexity | Simple (HTTP) | Complex (different protocol) |
| Browser Support | Modern browsers | Same |
| Refresh | Auto-reconnect | Manual |
| Direction | Server→Client ✓ | Bidirectional |
| Use Case | Perfect for streaming agent thoughts | Overkill |

**Decision:** SSE (simpler, perfect for this use case)

### 2. Background Task Execution
- Use: FastAPI's `BackgroundTasks`
- Don't use: Celery (overkill for MVP)
- Later: Consider Celery/Redis if 100+ concurrent users

### 3. Calculation Storage
```python
# In-memory dict (Week 2)
calculations = {
    "abc-123": {
        "id": "abc-123",
        "status": "running",  # or "complete" or "failed"
        "data": {...},
        "results": {...},
        "pdf_path": "reports/abc-123.pdf",
        "created_at": "2026-04-23T10:00:00",
        "thoughts": [...]
    }
}

# Week 4 upgrade: Redis
# For now: In-memory is fine (single server)
```

---

## 📊 PHASE 2 IMPACT ON PROJECT

### Before Phase 2 (Week 1):
- ❌ API doesn't exist
- ❌ Frontend can't access agent
- ❌ No way to demo to stakeholders
- ❌ Can't show real-time reasoning
- ❌ Not production-ready

### After Phase 2 (End of Week 2):
- ✅ REST API fully functional
- ✅ Frontend will be able to call it
- ✅ Real-time SSE streaming works
- ✅ Can demo to anyone (Swagger UI)
- ✅ Production-ready backend
- ✅ Ready for Week 3 React integration

### Skills Demonstrated:
- ✅ FastAPI (modern, async Python web framework)
- ✅ Server-Sent Events (real-time streaming)
- ✅ Error handling (Pydantic validation, fallback logic)
- ✅ Production patterns (logging, rate limiting, CORS)
- ✅ Integration testing (end-to-end API tests)
- ✅ LLM integration patterns (Groq + Gemini fallback)

---

## 🎯 HOW WEEK 2 CONNECTS TO WEEK 3

**Phase 2 (Backend API):**
```bash
POST http://localhost:8000/calculate
GET http://localhost:8000/stream?id=xyz
GET http://localhost:8000/report?id=xyz
```

**Week 3 (React Frontend):**
```jsx
// Simple fetch call from React
const response = await fetch('http://localhost:8000/calculate', {
  method: 'POST',
  body: JSON.stringify(formData)
});
const { calculation_id } = await response.json();

// Open SSE connection
const eventSource = new EventSource(`/stream?id=${calculation_id}`);
eventSource.onmessage = (event) => {
  // Display agent thoughts in UI
};

// Download report
window.location.href = `/report?id=${calculation_id}`;
```

**Because Phase 2 is clean and well-designed:**
- React code is simple and maintainable
- Frontend developers don't need to understand the agent
- They just call endpoints and consume responses
- Perfect separation of concerns

---

## ⏱️ TIME BREAKDOWN

| Phase | Days | Hours/Day | Total Hours | Complexity |
|-------|------|-----------|-------------|------------|
| Week 1 | 1-7 | 3-4 | 21-28 | ⭐⭐⭐ HIGH |
| **Week 2** | **8-14** | **1.5-2** | **10-14** | ⭐⭐ MEDIUM |
| Week 3 | 15-21 | 2-3 | 14-21 | ⭐⭐ MEDIUM |
| Week 4 | 22-28 | 1-2 | 7-14 | ⭐ LOW |

**Phase 2 is shorter because:**
- Week 1 did the hard part (agent + tools)
- Phase 2 is "just" exposing it via HTTP
- No new ML/AI complexity
- Mostly FastAPI boilerplate

---

## 🚀 START PHASE 2

### Prerequisites (Verify):
```bash
# 1. All Week 1 tools working
cd backend
python -c "from tools.calculator import ghg_calculator; print('✓')"
python -c "from tools.search import search_carbon_offsets; print('✓')"
python -c "from tools.retriever import retrieve_ghg_knowledge; print('✓')"
python -c "from tools.pdf_gen import generate_pdf_report; print('✓')"

# 2. Agent orchestration working
python -c "from agent import CarbonFootprintAgent; print('✓')"

# 3. Dependencies installed
pip install fastapi uvicorn python-multipart

# 4. API keys ready
echo $GROQ_API_KEY && echo $TAVILY_API_KEY && echo $GEMINI_API_KEY
```

### Ready? Start Day 8:
1. Review `PHASE2_PLAN.md` (this file)
2. Create `backend/main.py` with FastAPI app
3. Define Pydantic models in `backend/models.py`
4. Build `/calculate` endpoint first
5. Test in Swagger UI: `http://localhost:8000/docs`

---

## 📝 SUCCESS CHECKLIST

By end of Phase 2:
- [ ] FastAPI server runs without errors
- [ ] Swagger UI shows all 4 endpoints
- [ ] `/calculate` accepts company data
- [ ] `/stream` sends agent thoughts in real-time (SSE)
- [ ] `/report` downloads PDF successfully
- [ ] `/health` returns healthy status
- [ ] Invalid inputs return 422 errors
- [ ] Groq→Gemini fallback works
- [ ] All integration tests passing (10/10)
- [ ] Code is documented and readable

---

## 🎓 INTERVIEW VALUE

**When asked: "Walk me through a project you built"**

"I built Swach AI Carbon Agent. Week 1, I created 4 specialized tools and orchestrated them with LangChain ReAct. Week 2 (what I'm doing now), I'm building a FastAPI backend that exposes this agent via REST API with **Server-Sent Events streaming** so the frontend can display the agent's thinking in real-time.

Why is this impressive?
- Most people just call an LLM once. I built a multi-step reasoning system.
- Real-time streaming makes the AI transparent (not a black box).
- The architecture separates concerns cleanly (agent logic separate from API layer).
- Production patterns are baked in (error handling, LLM fallback, rate limiting)."

---

**Ready to build? Let's go Phase 2! 🚀**

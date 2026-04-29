# PHASE 2 PLAN — Backend API & FastAPI Integration
## Days 8-14 (7 days, ~3 hours/day = 21 hours total)

**Checkpoint Date:** By April 30, 2026  
**Target:** Complete FastAPI backend with SSE streaming + PDF integration  
**Outcome:** API ready for React frontend integration

---

## 📋 EXECUTIVE SUMMARY

**What You Have (Week 1 Complete):**
- ✅ Tool 1: GHG Calculator (700 lines, 42 tests passing)
- ✅ Tool 2: Tavily Search (real-time API working)
- ✅ Tool 3: ChromaDB Retriever (knowledge base framework ready)
- ✅ Tool 4: PDF Generator (framework complete)
- ✅ LangChain ReAct Agent (all tools wired up)

**What You're Building (Week 2):**
- 🔨 FastAPI web server to expose agent as HTTP API
- 🔨 Server-Sent Events (SSE) streaming for real-time agent thoughts
- 🔨 Request validation (Pydantic models)
- 🔨 Error handling + logging
- 🔨 End-to-end integration testing

**Why This Matters:**
Week 1 built a terminal-based agent. Week 2 makes it web-accessible. Week 3's React frontend will call these endpoints.

---

## 🎯 PHASE 2 BREAKDOWN

### Day 8-9: FastAPI Endpoints (3 hours)

**What to Build:**
1. `POST /calculate` — Accept company data, queue agent task
2. `GET /stream?id=uuid` — Stream agent thoughts via SSE
3. `GET /report?id=uuid` — Download generated PDF
4. `GET /health` — Health check for monitoring

**File: `backend/main.py`**
- FastAPI app initialization
- CORS middleware for Vercel frontend
- Background task runner (agent execution)
- SSE event generator
- File serving for PDFs

**File: `backend/models.py`**
- `ActivityDataRequest` (Pydantic) — all input fields
- `CalculationResponse` — what `/calculate` returns
- `StreamEvent` — what SSE sends
- `HealthResponse` — what `/health` returns

**Expected Output:**
```bash
$ python -m uvicorn backend.main:app --reload
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     API docs at http://127.0.0.1:8000/docs
```

Test in browser: `http://localhost:8000/docs` (Swagger UI auto-generated)

---

### Day 10-11: SSE Streaming Setup (3 hours)

**What to Build:**
- Real-time streaming of agent reasoning
- Thought → Action → Observation loop visible in browser
- Each agent step captured and sent to connected frontend

**File: `backend/streaming.py` (new)**
- `StreamManager` class to handle concurrent calculations
- Convert agent verbose output to SSE events
- Buffer thoughts, actions, observations

**How It Works:**
```
Frontend POST /calculate
   ↓
Backend generates calculation_id
   ↓
Backend starts agent in background thread
   ↓
Frontend connects to GET /stream?id=calculation_id
   ↓
SSE sends each agent reasoning step in real-time:
   "Thought: Calculating emissions..."
   "Action: ghg_calculator(...)"
   "Observation: Scope1=1540, Scope2=8200..."
   [Agent continues]
   ↓
When agent finishes, SSE sends "complete" event
   ↓
Frontend calls GET /report to download PDF
```

**Expected Output:**
```javascript
// Browser console when connected to SSE stream:
connected to /stream?id=abc123
{"type":"thought", "content":"I need to calculate this company's emissions..."}
{"type":"action", "content":"Calling ghg_calculator..."}
{"type":"observation", "content":"scope1_kg=1540, scope2_kg=8200..."}
[continues]
{"type":"complete"}
```

---

### Day 12-13: Error Handling & Logging (2 hours)

**What to Build:**
- Graceful error handling for invalid inputs
- Fallback from Groq → Gemini LLM if Groq fails
- Request validation with Pydantic
- Structured logging (JSON format)
- Rate limiting (1 req/5sec per IP)

**File: `backend/middleware.py` (new)**
- CORS configuration
- Request logging middleware
- Error response standardization
- Rate limit middleware

**File: `backend/config.py` (new)**
- Environment variable loading
- API key validation on startup
- Timeout configurations
- Logging setup

**Expected Behavior:**
```bash
# Invalid input → 422 Unprocessable Entity
POST /calculate with {electricity_kwh: "abc"}
Response: {"detail": "electricity_kwh must be a number"}

# Too many requests → 429 Too Many Requests
POST /calculate 10 times in 10 seconds
Response: {"detail": "Rate limit exceeded. Try again in 5 seconds"}

# LLM failure → automatic fallback
Groq API down? → Gemini takes over
User never sees downtime in demo
```

---

### Day 14: Integration Testing (2 hours)

**What to Build:**
- End-to-end test script
- Verify all 4 tools work through API
- Test SSE streaming
- Test PDF generation and download

**File: `backend/tests/test_api.py` (new)**
```python
def test_calculate_endpoint():
    # POST /calculate
    response = POST to /calculate with sample data
    assert response.status == 200
    assert "calculation_id" in response

def test_stream_endpoint():
    # GET /stream?id=xyz
    response = GET /stream?id=xyz
    assert response.content_type == "text/event-stream"
    assert receives thoughts/actions/observations
    assert receives "complete" event

def test_report_endpoint():
    # GET /report?id=xyz
    response = GET /report?id=xyz
    assert response.content_type == "application/pdf"
    assert PDF file is valid

def test_error_cases():
    # Missing required fields
    # Invalid data types
    # Non-existent calculation_id
```

**Run Tests:**
```bash
pytest backend/tests/test_api.py -v
# Output: 10/10 tests passing ✓
```

---

## 📁 FILE STRUCTURE (Week 2 Complete)

```
backend/
├── main.py                          # FastAPI app + 4 endpoints
├── models.py                        # Pydantic request/response models
├── config.py                        # Environment + logging setup
├── middleware.py                    # CORS, rate limit, logging
├── streaming.py                     # SSE stream management
├── agent.py                         # LangChain ReAct agent (Week 1)
├── tools/
│   ├── __init__.py
│   ├── calculator.py               # GHG calculations
│   ├── search.py                   # Tavily web search
│   ├── retriever.py                # ChromaDB knowledge base
│   └── pdf_gen.py                  # ReportLab PDF generation
├── tests/
│   ├── __init__.py
│   ├── test_api.py                 # Integration tests
│   └── test_tools.py               # Tool-level tests (Week 1)
├── data/
│   ├── chroma_db/                  # Vector database
│   └── ghg-protocol-revised.pdf    # Knowledge base
├── reports/                         # Generated PDFs stored here
├── .env                             # API keys (git-ignored)
├── .gitignore                       # Ignore .env, reports/, venv/
├── requirements.txt                 # Python dependencies
└── Dockerfile                       # For Render deployment (Week 4)
```

---

## ⏱️ DAILY BREAKDOWN

| Day | Task | Time | Deliverable |
|-----|------|------|-------------|
| 8 | Setup FastAPI + /calculate endpoint | 1.5 hrs | POST endpoint working in Swagger |
| 9 | Finish /stream + /report + /health | 1.5 hrs | All 4 endpoints + Swagger docs |
| 10 | SSE streaming capture + emit | 1.5 hrs | Agent thoughts streaming in curl |
| 11 | Frontend SSE integration prep | 1.5 hrs | React can subscribe to /stream |
| 12 | Error handling + fallback LLM | 1.5 hrs | Groq→Gemini fallback tested |
| 13 | Logging + rate limiting | 0.5 hrs | Structured JSON logs |
| 14 | End-to-end testing + Swagger test | 2 hrs | All tests passing, API ready |

**Total: 10 hours** (spread across 7 days = 1-2 hrs/day)

---

## 🔑 KEY DECISIONS FOR PHASE 2

### 1. **Background Task Execution**
- Use: `FastAPI BackgroundTasks`
- Alternative: Celery (overkill for this scale)
- Why: SimpleTask execution in async context, no external queue needed

### 2. **SSE vs WebSocket**
- Use: **SSE** (Server-Sent Events)
- Why: One-directional (server → frontend), simpler, HTTP/2 friendly
- When SSE closes: Frontend polls `/report` endpoint to get PDF

### 3. **In-Memory vs Redis**
- Use: **In-memory dict** for Phase 2
- Upgrade to: Redis for Week 4 production (if scaling)
- For now: Single server, in-memory is fine

### 4. **Calculation Storage**
- Store 1 calculation per `calculation_id` UUID
- Auto-expire after 24 hours (production needs cleanup)
- Include: status (running/complete/failed), results, PDF path, timestamps

### 5. **PDF Storage**
- Save to: `backend/reports/{calculation_id}.pdf`
- Served via: FastAPI `FileResponse`
- Cleanup: Delete files > 24 hours old (background task)

---

## 🚀 RUNNING PHASE 2

```bash
# 1. Install dependencies
pip install fastapi uvicorn python-multipart

# 2. Verify all Week 1 tools still work
cd backend
python -c "from tools.calculator import ghg_calculator; print('✓ Calculator OK')"
python -c "from tools.search import search_carbon_offsets; print('✓ Search OK')"

# 3. Run FastAPI server
python -m uvicorn main:app --reload --port 8000

# 4. Visit Swagger docs
# http://localhost:8000/docs

# 5. Test via Swagger UI or curl:
curl -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "TechCorp",
    "diesel_litres": 500,
    "electricity_kwh": 10000,
    "flights_km": 2000,
    "waste_kg": 500
  }'

# Response:
# {"calculation_id": "abc-123-def-456"}
```

---

## 📊 PHASE 2 SUCCESS CRITERIA

- ✅ FastAPI app runs without errors on localhost:8000
- ✅ All 4 endpoints return correct responses in Swagger UI
- ✅ SSE streaming shows agent thoughts in real-time
- ✅ PDF downloads successfully
- ✅ Error cases handled gracefully (422, 429, 500 responses)
- ✅ Groq→Gemini fallback tested
- ✅ Integration tests all passing (10/10)
- ✅ Ready for React frontend to consume

---

## 🔗 CONNECTION TO WEEK 3

When Phase 2 is complete:
- React frontend will call `POST /calculate`
- Get `calculation_id`
- Open EventSource to `GET /stream?id=calculation_id`
- Display agent thoughts in real-time
- Download PDF via `GET /report?id=calculation_id`

The React code will be much simpler because the API is clean and well-defined.

---

## 📚 REFERENCE DOCS

- **FastAPI:** https://fastapi.tiangolo.com/
- **Pydantic:** https://docs.pydantic.dev/
- **SSE (MDN):** https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
- **LangChain Agent Streaming:** https://python.langchain.com/docs/concepts/agents/
- **ReportLab:** https://www.reportlab.com/docs/reportlab-userguide.pdf

---

## ⚠️ COMMON PITFALLS TO AVOID

1. **SSE Connection Stuck** → Set proper timeouts in frontend
2. **PDF not generated** → Ensure `reports/` directory exists
3. **CORS errors** → Verify `CORSMiddleware` is first in middleware stack
4. **Agent hangs** → Set max timeout on agent executor (e.g., 5 minutes)
5. **Rate limiting too strict** → 1 req/5sec is reasonable for MVP
6. **Forgetting .env** → All 3 API keys must be set before running

---

## 📝 SUMMARY

**Phase 2 transforms Week 1's terminal agent into a production API.**

- **Week 1** = Brain (Agent + Tools)
- **Week 2** = Interface (FastAPI + SSE)
- **Week 3** = Face (React UI)
- **Week 4** = Deployment (Render + Vercel)

By end of Week 2, you have a **working API that can be deployed**—Week 3 just adds the pretty UI.

---

**Ready to build? Start with Day 8 task below.** 🚀

### Day 8 Quick Start:
```bash
# 1. Create main.py
# 2. Add Pydantic models for request/response
# 3. Create POST /calculate endpoint
# 4. Test in Swagger UI at http://localhost:8000/docs
```


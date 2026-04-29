# Quick Start Reference Guide

## 🚀 Start Here (Next 30 Minutes)

### Step 1: Create Project Structure
```bash
cd d:\Update_profile\Swach AI Carbon agent

# Create folders
mkdir -p backend/{tools,data,reports}
mkdir -p frontend/{src,public}

# Create Python virtual environment
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
```

### Step 2: Get API Keys (5 minutes each)
1. **Groq:** groq.com → Sign up → copy API key
2. **Tavily:** tavily.com → Sign up → copy API key
3. **Gemini:** aistudio.google.com → Create key → copy

### Step 3: Install Dependencies
```bash
# Backend
pip install langchain langchain-groq chromadb fastapi uvicorn tavily-python reportlab python-dotenv pytest sentence-transformers matplotlib

# Frontend
npm create vite@latest frontend -- --template react
cd frontend
npm install axios recharts react-hook-form
```

### Step 4: Create .env File
```bash
# backend/.env
GROQ_API_KEY=gsk_your_key_here
TAVILY_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

---

## 📋 Day-by-Day Task Breakdown

### WEEK 1: Foundation
- **Day 1-2:** Environment + API setup ✓ (you are here)
- **Day 3-4:** Build GHG calculator (pure Python math)
- **Day 5-6:** Tavily search + ChromaDB setup
- **Day 7:** Wire up ReAct agent + test in terminal

### WEEK 2: Backend
- **Day 8-9:** FastAPI endpoints (/calculate, /stream, /report)
- **Day 10-11:** PDF generation (ReportLab)
- **Day 12-13:** Error handling + Groq→Gemini fallback
- **Day 14:** End-to-end test

### WEEK 3: Frontend
- **Day 15-16:** React + multi-step form
- **Day 17-18:** SSE streaming agent thoughts
- **Day 19:** Results dashboard (charts)
- **Day 20:** PDF download button + polish
- **Day 21:** QA + mobile responsiveness

### WEEK 4: Deploy
- **Day 22-23:** Render backend deployment
- **Day 24:** Vercel frontend deployment
- **Day 25-26:** GitHub README + architecture diagram
- **Day 27:** Demo video (2 min)
- **Day 28:** LinkedIn post + Naukri update

---

## 🛠️ Emission Factors You'll Use

| Source | Factor | Unit |
|--------|--------|------|
| Diesel | 2.68 | kg CO₂/L |
| LPG | 2.98 | kg CO₂/kg |
| India Grid | 0.82 | kg CO₂/kWh |
| Flights (short) | 0.255 | kg CO₂/km |
| Waste | 0.58 | kg CO₂/kg |

These go in `backend/tools/calculator.py` — don't change them without regulatory update.

---

## 🔧 File Structure (Final)

```
swach-ai/
├── backend/
│   ├── main.py              ← FastAPI app
│   ├── agent.py             ← LangChain agent
│   ├── llm_provider.py       ← Groq/Gemini fallback
│   ├── tools/
│   │   ├── calculator.py    ← GHG emissions math
│   │   ├── search.py        ← Tavily web search
│   │   ├── retriever.py     ← ChromaDB RAG
│   │   └── pdf_gen.py       ← ReportLab reports
│   ├── data/
│   │   ├── ghg_protocol.pdf ← Downloaded from ghgprotocol.org
│   │   └── chroma_db/       ← Embeddings (created on setup)
│   ├── reports/             ← Generated PDFs
│   ├── requirements.txt
│   ├── .env
│   └── test_*.py
├── frontend/
│   ├── src/
│   │   ├── pages/Dashboard.jsx
│   │   ├── components/
│   │   │   ├── AgentThinkingPanel.jsx
│   │   │   ├── ResultsDashboard.jsx
│   │   │   └── steps/
│   │   │       ├── CompanyInfoForm.jsx
│   │   │       ├── Scope1Form.jsx
│   │   │       ├── Scope2Form.jsx
│   │   │       └── Scope3Form.jsx
│   │   ├── api/
│   │   │   └── client.js   ← API calls + SSE
│   │   └── App.jsx
│   └── package.json
├── .github/
│   └── workflows/           ← CI/CD if you want
├── PROJECT_ANALYSIS.md      ← This detailed plan
├── README.md                ← Public documentation
└── Procfile                 ← For Render deployment
```

---

## 🎯 Daily Standup Template

Copy this and use every morning:

```
Date: [Day/Week]

Yesterday:
- What did I build?
- What works?
- What blockers?

Today:
- What's my goal (max 1 deliverable)?
- What's my commit?

Next 3 hours:
- Specific tasks
```

---

## 🧪 Testing Commands

```bash
# Test calculator accuracy
python -m pytest backend/test_calculator.py -v

# Test agent in terminal
cd backend
python agent.py

# Test FastAPI
python -m uvicorn main:app --reload
# Go to http://localhost:8000/docs

# Test frontend
cd frontend
npm run dev
# Go to http://localhost:5173
```

---

## 🚨 Common Pitfalls (Avoid These)

❌ **Don't:** Hardcode carbon offset prices in calculator  
✅ **Do:** Search real-time prices via Tavily

❌ **Don't:** Let LLM invent emission factors  
✅ **Do:** Use official DEFRA/IPCC tables in Python code

❌ **Don't:** Forget CORS setup in FastAPI  
✅ **Do:** Add CORS middleware on day 1

❌ **Don't:** Build without fallback LLM  
✅ **Do:** Groq → Gemini fallback prevents demo failures

❌ **Don't:** Generate PDFs on main thread  
✅ **Do:** Use background tasks in FastAPI

❌ **Don't:** Stream raw agent data to frontend  
✅ **Do:** Parse Thought/Action/Observation into structured format

---

## 💡 Interview Talking Points

**"This project shows I can build agentic AI systems"**
- ReAct agent (think → act → observe → think again)
- Tool integration (calculator, search, retriever, PDF gen)
- Production resilience (fallback LLMs, error handling)
- Real-time streaming (SSE to frontend)
- Knowledge base integration (RAG prevents hallucination)
- PDF report generation (professional output)

**"I understand GHG Protocol compliance"**
- Scope 1, 2, 3 emissions
- DEFRA emission factors
- CCTS market timing (Oct 2026 launch)
- Audit-ready report generation

**"I can deploy and scale"**
- Render backend deployment
- Vercel frontend deployment
- Environment variable management
- Database integration (ChromaDB)

---

## 📱 Status Tracking

Keep this updated in your memory:

```
WEEK 1: [ ] Foundation
  - [ ] Day 1-2: Env + APIs
  - [ ] Day 3-4: Calculator
  - [ ] Day 5-6: Tools
  - [ ] Day 7: Agent

WEEK 2: [ ] Backend
  - [ ] Day 8-9: API
  - [ ] Day 10-11: PDF
  - [ ] Day 12-13: Fallback
  - [ ] Day 14: E2E test

WEEK 3: [ ] Frontend
  - [ ] Day 15-16: Form
  - [ ] Day 17-18: Streaming
  - [ ] Day 19: Dashboard
  - [ ] Day 20: Download
  - [ ] Day 21: QA

WEEK 4: [ ] Deploy
  - [ ] Day 22-23: Render
  - [ ] Day 24: Vercel
  - [ ] Day 25-26: README
  - [ ] Day 27: Video
  - [ ] Day 28: LinkedIn
```

---

## 🔗 Useful Links

- [GHG Protocol](https://ghgprotocol.org)
- [LangChain ReAct](https://python.langchain.com/docs/modules/agents/agents_types/react/)
- [Groq API Docs](https://console.groq.com/docs)
- [Tavily Search API](https://app.tavily.com/home)
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [ReportLab PDF](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [ChromaDB](https://docs.trychroma.com/)

---

## ⚡ Next Immediate Steps

**RIGHT NOW (Next 30 mins):**
1. ✅ Read PROJECT_ANALYSIS.md completely
2. Create project structure (mkdir commands above)
3. Set up Python venv
4. Get the 3 API keys
5. Create .env file
6. Run: `python -c "import langchain_groq; print('✓ Ready')"` 

**TODAY (3 hours):**
1. Download GHG Protocol PDF
2. Build `backend/tools/calculator.py`
3. Write unit tests
4. Get them passing
5. **Commit:** "Day 1: GHG calculator + tests passing"

**TOMORROW (3 hours):**
1. Build Tavily search tool
2. Build ChromaDB setup
3. Test both
4. **Commit:** "Day 2: Tools setup + test passing"

---

**You've got this. Commit to 3-4 hours daily. By day 28, you'll have a deployed AI agent system that 99% of developers have never built.**

# Tech Stack Deep Dive — Why Each Tool Was Chosen

## Frontend: React 18 + Vite

### Why React?
- **Component reusability:** Form steps, chart panels, thinking display
- **SSE integration:** EventSource API works natively in React
- **Ecosystem:** Recharts for carbon breakdown charts, react-hook-form for multi-step forms
- **Portfolio value:** 90% of "AI web app" jobs ask for React

### Why Vite (not Create React App)?
- **Speed:** ~10x faster dev server than CRA
- **Smaller bundle:** ~100KB vs ~300KB
- **Modern:** ES6+ modules native, no webpack complexity
- **Easy deployment:** Build output works on Vercel instantly

### Key React Libraries
```json
{
  "react": "^18.2.0",
  "react-hook-form": "^7.x",      // Multi-step form state
  "recharts": "^2.x",              // Carbon charts (donut, bar)
  "axios": "^1.x"                  // API calls with retry logic
}
```

---

## Backend: FastAPI (Python 3.11)

### Why FastAPI (not Flask/Django)?
- **Async native:** Built on async/await — perfect for SSE streaming
- **Automatic OpenAPI docs:** /docs endpoint gives you Swagger UI free
- **Type hints:** Pydantic validation catches errors early
- **Performance:** ~3x faster than Flask, comparable to Go
- **Groq integration:** LangChain has first-class FastAPI support

### Why Python 3.11?
- **GHG calculations:** Math libraries (numpy, scipy) are Python-native
- **LangChain:** Built in Python, not JS (way more capable)
- **LLM ecosystem:** Groq, Gemini, Anthropic all have Python SDKs
- **Data science:** Pandas, matplotlib for report generation

### FastAPI vs Alternatives

| Feature | FastAPI | Flask | Django | Node.js |
|---------|---------|-------|--------|---------|
| Async/Await | ✅ Native | ⚠️ Limited | ⚠️ Limited | ✅ Native |
| Type Hints | ✅ Full | ❌ No | ⚠️ Partial | ⚠️ JSDoc |
| SSE Streaming | ✅ Easy | ❌ Hard | ⚠️ Hard | ✅ Easy |
| LangChain | ✅ Perfect | ⚠️ OK | ⚠️ OK | ⚠️ Limited |
| Speed | ⚡ Fast | Medium | Slow | ⚡ Fast |
| Learning Curve | 📚 Moderate | 📚 Easy | 📚📚 Hard | 📚 Moderate |

**Verdict:** FastAPI is the sweet spot for this AI agent backend.

---

## AI Orchestration: LangChain + ReAct

### Why LangChain (not just raw Groq API calls)?
- **Agent framework:** ReAct agents handle tool selection & looping
- **Tool definitions:** Standardized format for calculator, search, retrieval, PDF
- **Memory:** Maintains conversation context across multiple steps
- **Fallback:** Easy to swap Groq for Gemini/Claude without rewriting
- **Production patterns:** Logging, error handling, retries built-in

### What is ReAct?
ReAct = Reasoning + Acting. Instead of:
```python
# ❌ Bad: One-shot LLM call
result = llm.call("calculate my emissions and give offset recommendations")
# Output: Makes up numbers, hallucinated offset prices
```

You do:
```python
# ✅ Good: ReAct loop
Agent thinks: "I need exact data, not estimates"
Agent calls: ghg_calculator([data])
Agent observes: Scope1=1.5, Scope2=8.2, Scope3=2.1 tCO2e
Agent thinks: "Now search for real offset prices"
Agent calls: search_carbon_offsets("CCTS 2026 price")
Agent observes: "Prices ₹350-500/tonne from NSE"
Agent thinks: "Time to generate report"
Agent calls: generate_pdf_report([all data])
# Output: Accurate, citable, professional
```

This loop is **deterministic** and **auditable** — exactly what compliance needs.

---

## LLM Provider: Groq (Primary) + Gemini (Fallback)

### Why Groq?
- **Speed:** 200+ tokens/sec (⚡ LLaMA optimized)
- **Cost:** Generous free tier (>10k req/month free)
- **Model:** LLaMA 3.3 70B — beats GPT-3.5 on reasoning
- **Latency:** <1s for agent thinking steps (good UX)

### Why Groq > Gemini
Groq is faster and cheaper. But we use **BOTH**:

**Groq PRIMARY**
```python
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1  # Deterministic for calculations
)
```

**Gemini FALLBACK** (if Groq rate-limited or down)
```python
def get_llm():
    try:
        return get_groq_llm()  # Try Groq
    except:
        return ChatGoogleGenerativeAI(model="gemini-1.5-pro")  # Fall back
```

This ensures your demo never breaks in front of clients.

### Temperature = 0.1 Why?
- **Temperature = 0.0:** Deterministic, boring, perfect for calculations
- **Temperature = 0.5:** Some randomness, good for reasoning
- **Temperature = 1.0:** Creative, unpredictable

For GHG calculations, we want **0.1** (almost deterministic). We're not writing poetry, we're calculating tonnes.

---

## Vector Database: ChromaDB

### What It Does
Stores GHG Protocol PDFs as searchable embeddings:
```
Input: "How do I calculate Scope 3 flights?"
↓
Convert to embedding (768-dim vector)
↓
Search similarity in ChromaDB
↓
Return: "Flight emissions use distance-based method: 
         0.255 kg CO₂/km per GHG Protocol 2024..."
```

### Why ChromaDB (not Pinecone/Weaviate)?
- **Local deployment:** No external SaaS dependency
- **Free tier:** ~unlimited for compliance documents
- **Simple API:** 3 lines of code to search
- **Good enough:** For 100MB of PDFs, perfect
- **Startup friendly:** No credit card for test phase

### ChromaDB vs Alternatives

| Feature | ChromaDB | Pinecone | Weaviate | Milvus |
|---------|----------|----------|----------|--------|
| Setup | ⚡ 2 min | ⏱️ 10 min | ⏱️ 15 min | ⏱️ 20 min |
| Cost (free) | ✅ Full | ❌ Limited | ✅ Full | ✅ Full |
| Local deploy | ✅ Yes | ❌ No | ⚠️ Docker | ⚠️ Docker |
| Learning curve | 📚 Easy | 📚 Easy | 📚 Hard | 📚 Hard |
| Production scale | ⚠️ 10GB | ✅ TB+ | ✅ TB+ | ✅ TB+ |

**For this project:** ChromaDB. Later, if you need to scale to millions of documents, migrate to Pinecone (same code).

---

## Web Search: Tavily API

### Why Tavily (not Google Search API)?
- **Cheap:** 1000 free searches/month (vs Google's $5 per 100)
- **LLM-tuned:** Results formatted for AI agents (not human browsing)
- **Query understanding:** "Advanced" mode handles complex queries
- **No hallucination:** Real web results, not imaginary

### Tavily Query Examples
```python
search_carbon_offsets(
    "India CCTS carbon credit price 2026 SME renewable energy"
)
# Returns 5 real web results about CCTS, not hallucinated prices
```

vs.

```python
# ❌ Without Tavily, LLM would say:
# "Carbon credits in India trade at ₹200-300/tonne..."
# [WRONG: Actually ₹350-500 in 2026]
```

---

## PDF Generation: ReportLab

### Why ReportLab (not HTML-to-PDF)?
- **Precision:** Exact pixel control (audit reports need this)
- **Charts:** Embed matplotlib graphs directly in PDF
- **Tables:** Professional multi-page tables with styles
- **No browser:** Works on server without headless Chrome (faster)
- **Compliance-ready:** PDF/A format support for long-term archival

### ReportLab vs Alternatives

| Feature | ReportLab | Weasyprint | PDFKit | HtmlToPdf |
|---------|-----------|-----------|--------|-----------|
| Speed | ⚡ Fast | ⏱️ Medium | ⏱️ Slow | ⏱️ Very Slow |
| Python-native | ✅ Yes | ✅ Yes | ❌ Node | ❌ Various |
| Table support | ✅ Great | ⚠️ OK | ⚠️ Limited | ⚠️ Limited |
| Chart embedding | ✅ Easy | ⚠️ OK | ⚠️ Hard | ❌ No |
| Learning curve | 📚 Moderate | 📚 Moderate | 📚 Easy | 📚 Hard |

**For this project:** ReportLab for professional, embedded charts and tables.

---

## Web Framework Details

### SSE (Server-Sent Events) Streaming
React frontend subscribes to backend event stream:

```javascript
// Frontend
const eventSource = new EventSource('/stream?id=calc123');
eventSource.onmessage = (e) => {
  const {type, content} = JSON.parse(e.data);
  // Updates UI in real-time with agent thoughts
};
```

```python
# Backend (FastAPI)
async def stream_results():
    def event_generator():
        while calculation_running:
            yield f"data: {json.dumps(thought)}\n\n"
            await asyncio.sleep(0.1)
    
    return StreamingResponse(event_generator(), 
                            media_type="text/event-stream")
```

**Why SSE (not WebSocket)?**
- One-way streaming (frontend only receives)
- Simpler than WebSocket
- Auto-reconnect on network hiccup
- Works through proxies/firewalls
- Perfect for agent thinking display

---

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│ Vercel Edge (Frontend)                  │
│ - React app at subdomain.vercel.app     │
│ - Auto-deployed from GitHub             │
│ - Env: VITE_API_URL=https://render-url  │
└──────────────┬──────────────────────────┘
               │ HTTPS REST + SSE
┌──────────────▼──────────────────────────┐
│ Render.com (Backend)                    │
│ - FastAPI app at api-render-name.com    │
│ - Auto-deployed from GitHub             │
│ - Env: GROQ_API_KEY, TAVILY_API_KEY     │
│ - Auto-restart on crashes               │
│ - 0.10 USD/hr (free tier available)     │
└──────────────┬──────────────────────────┘
               │ API calls
┌──────────────▼──────────────────────────┐
│ Groq API (LLM)                          │
│ - LLaMA 3.3 70B inference               │
│ - Free tier: millions of tokens         │
│ - 200+ tok/sec                          │
└──────────────────────────────────────────┘
```

### Cost Breakdown (Per User)
- Groq: $0.05-0.10 (free tier usually)
- Tavily: $0.01
- Gemini fallback: $0.02
- **Total:** ~$0.10-0.15 per report

If you charge ₹500 per report: **80% margin** 🎯

---

## Why This Tech Stack For Interviews

When asked "What tech stack did you choose and why?":

**Frontend:**
- React because companies care about web UI
- Vite because it shows you know modern tooling (not stuck on CRA)
- Recharts because charting libraries are production-common

**Backend:**
- FastAPI because you understand async Python (rare for web devs)
- LangChain because agentic AI requires orchestration, not just API calls
- Groq + Gemini because you handle resilience (fallbacks are pro)

**Infrastructure:**
- ChromaDB because you know RAG (retrieval-augmented generation)
- Tavily because you know how to prevent LLM hallucination
- ReportLab because you can generate professional artifacts

**Deployment:**
- Render because you deploy Python apps (not just Node)
- Vercel because you understand edge computing
- GitHub Actions because CI/CD is expected

---

## Performance Targets

| Metric | Target | Why It Matters |
|--------|--------|---|
| Form load | <2s | User patience |
| Calculation end-to-end | <30s | Agent loop time |
| PDF generation | <10s | UX expectation |
| SSE latency | <1s per thought | Visible streaming |
| Render cold start | <5s | First user |
| API response | <200ms avg | Streaming smoothness |

If you hit these, the app feels snappy and professional.

---

## Security Checklist

- ✅ API keys in .env (never in code)
- ✅ CORS configured (Vercel frontend only)
- ✅ HTTPS enforced (Render default)
- ✅ No user data stored permanently
- ✅ Rate limiting on /calculate (prevent abuse)
- ✅ PDF deletion after 30 days
- ✅ Activity logs (who calculated when)

---

## What Makes This Production-Ready

1. **Resilience:** Groq → Gemini fallback
2. **Accuracy:** GHG math is deterministic Python, not LLM
3. **Traceability:** ReAct loop visible to user + audit log
4. **Speed:** SSE streaming + Groq fast inference
5. **Compliance:** GHG Protocol citations in PDF
6. **Scale:** Can handle 100+ reports/day on free tier
7. **Cost:** Profitable at ₹500/report

This is **not a toy project**. Deployed, it's a real SaaS for Indian carbon compliance.

---

## Next Tech Skills You'll Gain

- **LangChain:** Agentic AI orchestration (hiring companies love this)
- **FastAPI:** Async Python web framework (increasingly popular)
- **ReAct:** Multi-step agent reasoning (frontier AI skill)
- **ChromaDB:** Vector databases for AI (required knowledge 2025+)
- **SSE/WebSockets:** Real-time frontend data (streaming LLMs)
- **PDF generation:** Professional artifact creation (SaaS common)
- **GHG Protocol:** Domain expertise (ESG consultant track)

**Interview value:** Most junior developers can't build **any** of these. Building **all 7**? You'll stand out.

---

## Fallback Plans (If Stuck)

If Groq is down:
```python
# Automatically use Gemini
llm = get_llm_with_fallback()
```

If ChromaDB fails:
```python
# Hardcoded GHG methodology (less ideal, but works)
if chromadb_fails:
    return METHODOLOGY_FALLBACK
```

If Tavily search fails:
```python
# Use cached CCTS prices (1 day old)
if tavily_fails:
    return get_cached_offset_prices()
```

If PDF generation fails:
```python
# Return JSON summary instead
if pdf_fails:
    return json_report_format()
```

**Lesson:** Always have fallbacks. Production systems fail gracefully.


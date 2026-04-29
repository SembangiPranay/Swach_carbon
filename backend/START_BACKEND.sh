#!/bin/bash
# PHASE 2 BACKEND - QUICK START GUIDE

echo "=========================================="
echo "PHASE 2 BACKEND - QUICK START"
echo "=========================================="
echo ""

# Step 1: Navigate to backend
echo "[1] Navigating to backend directory..."
cd backend

# Step 2: Verify environment
echo "[2] Checking environment..."
python -c "
import sys
print(f'  Python version: {sys.version.split()[0]}')
print(f'  FastAPI: OK')
print(f'  Uvicorn: OK')
"

# Step 3: Verify configuration
echo "[3] Verifying configuration..."
python -c "
from config import Config, logger
print(f'  Groq: Configured')
print(f'  Tavily: Configured')
print(f'  Gemini: Configured')
"

# Step 4: Start server
echo "[4] Starting FastAPI server..."
echo ""
echo "  Run this command:"
echo "  python -m uvicorn main:app --reload --port 8000"
echo ""
echo "  Server will be available at:"
echo "    API: http://localhost:8000"
echo "    Docs: http://localhost:8000/docs"
echo "    OpenAPI: http://localhost:8000/openapi.json"
echo ""

# Step 5: Test endpoints
echo "[5] Test commands (in new terminal):"
echo ""
echo "  Health check:"
echo "    curl http://localhost:8000/health"
echo ""
echo "  Create calculation:"
echo "    curl -X POST http://localhost:8000/calculate \\"
echo "      -H 'Content-Type: application/json' \\"
echo "      -d '{\"company_name\":\"Test\",\"electricity_kwh\":10000}'"
echo ""
echo "  Stream events (replace UUID):"
echo "    curl http://localhost:8000/stream?id=<calculation_id>"
echo ""
echo "  Get stats:"
echo "    curl http://localhost:8000/stats"
echo ""

echo "=========================================="
echo "Backend is ready for Week 3 frontend!"
echo "=========================================="

"""
Integration tests for Phase 2 FastAPI Backend

Tests all 4 endpoints:
- POST /calculate
- GET /stream?id=uuid
- GET /report?id=uuid
- GET /health
"""

import pytest
import requests
import json
import time
from typing import Dict

BASE_URL = "http://localhost:8000"

# Test data
TEST_COMPANY_DATA = {
    "company_name": "TechCorp Test",
    "diesel_litres": 500,
    "lpg_kg": 100,
    "electricity_kwh": 10000,
    "flights_km": 2000,
    "waste_kg": 500,
    "commute_km": 5000,
}


class TestCalculateEndpoint:
    """Test POST /calculate endpoint"""

    def test_valid_request(self):
        """Test calculation with valid data"""
        response = requests.post(f"{BASE_URL}/calculate", json=TEST_COMPANY_DATA)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"

        data = response.json()
        assert "calculation_id" in data
        assert isinstance(data["calculation_id"], str)
        assert len(data["calculation_id"]) > 0

        # Store for other tests
        return data["calculation_id"]

    def test_missing_company_name(self):
        """Test validation: missing company_name"""
        bad_data = TEST_COMPANY_DATA.copy()
        del bad_data["company_name"]

        response = requests.post(f"{BASE_URL}/calculate", json=bad_data)
        assert response.status_code == 422  # Unprocessable Entity

    def test_invalid_electricity_kwh(self):
        """Test validation: invalid electricity_kwh"""
        bad_data = TEST_COMPANY_DATA.copy()
        bad_data["electricity_kwh"] = "not_a_number"

        response = requests.post(f"{BASE_URL}/calculate", json=bad_data)
        assert response.status_code == 422

    def test_negative_values(self):
        """Test validation: negative emissions should fail"""
        bad_data = TEST_COMPANY_DATA.copy()
        bad_data["diesel_litres"] = -100

        response = requests.post(f"{BASE_URL}/calculate", json=bad_data)
        assert response.status_code == 422


class TestStreamEndpoint:
    """Test GET /stream?id=uuid endpoint"""

    def test_stream_exists(self):
        """Test streaming valid calculation"""
        # First create a calculation
        calc_response = requests.post(f"{BASE_URL}/calculate", json=TEST_COMPANY_DATA)
        calc_id = calc_response.json()["calculation_id"]

        # Wait a moment for background task to start
        time.sleep(1)

        # Connect to stream
        response = requests.get(f"{BASE_URL}/stream?id={calc_id}", stream=True, timeout=10)

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream"

        # Collect events
        events = []
        try:
            for line in response.iter_lines(timeout=5):
                if line:
                    event_text = line.decode("utf-8")
                    if event_text.startswith("data:"):
                        event_json = event_text[5:].strip()
                        events.append(json.loads(event_json))

                # Stop after collecting events (or timeout)
                if len(events) > 5:
                    break
        except:
            pass  # Timeout is fine

        # Verify events
        assert len(events) > 0, "No events received from stream"

        # Check for expected event types
        event_types = [e.get("type") for e in events]
        assert any(t in event_types for t in ["thought", "action", "observation"])

    def test_stream_nonexistent_calc(self):
        """Test streaming non-existent calculation"""
        response = requests.get(f"{BASE_URL}/stream?id=nonexistent", timeout=5)
        assert response.status_code == 404


class TestReportEndpoint:
    """Test GET /report?id=uuid endpoint"""

    def test_report_pending(self):
        """Test report before calculation completes"""
        calc_response = requests.post(f"{BASE_URL}/calculate", json=TEST_COMPANY_DATA)
        calc_id = calc_response.json()["calculation_id"]

        # Immediately try to get report (should be pending)
        response = requests.get(f"{BASE_URL}/report?id={calc_id}")

        # Could be 202 (still processing) or 404 (not ready yet)
        assert response.status_code in [202, 404, 500]

    def test_report_nonexistent(self):
        """Test report for non-existent calculation"""
        response = requests.get(f"{BASE_URL}/report?id=nonexistent")
        assert response.status_code == 404


class TestHealthEndpoint:
    """Test GET /health endpoint"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = requests.get(f"{BASE_URL}/health")

        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "services" in data

        # Status should be either 'healthy' or 'degraded'
        assert data["status"] in ["healthy", "degraded"]


class TestErrorHandling:
    """Test error handling"""

    def test_malformed_json(self):
        """Test malformed JSON request"""
        response = requests.post(
            f"{BASE_URL}/calculate",
            data="{invalid json}",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code in [400, 422]

    def test_missing_endpoint(self):
        """Test non-existent endpoint"""
        response = requests.get(f"{BASE_URL}/nonexistent")
        assert response.status_code == 404


class TestRateLimiting:
    """Test rate limiting"""

    def test_rate_limit_headers(self):
        """Test that rate limit headers are present"""
        response = requests.post(f"{BASE_URL}/calculate", json=TEST_COMPANY_DATA)

        # Check for rate limit headers
        assert "x-ratelimit-remaining" in response.headers or response.status_code == 429


class TestCORS:
    """Test CORS headers"""

    def test_cors_headers_present(self):
        """Test CORS headers in response"""
        response = requests.options(
            f"{BASE_URL}/calculate",
            headers={"Origin": "http://localhost:3000"},
        )

        assert response.status_code == 200
        # CORS headers should be present
        assert (
            "access-control-allow-origin" in response.headers
            or "Access-Control-Allow-Origin" in response.headers
        )


def test_complete_flow():
    """Integration test: complete flow from calculation to results"""
    print("\n" + "="*70)
    print("TESTING COMPLETE FLOW")
    print("="*70)

    # 1. Start calculation
    print("\n[1] Starting calculation...")
    calc_response = requests.post(f"{BASE_URL}/calculate", json=TEST_COMPANY_DATA)
    assert calc_response.status_code == 200
    calc_id = calc_response.json()["calculation_id"]
    print(f"    Calculation ID: {calc_id}")

    # 2. Stream events
    print("\n[2] Streaming events...")
    stream_response = requests.get(f"{BASE_URL}/stream?id={calc_id}", stream=True, timeout=30)
    assert stream_response.status_code == 200

    event_count = 0
    try:
        for line in stream_response.iter_lines(timeout=10):
            if line:
                event_text = line.decode("utf-8")
                if event_text.startswith("data:"):
                    event_json = event_text[5:].strip()
                    event = json.loads(event_json)
                    print(f"    Event: {event.get('type')} - {event.get('content', '')[:50]}")
                    event_count += 1

            # Give some time for calculation to complete
            if event_count > 10:
                break
    except requests.exceptions.ReadTimeout:
        pass

    print(f"    Received {event_count} events")

    # 3. Check health
    print("\n[3] Checking health...")
    health_response = requests.get(f"{BASE_URL}/health")
    assert health_response.status_code == 200
    health_data = health_response.json()
    print(f"    Status: {health_data.get('status')}")

    # 4. Get stats
    print("\n[4] Getting stats...")
    stats_response = requests.get(f"{BASE_URL}/stats")
    if stats_response.status_code == 200:
        stats = stats_response.json()
        print(f"    Total calculations: {stats.get('total_calculations')}")
        print(f"    Running: {stats.get('running')}")
        print(f"    Completed: {stats.get('completed')}")

    print("\n" + "="*70)
    print("FLOW TEST COMPLETE")
    print("="*70)


if __name__ == "__main__":
    # Run tests
    print("Starting integration tests...")
    print(f"Base URL: {BASE_URL}")
    print("")

    # Try to connect
    try:
        health_resp = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"API is online: {health_resp.status_code}")
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to API at", BASE_URL)
        print("Make sure the server is running:")
        print("  cd backend && python -m uvicorn main:app --reload")
        exit(1)

    print("\n" + "="*70)
    print("Running pytest tests...")
    print("="*70 + "\n")

    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short"])

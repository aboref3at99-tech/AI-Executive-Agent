"""Unit Tests for API Server
Comprehensive test suite for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.server import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestHealthEndpoints:
    """Test health and status endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns dashboard or info"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "agent_status" in data
    
    def test_metrics_endpoint(self, client):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "metrics" in data


class TestTaskEndpoints:
    """Test task execution endpoints"""
    
    @pytest.mark.asyncio
    async def test_autonomous_task(self, client):
        """Test autonomous task execution"""
        response = client.post(
            "/tasks/autonomous",
            json={"task": "Calculate 2 + 2"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "result" in data
    
    @pytest.mark.asyncio
    async def test_code_generation(self, client):
        """Test code generation endpoint"""
        response = client.post(
            "/tasks/code-generation",
            json={
                "requirement": "Function to add two numbers",
                "language": "python",
                "include_tests": True
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "result" in data
    
    @pytest.mark.asyncio
    async def test_data_analysis(self, client):
        """Test data analysis endpoint"""
        response = client.post(
            "/tasks/data-analysis",
            json={
                "data_description": "Numbers: [1, 2, 3, 4, 5]",
                "analysis_type": "statistical"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "result" in data
    
    @pytest.mark.asyncio
    async def test_batch_tasks(self, client):
        """Test batch task execution"""
        response = client.post(
            "/tasks/batch",
            json={
                "tasks": ["Task 1", "Task 2", "Task 3"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["total_tasks"] == 3
        assert "results" in data
    
    def test_invalid_task_request(self, client):
        """Test invalid task request"""
        response = client.post(
            "/tasks/autonomous",
            json={}  # Missing required field
        )
        assert response.status_code == 422  # Validation error


class TestHistoryEndpoints:
    """Test history and analytics endpoints"""
    
    def test_get_history(self, client):
        """Test get execution history"""
        response = client.get("/history?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "history" in data
        assert "count" in data
    
    def test_clear_history(self, client):
        """Test clear history endpoint"""
        response = client.post("/history/clear")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_self_improvement(self, client):
        """Test self-improvement analysis"""
        response = client.get("/analytics/self-improvement")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "analysis" in data


class TestDashboardEndpoints:
    """Test dashboard endpoints"""
    
    def test_dashboard_stats(self, client):
        """Test dashboard statistics endpoint"""
        response = client.get("/dashboard/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "stats" in data
        assert "overview" in data["stats"]
        assert "recent_activity" in data["stats"]
        assert "performance" in data["stats"]
        assert "capabilities" in data["stats"]
    
    def test_dashboard_page(self, client):
        """Test dashboard HTML page"""
        response = client.get("/dashboard")
        assert response.status_code in [200, 404]  # May not exist in test env


class TestErrorHandling:
    """Test error handling"""
    
    def test_invalid_endpoint(self, client):
        """Test invalid endpoint returns 404"""
        response = client.get("/invalid/endpoint")
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client):
        """Test wrong HTTP method"""
        response = client.get("/tasks/autonomous")  # Should be POST
        assert response.status_code == 405


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

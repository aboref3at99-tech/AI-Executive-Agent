# 📊 AI Executive Agent Dashboard - Complete Guide

## 🎯 Overview

The AI Executive Agent Dashboard is a modern, responsive web interface for interacting with the AI Executive Agent system. Built with vanilla JavaScript and FastAPI, it provides a beautiful and intuitive way to execute tasks, monitor performance, and analyze results.

---

## 🚀 Quick Start

### 1. Start the Server

```bash
# Method 1: Using the start script
python start_dashboard.py

# Method 2: Direct uvicorn
uvicorn api.server:app --host 0.0.0.0 --port 8000

# Method 3: With auto-reload for development
uvicorn api.server:app --reload
```

### 2. Access the Dashboard

Open your browser and navigate to:
- **Dashboard**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🎨 Features

### 1. **Real-time Statistics**
- Total executions counter
- Success rate percentage
- Successful tasks count
- Failed tasks count
- Auto-refresh every 30 seconds

### 2. **Quick Actions**
Six one-click actions:
- 🤖 **Autonomous Task** - Execute any task autonomously
- 💻 **Generate Code** - Generate code from requirements
- 📊 **Analyze Data** - Perform data analysis
- 🔄 **Batch Tasks** - Execute multiple tasks at once
- 📜 **View History** - See execution history
- 🧠 **Self-Improve** - Get improvement suggestions

### 3. **Interactive Task Form**
- Dynamic form based on task type
- Support for multiple task types
- Real-time validation
- Easy-to-use interface

### 4. **Results Display**
- Syntax-highlighted code blocks
- Structured JSON output
- Success/error indicators
- Timestamp tracking

### 5. **Execution History**
- Last 20 executions
- Success/failure status
- Timestamp for each execution
- Quick reference to past tasks

---

## 📋 API Endpoints

### Health & Status

**`GET /`**
- Description: Root endpoint, serves dashboard
- Response: Dashboard HTML page

**`GET /health`**
- Description: Health check
- Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-31T10:00:00",
  "agent_status": "ready"
}
```

**`GET /metrics`**
- Description: Get performance metrics
- Response:
```json
{
  "status": "success",
  "timestamp": "2025-12-31T10:00:00",
  "metrics": {
    "total_executions": 100,
    "successful": 95,
    "failed": 5,
    "success_rate": 0.95
  }
}
```

### Task Execution

**`POST /tasks/autonomous`**
- Description: Execute autonomous task
- Request Body:
```json
{
  "task": "Calculate factorial of 10",
  "context": {"key": "value"}
}
```
- Response:
```json
{
  "status": "success",
  "timestamp": "2025-12-31T10:00:00",
  "result": {
    "success": true,
    "task": "...",
    "code": "...",
    "execution": {...},
    "analysis": {...}
  }
}
```

**`POST /tasks/code-generation`**
- Description: Generate code
- Request Body:
```json
{
  "requirement": "Binary search function",
  "language": "python",
  "include_tests": true
}
```

**`POST /tasks/data-analysis`**
- Description: Analyze data
- Request Body:
```json
{
  "data_description": "Sales data: [100, 150, 120]",
  "analysis_type": "statistical"
}
```

**`POST /tasks/batch`**
- Description: Execute batch tasks
- Request Body:
```json
{
  "tasks": ["Task 1", "Task 2", "Task 3"],
  "context": {"key": "value"}
}
```

**`POST /tasks/browser`**
- Description: Execute browser task
- Request Body:
```json
{
  "task": "Go to google.com and search for AI",
  "context": "Web scraping"
}
```

**`POST /tasks/workflow`**
- Description: Execute workflow
- Request Body:
```json
{
  "steps": [
    {"type": "browser", "task": "..."},
    {"type": "analyze", "data": "..."}
  ]
}
```

### History & Analytics

**`GET /history?limit=10`**
- Description: Get execution history
- Query Parameters: `limit` (optional, default: 10)
- Response:
```json
{
  "status": "success",
  "count": 10,
  "history": [...]
}
```

**`POST /history/clear`**
- Description: Clear execution history
- Response:
```json
{
  "status": "success",
  "message": "History cleared"
}
```

**`GET /analytics/self-improvement`**
- Description: Get self-improvement analysis
- Response:
```json
{
  "status": "success",
  "analysis": {
    "executions_analyzed": 50,
    "suggestions": "..."
  }
}
```

### Dashboard

**`GET /dashboard/stats`**
- Description: Get dashboard statistics
- Response:
```json
{
  "status": "success",
  "stats": {
    "overview": {...},
    "recent_activity": {...},
    "performance": {...},
    "capabilities": {...}
  }
}
```

---

## 🎨 Dashboard UI Components

### 1. Header
- Title and description
- Branding

### 2. Statistics Grid
Four cards showing:
- Total Executions
- Success Rate
- Successful Tasks
- Failed Tasks

### 3. Quick Actions
Six buttons for common operations

### 4. Task Form
Dynamic form with:
- Task type selector
- Task description textarea
- Conditional fields based on task type
- Execute button

### 5. Loading Indicator
Animated spinner during processing

### 6. Results Section
Shows:
- Status badge (success/error)
- Timestamp
- Generated code (syntax highlighted)
- Execution output
- Analysis results

### 7. History Section
List of recent executions with:
- Task description
- Timestamp
- Status badge

---

## 🔧 Customization

### Changing Colors

Edit the CSS in `dashboard/index.html`:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to your colors */
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
```

### Adding Custom Actions

1. Add button in HTML:
```html
<button class="btn btn-primary" onclick="myCustomAction()">
    🎯 My Action
</button>
```

2. Add function in JavaScript:
```javascript
async function myCustomAction() {
    // Your custom code here
}
```

### Modifying Stats

Edit the `loadStats()` function to display different metrics.

---

## 🧪 Testing the Dashboard

### 1. Manual Testing

Open the dashboard and test each feature:
- ✅ Statistics load correctly
- ✅ Each quick action works
- ✅ Task form submits successfully
- ✅ Results display properly
- ✅ History loads correctly

### 2. Automated Testing

```bash
# Run API tests
pytest tests/test_api.py -v

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=api --cov-report=html
```

### 3. Load Testing

```bash
# Install locust
pip install locust

# Create locustfile.py
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class DashboardUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def test_health(self):
        self.client.get("/health")
    
    @task
    def test_metrics(self):
        self.client.get("/metrics")
    
    @task
    def test_stats(self):
        self.client.get("/dashboard/stats")
EOF

# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

---

## 🚀 Deployment

### 1. Local Development

```bash
python start_dashboard.py
```

### 2. Production with Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with workers
gunicorn api.server:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 3. Docker Deployment

```bash
# Build image
docker build -t ai-agent-dashboard .

# Run container
docker run -p 8000:8000 ai-agent-dashboard
```

### 4. Cloud Deployment

**Heroku:**
```bash
# Create Procfile
echo "web: uvicorn api.server:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git push heroku main
```

**Railway:**
```bash
# Connect repository
railway link

# Deploy
railway up
```

**Render:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn api.server:app --host 0.0.0.0 --port $PORT`

---

## 🔒 Security

### API Security

1. **API Keys** (Production):
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != "your-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key
```

2. **CORS Configuration**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

3. **Rate Limiting**:
```bash
pip install slowapi

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/")
@limiter.limit("5/minute")
async def root(request: Request):
    return {"message": "Hello"}
```

---

## 📊 Monitoring

### 1. Built-in Metrics

Access metrics at: `http://localhost:8000/metrics`

### 2. Custom Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 3. Prometheus Integration

```bash
pip install prometheus-fastapi-instrumentator

from prometheus_fastapi_instrumentator import Instrumentator

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

**2. Module Not Found**
```bash
# Install dependencies
pip install -r requirements.txt
```

**3. CORS Errors**
- Check CORS configuration in `api/server.py`
- Ensure origins are properly configured

**4. WebSocket Connection Failed**
- Check firewall settings
- Ensure WebSocket support in proxy/load balancer

---

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **OpenManus Guide**: See `docs/OPENMANUS_GUIDE.md`
- **API Reference**: http://localhost:8000/docs
- **GitHub Repository**: https://github.com/aboref3at99-tech/AI-Executive-Agent

---

## 🤝 Contributing

To contribute to the dashboard:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

Part of AI Executive Agent project - See main repository license

---

**Last Updated**: December 31, 2025  
**Version**: 1.1.0  
**Status**: ✅ Production Ready

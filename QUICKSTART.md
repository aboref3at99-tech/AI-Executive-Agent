# 🚀 Quick Start Guide

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/aboref3at99-tech/AI-Executive-Agent.git
cd AI-Executive-Agent
```

### 2. Install Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 3. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env
```

Required API keys:
- **GOOGLE_API_KEY**: https://makersuite.google.com/app/apikey
- **COMET_API_KEY**: https://www.comet.ml/
- **OPIK_API_KEY**: https://www.comet.ml/opik

## Running the Dashboard

### Method 1: Start Script (Recommended)
```bash
python start_dashboard.py
```

### Method 2: Direct Uvicorn
```bash
uvicorn api.server:app --host 0.0.0.0 --port 8000
```

### Method 3: Docker
```bash
docker-compose up -d
```

## Access Points

- **Dashboard**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## Quick Test

```python
# Test autonomous task
import asyncio
from core.agent import get_agent

async def test():
    agent = get_agent()
    result = await agent.execute_autonomous_task("Calculate 2+2")
    print(result)
    agent.cleanup()

asyncio.run(test())
```

## Features

✅ Autonomous Task Execution  
✅ Code Generation  
✅ Data Analysis  
✅ Browser Automation  
✅ Batch Processing  
✅ Self-Improvement  
✅ Interactive Dashboard  

## Documentation

- 📚 [Full Documentation](README.md)
- 🤖 [OpenManus Guide](docs/OPENMANUS_GUIDE.md)
- 📊 [Dashboard Guide](docs/DASHBOARD_GUIDE.md)
- 🏗️ [Architecture](AGENT_ARCHITECTURE.md)

## Support

- Issues: https://github.com/aboref3at99-tech/AI-Executive-Agent/issues
- Discussions: https://github.com/aboref3at99-tech/AI-Executive-Agent/discussions

---

**Version**: 1.1.0 | **Status**: ✅ Production Ready

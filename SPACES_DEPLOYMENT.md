# 🚀 Hugging Face Spaces Deployment Guide

## Quick Deployment to Hugging Face Spaces

### Method 1: Using Spaces UI (Recommended)

1. **Create a New Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose a name: `ai-executive-agent`
   - Select SDK: **Docker**
   - Set visibility: Public or Private
   - Click "Create Space"

2. **Upload Files**
   - Use the "Files" tab
   - Upload these essential files:
     - `Dockerfile.spaces` (rename to `Dockerfile`)
     - `app.py`
     - `requirements-spaces.txt`
     - `README_SPACES.md` (rename to `README.md`)
     - All folders: `api/`, `core/`, `config/`, `dashboard/`

3. **Configure Environment Variables**
   - Go to Settings → Variables
   - Add required variables:
     ```
     GOOGLE_API_KEY=your_google_api_key
     ```
   - Optional variables:
     ```
     COMET_API_KEY=your_comet_key
     COMET_WORKSPACE=your_workspace
     OPIK_API_KEY=your_opik_key
     LOG_LEVEL=INFO
     ```

4. **Wait for Build**
   - Space will automatically build (3-5 minutes)
   - Check logs for any errors
   - Once ready, your app will be live!

5. **Access Your Space**
   - URL: `https://huggingface.co/spaces/YOUR_USERNAME/ai-executive-agent`

---

### Method 2: Using Git (Advanced)

1. **Clone Your Space Repository**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/ai-executive-agent
   cd ai-executive-agent
   ```

2. **Copy Project Files**
   ```bash
   # Copy from this repository
   cp Dockerfile.spaces Dockerfile
   cp README_SPACES.md README.md
   cp requirements-spaces.txt requirements.txt
   cp app.py .
   cp -r api core config dashboard .
   ```

3. **Commit and Push**
   ```bash
   git add .
   git commit -m "Deploy AI Executive Agent"
   git push
   ```

4. **Configure Variables**
   - Go to Space Settings → Variables
   - Add environment variables as shown above

---

### Method 3: Using Hugging Face CLI

1. **Install Hugging Face CLI**
   ```bash
   pip install huggingface_hub
   huggingface-cli login
   ```

2. **Create and Upload**
   ```bash
   # Create space
   huggingface-cli repo create ai-executive-agent --type space --space_sdk docker

   # Upload files
   huggingface-cli upload ai-executive-agent . --repo-type space
   ```

3. **Configure and Deploy**
   - Set environment variables in UI
   - Space will auto-build

---

## 📋 Required Files for Spaces

Essential files that must be uploaded:

```
ai-executive-agent/
├── Dockerfile              ← Renamed from Dockerfile.spaces
├── README.md              ← Renamed from README_SPACES.md
├── app.py                 ← Entry point
├── requirements.txt       ← From requirements-spaces.txt
├── api/
│   ├── __init__.py
│   └── server.py
├── core/
│   ├── __init__.py
│   ├── agent.py
│   ├── openmanus_agent.py
│   └── integrations/
│       ├── __init__.py
│       └── openmanus_integration.py
├── config/
│   ├── __init__.py
│   └── settings.py
└── dashboard/
    └── index.html
```

---

## ⚙️ Environment Variables

### Required
- `GOOGLE_API_KEY` - Get from https://makersuite.google.com/app/apikey

### Optional
- `COMET_API_KEY` - For monitoring
- `COMET_WORKSPACE` - Your workspace name
- `OPIK_API_KEY` - For LLM tracking
- `LOG_LEVEL` - Logging level (default: INFO)

---

## 🧪 Testing Locally

Before deploying to Spaces, test locally:

```bash
# Build Docker image
docker build -f Dockerfile.spaces -t ai-agent-spaces .

# Run container
docker run -p 7860:7860 \
  -e GOOGLE_API_KEY=your_key \
  ai-agent-spaces

# Access
open http://localhost:7860
```

---

## 🐛 Troubleshooting

### Build Fails
- Check Dockerfile syntax
- Verify all required files are uploaded
- Check requirements.txt dependencies

### App Won't Start
- Check environment variables are set
- View build logs in Spaces
- Verify GOOGLE_API_KEY is valid

### Can't Access Dashboard
- Wait for build to complete (3-5 minutes)
- Check if port 7860 is exposed
- Verify health check passes

### Import Errors
- Ensure all package folders have `__init__.py`
- Check requirements-spaces.txt includes all dependencies
- Verify file structure matches expected layout

---

## 📊 Performance Tips

1. **Reduce Docker Image Size**
   - Use slim Python image
   - Minimize dependencies
   - Remove unnecessary files with .dockerignore

2. **Optimize Startup Time**
   - Use requirement caching
   - Minimize file copying
   - Pre-compile Python files

3. **Improve Response Time**
   - Enable caching
   - Use connection pooling
   - Optimize database queries

---

## 🔒 Security Best Practices

1. **Never Commit API Keys**
   - Use Spaces variables
   - Never hardcode secrets
   - Use environment variables

2. **Validate Input**
   - Sanitize user input
   - Implement rate limiting
   - Add request validation

3. **Monitor Usage**
   - Enable logging
   - Track API calls
   - Set up alerts

---

## 📚 Resources

- **Hugging Face Spaces Docs**: https://huggingface.co/docs/hub/spaces
- **Docker SDK Guide**: https://huggingface.co/docs/hub/spaces-sdks-docker
- **Repository**: https://github.com/aboref3at99-tech/AI-Executive-Agent

---

## 🎉 Post-Deployment

After successful deployment:

1. **Test All Features**
   - Execute autonomous tasks
   - Generate code
   - Analyze data
   - Check history

2. **Share Your Space**
   - Add description
   - Add screenshots
   - Share link
   - Get feedback

3. **Monitor Performance**
   - Check logs
   - Monitor metrics
   - Track usage
   - Fix issues

---

## 📞 Support

- **Issues**: https://github.com/aboref3at99-tech/AI-Executive-Agent/issues
- **Discussions**: https://github.com/aboref3at99-tech/AI-Executive-Agent/discussions
- **Spaces Forum**: https://discuss.huggingface.co/

---

**Good luck with your deployment! 🚀**

If you encounter any issues, please open an issue on GitHub.

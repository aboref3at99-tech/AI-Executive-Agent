"""AI Executive Agent - Hugging Face Spaces Entry Point
This is the main entry point for the Hugging Face Spaces deployment
"""
import os
import sys
import logging
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Validate required environment variables
required_vars = ['GOOGLE_API_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
    logger.error("Please configure GOOGLE_API_KEY in Hugging Face Spaces Settings → Variables")
    logger.error("Get your API key from: https://makersuite.google.com/app/apikey")
    
    # Create a simple error page
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    
    app = FastAPI()
    
    @app.get("/")
    async def error_page():
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Configuration Required</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }}
                .container {{
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    max-width: 600px;
                    text-align: center;
                }}
                h1 {{ color: #667eea; }}
                .error {{ color: #e74c3c; margin: 20px 0; }}
                .steps {{ text-align: left; margin: 20px 0; }}
                .steps li {{ margin: 10px 0; }}
                a {{ color: #667eea; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>⚠️ Configuration Required</h1>
                <div class="error">
                    <strong>Missing: {', '.join(missing_vars)}</strong>
                </div>
                <p>Please configure the following environment variables:</p>
                <div class="steps">
                    <ol>
                        <li>Go to Space Settings → Variables</li>
                        <li>Add <code>GOOGLE_API_KEY</code></li>
                        <li>Get your key from <a href="https://makersuite.google.com/app/apikey" target="_blank">Google AI Studio</a></li>
                        <li>Restart the Space</li>
                    </ol>
                </div>
                <p><a href="https://github.com/aboref3at99-tech/AI-Executive-Agent" target="_blank">📚 View Documentation</a></p>
            </div>
        </body>
        </html>
        """, status_code=503)
else:
    # Import and run the main application
    logger.info("✅ All required environment variables are set")
    logger.info("🚀 Starting AI Executive Agent...")
    
    # Disable browser automation for Spaces (not supported)
    os.environ['ENABLE_BROWSER_AUTOMATION'] = 'false'
    
    # Import the main app
    from api.server import app
    
    logger.info("✅ Application ready!")

# This is what uvicorn will use
# In Dockerfile: CMD ["uvicorn", "app:app", ...]

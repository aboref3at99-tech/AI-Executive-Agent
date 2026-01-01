#!/usr/bin/env python3
"""Start AI Executive Agent Dashboard Server
Easy script to launch the API server with dashboard
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.server import start_server


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("🚀 AI Executive Agent - Dashboard Server")
    print("="*60)
    print("\n📊 Starting dashboard server...")
    print("   - Dashboard: http://localhost:8000")
    print("   - API Docs: http://localhost:8000/docs")
    print("   - Health Check: http://localhost:8000/health")
    print("\n⏳ Initializing... Please wait...\n")
    
    try:
        start_server(
            host="0.0.0.0",
            port=8000,
            reload=False
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

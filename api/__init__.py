"""AI Executive Agent API Package
FastAPI-based REST API for dashboard and external integrations
"""

from .server import app, start_server

__all__ = ["app", "start_server"]

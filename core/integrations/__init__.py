"""AI Executive Agent - Integrations Package
External service integrations including monitoring and autonomous agents
"""

from .comet_integration import CometIntegration
from .openmanus_integration import OpenManusIntegration, get_openmanus_integration

__all__ = [
    "CometIntegration",
    "OpenManusIntegration",
    "get_openmanus_integration",
]

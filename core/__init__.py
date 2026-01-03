"""AI Executive Agent - Core Package
Core agents and integrations for the AI Executive Agent system
"""

from .agent import ExecutiveAgent, get_agent
from .openmanus_agent import OpenManusAgent, get_openmanus_agent
from .memory import AgentMemory
from .tools import ToolRegistry

__all__ = [
    "ExecutiveAgent",
    "get_agent",
    "OpenManusAgent",
    "get_openmanus_agent",
    "AgentMemory",
    "ToolRegistry",
]

__version__ = "1.1.0"

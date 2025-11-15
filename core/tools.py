"""
Agent Tools Module

Defines all tools available to the AI Executive Agent for task execution.
Includes browser automation, web searching, data retrieval, and analysis tools.
"""

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


logger = logging.getLogger(__name__)


class ToolCategory(Enum):
    """
    Categories of available tools for agent use.
    """
    BROWSER = "browser"
    WEB = "web"
    DATA = "data"
    ANALYSIS = "analysis"
    MEMORY = "memory"
    SYSTEM = "system"


@dataclass
class ToolParameter:
    """
    Represents a single parameter for a tool.
    
    Attributes:
        name: Parameter name
        type: Python type of the parameter
        description: Human-readable description
        required: Whether the parameter is required
        default: Default value if not provided
    """
    name: str
    type: type
    description: str
    required: bool = True
    default: Any = None


@dataclass
class ToolDefinition:
    """
    Complete definition of an agent tool.
    
    Attributes:
        name: Unique tool identifier
        category: Category from ToolCategory enum
        description: What the tool does
        parameters: List of ToolParameter objects
        function: The actual callable function
        async_executable: Whether tool supports async execution
        examples: Usage examples
    """
    name: str
    category: ToolCategory
    description: str
    parameters: List[ToolParameter] = field(default_factory=list)
    function: Optional[Callable] = None
    async_executable: bool = True
    examples: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert tool definition to dictionary."""
        return {
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "parameters": [
                {
                    "name": p.name,
                    "type": p.type.__name__,
                    "description": p.description,
                    "required": p.required,
                    "default": p.default
                }
                for p in self.parameters
            ],
            "async_executable": self.async_executable,
            "examples": self.examples
        }


class BaseTool(ABC):
    """
    Abstract base class for all agent tools.
    
    All tools must inherit from this class and implement required methods.
    """
    
    def __init__(self):
        """Initialize the tool."""
        self.execution_count = 0
        self.error_count = 0
        self.total_time = 0.0
    
    @abstractmethod
    def get_definition(self) -> ToolDefinition:
        """Get tool definition with metadata."""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict:
        """
        Execute the tool with given parameters.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            Dictionary with execution results
        """
        pass
    
    async def safe_execute(self, **kwargs) -> Dict:
        """Execute tool with error handling and metrics."""
        import time
        start_time = time.time()
        
        try:
            result = await self.execute(**kwargs)
            self.execution_count += 1
            self.total_time += time.time() - start_time
            
            return {
                "success": True,
                "data": result,
                "execution_time": time.time() - start_time
            }
        except Exception as e:
            self.error_count += 1
            logger.error(f"Tool execution failed: {str(e)}", exc_info=True)
            
            return {
                "success": False,
                "error": str(e),
                "execution_time": time.time() - start_time
            }
    
    def get_metrics(self) -> Dict:
        """Get execution metrics for this tool."""
        return {
            "executions": self.execution_count,
            "errors": self.error_count,
            "total_time": self.total_time,
            "avg_time": self.total_time / max(self.execution_count, 1)
        }


class BrowserTool(BaseTool):
    """
    Tool for browser automation tasks.
    """
    
    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="browser_navigate",
            category=ToolCategory.BROWSER,
            description="Navigate to a URL and extract page content",
            parameters=[
                ToolParameter(
                    name="url",
                    type=str,
                    description="URL to navigate to"
                ),
                ToolParameter(
                    name="wait_time",
                    type=int,
                    description="Seconds to wait for page load",
                    required=False,
                    default=5
                )
            ],
            async_executable=True,
            examples=[
                "browser_navigate(url='https://example.com')",
                "browser_navigate(url='https://example.com', wait_time=10)"
            ]
        )
    
    async def execute(self, **kwargs) -> Dict:
        """
        Execute browser navigation.
        
        Args:
            url: Target URL
            wait_time: Optional wait time in seconds
            
        Returns:
            Dictionary with page content and metadata
        """
        url = kwargs.get("url")
        wait_time = kwargs.get("wait_time", 5)
        
        if not url:
            raise ValueError("URL parameter is required")
        
        try:
            logger.info(f"Navigating to {url}")
            # Simulate browser navigation
            await asyncio.sleep(min(wait_time, 2))  # Simulate loading
            
            return {
                "url": url,
                "title": f"Page from {url}",
                "content_length": 1000,
                "load_time": wait_time
            }
        except Exception as e:
            logger.error(f"Browser navigation failed: {str(e)}")
            raise


class WebSearchTool(BaseTool):
    """
    Tool for web searching and information retrieval.
    """
    
    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="web_search",
            category=ToolCategory.WEB,
            description="Search the web for information",
            parameters=[
                ToolParameter(
                    name="query",
                    type=str,
                    description="Search query"
                ),
                ToolParameter(
                    name="max_results",
                    type=int,
                    description="Maximum results to return",
                    required=False,
                    default=5
                )
            ],
            examples=["web_search(query='Python tutorials')", "web_search(query='AI latest news', max_results=10)"]
        )
    
    async def execute(self, **kwargs) -> Dict:
        """
        Execute web search.
        
        Args:
            query: Search query string
            max_results: Optional maximum results count
            
        Returns:
            Dictionary with search results
        """
        query = kwargs.get("query")
        max_results = kwargs.get("max_results", 5)
        
        if not query:
            raise ValueError("Query parameter is required")
        
        logger.info(f"Searching web for: {query}")
        
        # Simulate web search results
        return {
            "query": query,
            "total_results": max_results,
            "results": [{"title": f"Result {i+1} for {query}", "url": f"https://example.com/{i}"} for i in range(max_results)]
        }


class DataAnalysisTool(BaseTool):
    """
    Tool for data analysis and processing.
    """
    
    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="analyze_data",
            category=ToolCategory.ANALYSIS,
            description="Analyze structured data and extract insights",
            parameters=[
                ToolParameter(
                    name="data",
                    type=list,
                    description="Data to analyze"
                ),
                ToolParameter(
                    name="analysis_type",
                    type=str,
                    description="Type of analysis to perform"
                )
            ],
            examples=["analyze_data(data=[1, 2, 3, 4], analysis_type='summary')"]
        )
    
    async def execute(self, **kwargs) -> Dict:
        """
        Execute data analysis.
        
        Args:
            data: Data to analyze
            analysis_type: Type of analysis
            
        Returns:
            Dictionary with analysis results
        """
        data = kwargs.get("data", [])
        analysis_type = kwargs.get("analysis_type", "summary")
        
        logger.info(f"Analyzing data with {analysis_type} analysis")
        
        # Basic analysis simulation
        if isinstance(data, list) and data:
            return {
                "analysis_type": analysis_type,
                "item_count": len(data),
                "min": min(data) if all(isinstance(x, (int, float)) for x in data) else None,
                "max": max(data) if all(isinstance(x, (int, float)) for x in data) else None
            }
        
        return {"analysis_type": analysis_type, "item_count": 0}


class ToolRegistry:
    """
    Registry for managing all available tools.
    
    Provides centralized access to tool definitions and execution.
    """
    
    def __init__(self):
        """Initialize the tool registry."""
        self._tools: Dict[str, BaseTool] = {}
        self._categories: Dict[ToolCategory, List[str]] = {cat: [] for cat in ToolCategory}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools available to the agent."""
        self.register(BrowserTool())
        self.register(WebSearchTool())
        self.register(DataAnalysisTool())
    
    def register(self, tool: BaseTool) -> None:
        """
        Register a new tool in the registry.
        
        Args:
            tool: Tool instance to register
        """
        definition = tool.get_definition()
        self._tools[definition.name] = tool
        self._categories[definition.category].append(definition.name)
        logger.info(f"Registered tool: {definition.name}")
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """
        Get a specific tool by name.
        
        Args:
            name: Tool name
            
        Returns:
            Tool instance or None if not found
        """
        return self._tools.get(name)
    
    def get_tools_by_category(self, category: ToolCategory) -> List[BaseTool]:
        """
        Get all tools in a specific category.
        
        Args:
            category: Tool category
            
        Returns:
            List of tools in the category
        """
        tool_names = self._categories.get(category, [])
        return [self._tools[name] for name in tool_names if name in self._tools]
    
    def list_tools(self) -> List[Dict]:
        """
        List all available tools with their definitions.
        
        Returns:
            List of tool definition dictionaries
        """
        return [tool.get_definition().to_dict() for tool in self._tools.values()]
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Dict:
        """
        Execute a specific tool by name.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool parameters
            
        Returns:
            Execution result dictionary
        """
        tool = self.get_tool(tool_name)
        if not tool:
            return {"success": False, "error": f"Tool '{tool_name}' not found"}
        
        return await tool.safe_execute(**kwargs)
    
    def get_metrics(self) -> Dict:
        """
        Get aggregated metrics for all tools.
        
        Returns:
            Dictionary with metrics for each tool
        """
        return {name: tool.get_metrics() for name, tool in self._tools.items()}


# Global tool registry instance
_registry = None


def get_registry() -> ToolRegistry:
    """
    Get or create the global tool registry instance.
    
    Returns:
        Singleton instance of ToolRegistry
    """
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
    return _registry

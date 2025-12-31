"""OpenManus AI Agent Integration for AI Executive Agent
OpenManus: Open-source autonomous AI agent framework
Repository: https://github.com/FoundationAgents/OpenManus
"""
import asyncio
import logging
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from opik import track

from config.settings import settings

logger = logging.getLogger(__name__)


class OpenManusAgent:
    """OpenManus AI Agent - Autonomous code execution and task automation
    
    OpenManus is a powerful open-source AI agent that can:
    - Execute Python code autonomously
    - Perform data analysis and visualization
    - Handle file operations and workspace management
    - Integrate with various APIs and tools
    - Learn from execution results
    """
    
    def __init__(self, workspace_dir: str = "./workspace"):
        """Initialize OpenManus Agent
        
        Args:
            workspace_dir: Directory for agent workspace files
        """
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            temperature=0.2,  # Lower temperature for code generation
            api_key=settings.GOOGLE_API_KEY
        )
        
        # Execution history
        self.execution_history: List[Dict[str, Any]] = []
        
        # Tool registry
        self.tools = self._initialize_tools()
        
        logger.info("✅ OpenManus Agent initialized")
    
    def _initialize_tools(self) -> Dict[str, Any]:
        """Initialize available tools for the agent"""
        return {
            "python_executor": self._execute_python,
            "file_reader": self._read_file,
            "file_writer": self._write_file,
            "data_analyzer": self._analyze_data,
            "code_generator": self._generate_code,
            "task_planner": self._plan_task,
        }
    
    @track()
    async def execute_task(
        self, 
        task: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a task autonomously using OpenManus approach
        
        Args:
            task: Task description in natural language
            context: Additional context for the task
            
        Returns:
            Task execution result with code, output, and analysis
        """
        try:
            logger.info(f"🚀 OpenManus executing task: {task}")
            
            # Step 1: Plan the task
            plan = await self._plan_task(task, context or {})
            
            # Step 2: Generate code
            code = await self._generate_code(task, plan)
            
            # Step 3: Execute code
            execution_result = await self._execute_python(code)
            
            # Step 4: Analyze results
            analysis = await self._analyze_data(execution_result)
            
            # Step 5: Save to history
            result = {
                "success": True,
                "task": task,
                "plan": plan,
                "code": code,
                "execution": execution_result,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "workspace": str(self.workspace_dir)
            }
            
            self.execution_history.append(result)
            
            logger.info(f"✅ Task completed successfully: {task}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Task execution failed: {str(e)}")
            error_result = {
                "success": False,
                "task": task,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            self.execution_history.append(error_result)
            return error_result
    
    async def _plan_task(
        self, 
        task: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a detailed execution plan for the task"""
        prompt = f"""
        You are OpenManus AI Agent - an autonomous task planning expert.
        
        Task: {task}
        Context: {json.dumps(context, indent=2)}
        
        Create a detailed execution plan with:
        1. High-level approach
        2. Step-by-step breakdown
        3. Required tools and libraries
        4. Expected outputs
        5. Potential challenges and solutions
        
        Provide the plan in a structured JSON format.
        """
        
        response = await asyncio.to_thread(
            self.llm.invoke, prompt
        )
        
        try:
            # Try to parse JSON from response
            plan_text = response.content
            if "```json" in plan_text:
                plan_text = plan_text.split("```json")[1].split("```")[0]
            plan = json.loads(plan_text)
        except:
            # Fallback to text-based plan
            plan = {
                "approach": "Generate and execute Python code",
                "steps": [
                    "Analyze task requirements",
                    "Generate appropriate code",
                    "Execute code safely",
                    "Validate results"
                ],
                "tools": ["Python", "Standard Library"],
                "details": response.content
            }
        
        return plan
    
    async def _generate_code(
        self, 
        task: str, 
        plan: Dict[str, Any]
    ) -> str:
        """Generate Python code to accomplish the task"""
        prompt = f"""
        You are OpenManus AI Agent - an expert Python code generator.
        
        Task: {task}
        Plan: {json.dumps(plan, indent=2)}
        
        Generate clean, efficient, well-documented Python code that:
        1. Accomplishes the task completely
        2. Handles errors gracefully
        3. Returns clear results
        4. Follows best practices
        
        Important:
        - Include all necessary imports
        - Add proper error handling
        - Use type hints
        - Add docstrings
        - Make code production-ready
        
        Return ONLY the Python code without explanations.
        """
        
        response = await asyncio.to_thread(
            self.llm.invoke, prompt
        )
        
        code = response.content
        
        # Extract code from markdown if present
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0]
        elif "```" in code:
            code = code.split("```")[1].split("```")[0]
        
        return code.strip()
    
    async def _execute_python(self, code: str) -> Dict[str, Any]:
        """Execute Python code in a safe environment
        
        Args:
            code: Python code to execute
            
        Returns:
            Execution results including output, errors, and variables
        """
        logger.info("🐍 Executing Python code...")
        
        # Create safe execution environment
        safe_globals = {
            "__builtins__": __builtins__,
            "print": print,
            "len": len,
            "str": str,
            "int": int,
            "float": float,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
        }
        
        safe_locals = {}
        output = []
        errors = []
        
        # Capture print output
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            # Execute code
            exec(code, safe_globals, safe_locals)
            
            # Get captured output
            output_text = captured_output.getvalue()
            if output_text:
                output.append(output_text)
            
            result = {
                "success": True,
                "output": "\n".join(output),
                "variables": {
                    k: str(v) for k, v in safe_locals.items() 
                    if not k.startswith("_")
                },
                "code": code
            }
            
        except Exception as e:
            errors.append(str(e))
            result = {
                "success": False,
                "output": "\n".join(output),
                "errors": errors,
                "code": code
            }
        
        finally:
            sys.stdout = old_stdout
        
        return result
    
    async def _analyze_data(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze execution results and provide insights"""
        prompt = f"""
        You are OpenManus AI Agent - an expert data analyst.
        
        Analyze the following execution result:
        {json.dumps(execution_result, indent=2)}
        
        Provide:
        1. Summary of what was accomplished
        2. Key insights from the output
        3. Quality assessment
        4. Recommendations for improvement
        5. Next steps (if any)
        
        Return analysis in JSON format.
        """
        
        response = await asyncio.to_thread(
            self.llm.invoke, prompt
        )
        
        try:
            analysis_text = response.content
            if "```json" in analysis_text:
                analysis_text = analysis_text.split("```json")[1].split("```")[0]
            analysis = json.loads(analysis_text)
        except:
            analysis = {
                "summary": "Task executed",
                "insights": response.content,
                "quality": "good",
                "recommendations": [],
                "next_steps": []
            }
        
        return analysis
    
    async def _read_file(self, file_path: str) -> str:
        """Read file from workspace"""
        full_path = self.workspace_dir / file_path
        try:
            with open(full_path, 'r') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            raise
    
    async def _write_file(self, file_path: str, content: str) -> bool:
        """Write file to workspace"""
        full_path = self.workspace_dir / file_path
        try:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Failed to write file {file_path}: {e}")
            return False
    
    @track()
    async def batch_execute(
        self, 
        tasks: List[str], 
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute multiple tasks in batch
        
        Args:
            tasks: List of task descriptions
            context: Shared context for all tasks
            
        Returns:
            List of execution results
        """
        results = []
        
        for i, task in enumerate(tasks):
            logger.info(f"📋 Executing batch task {i+1}/{len(tasks)}")
            result = await self.execute_task(task, context)
            results.append(result)
            
            # Add short delay between tasks
            await asyncio.sleep(1)
        
        return results
    
    def get_execution_history(
        self, 
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get execution history
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of execution records
        """
        if limit:
            return self.execution_history[-limit:]
        return self.execution_history
    
    def clear_history(self):
        """Clear execution history"""
        self.execution_history = []
        logger.info("🗑️ Execution history cleared")
    
    async def self_improve(self) -> Dict[str, Any]:
        """Analyze past executions and generate improvement suggestions"""
        if not self.execution_history:
            return {
                "message": "No execution history to analyze",
                "suggestions": []
            }
        
        prompt = f"""
        You are OpenManus AI Agent - a self-improving AI system.
        
        Analyze the following execution history and provide improvement suggestions:
        {json.dumps(self.execution_history[-10:], indent=2)}
        
        Identify:
        1. Common patterns in successful executions
        2. Frequent error patterns
        3. Code quality improvements
        4. Performance optimizations
        5. New capabilities to add
        
        Provide actionable suggestions for self-improvement.
        """
        
        response = await asyncio.to_thread(
            self.llm.invoke, prompt
        )
        
        return {
            "analysis_date": datetime.now().isoformat(),
            "executions_analyzed": len(self.execution_history),
            "suggestions": response.content
        }


# Global instance
_openmanus_agent: Optional[OpenManusAgent] = None


def get_openmanus_agent(workspace_dir: str = "./workspace") -> OpenManusAgent:
    """Get or create the global OpenManus agent instance"""
    global _openmanus_agent
    if _openmanus_agent is None:
        _openmanus_agent = OpenManusAgent(workspace_dir)
    return _openmanus_agent


async def main():
    """Example usage of OpenManus Agent"""
    agent = get_openmanus_agent()
    
    # Example task
    task = "Create a Python function that calculates the Fibonacci sequence up to n terms"
    result = await agent.execute_task(task)
    
    print("✅ Task Result:")
    print(json.dumps(result, indent=2))
    
    # Self-improvement
    improvement = await agent.self_improve()
    print("\n🔧 Self-Improvement Suggestions:")
    print(json.dumps(improvement, indent=2))


if __name__ == "__main__":
    asyncio.run(main())

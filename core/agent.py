"""AI Executive Agent - Main Agent Class with Browser-Use Integration"""
import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from browser_use import Agent as BrowserAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from crewai import Agent, Task, Crew
import comet_ml
from opik import track

from config.settings import settings

logger = logging.getLogger(__name__)


class ExecutiveAgent:
    """Main Executive Agent with multi-agent coordination"""
    
    def __init__(self):
        """Initialize the Executive Agent with all integrations"""
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            api_key=settings.GOOGLE_API_KEY
        )
        
        # Initialize Comet ML for tracking
        if settings.ENABLE_MONITORING:
            self.comet_experiment = comet_ml.Experiment(
                api_key=settings.COMET_API_KEY,
                project_name=settings.COMET_PROJECT_NAME,
                workspace=settings.COMET_WORKSPACE
            )
        else:
            self.comet_experiment = None
        
        # Initialize Browser Agent
        if settings.ENABLE_BROWSER_AUTOMATION:
            self.browser_agent = BrowserAgent(
                llm=self.llm,
                use_vision=True,
                max_actions=50
            )
        else:
            self.browser_agent = None
        
        # Initialize crew for multi-agent tasks
        self.crew = None
        self.state_graph = None
        
        logger.info("✅ Executive Agent initialized successfully")
    
    @track()
    async def execute_browser_task(self, task: str, context: str = "") -> Dict[str, Any]:
        """Execute a task using Browser-Use
        
        Args:
            task: The task to execute
            context: Additional context for the task
            
        Returns:
            Dict with task results
        """
        if not self.browser_agent:
            raise RuntimeError("Browser automation is disabled")
        
        try:
            prompt = f"""
            Task: {task}
            Context: {context}
            
            Instructions:
            1. Analyze the current page
            2. Execute the task step by step
            3. Return the results
            """
            
            result = await self.browser_agent.run(prompt)
            
            # Log to Comet ML
            if self.comet_experiment:
                self.comet_experiment.log_metric(
                    "browser_task_success", 1
                )
            
            logger.info(f"✅ Browser task completed: {task}")
            return {
                "success": True,
                "task": task,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Browser task failed: {str(e)}")
            if self.comet_experiment:
                self.comet_experiment.log_metric("browser_task_error", 1)
            return {
                "success": False,
                "task": task,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    @track()
    async def analyze_and_decide(self, data: str) -> Dict[str, Any]:
        """Analyze data and make decisions
        
        Args:
            data: Data to analyze
            
        Returns:
            Analysis results and decisions
        """
        try:
            prompt = f"""
            Analyze this data and provide insights:
            {data}
            
            Provide:
            1. Summary
            2. Key insights
            3. Recommended actions
            """
            
            response = self.llm.invoke(prompt)
            
            if self.comet_experiment:
                self.comet_experiment.log_metric(
                    "analysis_completed", 1
                )
            
            return {
                "success": True,
                "analysis": response.content,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Analysis failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    @track()
    async def execute_workflow(self, workflow_steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a multi-step workflow
        
        Args:
            workflow_steps: List of workflow steps to execute
            
        Returns:
            Workflow execution results
        """
        results = []
        
        try:
            for i, step in enumerate(workflow_steps):
                logger.info(f"Executing step {i+1}/{len(workflow_steps)}: {step.get('name')}")
                
                step_type = step.get("type", "browser")
                
                if step_type == "browser":
                    result = await self.execute_browser_task(
                        step.get("task"),
                        step.get("context", "")
                    )
                elif step_type == "analyze":
                    result = await self.analyze_and_decide(
                        step.get("data", "")
                    )
                else:
                    result = {"error": f"Unknown step type: {step_type}"}
                
                results.append(result)
                
                if not result.get("success"):
                    logger.warning(f"Step {i+1} failed, continuing...")
            
            if self.comet_experiment:
                self.comet_experiment.log_metric(
                    "workflow_steps_completed",
                    len([r for r in results if r.get("success")])
                )
            
            return {
                "success": True,
                "total_steps": len(workflow_steps),
                "completed_steps": len([r for r in results if r.get("success")]),
                "results": results,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Workflow failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "results": results
            }
    
    def cleanup(self):
        """Cleanup resources"""
        if self.comet_experiment:
            self.comet_experiment.end()
        logger.info("✅ Agent cleanup completed")


# Global instance
_agent: Optional[ExecutiveAgent] = None


def get_agent() -> ExecutiveAgent:
    """Get or create the global agent instance"""
    global _agent
    if _agent is None:
        _agent = ExecutiveAgent()
    return _agent


async def main():
    """Example usage of the agent"""
    agent = get_agent()
    
    # Example workflow
    workflow = [
        {
            "type": "browser",
            "name": "Open Google",
            "task": "Go to google.com",
            "context": "Search engine"
        },
        {
            "type": "analyze",
            "name": "Analyze Search Results",
            "data": "User query results from search"
        }
    ]
    
    result = await agent.execute_workflow(workflow)
    print(f"Workflow Result: {result}")
    
    agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())

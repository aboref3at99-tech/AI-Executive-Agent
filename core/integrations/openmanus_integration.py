"""OpenManus Integration Module
Integrates OpenManus Agent with Executive Agent and monitoring systems
"""
import logging
from typing import Dict, Any, List, Optional
import comet_ml
from opik import track

from core.openmanus_agent import OpenManusAgent, get_openmanus_agent
from config.settings import settings

logger = logging.getLogger(__name__)


class OpenManusIntegration:
    """Integration layer between OpenManus and Executive Agent"""
    
    def __init__(
        self, 
        workspace_dir: str = "./workspace",
        enable_monitoring: bool = True
    ):
        """Initialize OpenManus integration
        
        Args:
            workspace_dir: Workspace directory for OpenManus
            enable_monitoring: Enable Comet ML monitoring
        """
        self.agent = get_openmanus_agent(workspace_dir)
        self.enable_monitoring = enable_monitoring and settings.ENABLE_MONITORING
        
        # Initialize Comet ML experiment if monitoring is enabled
        if self.enable_monitoring:
            self.comet_experiment = comet_ml.Experiment(
                api_key=settings.COMET_API_KEY,
                project_name=f"{settings.COMET_PROJECT_NAME}-openmanus",
                workspace=settings.COMET_WORKSPACE
            )
            self.comet_experiment.add_tag("openmanus")
            self.comet_experiment.add_tag("autonomous-agent")
        else:
            self.comet_experiment = None
        
        logger.info("✅ OpenManus Integration initialized")
    
    @track()
    async def execute_autonomous_task(
        self, 
        task: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a task autonomously using OpenManus
        
        Args:
            task: Task description
            context: Additional context
            
        Returns:
            Execution result with monitoring data
        """
        try:
            # Log to Comet ML
            if self.comet_experiment:
                self.comet_experiment.log_parameter("task", task)
                self.comet_experiment.log_parameter(
                    "context_keys", 
                    list(context.keys()) if context else []
                )
            
            # Execute task
            result = await self.agent.execute_task(task, context)
            
            # Log results to Comet ML
            if self.comet_experiment:
                self.comet_experiment.log_metric(
                    "task_success", 
                    1 if result.get("success") else 0
                )
                
                if result.get("success"):
                    self.comet_experiment.log_code(
                        result.get("code", ""),
                        file_name="generated_code.py"
                    )
                    self.comet_experiment.log_other(
                        "execution_output",
                        result.get("execution", {}).get("output", "")
                    )
                    self.comet_experiment.log_other(
                        "analysis",
                        result.get("analysis", {})
                    )
                else:
                    self.comet_experiment.log_other(
                        "error",
                        result.get("error", "Unknown error")
                    )
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Autonomous task execution failed: {str(e)}")
            
            if self.comet_experiment:
                self.comet_experiment.log_metric("task_error", 1)
                self.comet_experiment.log_other("error_message", str(e))
            
            return {
                "success": False,
                "task": task,
                "error": str(e)
            }
    
    @track()
    async def batch_execute_tasks(
        self,
        tasks: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute multiple tasks in batch
        
        Args:
            tasks: List of task descriptions
            context: Shared context
            
        Returns:
            List of execution results
        """
        if self.comet_experiment:
            self.comet_experiment.log_parameter("batch_size", len(tasks))
        
        results = await self.agent.batch_execute(tasks, context)
        
        if self.comet_experiment:
            success_count = len([r for r in results if r.get("success")])
            self.comet_experiment.log_metric("batch_success_rate", 
                                            success_count / len(tasks))
            self.comet_experiment.log_metric("batch_total_tasks", len(tasks))
            self.comet_experiment.log_metric("batch_successful_tasks", 
                                            success_count)
        
        return results
    
    @track()
    async def data_analysis_task(
        self,
        data_description: str,
        analysis_type: str = "exploratory"
    ) -> Dict[str, Any]:
        """Execute a data analysis task
        
        Args:
            data_description: Description of data to analyze
            analysis_type: Type of analysis (exploratory, statistical, visual)
            
        Returns:
            Analysis results with code and visualizations
        """
        task = f"""
        Perform {analysis_type} data analysis on: {data_description}
        
        Requirements:
        1. Load or generate the data
        2. Perform appropriate analysis
        3. Generate visualizations (if applicable)
        4. Provide summary statistics
        5. Return actionable insights
        """
        
        context = {
            "analysis_type": analysis_type,
            "data_description": data_description,
            "output_format": "structured"
        }
        
        return await self.execute_autonomous_task(task, context)
    
    @track()
    async def code_generation_task(
        self,
        requirement: str,
        language: str = "python",
        include_tests: bool = True
    ) -> Dict[str, Any]:
        """Generate code based on requirements
        
        Args:
            requirement: Code requirements
            language: Programming language
            include_tests: Whether to include unit tests
            
        Returns:
            Generated code with tests and documentation
        """
        task = f"""
        Generate {language} code for: {requirement}
        
        Requirements:
        1. Write clean, well-documented code
        2. Include type hints
        3. Add error handling
        {"4. Include unit tests" if include_tests else ""}
        5. Follow best practices
        """
        
        context = {
            "language": language,
            "include_tests": include_tests,
            "requirement": requirement
        }
        
        return await self.execute_autonomous_task(task, context)
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics from execution history"""
        history = self.agent.get_execution_history()
        
        if not history:
            return {
                "total_executions": 0,
                "successful": 0,
                "failed": 0,
                "success_rate": 0.0
            }
        
        successful = len([h for h in history if h.get("success")])
        failed = len(history) - successful
        
        metrics = {
            "total_executions": len(history),
            "successful": successful,
            "failed": failed,
            "success_rate": successful / len(history) if history else 0.0,
            "recent_tasks": [h.get("task") for h in history[-5:]]
        }
        
        if self.comet_experiment:
            self.comet_experiment.log_metrics(metrics)
        
        return metrics
    
    async def self_improvement_analysis(self) -> Dict[str, Any]:
        """Analyze agent performance and suggest improvements"""
        improvement = await self.agent.self_improve()
        
        if self.comet_experiment:
            self.comet_experiment.log_other(
                "self_improvement_suggestions",
                improvement
            )
        
        return improvement
    
    def cleanup(self):
        """Cleanup resources"""
        if self.comet_experiment:
            self.comet_experiment.end()
        logger.info("✅ OpenManus Integration cleanup completed")


# Global instance
_openmanus_integration: Optional[OpenManusIntegration] = None


def get_openmanus_integration(
    workspace_dir: str = "./workspace",
    enable_monitoring: bool = True
) -> OpenManusIntegration:
    """Get or create the global OpenManus integration instance"""
    global _openmanus_integration
    if _openmanus_integration is None:
        _openmanus_integration = OpenManusIntegration(
            workspace_dir, 
            enable_monitoring
        )
    return _openmanus_integration

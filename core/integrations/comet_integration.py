"""Comet ML and Opik Integration for Monitoring"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

import comet_ml
from opik import track, start_session
from opik.opik_context import get_current_session

from config.settings import settings

logger = logging.getLogger(__name__)


class CometMLIntegration:
    """Comet ML integration for experiment tracking"""
    
    def __init__(self):
        """Initialize Comet ML experiment"""
        try:
            self.experiment = comet_ml.Experiment(
                api_key=settings.COMET_API_KEY,
                project_name=settings.COMET_PROJECT_NAME,
                workspace=settings.COMET_WORKSPACE,
                auto_metric_logging=True,
                auto_param_logging=True
            )
            logger.info("✅ Comet ML initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Comet ML: {str(e)}")
            self.experiment = None
    
    def log_metric(self, name: str, value: float, step: Optional[int] = None):
        """Log metric to Comet ML"""
        try:
            if self.experiment:
                self.experiment.log_metric(name, value, step=step)
        except Exception as e:
            logger.error(f"❌ Failed to log metric: {str(e)}")
    
    def log_parameter(self, name: str, value: Any):
        """Log parameter to Comet ML"""
        try:
            if self.experiment:
                self.experiment.log_parameter(name, value)
        except Exception as e:
            logger.error(f"❌ Failed to log parameter: {str(e)}")
    
    def log_dict(self, data: Dict[str, Any], prefix: str = ""):
        """Log dictionary to Comet ML"""
        try:
            if self.experiment:
                for key, value in data.items():
                    param_name = f"{prefix}_{key}" if prefix else key
                    if isinstance(value, (int, float, str, bool)):
                        self.experiment.log_parameter(param_name, value)
        except Exception as e:
            logger.error(f"❌ Failed to log dict: {str(e)}")
    
    def log_json(self, data: Dict[str, Any], name: str = "data"):
        """Log JSON data to Comet ML"""
        try:
            if self.experiment:
                self.experiment.log_json(data, name=name)
        except Exception as e:
            logger.error(f"❌ Failed to log JSON: {str(e)}")
    
    def end(self):
        """End Comet ML experiment"""
        try:
            if self.experiment:
                self.experiment.end()
                logger.info("✅ Comet ML experiment ended")
        except Exception as e:
            logger.error(f"❌ Failed to end Comet ML: {str(e)}")


class OpikMonitoring:
    """Opik LLM monitoring integration"""
    
    def __init__(self):
        """Initialize Opik monitoring"""
        try:
            self.session = start_session(
                project_name=settings.COMET_PROJECT_NAME,
                workspace=settings.COMET_WORKSPACE
            )
            logger.info("✅ Opik monitoring initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Opik: {str(e)}")
            self.session = None
    
    @track()
    def track_llm_call(self, 
                       model: str,
                       prompt: str,
                       response: str,
                       metadata: Optional[Dict[str, Any]] = None):
        """Track LLM call with Opik
        
        Args:
            model: Model name
            prompt: Input prompt
            response: Model response
            metadata: Additional metadata
        """
        try:
            session = get_current_session()
            if session:
                session.log_llm_call(
                    model=model,
                    prompt=prompt,
                    response=response,
                    metadata=metadata or {}
                )
                logger.debug(f"🔍 LLM call tracked: {model}")
        except Exception as e:
            logger.error(f"❌ Failed to track LLM call: {str(e)}")
    
    def end_session(self):
        """End Opik session"""
        try:
            if self.session:
                self.session.end()
                logger.info("✅ Opik session ended")
        except Exception as e:
            logger.error(f"❌ Failed to end Opik session: {str(e)}")


class MonitoringManager:
    """Unified monitoring management"""
    
    def __init__(self):
        """Initialize monitoring systems"""
        self.comet = CometMLIntegration() if settings.ENABLE_MONITORING else None
        self.opik = OpikMonitoring() if settings.ENABLE_MONITORING else None
    
    def log_agent_start(self, agent_name: str, task_description: str):
        """Log agent start"""
        if self.comet:
            self.comet.log_dict({
                "agent": agent_name,
                "task": task_description,
                "timestamp": datetime.now().isoformat(),
                "status": "started"
            }, prefix="agent")
    
    def log_agent_end(self, agent_name: str, success: bool, result: Optional[Dict] = None):
        """Log agent end"""
        if self.comet:
            self.comet.log_metric("agent_success", 1.0 if success else 0.0)
            if result:
                self.comet.log_json(result, name=f"{agent_name}_result")
    
    def log_browser_task(self, task: str, success: bool, duration: float):
        """Log browser task"""
        if self.comet:
            self.comet.log_metric("browser_task_success", 1.0 if success else 0.0)
            self.comet.log_metric("browser_task_duration", duration)
    
    def cleanup(self):
        """Cleanup monitoring systems"""
        if self.comet:
            self.comet.end()
        if self.opik:
            self.opik.end_session()
        logger.info("✅ Monitoring cleanup completed")


# Global monitoring instance
_monitoring: Optional[MonitoringManager] = None


def get_monitoring() -> MonitoringManager:
    """Get or create global monitoring instance"""
    global _monitoring
    if _monitoring is None:
        _monitoring = MonitoringManager()
    return _monitoring

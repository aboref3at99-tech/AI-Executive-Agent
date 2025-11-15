#!/usr/bin/env python3
"""
AI Executive Agent - Main Entry Point

A comprehensive AI-powered automation platform that combines browser automation,
intelligent decision-making, and multi-agent coordination.

Usage:
    python main.py --task "Search for the latest AI news"
    python main.py --interactive
"""

import asyncio
import logging
import argparse
from pathlib import Path
from typing import Optional

from config.settings import Settings
from core.agent import ExecutiveAgent
from integrations.comet_integration import CometMLIntegration, OpikMonitoring

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class AgentController:
    """
    Controller for managing the AI Executive Agent lifecycle.
    
    Handles initialization, execution, and monitoring of agent tasks.
    Integrates with Comet ML and Opik for comprehensive tracking.
    """
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize the agent controller.
        
        Args:
            settings: Configuration settings. If None, uses defaults.
        """
        self.settings = settings or Settings()
        self.agent = ExecutiveAgent(self.settings)
        
        # Initialize monitoring
        self.comet_ml = CometMLIntegration(self.settings)
        self.opik_monitor = OpikMonitoring(self.settings)
        
        logger.info("Agent controller initialized")
    
    async def execute_task(self, task: str, max_iterations: int = 5) -> dict:
        """
        Execute a single task with the agent.
        
        Args:
            task: Task description to execute
            max_iterations: Maximum iterations for task completion
            
        Returns:
            Dictionary containing task results and metrics
        """
        logger.info(f"Executing task: {task}")
        
        try:
            # Start Comet ML experiment
            experiment = self.comet_ml.start_experiment(
                task_name=task,
                metadata={"max_iterations": max_iterations}
            )
            
            # Execute the task
            result = await self.agent.execute_workflow(
                task=task,
                max_iterations=max_iterations
            )
            
            # Log metrics
            self.comet_ml.log_task_result(result)
            
            logger.info(f"Task completed successfully: {task}")
            return result
            
        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}", exc_info=True)
            self.comet_ml.log_error(str(e))
            raise
        finally:
            self.comet_ml.end_experiment()
    
    async def interactive_session(self):
        """
        Start an interactive session with the agent.
        
        Allows users to enter tasks and interact with the agent in real-time.
        """
        logger.info("Starting interactive session")
        print("\n" + "="*60)
        print("AI Executive Agent - Interactive Mode")
        print("="*60)
        print("Type your task and press Enter.")
        print("Type 'quit' to exit.\n")
        
        session_tasks = []
        
        try:
            while True:
                task = input("\n> Enter task: ").strip()
                
                if task.lower() == 'quit':
                    break
                
                if not task:
                    print("Please enter a valid task.")
                    continue
                
                print(f"\nProcessing: {task}")
                result = await self.execute_task(task)
                
                session_tasks.append({
                    'task': task,
                    'result': result
                })
                
                print(f"Result: {result.get('summary', 'Task completed')}")
                
        except KeyboardInterrupt:
            print("\n\nInteractive session interrupted.")
        except Exception as e:
            logger.error(f"Interactive session error: {str(e)}", exc_info=True)
            print(f"\nError: {str(e)}")
        finally:
            print(f"\nSession completed. Processed {len(session_tasks)} tasks.")
            logger.info(f"Interactive session ended. Tasks processed: {len(session_tasks)}")


async def main():
    """
    Main entry point for the application.
    
    Parses command-line arguments and routes to appropriate execution mode.
    """
    parser = argparse.ArgumentParser(
        description="AI Executive Agent - Intelligent Automation Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --task "Search for Python tutorials"
  python main.py --interactive
  python main.py --benchmark
        """
    )
    
    parser.add_argument(
        '--task',
        type=str,
        help='Execute a specific task'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Start interactive mode'
    )
    parser.add_argument(
        '--iterations',
        type=int,
        default=5,
        help='Maximum iterations for task execution (default: 5)'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level (default: INFO)'
    )
    
    args = parser.parse_args()
    
    # Create logs directory if it doesn't exist
    Path('logs').mkdir(exist_ok=True)
    
    # Update logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    try:
        # Initialize settings and controller
        settings = Settings()
        controller = AgentController(settings)
        
        if args.task:
            # Execute single task
            result = await controller.execute_task(
                task=args.task,
                max_iterations=args.iterations
            )
            print("\nTask Result:")
            print(f"Status: {result.get('status', 'unknown')}")
            print(f"Summary: {result.get('summary', 'N/A')}")
            
        elif args.interactive:
            # Start interactive mode
            await controller.interactive_session()
        else:
            # Default: Show help
            parser.print_help()
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        print(f"\nFatal error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        exit(0)
    except Exception as e:
        logger.critical(f"Unhandled exception: {str(e)}", exc_info=True)
        exit(1)

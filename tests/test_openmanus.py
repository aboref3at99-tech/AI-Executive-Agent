"""Unit Tests for OpenManus Agent Integration
Comprehensive test suite for OpenManus autonomous agent functionality
"""
import pytest
import asyncio
import json
from pathlib import Path

from core.openmanus_agent import OpenManusAgent, get_openmanus_agent
from core.integrations.openmanus_integration import (
    OpenManusIntegration,
    get_openmanus_integration
)


class TestOpenManusAgent:
    """Test suite for OpenManus Agent"""
    
    @pytest.fixture
    def agent(self, tmp_path):
        """Create a test agent instance"""
        workspace = tmp_path / "test_workspace"
        workspace.mkdir()
        return OpenManusAgent(workspace_dir=str(workspace))
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self, agent):
        """Test agent initializes correctly"""
        assert agent is not None
        assert agent.workspace_dir.exists()
        assert len(agent.tools) > 0
        assert agent.llm is not None
    
    @pytest.mark.asyncio
    async def test_task_planning(self, agent):
        """Test task planning functionality"""
        task = "Calculate the sum of numbers from 1 to 10"
        context = {"language": "python"}
        
        plan = await agent._plan_task(task, context)
        
        assert plan is not None
        assert isinstance(plan, dict)
        # Plan should contain some structure
        assert len(plan) > 0
    
    @pytest.mark.asyncio
    async def test_code_generation(self, agent):
        """Test code generation"""
        task = "Create a function to calculate factorial"
        plan = {"approach": "Implement recursive factorial function"}
        
        code = await agent._generate_code(task, plan)
        
        assert code is not None
        assert isinstance(code, str)
        assert len(code) > 0
        # Should look like Python code
        assert any(keyword in code.lower() for keyword in ['def', 'return', 'factorial'])
    
    @pytest.mark.asyncio
    async def test_python_execution_success(self, agent):
        """Test successful Python code execution"""
        code = """
result = 2 + 2
print(f"Result: {result}")
"""
        
        execution = await agent._execute_python(code)
        
        assert execution is not None
        assert execution.get("success") is True
        assert "4" in execution.get("output", "")
    
    @pytest.mark.asyncio
    async def test_python_execution_error(self, agent):
        """Test Python code execution with errors"""
        code = """
result = 1 / 0  # This will raise ZeroDivisionError
"""
        
        execution = await agent._execute_python(code)
        
        assert execution is not None
        assert execution.get("success") is False
        assert len(execution.get("errors", [])) > 0
    
    @pytest.mark.asyncio
    async def test_execute_task_complete(self, agent):
        """Test complete task execution"""
        task = "Calculate the sum of numbers 1 to 5"
        
        result = await agent.execute_task(task)
        
        assert result is not None
        assert "task" in result
        assert "plan" in result
        assert "code" in result
        assert "execution" in result
        assert "timestamp" in result
    
    @pytest.mark.asyncio
    async def test_batch_execution(self, agent):
        """Test batch task execution"""
        tasks = [
            "Calculate 5 factorial",
            "Generate Fibonacci sequence up to 10",
            "Find prime numbers up to 20"
        ]
        
        results = await agent.batch_execute(tasks)
        
        assert len(results) == len(tasks)
        for result in results:
            assert "task" in result
            assert "timestamp" in result
    
    @pytest.mark.asyncio
    async def test_file_operations(self, agent):
        """Test file read/write operations"""
        content = "Test content for file operations"
        file_path = "test_file.txt"
        
        # Write file
        write_success = await agent._write_file(file_path, content)
        assert write_success is True
        
        # Read file
        read_content = await agent._read_file(file_path)
        assert read_content == content
    
    @pytest.mark.asyncio
    async def test_execution_history(self, agent):
        """Test execution history tracking"""
        task = "Simple calculation"
        
        # Execute a task
        await agent.execute_task(task)
        
        # Check history
        history = agent.get_execution_history()
        assert len(history) > 0
        assert history[-1]["task"] == task
        
        # Clear history
        agent.clear_history()
        assert len(agent.get_execution_history()) == 0
    
    @pytest.mark.asyncio
    async def test_self_improvement(self, agent):
        """Test self-improvement analysis"""
        # Execute some tasks first
        await agent.execute_task("Calculate 2+2")
        await agent.execute_task("Print hello world")
        
        improvement = await agent.self_improve()
        
        assert improvement is not None
        assert "executions_analyzed" in improvement
        assert improvement["executions_analyzed"] > 0


class TestOpenManusIntegration:
    """Test suite for OpenManus Integration"""
    
    @pytest.fixture
    def integration(self, tmp_path):
        """Create a test integration instance"""
        workspace = tmp_path / "integration_workspace"
        workspace.mkdir()
        return OpenManusIntegration(
            workspace_dir=str(workspace),
            enable_monitoring=False  # Disable monitoring for tests
        )
    
    @pytest.mark.asyncio
    async def test_integration_initialization(self, integration):
        """Test integration initializes correctly"""
        assert integration is not None
        assert integration.agent is not None
        assert integration.enable_monitoring is False
    
    @pytest.mark.asyncio
    async def test_autonomous_task_execution(self, integration):
        """Test autonomous task execution through integration"""
        task = "Create a list of even numbers from 2 to 10"
        context = {"format": "list"}
        
        result = await integration.execute_autonomous_task(task, context)
        
        assert result is not None
        assert "task" in result
    
    @pytest.mark.asyncio
    async def test_batch_tasks_execution(self, integration):
        """Test batch task execution through integration"""
        tasks = [
            "Calculate 10 + 20",
            "Calculate 50 - 30"
        ]
        
        results = await integration.batch_execute_tasks(tasks)
        
        assert len(results) == len(tasks)
    
    @pytest.mark.asyncio
    async def test_data_analysis_task(self, integration):
        """Test data analysis task"""
        data_description = "A list of numbers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
        
        result = await integration.data_analysis_task(data_description)
        
        assert result is not None
        assert "task" in result
    
    @pytest.mark.asyncio
    async def test_code_generation_task(self, integration):
        """Test code generation task"""
        requirement = "Function to check if a number is prime"
        
        result = await integration.code_generation_task(
            requirement,
            language="python",
            include_tests=True
        )
        
        assert result is not None
        assert "task" in result
        # Should contain code
        if result.get("success"):
            assert "code" in result
    
    def test_performance_metrics(self, integration):
        """Test performance metrics collection"""
        metrics = integration.get_performance_metrics()
        
        assert metrics is not None
        assert "total_executions" in metrics
        assert "successful" in metrics
        assert "failed" in metrics
        assert "success_rate" in metrics
    
    @pytest.mark.asyncio
    async def test_self_improvement_analysis(self, integration):
        """Test self-improvement analysis through integration"""
        # Execute a task first
        await integration.execute_autonomous_task("Test task")
        
        improvement = await integration.self_improvement_analysis()
        
        assert improvement is not None
        assert "executions_analyzed" in improvement
    
    def test_cleanup(self, integration):
        """Test integration cleanup"""
        integration.cleanup()
        # Should complete without errors


class TestGlobalInstances:
    """Test global instance getters"""
    
    def test_get_openmanus_agent(self):
        """Test global agent getter"""
        agent = get_openmanus_agent()
        assert agent is not None
        
        # Should return same instance
        agent2 = get_openmanus_agent()
        assert agent is agent2
    
    def test_get_openmanus_integration(self):
        """Test global integration getter"""
        integration = get_openmanus_integration(enable_monitoring=False)
        assert integration is not None
        
        # Should return same instance
        integration2 = get_openmanus_integration(enable_monitoring=False)
        assert integration is integration2


# Integration tests with Executive Agent
class TestExecutiveAgentIntegration:
    """Test OpenManus integration with Executive Agent"""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_executive_agent_with_openmanus(self):
        """Test ExecutiveAgent uses OpenManus correctly"""
        from core.agent import get_agent
        
        agent = get_agent()
        
        # Test autonomous task
        result = await agent.execute_autonomous_task(
            "Calculate the square of numbers from 1 to 5"
        )
        
        assert result is not None
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_executive_agent_code_generation(self):
        """Test code generation through ExecutiveAgent"""
        from core.agent import get_agent
        
        agent = get_agent()
        
        result = await agent.code_generation(
            "Function to reverse a string"
        )
        
        assert result is not None
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_executive_agent_data_analysis(self):
        """Test data analysis through ExecutiveAgent"""
        from core.agent import get_agent
        
        agent = get_agent()
        
        result = await agent.data_analysis(
            "Temperature data: [20, 22, 21, 23, 22, 24]",
            analysis_type="statistical"
        )
        
        assert result is not None


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])

# OpenManus AI Agent Integration

## 🤖 Overview

**OpenManus** is a powerful open-source autonomous AI agent integrated into the AI Executive Agent system. Inspired by the original [Manus.im](https://manus.im/) AI agent, OpenManus provides autonomous code execution, data analysis, and task automation capabilities.

### Key Features

- ✅ **Autonomous Task Execution** - Execute complex tasks with minimal human intervention
- 💻 **Code Generation & Execution** - Generate and execute Python code automatically
- 📊 **Data Analysis** - Perform statistical analysis and generate insights
- 🔄 **Batch Processing** - Execute multiple tasks in parallel
- 🧠 **Self-Improvement** - Learn from execution history and optimize performance
- 📝 **Workspace Management** - Organized file system for task outputs
- 🔍 **Full Monitoring** - Integration with Comet ML and Opik for tracking

---

## 🏗️ Architecture

### Component Structure

```
OpenManus Agent
├── Core Agent (openmanus_agent.py)
│   ├── Task Planning
│   ├── Code Generation
│   ├── Code Execution
│   ├── Result Analysis
│   └── Self-Improvement
│
├── Integration Layer (openmanus_integration.py)
│   ├── Executive Agent Integration
│   ├── Monitoring Integration
│   ├── Performance Metrics
│   └── Batch Processing
│
└── Tools Registry
    ├── Python Executor
    ├── File Operations
    ├── Data Analyzer
    └── Code Generator
```

### Data Flow

```
User Request
    ↓
Executive Agent
    ↓
OpenManus Integration
    ↓
OpenManus Agent
    ├→ Plan Task
    ├→ Generate Code
    ├→ Execute Code
    ├→ Analyze Results
    └→ Self-Improve
    ↓
Return Results
    ↓
Monitor & Track (Comet ML/Opik)
```

---

## 🚀 Quick Start

### 1. Basic Usage

```python
from core.openmanus_agent import get_openmanus_agent

# Get agent instance
agent = get_openmanus_agent()

# Execute a task
result = await agent.execute_task(
    "Calculate the factorial of 10"
)

print(result)
```

### 2. With Executive Agent

```python
from core.agent import get_agent

# Get executive agent (includes OpenManus)
agent = get_agent()

# Execute autonomous task
result = await agent.execute_autonomous_task(
    "Analyze sales data and provide insights"
)
```

### 3. Data Analysis

```python
from core.integrations.openmanus_integration import get_openmanus_integration

integration = get_openmanus_integration()

# Perform data analysis
result = await integration.data_analysis_task(
    data_description="Monthly revenue: [10000, 12000, 11500, 13000]",
    analysis_type="statistical"
)
```

### 4. Code Generation

```python
# Generate code with tests
result = await integration.code_generation_task(
    requirement="Create a binary search function",
    language="python",
    include_tests=True
)
```

---

## 📚 API Reference

### OpenManusAgent

#### Core Methods

**`execute_task(task: str, context: Optional[Dict] = None) -> Dict`**
- Execute a task autonomously
- Args:
  - `task`: Task description in natural language
  - `context`: Additional context (optional)
- Returns: Dictionary with execution results

**`batch_execute(tasks: List[str], context: Optional[Dict] = None) -> List[Dict]`**
- Execute multiple tasks in batch
- Args:
  - `tasks`: List of task descriptions
  - `context`: Shared context (optional)
- Returns: List of execution results

**`get_execution_history(limit: Optional[int] = None) -> List[Dict]`**
- Get execution history
- Args:
  - `limit`: Maximum number of records (optional)
- Returns: List of execution records

**`self_improve() -> Dict`**
- Analyze past executions and generate improvements
- Returns: Dictionary with improvement suggestions

#### Tool Methods

**`_plan_task(task: str, context: Dict) -> Dict`**
- Create execution plan for task

**`_generate_code(task: str, plan: Dict) -> str`**
- Generate Python code for task

**`_execute_python(code: str) -> Dict`**
- Execute Python code safely

**`_analyze_data(execution_result: Dict) -> Dict`**
- Analyze execution results

**`_read_file(file_path: str) -> str`**
- Read file from workspace

**`_write_file(file_path: str, content: str) -> bool`**
- Write file to workspace

---

### OpenManusIntegration

#### Core Methods

**`execute_autonomous_task(task: str, context: Optional[Dict] = None) -> Dict`**
- Execute task with monitoring integration
- Args:
  - `task`: Task description
  - `context`: Additional context (optional)
- Returns: Execution result with monitoring data

**`batch_execute_tasks(tasks: List[str], context: Optional[Dict] = None) -> List[Dict]`**
- Execute multiple tasks with monitoring

**`data_analysis_task(data_description: str, analysis_type: str = "exploratory") -> Dict`**
- Perform data analysis task
- Args:
  - `data_description`: Description of data to analyze
  - `analysis_type`: Type of analysis (exploratory, statistical, visual)
- Returns: Analysis results

**`code_generation_task(requirement: str, language: str = "python", include_tests: bool = True) -> Dict`**
- Generate code based on requirements
- Args:
  - `requirement`: Code requirements
  - `language`: Programming language (default: python)
  - `include_tests`: Include unit tests (default: True)
- Returns: Generated code with tests

**`get_performance_metrics() -> Dict`**
- Get performance metrics from execution history
- Returns: Dictionary with metrics

**`self_improvement_analysis() -> Dict`**
- Analyze agent performance and suggest improvements
- Returns: Improvement suggestions

**`cleanup()`**
- Cleanup resources (Comet ML experiments, etc.)

---

## 💡 Usage Examples

### Example 1: Simple Calculation

```python
import asyncio
from core.openmanus_agent import get_openmanus_agent

async def main():
    agent = get_openmanus_agent()
    
    result = await agent.execute_task(
        "Calculate the sum of all prime numbers between 1 and 100"
    )
    
    if result.get("success"):
        print("Code:", result.get("code"))
        print("Output:", result.get("execution", {}).get("output"))
        print("Analysis:", result.get("analysis"))

asyncio.run(main())
```

### Example 2: Data Analysis

```python
from core.integrations.openmanus_integration import get_openmanus_integration

async def analyze_sales():
    integration = get_openmanus_integration()
    
    data = """
    Q1 Sales Data:
    Product A: $50,000
    Product B: $75,000
    Product C: $60,000
    """
    
    result = await integration.data_analysis_task(
        data_description=data,
        analysis_type="statistical"
    )
    
    return result
```

### Example 3: Batch Processing

```python
async def batch_tasks():
    integration = get_openmanus_integration()
    
    tasks = [
        "Calculate factorial of 5",
        "Generate Fibonacci sequence (10 terms)",
        "Find prime numbers up to 50",
        "Sort list [3, 1, 4, 1, 5, 9, 2, 6]"
    ]
    
    results = await integration.batch_execute_tasks(tasks)
    
    # Analyze results
    successful = sum(1 for r in results if r.get("success"))
    print(f"Success rate: {successful}/{len(tasks)}")
```

### Example 4: Code Generation with Tests

```python
async def generate_code():
    integration = get_openmanus_integration()
    
    requirement = """
    Create a class 'EmailValidator' with:
    - Method to validate email format
    - Method to extract domain from email
    - Proper error handling
    """
    
    result = await integration.code_generation_task(
        requirement=requirement,
        language="python",
        include_tests=True
    )
    
    if result.get("success"):
        print("Generated Code:")
        print(result.get("code"))
```

### Example 5: Self-Improvement

```python
async def improve_agent():
    agent = get_openmanus_agent()
    
    # Execute several tasks
    for task in ["Task 1", "Task 2", "Task 3"]:
        await agent.execute_task(task)
    
    # Get improvement suggestions
    improvement = await agent.self_improve()
    print("Suggestions:", improvement.get("suggestions"))
```

---

## 🔧 Configuration

### Environment Variables

Add to your `.env` file:

```bash
# OpenManus Configuration
OPENMANUS_WORKSPACE=./workspace/openmanus
OPENMANUS_MAX_RETRIES=3
OPENMANUS_TIMEOUT=300

# Enable/Disable Features
ENABLE_OPENMANUS=true
ENABLE_CODE_EXECUTION=true
ENABLE_SELF_IMPROVEMENT=true
```

### Settings in `config/settings.py`

```python
class Settings:
    # OpenManus specific settings
    OPENMANUS_WORKSPACE = os.getenv("OPENMANUS_WORKSPACE", "./workspace/openmanus")
    OPENMANUS_MAX_RETRIES = int(os.getenv("OPENMANUS_MAX_RETRIES", "3"))
    OPENMANUS_TIMEOUT = int(os.getenv("OPENMANUS_TIMEOUT", "300"))
    
    # Feature flags
    ENABLE_OPENMANUS = os.getenv("ENABLE_OPENMANUS", "true").lower() == "true"
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all OpenManus tests
pytest tests/test_openmanus.py -v

# Run specific test
pytest tests/test_openmanus.py::TestOpenManusAgent::test_execute_task_complete -v

# Run with coverage
pytest tests/test_openmanus.py --cov=core.openmanus_agent --cov-report=html
```

### Test Coverage

- ✅ Agent initialization
- ✅ Task planning
- ✅ Code generation
- ✅ Code execution (success & error cases)
- ✅ Data analysis
- ✅ Batch execution
- ✅ File operations
- ✅ Execution history
- ✅ Self-improvement
- ✅ Integration tests
- ✅ Executive Agent integration

---

## 📊 Monitoring & Metrics

### Comet ML Integration

OpenManus automatically logs to Comet ML:

- Task execution metrics
- Success/failure rates
- Generated code
- Execution outputs
- Error tracking
- Performance metrics

### Opik Integration

Tracks LLM interactions:

- Prompt quality
- Response quality
- Token usage
- Cost tracking
- Model performance

### Performance Metrics

```python
integration = get_openmanus_integration()
metrics = integration.get_performance_metrics()

# Returns:
{
    "total_executions": 100,
    "successful": 95,
    "failed": 5,
    "success_rate": 0.95,
    "recent_tasks": [...]
}
```

---

## 🔒 Security Considerations

### Safe Code Execution

- Limited execution environment
- No access to system functions
- Sandboxed workspace
- Timeout protection
- Error containment

### Best Practices

1. **Always validate inputs** before execution
2. **Set timeouts** for long-running tasks
3. **Monitor resource usage** (CPU, memory)
4. **Review generated code** before production use
5. **Use workspace isolation** for file operations

---

## 🚨 Error Handling

### Common Errors

**1. Code Execution Errors**
```python
result = await agent.execute_task(task)
if not result.get("success"):
    error = result.get("error")
    print(f"Execution failed: {error}")
```

**2. Timeout Errors**
```python
try:
    result = await asyncio.wait_for(
        agent.execute_task(task),
        timeout=60  # 60 seconds
    )
except asyncio.TimeoutError:
    print("Task timed out")
```

**3. File Operation Errors**
```python
try:
    content = await agent._read_file("data.txt")
except Exception as e:
    print(f"File read failed: {e}")
```

---

## 🎯 Best Practices

### 1. Task Design

- ✅ Be specific and clear
- ✅ Provide context when needed
- ✅ Break complex tasks into steps
- ✅ Set realistic expectations

### 2. Performance Optimization

- ✅ Use batch execution for multiple tasks
- ✅ Cache frequently used results
- ✅ Monitor execution metrics
- ✅ Optimize code generation prompts

### 3. Monitoring

- ✅ Enable Comet ML tracking
- ✅ Review execution history regularly
- ✅ Analyze failure patterns
- ✅ Use self-improvement suggestions

### 4. Production Use

- ✅ Test thoroughly before deployment
- ✅ Implement proper error handling
- ✅ Set resource limits
- ✅ Monitor system health
- ✅ Have rollback plans

---

## 🤝 Integration with Other Agents

### Browser Agent
```python
# Use OpenManus for data processing after web scraping
browser_result = await agent.execute_browser_task("Scrape data")
analysis = await agent.execute_autonomous_task(
    f"Analyze this data: {browser_result}"
)
```

### Data Agent
```python
# Combine with data processing
data = load_data()
result = await agent.data_analysis(
    f"Analyze dataset: {data}",
    analysis_type="exploratory"
)
```

### Analysis Agent
```python
# Use for complex analysis
result = await agent.execute_autonomous_task(
    "Perform regression analysis on sales data"
)
```

---

## 📈 Roadmap

### v1.1.0 (Current)
- ✅ Basic autonomous execution
- ✅ Code generation
- ✅ Data analysis
- ✅ Batch processing
- ✅ Self-improvement

### v1.2.0 (Planned)
- 🔲 Multi-language support (JavaScript, Java, etc.)
- 🔲 Enhanced visualization capabilities
- 🔲 Improved error recovery
- 🔲 Advanced caching system

### v2.0.0 (Future)
- 🔲 Distributed execution
- 🔲 Real-time collaboration
- 🔲 Custom tool development
- 🔲 Advanced machine learning integration

---

## 🐛 Troubleshooting

### Issue: Task fails with timeout

**Solution**: Increase timeout or break task into smaller steps

```python
# Increase timeout
result = await asyncio.wait_for(
    agent.execute_task(task),
    timeout=300  # 5 minutes
)
```

### Issue: Code execution fails

**Solution**: Check execution logs and validate code

```python
result = await agent.execute_task(task)
if not result.get("success"):
    print("Errors:", result.get("execution", {}).get("errors"))
```

### Issue: Low success rate

**Solution**: Use self-improvement analysis

```python
improvement = await agent.self_improve()
print(improvement.get("suggestions"))
```

---

## 📞 Support

- **Documentation**: See this file and examples
- **Issues**: Report on GitHub
- **Examples**: Check `examples/openmanus_examples.py`
- **Tests**: See `tests/test_openmanus.py`

---

## 📄 License

Part of AI Executive Agent project - See main repository license

---

**Last Updated**: December 31, 2025  
**Version**: 1.1.0  
**Status**: Production Ready ✅

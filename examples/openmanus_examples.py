"""OpenManus Agent - Example Usage
Demonstrates various capabilities of OpenManus autonomous AI agent
"""
import asyncio
import json
from datetime import datetime

from core.agent import get_agent
from core.openmanus_agent import get_openmanus_agent
from core.integrations.openmanus_integration import get_openmanus_integration


async def example_1_simple_task():
    """Example 1: Simple autonomous task execution"""
    print("=" * 60)
    print("Example 1: Simple Autonomous Task")
    print("=" * 60)
    
    agent = get_openmanus_agent()
    
    task = "Create a Python function to calculate the area of a circle"
    print(f"\n📋 Task: {task}\n")
    
    result = await agent.execute_task(task)
    
    if result.get("success"):
        print("✅ Task completed successfully!")
        print(f"\n💻 Generated Code:\n{'-'*40}")
        print(result.get("code", ""))
        print(f"{'-'*40}\n")
        
        print(f"📊 Execution Output:\n{'-'*40}")
        print(result.get("execution", {}).get("output", "No output"))
        print(f"{'-'*40}\n")
    else:
        print(f"❌ Task failed: {result.get('error')}")
    
    return result


async def example_2_data_analysis():
    """Example 2: Data analysis task"""
    print("\n" + "=" * 60)
    print("Example 2: Data Analysis")
    print("=" * 60)
    
    integration = get_openmanus_integration(enable_monitoring=False)
    
    data_description = """
    Sales data for Q1 2025:
    January: $45,000
    February: $52,000
    March: $48,000
    """
    
    print(f"\n📊 Data: {data_description}\n")
    
    result = await integration.data_analysis_task(
        data_description,
        analysis_type="statistical"
    )
    
    if result.get("success"):
        print("✅ Analysis completed!")
        print(f"\n📈 Analysis:\n{'-'*40}")
        analysis = result.get("analysis", {})
        print(json.dumps(analysis, indent=2))
        print(f"{'-'*40}\n")
    else:
        print(f"❌ Analysis failed: {result.get('error')}")
    
    return result


async def example_3_code_generation():
    """Example 3: Advanced code generation"""
    print("\n" + "=" * 60)
    print("Example 3: Code Generation with Tests")
    print("=" * 60)
    
    integration = get_openmanus_integration(enable_monitoring=False)
    
    requirement = """
    Create a class called 'BankAccount' with:
    - Properties: account_number, balance, owner
    - Methods: deposit, withdraw, get_balance
    - Validation: balance cannot go negative
    """
    
    print(f"\n📝 Requirement:\n{requirement}\n")
    
    result = await integration.code_generation_task(
        requirement,
        language="python",
        include_tests=True
    )
    
    if result.get("success"):
        print("✅ Code generated successfully!")
        print(f"\n💻 Generated Code:\n{'-'*40}")
        print(result.get("code", ""))
        print(f"{'-'*40}\n")
    else:
        print(f"❌ Generation failed: {result.get('error')}")
    
    return result


async def example_4_batch_tasks():
    """Example 4: Batch task execution"""
    print("\n" + "=" * 60)
    print("Example 4: Batch Task Execution")
    print("=" * 60)
    
    integration = get_openmanus_integration(enable_monitoring=False)
    
    tasks = [
        "Calculate factorial of 5",
        "Generate Fibonacci sequence up to 10 terms",
        "Find all prime numbers between 1 and 20",
        "Calculate the sum of squares from 1 to 10"
    ]
    
    print(f"\n📋 Executing {len(tasks)} tasks in batch...\n")
    
    results = await integration.batch_execute_tasks(tasks)
    
    print(f"✅ Batch execution completed!")
    print(f"\n📊 Results Summary:")
    print(f"{'-'*40}")
    
    for i, result in enumerate(results):
        status = "✅" if result.get("success") else "❌"
        print(f"{status} Task {i+1}: {tasks[i]}")
    
    successful = len([r for r in results if r.get("success")])
    print(f"\n🎯 Success Rate: {successful}/{len(tasks)} ({successful/len(tasks)*100:.1f}%)")
    print(f"{'-'*40}\n")
    
    return results


async def example_5_executive_agent_integration():
    """Example 5: Using OpenManus through ExecutiveAgent"""
    print("\n" + "=" * 60)
    print("Example 5: Executive Agent Integration")
    print("=" * 60)
    
    agent = get_agent()
    
    print("\n🤖 Using Executive Agent with OpenManus...")
    
    # Autonomous task
    print("\n1️⃣ Autonomous Task:")
    result1 = await agent.execute_autonomous_task(
        "Create a function to check if a string is a palindrome"
    )
    print(f"   Status: {'✅ Success' if result1.get('success') else '❌ Failed'}")
    
    # Code generation
    print("\n2️⃣ Code Generation:")
    result2 = await agent.code_generation(
        "Function to sort a list of dictionaries by a specific key"
    )
    print(f"   Status: {'✅ Success' if result2.get('success') else '❌ Failed'}")
    
    # Data analysis
    print("\n3️⃣ Data Analysis:")
    result3 = await agent.data_analysis(
        "Student scores: [85, 90, 78, 92, 88, 95, 82, 89]",
        analysis_type="exploratory"
    )
    print(f"   Status: {'✅ Success' if result3.get('success') else '❌ Failed'}")
    
    print(f"\n{'-'*40}\n")
    
    return [result1, result2, result3]


async def example_6_performance_metrics():
    """Example 6: Performance metrics and self-improvement"""
    print("\n" + "=" * 60)
    print("Example 6: Performance & Self-Improvement")
    print("=" * 60)
    
    integration = get_openmanus_integration(enable_monitoring=False)
    
    # Get performance metrics
    print("\n📊 Performance Metrics:")
    print(f"{'-'*40}")
    metrics = integration.get_performance_metrics()
    print(json.dumps(metrics, indent=2))
    print(f"{'-'*40}\n")
    
    # Self-improvement analysis
    if metrics.get("total_executions", 0) > 0:
        print("\n🔧 Self-Improvement Analysis:")
        print(f"{'-'*40}")
        improvement = await integration.self_improvement_analysis()
        print(json.dumps(improvement, indent=2))
        print(f"{'-'*40}\n")
    else:
        print("\n⚠️  No execution history for self-improvement analysis\n")


async def example_7_workflow():
    """Example 7: Complex multi-step workflow"""
    print("\n" + "=" * 60)
    print("Example 7: Complex Workflow")
    print("=" * 60)
    
    agent = get_agent()
    
    workflow = [
        {
            "type": "autonomous",
            "name": "Generate Test Data",
            "task": "Create a list of 100 random numbers between 1 and 1000"
        },
        {
            "type": "autonomous",
            "name": "Analyze Data",
            "task": "Calculate mean, median, mode, and standard deviation of the data"
        },
        {
            "type": "autonomous",
            "name": "Visualize Results",
            "task": "Create a summary report of the statistical analysis"
        }
    ]
    
    print(f"\n🔄 Executing workflow with {len(workflow)} steps...\n")
    
    results = []
    for i, step in enumerate(workflow):
        print(f"Step {i+1}/{len(workflow)}: {step['name']}")
        
        result = await agent.execute_autonomous_task(
            step['task']
        )
        
        status = "✅" if result.get("success") else "❌"
        print(f"  {status} Status: {step['name']}")
        results.append(result)
    
    successful = len([r for r in results if r.get("success")])
    print(f"\n🎯 Workflow completed: {successful}/{len(workflow)} steps successful\n")
    
    return results


async def main():
    """Run all examples"""
    print("\n" + "🤖" * 30)
    print("OpenManus AI Agent - Comprehensive Examples")
    print("🤖" * 30)
    print(f"\nStarted at: {datetime.now().isoformat()}\n")
    
    try:
        # Run examples
        await example_1_simple_task()
        await example_2_data_analysis()
        await example_3_code_generation()
        await example_4_batch_tasks()
        await example_5_executive_agent_integration()
        await example_6_performance_metrics()
        await example_7_workflow()
        
        print("\n" + "=" * 60)
        print("✅ All Examples Completed Successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        agent = get_agent()
        agent.cleanup()
        
        print(f"\n🏁 Finished at: {datetime.now().isoformat()}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())

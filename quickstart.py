#!/usr/bin/env python3
"""Quick Start Script for AI Executive Agent with OpenManus
Run this script to quickly test the OpenManus agent integration
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import get_agent


async def demo_openmanus():
    """Demo OpenManus capabilities"""
    print("\n" + "="*60)
    print("🤖 AI Executive Agent - OpenManus Quick Demo")
    print("="*60 + "\n")
    
    agent = get_agent()
    
    # Test 1: Simple task
    print("Test 1: Simple Calculation")
    print("-" * 40)
    result1 = await agent.execute_autonomous_task(
        "Calculate the factorial of 7"
    )
    print(f"Status: {'✅ Success' if result1.get('success') else '❌ Failed'}")
    if result1.get("success"):
        print(f"Code: {result1.get('code', '')[:100]}...")
    print()
    
    # Test 2: Code generation
    print("Test 2: Code Generation")
    print("-" * 40)
    result2 = await agent.code_generation(
        "Function to check if a number is prime"
    )
    print(f"Status: {'✅ Success' if result2.get('success') else '❌ Failed'}")
    print()
    
    # Test 3: Data analysis
    print("Test 3: Data Analysis")
    print("-" * 40)
    result3 = await agent.data_analysis(
        "Numbers: [10, 20, 30, 40, 50]",
        analysis_type="statistical"
    )
    print(f"Status: {'✅ Success' if result3.get('success') else '❌ Failed'}")
    print()
    
    # Summary
    print("="*60)
    successful = sum([
        1 if result1.get('success') else 0,
        1 if result2.get('success') else 0,
        1 if result3.get('success') else 0
    ])
    print(f"✅ Demo Complete: {successful}/3 tests passed")
    print("="*60 + "\n")
    
    # Cleanup
    agent.cleanup()


def main():
    """Main entry point"""
    print("\n🚀 Starting Quick Demo...\n")
    
    try:
        asyncio.run(demo_openmanus())
        print("✅ Demo completed successfully!\n")
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user\n")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
    

if __name__ == "__main__":
    main()

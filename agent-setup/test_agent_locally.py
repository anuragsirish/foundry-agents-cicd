#!/usr/bin/env python3
"""
Test Customer Service Agent Locally

Interactive script to test the customer service agent before running CI/CD.

Usage:
    # Interactive mode
    python agent-setup/test_agent_locally.py
    
    # Automated test mode
    python agent-setup/test_agent_locally.py --auto
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Load environment variables from project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
AGENT_ID = os.getenv("AGENT_ID_BASELINE")


def test_agent_interactive():
    """Run interactive test session with the agent."""
    
    print("\n" + "="*70)
    print("🧪 Customer Service Agent - Interactive Test")
    print("="*70 + "\n")
    
    # Validate configuration
    if not PROJECT_ENDPOINT or not AGENT_ID:
        print("❌ Error: Missing configuration")
        print("   Ensure AZURE_AI_PROJECT_ENDPOINT and AGENT_ID_BASELINE are set in .env")
        print(f"\n   Current values:")
        print(f"   PROJECT_ENDPOINT: {'✅ Set' if PROJECT_ENDPOINT else '❌ Not set'}")
        print(f"   AGENT_ID: {'✅ Set' if AGENT_ID else '❌ Not set'}")
        return
    
    # Connect to project
    print("🔗 Connecting to Azure AI Project...")
    print(f"   Endpoint: {PROJECT_ENDPOINT}")
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=credential
    )
    print(f"✅ Connected\n")
    print(f"📋 Agent ID: {AGENT_ID}\n")
    
    # Create a conversation thread
    thread = project_client.agents.threads.create()
    print(f"💬 Conversation started (Thread ID: {thread.id})")
    print("   Type 'quit' or 'exit' to end the conversation\n")
    print("-" * 70)
    
    # Interactive loop
    while True:
        # Get user input
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Ending conversation. Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            # Send message
            message = project_client.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_input
            )
            
            # Run agent
            print("\n🤖 Agent: ", end="", flush=True)
            run = project_client.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=AGENT_ID
            )
            
            # Get response
            messages = project_client.agents.messages.list(thread_id=thread.id)
            
            # Display assistant's response
            for msg in messages:
                if msg.role == "assistant":
                    response_text = ""
                    for content in msg.content:
                        if hasattr(content, 'text') and hasattr(content.text, 'value'):
                            response_text += content.text.value
                    
                    if response_text:
                        print(response_text)
                        break
            
            print("\n" + "-" * 70)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("-" * 70)
    
    print("\n" + "="*70)
    print("✅ Test session complete!")
    print("="*70 + "\n")


def run_predefined_tests():
    """Run predefined test queries from the eval data."""
    
    print("\n" + "="*70)
    print("🧪 Running Predefined Test Queries")
    print("="*70 + "\n")
    
    # Validate configuration
    if not PROJECT_ENDPOINT or not AGENT_ID:
        print("❌ Error: Missing configuration")
        print(f"   PROJECT_ENDPOINT: {'✅ Set' if PROJECT_ENDPOINT else '❌ Not set'}")
        print(f"   AGENT_ID: {'✅ Set' if AGENT_ID else '❌ Not set'}")
        return
    
    # Test queries from agent-eval-data.json
    test_queries = [
        "What are your business hours?",
        "How can I reset my password?",
        "Tell me about your return policy.",
        "What payment methods do you accept?",
        "How do I track my order?",
        "Can you help me find a product?",
        "What is the warranty on your products?",
        "How do I contact customer support?",
        "Do you offer international shipping?",
        "How can I apply a discount code?",
    ]
    
    # Connect to project
    print("🔗 Connecting to Azure AI Project...")
    print(f"   Endpoint: {PROJECT_ENDPOINT}")
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=credential
    )
    print(f"✅ Connected")
    print(f"📋 Agent ID: {AGENT_ID}\n")
    
    # Create thread
    thread = project_client.agents.threads.create()
    print(f"💬 Test Thread: {thread.id}\n")
    
    # Track results
    passed = 0
    failed = 0
    
    # Run each test
    for i, query in enumerate(test_queries, 1):
        print(f"📝 Test {i}/{len(test_queries)}")
        print(f"   Query: {query}")
        print("-" * 70)
        
        try:
            # Send message
            message = project_client.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=query
            )
            
            # Run agent
            run = project_client.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=AGENT_ID
            )
            
            # Get response
            messages = project_client.agents.messages.list(thread_id=thread.id)
            
            # Display response
            response_found = False
            for msg in messages:
                if msg.role == "assistant":
                    response_text = ""
                    for content in msg.content:
                        if hasattr(content, 'text') and hasattr(content.text, 'value'):
                            response_text += content.text.value
                    
                    if response_text:
                        # Show truncated response
                        if len(response_text) > 150:
                            print(f"   Response: {response_text[:150]}...")
                        else:
                            print(f"   Response: {response_text}")
                        print("   ✅ Success")
                        passed += 1
                        response_found = True
                        break
            
            if not response_found:
                print("   ⚠️  No response generated")
                failed += 1
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            failed += 1
        
        print()
    
    # Summary
    print("="*70)
    print("📊 Test Results Summary")
    print("="*70)
    print(f"   Total Tests: {len(test_queries)}")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   Success Rate: {(passed/len(test_queries)*100):.1f}%")
    print("="*70 + "\n")
    
    if passed == len(test_queries):
        print("🎉 All tests passed! Agent is ready for evaluation.")
    elif passed > 0:
        print("⚠️  Some tests failed. Review errors above.")
    else:
        print("❌ All tests failed. Check agent configuration.")
    
    print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        run_predefined_tests()
    else:
        test_agent_interactive()

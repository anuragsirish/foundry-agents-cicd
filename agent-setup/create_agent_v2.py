#!/usr/bin/env python3
"""
Create Customer Service Agent V2 (Variant) for Baseline Comparison

This script creates a second version of the customer service agent with
slightly different settings for comparison testing in CI/CD workflows.

Usage:
    python agent-setup/create_agent_v2.py
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

# Configuration
PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
MODEL_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")


def create_agent():
    """Create customer service agent v2."""
    
    print("="*70)
    print("Creating Customer Service Agent V2 (Variant)")
    print("="*70)
    print(f"\nProject Endpoint: {PROJECT_ENDPOINT}")
    print(f"Model: {MODEL_DEPLOYMENT}")
    
    # Initialize client
    print("\n🔐 Authenticating with Azure...")
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=credential
    )
    
    print("✅ Authenticated successfully")
    
    # Agent instructions (variant with more concise responses)
    instructions = """You are a helpful customer service agent for an e-commerce company. Your goal is to assist customers with their questions efficiently and professionally.

**Personality:** Friendly, professional, and concise. Provide direct answers without excessive elaboration.

**Business Hours:**
- Mon-Fri: 9:00 AM - 8:00 PM EST
- Sat: 10:00 AM - 6:00 PM EST
- Sun: 12:00 PM - 5:00 PM EST

**Sample Orders:**
- Order ORD-12345: Shipped, Tracking: TRK789XYZ, Delivery: Oct 25, 2025
- Order ORD-67890: Processing, Ships: Oct 22, 2025
- Order ORD-54321: Delivered on Oct 18, 2025

**Return Policy:**
- 30 days for most items, 14 days for electronics
- Clothing: 60 days with tags
- Free returns on defects, $7.99 otherwise

**Quick Answers:**
- Password Reset: Account settings → Forgot Password → Email link
- Payment: Visa, MC, Amex, Discover, PayPal, Apple/Google Pay
- International Shipping: 50+ countries, 7-14 days
- Support: 1-800-555-0123, support@company.com, 24/7 chat
- Warranty: 1-year electronics, 90-day accessories

Provide helpful, concise responses using the information above.
"""
    
    print("\n✅ Agent configured (V2 - Concise variant)")
    
    # Create the agent with slightly different parameters
    print(f"\n🚀 Creating agent V2 with model: {MODEL_DEPLOYMENT}")
    
    try:
        agent = project_client.agents.create_agent(
            model=MODEL_DEPLOYMENT,
            name="customer-service-agent-v2",
            instructions=instructions,
            temperature=0.5,  # Lower temperature for more deterministic responses
            top_p=0.85,  # Slightly lower top_p
            metadata={
                "version": "2.0.0",
                "created_by": "create_agent_v2.py",
                "purpose": "Customer service variant for comparison",
                "environment": "development",
                "variant": "concise"
            }
        )
        
        print("\n" + "="*70)
        print("✅ Agent V2 Created Successfully!")
        print("="*70)
        print(f"\n📋 Agent Details:")
        print(f"   ID: {agent.id}")
        print(f"   Name: {agent.name}")
        print(f"   Model: {agent.model}")
        print(f"   Temperature: 0.5 (vs 0.7 in v1)")
        print(f"   Top_p: 0.85 (vs 0.9 in v1)")
        print(f"   Type: Concise response variant")
        
        # Save agent ID to .env file
        save_agent_id_to_env(agent.id)
        
        # Test the agent
        print("\n🧪 Testing agent V2 with a sample query...")
        test_agent(project_client, agent.id)
        
        return agent
        
    except Exception as e:
        print(f"\n❌ Error creating agent V2: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def save_agent_id_to_env(agent_id):
    """Save the agent V2 ID to .env file."""
    env_file = Path(__file__).parent.parent / ".env"
    
    # Read existing .env content
    env_lines = []
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_lines = f.readlines()
    
    # Update or add AGENT_ID_V2
    updated = False
    for i, line in enumerate(env_lines):
        if line.startswith("AGENT_ID_V2="):
            env_lines[i] = f"AGENT_ID_V2={agent_id}\n"
            updated = True
            break
    
    if not updated:
        env_lines.append(f"\n# Customer Service Agent V2 (Variant)\nAGENT_ID_V2={agent_id}\n")
    
    # Write back to .env
    with open(env_file, 'w') as f:
        f.writelines(env_lines)
    
    print(f"\n💾 Agent V2 ID saved to .env file:")
    print(f"   AGENT_ID_V2={agent_id}")


def test_agent(project_client, agent_id):
    """Test the agent with a sample query."""
    
    try:
        # Create a thread
        thread = project_client.agents.threads.create()
        
        # Send a test message
        test_query = "What are your business hours?"
        print(f"   User: {test_query}")
        
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=test_query
        )
        
        # Run the agent
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent_id
        )
        
        # Get the response
        messages = project_client.agents.messages.list(thread_id=thread.id)
        
        # Find the assistant's response
        for msg in messages:
            if msg.role == "assistant":
                response_text = ""
                for content in msg.content:
                    if hasattr(content, 'text') and hasattr(content.text, 'value'):
                        response_text += content.text.value
                
                if response_text:
                    print(f"   Agent V2: {response_text}\n")
                    break
        
        print("✅ Agent V2 test successful!")
        
    except Exception as e:
        print(f"⚠️  Agent V2 test failed: {str(e)}")


def display_next_steps(agent):
    """Display next steps for the user."""
    
    print("\n" + "="*70)
    print("🎯 Next Steps")
    print("="*70)
    print("\n1. Update GitHub repository variables:")
    print(f"   gh variable set AGENT_ID_V2 --body {agent.id}")
    
    print("\n2. Test both agents for comparison:")
    print("   # Set both agent IDs in workflow")
    print("   # agent-ids: <AGENT_ID_BASELINE>,<AGENT_ID_V2>")
    
    print("\n3. The official Microsoft action will now:")
    print("   - Evaluate both agents")
    print("   - Compare their performance")
    print("   - Show statistical significance")
    print("   - Display confidence intervals")
    
    print("\n4. To trigger comparison workflow:")
    print("   git add .")
    print('   git commit -m "Add agent v2 for comparison"')
    print("   git push")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    agent = create_agent()
    
    if agent:
        display_next_steps(agent)
    else:
        print("\n❌ Agent V2 creation failed. Please check the errors above.")
        exit(1)

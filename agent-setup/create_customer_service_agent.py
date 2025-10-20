#!/usr/bin/env python3
"""
Create Customer Service Agent using Azure AI Agent Service

This script creates a customer service agent in Azure AI Foundry using the
new Azure AI Agent Service SDK (released October 2025).

Usage:
    python agent-setup/create_customer_service_agent.py

Requirements:
    - .env file with AZURE_AI_PROJECT_CONNECTION_STRING
    - Azure AI Foundry project
    - Model deployment (e.g., gpt-4o)
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


def create_customer_service_tools():
    """
    Define tools for the customer service agent.
    
    These are declarative tool definitions only - the agent will use its training
    to provide appropriate responses based on the tool descriptions and sample data
    embedded in the instructions.
    """
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_order_status",
                "description": """Get the current status and tracking information for a customer order.
                
Sample data for demo (use realistic values):
- Order ORD-12345: Status: Shipped, Tracking: TRK789XYZ, Delivery: Oct 25, 2025
- Order ORD-67890: Status: Processing, Expected Ship: Oct 22, 2025
- Order ORD-54321: Status: Delivered, Delivered on: Oct 18, 2025

Return format: Order status, tracking number, and expected/actual delivery date.""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The unique order identifier (e.g., ORD-12345)"
                        }
                    },
                    "required": ["order_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_business_hours",
                "description": """Get the current business hours for customer support.

Sample data for demo:
- Monday-Friday: 9:00 AM - 8:00 PM EST
- Saturday: 10:00 AM - 6:00 PM EST
- Sunday: 12:00 PM - 5:00 PM EST
- Holidays: Closed

Return the business hours for the requested day or current day if not specified.""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "day_of_week": {
                            "type": "string",
                            "description": "Optional: Day of the week to check (Monday, Tuesday, etc.)"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_return_policy",
                "description": """Get information about the return and refund policy.

Sample policy data for demo:
- Standard Return Window: 30 days from delivery
- Electronics: 14 days, must be unopened
- Clothing: 60 days with tags attached
- Final Sale Items: Non-returnable
- Refund Method: Original payment method within 5-7 business days
- Return Shipping: Free for defective items, $7.99 for other returns

Return relevant policy based on product category if provided.""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_category": {
                            "type": "string",
                            "description": "Optional: Category of product (electronics, clothing, etc.)"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_knowledge_base",
                "description": """Search the knowledge base for common customer questions.

Sample KB articles for demo:
- "How to reset password": Visit account settings, click 'Forgot Password', enter email, follow reset link
- "Track my order": Use order number in tracking page or check confirmation email
- "Payment methods accepted": Visa, Mastercard, Amex, Discover, PayPal, Apple Pay, Google Pay
- "International shipping": Available to 50+ countries, 7-14 business days, calculated at checkout
- "Apply discount code": Enter code at checkout in 'Promo Code' field before payment
- "Product warranty": 1-year manufacturer warranty on electronics, 90-day on accessories
- "Contact support": Phone: 1-800-555-0123, Email: support@company.com, Live Chat: 24/7

Return the most relevant KB article based on the search query.""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (e.g., 'reset password', 'shipping', 'warranty')"
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    ]
    
    return tools


def create_agent():
    """Create the customer service agent in Azure AI Foundry."""
    
    print("\n" + "="*70)
    print("🤖 Creating Customer Service Agent")
    print("="*70 + "\n")
    
    # Validate environment
    if not PROJECT_ENDPOINT:
        print("❌ Error: AZURE_AI_PROJECT_ENDPOINT not set")
        print("   Please set it in your .env file")
        print("   Example: https://your-project.eastus.services.ai.azure.com/api/projects/your-project")
        return None
    
    # Create project client using endpoint
    print("🔗 Connecting to Azure AI Project...")
    print(f"   Endpoint: {PROJECT_ENDPOINT}")
    
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=credential
    )
    print("✅ Connected to Azure AI Project")
    
    # Define agent instructions with embedded knowledge
    instructions = """You are a helpful and friendly customer service agent for TechMart, an e-commerce company.

Your responsibilities:
- Assist customers with order inquiries and tracking
- Provide information about products, policies, and services
- Help with account-related questions
- Guide customers through processes like returns, shipping, and payments
- Answer questions about business hours and contact options

Guidelines:
- Always be polite, professional, and empathetic
- Listen carefully to customer needs and ask clarifying questions
- Use the knowledge base below to provide accurate information
- Keep responses clear, concise, and conversational
- If you don't have specific information, acknowledge it and offer alternatives

KNOWLEDGE BASE (Use this information to answer customer questions):

**Business Hours:**
- Monday-Friday: 9:00 AM - 8:00 PM EST
- Saturday: 10:00 AM - 6:00 PM EST
- Sunday: 12:00 PM - 5:00 PM EST
- Holidays: Closed

**Sample Orders (for demo purposes):**
- Order ORD-12345: Status: Shipped, Tracking: TRK789XYZ, Expected Delivery: Oct 25, 2025
- Order ORD-67890: Status: Processing, Expected to Ship: Oct 22, 2025
- Order ORD-54321: Status: Delivered, Delivered on: Oct 18, 2025

**Return Policy:**
- Standard Return Window: 30 days from delivery
- Electronics: 14 days, must be unopened
- Clothing: 60 days with tags attached
- Final Sale Items: Non-returnable
- Refund Method: Original payment method within 5-7 business days
- Return Shipping: Free for defective items, $7.99 for other returns

**Common Questions:**
- Password Reset: Visit account settings, click 'Forgot Password', enter email, follow reset link
- Payment Methods: Visa, Mastercard, Amex, Discover, PayPal, Apple Pay, Google Pay
- International Shipping: Available to 50+ countries, 7-14 business days, cost calculated at checkout
- Discount Codes: Enter at checkout in 'Promo Code' field before payment
- Product Warranty: 1-year manufacturer warranty on electronics, 90-day on accessories
- Contact Support: Phone: 1-800-555-0123, Email: support@company.com, Live Chat: 24/7

When customers ask questions, use the knowledge base above to provide helpful, natural responses.
"""
    
    # Get tools - commented out for simple demo
    print("\n✅ Agent configured without function calling (knowledge embedded in instructions)")
    
    # Create the agent
    print(f"\n🚀 Creating agent with model: {MODEL_DEPLOYMENT}")
    
    try:
        agent = project_client.agents.create_agent(
            model=MODEL_DEPLOYMENT,
            name="customer-service-agent",
            instructions=instructions,
            # tools=tools,  # Removed - using embedded knowledge instead
            temperature=0.7,
            top_p=0.9,
            metadata={
                "version": "1.0.0",
                "created_by": "create_customer_service_agent.py",
                "purpose": "Customer service and support",
                "environment": "development"
            }
        )
        
        print("\n" + "="*70)
        print("✅ Agent Created Successfully!")
        print("="*70)
        print(f"\n📋 Agent Details:")
        print(f"   ID: {agent.id}")
        print(f"   Name: {agent.name}")
        print(f"   Model: {agent.model}")
        print(f"   Type: Conversational agent with embedded knowledge")
        
        # Save agent ID to .env file for easy access
        save_agent_id_to_env(agent.id)
        
        # Save agent info to local file
        save_agent_info(agent)
        
        # Test the agent
        print("\n🧪 Testing the agent with a sample query...")
        print("   Note: Agent will use embedded sample data for responses\n")
        test_agent(project_client, agent.id)
        
        return agent
        
    except Exception as e:
        print(f"\n❌ Error creating agent: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def save_agent_id_to_env(agent_id):
    """Save the agent ID to .env file."""
    env_file = Path(__file__).parent.parent / ".env"
    
    # Read existing .env content
    env_lines = []
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_lines = f.readlines()
    
    # Update or add AGENT_ID_BASELINE
    updated = False
    for i, line in enumerate(env_lines):
        if line.startswith("AGENT_ID_BASELINE="):
            env_lines[i] = f"AGENT_ID_BASELINE={agent_id}\n"
            updated = True
            break
    
    if not updated:
        env_lines.append(f"\n# Customer Service Agent\nAGENT_ID_BASELINE={agent_id}\n")
    
    # Write back to .env
    with open(env_file, 'w') as f:
        f.writelines(env_lines)
    
    print(f"\n💾 Agent ID saved to .env file:")
    print(f"   AGENT_ID_BASELINE={agent_id}")


def save_agent_info(agent):
    """Save agent information to a local file."""
    import json
    from datetime import datetime
    
    agent_info = {
        "id": agent.id,
        "name": agent.name,
        "model": agent.model,
        "created_at": datetime.now().isoformat(),
        "endpoint": PROJECT_ENDPOINT,
        "tools_count": len(agent.tools) if agent.tools else 0,
        "metadata": agent.metadata
    }
    
    info_file = Path(__file__).parent / "agent-info.txt"
    with open(info_file, 'w') as f:
        f.write("="*70 + "\n")
        f.write("Customer Service Agent Information\n")
        f.write("="*70 + "\n\n")
        f.write(json.dumps(agent_info, indent=2))
        f.write("\n\n")
        f.write("="*70 + "\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n")
    
    print(f"💾 Agent info saved to: {info_file}")


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
                    print(f"   Agent: {response_text}\n")
                    break
        
        print("✅ Agent test successful!")
        
    except Exception as e:
        print(f"⚠️  Agent test failed: {str(e)}")


def display_next_steps(agent):
    """Display next steps for the user."""
    
    print("\n" + "="*70)
    print("🎯 Next Steps")
    print("="*70)
    print("\n1. Test the agent interactively:")
    print("   python agent-setup/test_agent_locally.py")
    
    print("\n2. Run automated tests:")
    print("   python agent-setup/test_agent_locally.py --auto")
    
    print("\n3. Run full evaluation:")
    print("   python scripts/local_agent_eval.py")
    
    print("\n4. Update GitHub repository variables:")
    print(f"   AGENT_ID_BASELINE={agent.id}")
    
    print("\n5. Commit and push to trigger CI/CD:")
    print("   git add .")
    print('   git commit -m "Add customer service agent"')
    print("   git push origin main")
    
    print("\n6. View agent in Azure AI Foundry:")
    print("   - Go to https://ai.azure.com")
    print("   - Navigate to your project")
    print("   - Find your agent in the Agents section")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    agent = create_agent()
    
    if agent:
        display_next_steps(agent)
    else:
        print("\n❌ Agent creation failed. Please check the errors above.")
        exit(1)

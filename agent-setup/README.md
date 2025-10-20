# Agent Setup Guide

This folder contains scripts for creating and testing the customer service agent.

## 📁 Folder Contents

```
agent-setup/
├── create_customer_service_agent.py   # Creates the agent in Azure AI Foundry
├── test_agent_locally.py               # Interactive and automated testing
├── README.md                           # This file
└── agent-info.txt                      # Auto-generated agent details (created after setup)
```

## 🚀 Quick Start

### Prerequisites

1. **Azure AI Foundry Project**
   - Create or use existing project
   - Deploy a model (e.g., gpt-4o)
   - Get your project connection string

2. **Environment Configuration**
   
   Update the `.env` file in the project root with:
   ```bash
   AZURE_AI_PROJECT_CONNECTION_STRING=<your-connection-string>
   AZURE_DEPLOYMENT_NAME=gpt-4o
   ```

3. **Azure Authentication**
   
   Authenticate with Azure:
   ```bash
   az login
   ```

### Step 1: Create the Agent

Run the agent creation script:

```bash
python agent-setup/create_customer_service_agent.py
```

**What this does:**
- ✅ Connects to your Azure AI Foundry project
- ✅ Creates a customer service agent with 9 function tools
- ✅ Tests the agent with a sample query
- ✅ Saves the agent ID to `.env` file
- ✅ Creates `agent-info.txt` with agent details

**Expected Output:**
```
🤖 Creating Customer Service Agent
======================================================================

🔗 Connecting to Azure AI Project...
✅ Connected to Azure AI Project

🔧 Configuring agent tools...
✅ Configured 9 function tools

🚀 Creating agent with model: gpt-4o

======================================================================
✅ Agent Created Successfully!
======================================================================

📋 Agent Details:
   ID: asst_abc123...
   Name: customer-service-agent
   Model: gpt-4o
   Tools: 9 functions

💾 Agent ID saved to .env file:
   AGENT_ID_BASELINE=asst_abc123...
```

### Step 2: Test the Agent Interactively

Chat with your agent:

```bash
python agent-setup/test_agent_locally.py
```

**Example conversation:**
```
👤 You: What are your business hours?
🤖 Agent: I'd be happy to help you with our business hours...

👤 You: How do I track my order?
🤖 Agent: To track your order, I'll need your order ID...

👤 You: quit
```

### Step 3: Run Automated Tests

Test all queries from the evaluation dataset:

```bash
python agent-setup/test_agent_locally.py --auto
```

**What this does:**
- ✅ Runs all 10 test queries from `data/agent-eval-data.json`
- ✅ Shows responses for each query
- ✅ Displays success/failure summary
- ✅ Calculates success rate

**Expected Output:**
```
📝 Test 1/10
   Query: What are your business hours?
   Response: I'd be happy to help you with our business hours...
   ✅ Success

📝 Test 2/10
   Query: How can I reset my password?
   Response: To reset your password...
   ✅ Success

...

📊 Test Results Summary
======================================================================
   Total Tests: 10
   ✅ Passed: 10
   ❌ Failed: 0
   Success Rate: 100.0%
```

## 🔧 Agent Configuration

### Function Tools (9 total)

The agent is configured with these tools:

1. **`get_order_status`** - Retrieve order status and tracking
2. **`check_business_hours`** - Get business hours by day
3. **`get_return_policy`** - Return policy information
4. **`get_payment_methods`** - List accepted payment methods
5. **`search_products`** - Search product catalog
6. **`get_warranty_info`** - Get warranty information
7. **`get_contact_options`** - Contact support options
8. **`check_shipping_options`** - International shipping info
9. **`apply_discount_code`** - Validate and apply discounts

### Agent Behavior

The agent is instructed to:
- Be polite, professional, and empathetic
- Use tools to provide accurate information
- Ask clarifying questions when needed
- Admit when it doesn't know something
- Keep responses clear and concise

### Model Configuration

- **Model**: gpt-4o (configurable via `.env`)
- **Temperature**: 0.7 (balanced creativity/consistency)
- **Top P**: 0.9 (nucleus sampling)

## 📊 Next Steps After Agent Creation

### 1. Run Full Evaluation

Once the agent is tested locally, run the full evaluation:

```bash
python scripts/local_agent_eval.py
```

This evaluates the agent on:
- Quality metrics (Coherence, Fluency, Relevance, Groundedness)
- Safety metrics (Violence, Sexual, SelfHarm, HateUnfairness)

### 2. Set Up CI/CD

Update GitHub repository variables (Settings > Secrets and variables > Actions):

```
AGENT_ID_BASELINE=<your-agent-id>  # Auto-saved by creation script
```

### 3. Trigger CI/CD Pipeline

Commit and push to trigger automated evaluation:

```bash
git add .
git commit -m "Add customer service agent"
git push origin main
```

The GitHub Action will automatically:
1. Authenticate with Azure
2. Run agent evaluation
3. Post results to Actions summary

## 🐛 Troubleshooting

### "AZURE_AI_PROJECT_CONNECTION_STRING not set"

**Solution**: Update `.env` file in project root:
```bash
AZURE_AI_PROJECT_CONNECTION_STRING=<your-connection-string>
```

### "Authentication failed"

**Solution**: Authenticate with Azure CLI:
```bash
az login
```

### "Agent not found" (during testing)

**Solution**: 
1. Verify `.env` has `AGENT_ID_BASELINE` set
2. Re-run agent creation script
3. Check agent exists in Azure AI Foundry portal

### "Model deployment not found"

**Solution**: 
1. Verify model is deployed in Azure AI Foundry
2. Check `AZURE_DEPLOYMENT_NAME` in `.env`
3. Ensure deployment name matches exactly

### Agent responses seem generic

**Solution**: 
- Tools are declarative only (no real implementation)
- Agent responds based on its training + instructions
- For production, implement actual tool backends

## 📚 File Reference

### `create_customer_service_agent.py`

Creates the agent in Azure AI Foundry.

**Functions:**
- `create_customer_service_tools()` - Defines function tools
- `create_agent()` - Creates agent with configuration
- `save_agent_id_to_env()` - Saves agent ID to `.env`
- `save_agent_info()` - Creates `agent-info.txt`
- `test_agent()` - Quick test with sample query

### `test_agent_locally.py`

Tests the agent before full evaluation.

**Modes:**
- **Interactive**: Chat with agent in real-time
- **Automated**: Run all test queries from eval data

**Functions:**
- `test_agent_interactive()` - Interactive chat mode
- `run_predefined_tests()` - Automated test mode

### `agent-info.txt`

Auto-generated file containing:
- Agent ID
- Agent name
- Model used
- Tool list
- Metadata

## 💡 Tips for Your Demo

1. **Show the creation process**: Run `create_customer_service_agent.py` live
2. **Interactive test**: Chat with agent to show capabilities
3. **Automated tests**: Show all 10 queries passing
4. **Trigger CI/CD**: Push to GitHub and show automated evaluation
5. **Show results**: Display evaluation metrics from GitHub Actions

## 🎯 Demo Talking Points

- **Declarative agent definition** - Tools defined as JSON schemas
- **Version controlled** - Agent config can be stored in Git
- **Automated testing** - CI/CD runs evaluation on every change
- **Comprehensive metrics** - Quality + safety evaluations
- **Production ready** - Same agent runs locally and in cloud

---

**Ready for your Thursday demo!** 🚀

For questions or issues, refer to the main project README or Azure AI Foundry documentation.

# Azure AI Foundry - CI/CD Evaluation Demo

This project demonstrates how to integrate Azure AI Foundry evaluation capabilities into GitHub Actions CI/CD pipelines for automated testing of AI agents and generative AI models.

## 🎯 Overview

This repository contains everything you need to run automated evaluations in your CI/CD pipeline:

- **AI Agent Evaluations**: For AI Foundry agents with conversation-based testing
- **GenAI Evaluations**: For generative AI models with structured input/output testing
- **Local Evaluation Scripts**: Run evaluations locally before committing to CI/CD

## 📋 Prerequisites

1. **Azure AI Foundry Project**
   - Create a project in [Azure AI Foundry](https://ai.azure.com)
   - Deploy an evaluation judge model (e.g., GPT-4o)

2. **GitHub Repository Setup**
   - Fork or clone this repository
   - Configure GitHub Actions secrets and variables

3. **Python Environment** (for local testing)
   - Python 3.9+
   - pip or conda

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd foundry-agents-cicd

# Copy environment template
cp .env.example .env

# Edit .env with your Azure credentials
# (See Configuration section below)
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Edit `.env` file with your Azure credentials:

```bash
# Required for Agent Evaluations
AZURE_AI_PROJECT_ENDPOINT=https://your-project.eastus.api.azureml.ms
AZURE_DEPLOYMENT_NAME=gpt-4o
AGENT_ID_BASELINE=your-agent-id

# Required for GenAI Evaluations
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_KEY=your-api-key
```

### 4. Run Local Evaluation

```bash
# Test AI Agent Evaluation
python scripts/local_agent_eval.py

# Test GenAI Evaluation
python scripts/local_genai_eval.py
```

## 📁 Project Structure

```
foundry-agents-cicd/
├── .github/
│   └── workflows/
│       ├── ai-agent-eval.yml          # AI Agent evaluation workflow
│       └── genai-eval.yml              # GenAI evaluation workflow
├── data/
│   ├── agent-eval-data.json            # Test queries for agent evaluation
│   └── genai-eval-data.jsonl           # Test data for GenAI evaluation
├── scripts/
│   ├── local_agent_eval.py             # Local agent evaluation script
│   └── local_genai_eval.py             # Local GenAI evaluation script
├── configs/
│   └── genai-eval-config.json          # GenAI evaluation configuration
├── .env.example                        # Environment variables template
├── .gitignore
├── requirements.txt                    # Python dependencies
└── README.md
```

## 🔧 Configuration

### GitHub Secrets (Required for CI/CD)

Configure these in GitHub Settings > Secrets and variables > Actions:

**Variables:**
- `AZURE_CLIENT_ID`: Azure service principal client ID
- `AZURE_TENANT_ID`: Azure tenant ID
- `AZURE_SUBSCRIPTION_ID`: Azure subscription ID

**Secrets:**
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key (for GenAI evals)

### Azure Federated Credentials Setup

For GitHub Actions to authenticate with Azure, set up federated credentials:

1. Go to Azure Portal > Azure Active Directory > App Registrations
2. Select your application
3. Go to Certificates & secrets > Federated credentials
4. Add credentials for:
   - **Entity type**: Environment (or Branch)
   - **GitHub organization**: Your org
   - **Repository**: Your repo
   - **Environment/Branch**: main (or your branch)

## 📊 Evaluation Types

### AI Agent Evaluations

Best for testing conversational AI agents built in Azure AI Foundry.

**Supported Evaluators:**
- General: Coherence, Fluency
- RAG: Groundedness, Relevance
- Safety: Violence, Sexual, SelfHarm, HateUnfairness, IndirectAttack
- Agent-specific: IntentResolution, TaskAdherence, ToolCallAccuracy

**Data Format:**
```json
{
  "name": "MyTestData",
  "evaluators": ["RelevanceEvaluator", "CoherenceEvaluator"],
  "data": [
    {"query": "Tell me about Tokyo?"},
    {"query": "Where is Italy?"}
  ]
}
```

### GenAI Evaluations

Best for testing generative AI models with structured inputs and outputs.

**Supported Evaluators:**
- All AI Agent evaluators
- Additional: QA, Similarity, F1Score, BleuScore, GroundednessProEvaluator

**Data Format:**
```jsonl
{"query": "Tell me about Tokyo?", "response": "Tokyo is the capital...", "ground_truth": "Tokyo is..."}
{"query": "Where is Italy?", "response": "Italy is in Europe...", "ground_truth": "Italy is..."}
```

## 🔄 CI/CD Integration

### Trigger Options

Both workflows support:
- **Manual trigger**: `workflow_dispatch`
- **Push to main**: Automatic on commits to main branch
- **Pull request**: Run on PR creation/update

### Customizing Triggers

Edit `.github/workflows/*.yml` to add conditional triggers:

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'prompts/**'          # Only run when prompts change
      - 'agent-config/**'     # Only run when agent config changes
```

## 📈 Viewing Results

### In GitHub Actions

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select the workflow run
4. View **Summary** for evaluation results

### In Azure AI Foundry

Results include links to Azure AI Foundry portal for detailed analysis:
- Individual test case results
- Confidence intervals
- Statistical significance (when comparing multiple agents)

## 🎯 Demo Scenarios

### Scenario 1: Single Agent Evaluation

Test a single agent version with confidence intervals:

```bash
# Update .env
AGENT_ID_BASELINE=your-agent-id

# Run locally
python scripts/local_agent_eval.py
```

### Scenario 2: A/B Testing (Multiple Agents)

Compare multiple agent versions with statistical significance:

```bash
# Update .env
AGENT_ID_BASELINE=agent-v1-id
AGENT_ID_VARIANT1=agent-v2-id

# Commit and push to trigger CI/CD
git add .
git commit -m "Test agent v2 against baseline"
git push
```

### Scenario 3: GenAI Model Evaluation

Evaluate a generative AI model with custom metrics:

```bash
# Configure genai-eval-config.json
# Run locally
python scripts/local_genai_eval.py
```

## 🎓 Best Practices

1. **Start Small**: Begin with 5-10 test queries, expand as needed
2. **Use Specific Triggers**: Avoid running on every commit to minimize costs
3. **Review Statistical Significance**: For multi-agent comparisons
4. **Monitor Costs**: Track evaluation token usage in Azure
5. **Version Your Data**: Keep test data in version control
6. **Baseline First**: Always establish a baseline before testing variants

## 🐛 Troubleshooting

### Common Issues

**Authentication Errors:**
- Verify federated credentials are configured correctly
- Check that GitHub variables match Azure app registration

**Evaluation Failures:**
- Ensure deployment name is correct and deployed
- Verify agent IDs are valid and accessible
- Check data format matches expected schema

**Token Limits:**
- Reduce dataset size for testing
- Use appropriate model for evaluation judges

## 📚 Additional Resources

- [Azure AI Evaluation SDK Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk)
- [GitHub Actions - Azure Login](https://github.com/Azure/login)
- [AI Agent Evals Action](https://github.com/microsoft/ai-agent-evals)
- [GenAI Evals Action](https://github.com/microsoft/genai-evals)

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

---

**Ready for your Thursday demo!** 🚀

For questions or support, reach out to the Azure AI Foundry team.

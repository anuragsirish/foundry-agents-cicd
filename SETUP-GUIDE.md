# Setup Guide for Azure AI Foundry CI/CD Evaluation Demo

This guide walks you through setting up the evaluation CI/CD pipeline for your Thursday customer demo.

## 📋 Pre-Demo Checklist

### ✅ Azure Resources (Do First)

1. **Azure AI Foundry Project**
   - [ ] Create or identify your Azure AI Foundry project
   - [ ] Note the project endpoint URL
   - [ ] Deploy an evaluation judge model (GPT-4o recommended)

2. **Azure Service Principal (for GitHub Actions)**
   - [ ] Create a service principal with access to your AI Foundry project
   - [ ] Configure federated credentials for GitHub Actions
   - [ ] Note: Client ID, Tenant ID, Subscription ID

3. **AI Agent (for Agent Evaluations)**
   - [ ] Deploy your AI agent in Azure AI Foundry
   - [ ] Note the agent ID(s)
   - [ ] Test the agent works in the portal

4. **Azure OpenAI (for GenAI Evaluations)**
   - [ ] Create Azure OpenAI resource
   - [ ] Deploy a chat model (GPT-4o or GPT-3.5-turbo)
   - [ ] Copy the endpoint and API key

### ✅ GitHub Setup

1. **Repository Configuration**
   - [ ] Fork or push this repository to GitHub
   - [ ] Enable GitHub Actions in repository settings

2. **Configure GitHub Variables** (Settings > Secrets and variables > Actions > Variables)
   ```
   AZURE_CLIENT_ID=<your-client-id>
   AZURE_TENANT_ID=<your-tenant-id>
   AZURE_SUBSCRIPTION_ID=<your-subscription-id>
   AZURE_AI_PROJECT_ENDPOINT=<your-project-endpoint>
   AZURE_DEPLOYMENT_NAME=<your-deployment-name>
   AGENT_ID_BASELINE=<your-agent-id>
   AZURE_OPENAI_ENDPOINT=<your-openai-endpoint>
   AZURE_OPENAI_CHAT_DEPLOYMENT=<your-chat-deployment>
   AZURE_OPENAI_API_VERSION=2024-08-01-preview
   API_VERSION=2024-08-01-preview
   ```

3. **Configure GitHub Secrets** (Settings > Secrets and variables > Actions > Secrets)
   ```
   AZURE_OPENAI_API_KEY=<your-api-key>
   ```

### ✅ Local Testing

1. **Environment Setup**
   ```bash
   # Clone repository
   git clone <your-repo-url>
   cd foundry-agents-cicd

   # Create and activate virtual environment
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure Local .env**
   ```bash
   # Copy template
   cp .env.example .env

   # Edit .env with your values
   # (Use your favorite text editor)
   ```

3. **Test Locally**
   ```bash
   # Test GenAI evaluation (easier to test first)
   python scripts/local_genai_eval.py

   # Test Agent evaluation (requires agent deployed)
   python scripts/local_agent_eval.py
   ```

## 🎯 Demo Preparation Steps

### Step 1: Prepare Your Test Data (15 minutes)

1. **For Agent Evaluations**:
   - Edit `data/agent-eval-data.json`
   - Add 5-10 queries relevant to your agent's domain
   - Example queries that showcase your agent's capabilities

2. **For GenAI Evaluations**:
   - Edit `data/genai-eval-data.jsonl`
   - Add query-response-ground_truth triples
   - Use real examples from your use case

### Step 2: Configure Evaluators (5 minutes)

Edit the evaluator lists in:
- `data/agent-eval-data.json` (for agent evals)
- `configs/genai-eval-config.json` (for GenAI evals)

Choose relevant evaluators:
- **Quality**: Coherence, Fluency, Relevance, Groundedness
- **Safety**: Violence, Sexual, SelfHarm, HateUnfairness
- **Agent-specific**: IntentResolution, TaskAdherence, ToolCallAccuracy

### Step 3: Test Locally (30 minutes)

1. Run local evaluation scripts
2. Verify results look correct
3. Check output files in `evaluation_results/`
4. Fix any configuration issues

### Step 4: Test CI/CD Pipeline (20 minutes)

1. **Commit and Push**:
   ```bash
   git add .
   git commit -m "Configure evaluation pipeline"
   git push origin main
   ```

2. **Monitor GitHub Actions**:
   - Go to GitHub > Actions tab
   - Watch the workflow run
   - Check for any errors

3. **Review Results**:
   - Click on the completed workflow
   - View the summary page
   - Verify results look good

### Step 5: Prepare Demo Scenarios (20 minutes)

Create 2-3 demo scenarios:

**Scenario 1: Single Agent Baseline**
- Show evaluation of one agent version
- Highlight key metrics and confidence intervals

**Scenario 2: A/B Testing**
- Update agent configuration
- Run evaluation comparing two versions
- Show statistical significance

**Scenario 3: Continuous Monitoring**
- Show how evaluation runs on every commit
- Demonstrate automated quality gates

## 🎤 Demo Script Suggestions

### Introduction (2 minutes)
"Today I'll show you how to integrate AI evaluation into your CI/CD pipeline using Azure AI Foundry and GitHub Actions."

### Demo Flow (15 minutes)

1. **Show the Problem** (2 min)
   - "How do we know if our AI agent changes improve quality?"
   - "Manual testing is time-consuming and inconsistent"

2. **Walk Through Setup** (3 min)
   - Show repository structure
   - Explain test data format
   - Show GitHub Actions workflow

3. **Run Live Evaluation** (5 min)
   - Make a change to test data or configuration
   - Commit and push
   - Watch GitHub Actions run in real-time
   - Show results in summary

4. **Explain Results** (3 min)
   - Walk through metrics
   - Explain confidence intervals
   - Show detailed results in Azure AI Foundry portal

5. **Advanced Features** (2 min)
   - A/B testing with multiple agents
   - Statistical significance testing
   - Integration with PR workflows

### Key Talking Points

✅ **Automated Quality Assurance**
- Evaluations run automatically on every change
- Catch regressions before production

✅ **Multiple Evaluation Dimensions**
- Quality: Coherence, Fluency, Relevance
- Safety: Violence, Hate, Self-harm detection
- Task-specific: Intent resolution, Tool accuracy

✅ **Statistical Rigor**
- Confidence intervals for single agent
- Statistical significance for comparisons
- Not just point estimates

✅ **Integration Ready**
- Works with existing GitHub workflows
- Can block PRs based on evaluation results
- Integrates with Azure AI Foundry portal

## 🐛 Troubleshooting Common Issues

### Issue: Authentication Failed
**Solution**: 
- Verify federated credentials are configured
- Check GitHub variables match Azure app registration
- Ensure service principal has correct permissions

### Issue: Agent Not Found
**Solution**:
- Verify agent ID is correct
- Check agent is deployed in Azure AI Foundry
- Ensure agent is in the same project as endpoint

### Issue: Evaluation Takes Too Long
**Solution**:
- Reduce number of test cases for demo
- Use smaller, faster models for judges
- Consider using GitHub Models (free tier)

### Issue: Data Format Errors
**Solution**:
- Validate JSONL format (one JSON object per line)
- Ensure required fields present (query, response)
- Remove any timestamp fields

### Issue: Rate Limiting
**Solution**:
- Use deployment with higher rate limits
- Reduce concurrent evaluators
- Add delays between evaluations

## 📊 Expected Demo Outcomes

After setup, you should be able to:

✅ Show automated evaluation running in GitHub Actions
✅ Display evaluation results in GitHub Actions summary
✅ Navigate to Azure AI Foundry portal for detailed results
✅ Demonstrate A/B testing between agent versions
✅ Explain how this integrates into existing CI/CD

## 🎓 Additional Demo Tips

1. **Have Backup Screenshots**: In case of live demo issues
2. **Pre-run Evaluations**: Have successful runs to show if needed
3. **Prepare FAQs**: Common questions about costs, setup time, limitations
4. **Show ROI**: Time saved, bugs caught, confidence in deployments
5. **Discuss Roadmap**: Future features, custom evaluators, integration plans

## ⏰ Time Estimate

- Azure setup: 1-2 hours (if starting fresh)
- GitHub configuration: 30 minutes
- Test data preparation: 30 minutes
- Local testing: 30 minutes
- CI/CD testing: 30 minutes
- Demo preparation: 1 hour

**Total: 4-5 hours** (less if Azure resources already exist)

## 📞 Getting Help

If you run into issues:
1. Check the troubleshooting section above
2. Review Azure AI Foundry documentation
3. Check GitHub Actions logs for detailed error messages
4. Verify all environment variables are set correctly

Good luck with your demo! 🚀

# 🤖 Azure AI Foundry - Comprehensive Agent Evaluation CI/CD

This project demonstrates automated AI agent evaluation and comparison using Azure AI Foundry and GitHub Actions. Every pull request automatically evaluates both baseline and V2 agents across **three tiers** (Quality, Safety, Red Team), compares their performance, and provides clear metrics for merge decisions.

## 🎯 Overview

**Automated Agent Quality Assurance** - Never merge agent changes without knowing their impact on quality, safety, and security metrics.

### Key Features

- **🎯 Comprehensive Evaluation**: Three-tier evaluation (Quality + Safety + Red Team) on every PR
- **📊 Visual Comparison**: Clear percentage changes and improvements/regressions
- **🛡️ Safety Evaluation**: ContentSafetyEvaluator for Violence, Sexual, SelfHarm, Hate/Unfairness
- **🔴 Red Team Testing**: 10+ attack scenarios per risk category with granular attack strategy breakdown
- **💬 PR Integration**: Results posted directly to PR comments
- **📋 GitHub Actions Summary**: Full comparison table visible on Actions tab
- **✅ Always Passes**: Workflow provides metrics, you decide whether to merge
- **📦 Artifacts**: Full evaluation results downloadable for deep analysis
- **🔒 Secure**: Uses Azure federated credentials (OIDC) - no secrets in code

## 📊 What You Get

When you create a PR, a comprehensive evaluation workflow automatically runs:

### Three-Tier Evaluation Pipeline

#### 1. Quality Metrics Evaluation
- **Evaluates Both Agents** against test queries
- **Compares Results** across 8 quality dimensions:
  - Relevance
  - Coherence
  - Fluency
  - Groundedness
  - Similarity (to reference answers)
  - Intent Resolution
  - Task Adherence
  - Tool Call Accuracy
- **Shows Percentage Changes** and trends

#### 2. Safety Evaluation
- **ContentSafetyEvaluator** assesses both agents for:
  - Violence
  - Sexual content
  - Self-harm
  - Hate/Unfairness
- **Defect Rates** calculated for each category
- **Threshold Performance** tracking (pass rate at severity ≥3)

#### 3. Red Team Testing
- **10+ Attack Scenarios** per risk category
- **11 Attack Strategies** including:
  - EASY, MODERATE (difficulty levels)
  - CharacterSpace, ROT13, Leetspeak (encoding attacks)
  - CharSwap, UnicodeConfusable, Flip (character attacks)
  - Base64+ROT13, Base64, Morse, Tense (transformation attacks)
- **Granular Attack Breakdown** showing counts per strategy
- **Vulnerable Categories** identified with examples

All results are:
- **Posted to PR Comments** with comprehensive comparison tables
- **Visible in GitHub Actions Summary**
- **Downloadable as Artifacts** for deep analysis

### Example Output

```
📊 Comprehensive Agent Comparison

Quality Metrics (8 evaluators):
| Metric              | Baseline | V2   | Change   |
|---------------------|----------|------|----------|
| Relevance           | 4.20     | 4.50 | +7%      |
| Coherence           | 4.10     | 4.15 | +1%      |
| Groundedness        | 4.00     | 4.20 | +5%      |
| Similarity          | 3.80     | 4.10 | +8%      |

Safety Evaluation (4 risk categories):
| Risk Category       | Baseline Defects | V2 Defects | Change   |
|---------------------|------------------|------------|----------|
| Violence            | 0                | 0          | 0%       |
| Sexual              | 0                | 0          | 0%       |
| Hate/Unfairness     | 1                | 0          | -100%    |

Red Team Testing (10+ scenarios per category):
| Attack Strategy     | Baseline Vulnerable | V2 Vulnerable | Change   |
|---------------------|---------------------|---------------|----------|
| ROT13               | 2                   | 1             | -50%     |
| Leetspeak           | 3                   | 1             | -67%     |
| Base64              | 1                   | 0             | -100%    |

Summary:
- 📈 Overall Quality: +5%
- �️ Safety Defects: -50%
- 🔴 Red Team Resilience: +40%
```

## �📋 Prerequisites

1. **Azure AI Foundry Project**
   - Create a project in [Azure AI Foundry](https://ai.azure.com)
   - Deploy a GPT-4 or GPT-4.1 model for evaluation
   - Create baseline and V2 agents

2. **GitHub Repository Setup**
   - Fork or clone this repository
   - Configure federated credentials (OIDC)
   - Set up GitHub Actions variables

3. **Python Environment** (for local testing)
   - Python 3.11+
   - pip or conda

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/anuragsirish/foundry-agents-cicd.git
cd foundry-agents-cicd
```

### 2. Set Up Azure (One-time)

See [`SETUP-GUIDE.md`](SETUP-GUIDE.md) for detailed instructions on:
- Creating Azure AI Foundry project
- Deploying evaluation model
- Setting up federated credentials
- Configuring GitHub Actions variables

### 3. Configure GitHub Variables

```bash
# Set required variables
gh variable set AGENT_ID_BASELINE --body "asst_xxxxx"
gh variable set AGENT_ID_V2 --body "asst_yyyyy"
gh variable set AZURE_AI_PROJECT_ENDPOINT --body "https://..."
gh variable set AZURE_DEPLOYMENT_NAME --body "gpt-4.1"
gh variable set AZURE_CLIENT_ID --body "xxxxx"
gh variable set AZURE_TENANT_ID --body "xxxxx"
gh variable set AZURE_SUBSCRIPTION_ID --body "xxxxx"
```

### 4. Test Locally (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export AGENT_ID_BASELINE="asst_xxxxx"
export AZURE_AI_PROJECT_ENDPOINT="https://..."
export AZURE_DEPLOYMENT_NAME="gpt-4.1"

# Run evaluations (choose one or all)
python scripts/local_quality_eval.py     # Quality metrics
python scripts/local_safety_eval.py      # Safety evaluation
python scripts/local_redteam_eval.py     # Red team testing
```

### 5. Create a Test PR

```bash
# Create a new branch
git checkout -b test/agent-evaluation

# Make a small change to trigger workflow
echo '{"query": "Test query"}' >> data/agent-eval-data.json

# Commit and push
git add data/agent-eval-data.json
git commit -m "test: Trigger agent evaluation"
git push -u origin test/agent-evaluation

# Create PR
gh pr create --title "Test: Agent Evaluation" --body "Testing comprehensive three-tier evaluation workflow"
```

### 6. View Results

- Check **GitHub Actions tab** for workflow progress
- See **PR comments** for comparison table
- Download **artifacts** for full JSON results

## 📁 Project Structure

```
foundry-agents-cicd/
├── .github/
│   └── workflows/
│       └── agent-evaluation-unified.yml      # 🤖 Comprehensive three-tier evaluation (ACTIVE)
├── agent-setup/
│   ├── create_agent_v2.py                    # Script to create V2 agent
│   └── test_agent_locally.py                 # Local agent testing
├── data/
│   └── agent-eval-data.json                  # Test queries and evaluators config
├── scripts/
│   ├── local_quality_eval.py                 # Quality evaluation (8 metrics)
│   ├── local_safety_eval.py                  # Safety evaluation (4 categories)
│   └── local_redteam_eval.py                 # Red team testing (10+ scenarios)
├── evaluation_results/
│   ├── quality_eval_output/                  # Quality evaluation results
│   ├── safety_eval_output/                   # Safety evaluation results
│   ├── redteam_eval_output/                  # Red team testing results
│   └── baseline/                             # Baseline agent results
│   ├── v2/                                   # V2 agent results
│   └── agent_eval_output/                    # Raw evaluation output
├── docs/
│   ├── SETUP-GUIDE.md                        # Detailed setup instructions
│   ├── ARCHITECTURE.md                       # System architecture
│   ├── CICD_PIPELINE.md                      # Pipeline documentation
│   ├── WORKFLOW_COMPARISON.md                # Workflow approach comparison
│   ├── QUICK_REFERENCE.md                    # Quick command reference
│   ├── DEMO_GUIDE.md                         # Customer demo guide
│   └── IMPLEMENTATION_SUMMARY.md             # Implementation details
├── requirements.txt                          # Python dependencies
└── README.md                                 # This file
├── requirements.txt                    # Python dependencies
└── README.md
```

## 🔧 Configuration

### GitHub Variables (Required)

Configure these in GitHub Settings > Secrets and variables > Actions > Variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `AGENT_ID_BASELINE` | Baseline agent ID | `asst_z8OW7ueROQbJydYkgLXG1lid` |
| `AGENT_ID_V2` | V2 agent ID to compare | `asst_Q15Vo007Ejlu1jSWGj1kuncR` |
| `AZURE_CLIENT_ID` | Service principal client ID | `7c64d271-6345-43b3-b9ba-...` |
| `AZURE_TENANT_ID` | Azure tenant ID | `ed276d0c-896f-484d-881f-...` |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID | `0debeb64-562c-44d8-9966-...` |
| `AZURE_AI_PROJECT_ENDPOINT` | AI Foundry project endpoint | `https://xxx.services.ai.azure.com/api/projects/...` |
| `AZURE_DEPLOYMENT_NAME` | Model deployment name | `gpt-4.1` |

### Quick Configuration

```bash
# Set all variables at once
gh variable set AGENT_ID_BASELINE --body "asst_xxxxx"
gh variable set AGENT_ID_V2 --body "asst_yyyyy"
gh variable set AZURE_CLIENT_ID --body "xxxxx"
gh variable set AZURE_TENANT_ID --body "xxxxx"
gh variable set AZURE_SUBSCRIPTION_ID --body "xxxxx"
gh variable set AZURE_AI_PROJECT_ENDPOINT --body "https://..."
gh variable set AZURE_DEPLOYMENT_NAME --body "gpt-4.1"
```

### Azure Federated Credentials (OIDC)

The workflow uses federated credentials for secure authentication without storing secrets.

1. Go to Azure Portal > Azure Active Directory > App Registrations
2. Select your application
3. Go to Certificates & secrets > Federated credentials
4. Add credentials for:
   - **Entity type**: Environment (or Branch)
   - **GitHub organization**: Your org
   - **Repository**: Your repo
   - **Environment/Branch**: main (or your branch)

## 📊 Evaluation Metrics

The workflow evaluates agents across 5 quality dimensions:

### Quality Metrics (1-5 scale)

| Metric | Description | What it measures |
|--------|-------------|------------------|
| **Relevance** | How relevant is the response to the query? | Alignment with user intent |
| **Coherence** | Does the response flow logically? | Internal consistency |
| **Fluency** | Is the response grammatically correct? | Language quality |
| **Groundedness** | Is the response based on provided context? | Factual accuracy |
| **Tool Call Accuracy** | Did the agent use the right tools? | Tool selection & usage |

### Status Indicators

- 🟢 **Green**: V2 improved over baseline
- 🔴 **Red**: V2 regressed from baseline
- 🟡 **Yellow**: No significant change

### Test Data Format

Edit `data/agent-eval-data.json`:

```json
{
  "name": "CustomerServiceAgentEval",
  "evaluators": [
    "RelevanceEvaluator",
    "CoherenceEvaluator",
    "FluencyEvaluator",
    "GroundednessEvaluator",
    "ToolCallAccuracyEvaluator"
  ],
  "data": [
    {"query": "What are your return policies?"},
    {"query": "How do I track my order?"},
    {"query": "Do you ship internationally?"}
  ]
}
```

## 🔄 Workflow Triggers

Two evaluation workflows run automatically on PRs:

### Quality Metrics Workflow (`agent-eval-on-pr.yml`)
- **Triggers on**: Pull requests when these files change:
  - `agent-setup/**` (agent code changes)
  - `data/agent-eval-data.json` (test queries)
  - `.github/workflows/agent-eval-on-pr.yml` (workflow updates)

### Safety Evaluation Workflow (`agent-safety-eval-on-pr.yml`)
- **Triggers on**: Pull requests when these files change:
  - `agent-setup/**` (agent code changes)
  - `data/**` (test data)
  - `scripts/**` (evaluation scripts)
  - `.github/workflows/agent-safety-eval-on-pr.yml` (workflow updates)

Both workflows support **manual trigger** via `workflow_dispatch` for testing

### Customizing Triggers

Edit `.github/workflows/agent-eval-on-pr.yml`:

```yaml
on:
  pull_request:
    branches: [main]
    paths:
      - 'agent-setup/**'
      - 'data/agent-eval-data.json'
      # Add your paths here
```

## 📈 Viewing Results

### GitHub Actions Tab

1. Go to repository **Actions** tab
2. Click on latest workflow run
3. Scroll to **Summary** section
4. View comparison table with metrics

### PR Comments

- Automated bot comment posts results
- Includes comparison table
- Shows agent IDs and run details
- Links to workflow run and artifacts

### Artifacts

Download full evaluation results:
1. Click on workflow run
2. Scroll to **Artifacts** section
3. Download `evaluation-results-*`
4. Contains:
   - `baseline_results.json` - Full baseline evaluation
   - `v2_results.json` - Full V2 evaluation
   - `comparison.json` - Comparison summary

## 🎯 Use Cases

### Pre-Production Testing

Ensure agent changes maintain quality before production:
```bash
git checkout -b feature/improve-responses
# Make agent changes
git push
# PR triggers automatic evaluation
# Review metrics before merging
```

### A/B Testing

Compare two agent versions:
- Baseline: Current production agent
- V2: Experimental agent with new features

### Continuous Monitoring

Track agent quality over time:
- Every PR adds a data point
- Artifacts provide historical record
- Identify quality trends

## 🎓 Best Practices

### Test Data Management

1. **Start with 5-10 representative queries**
   - Cover main use cases
   - Include edge cases
   - Add failing scenarios

2. **Keep test data in version control**
   - Track changes over time
   - Review test updates in PRs
   - Document why queries were added

3. **Update tests when agent capabilities change**
   - Add tests for new features
   - Remove obsolete tests
   - Adjust expected behaviors

### Workflow Optimization

1. **Use path filters** to avoid unnecessary runs
   ```yaml
   paths:
     - 'agent-setup/**'
     - 'data/agent-eval-data.json'
   ```

2. **Monitor costs** - Track evaluation token usage in Azure

3. **Archive old artifacts** - Clean up artifacts older than 30 days

### Agent Development

1. **Test locally first** - Run `local_agent_eval.py` before pushing

2. **Small, focused changes** - Easier to understand metric impacts

3. **Document regressions** - If merging despite regressions, explain why

## 🐛 Troubleshooting

### Common Issues

**Authentication Errors**
```
Error: Failed to get federated token
```
- Verify federated credentials in Azure Portal
- Check GitHub variables match Azure app registration
- Ensure repository environment matches federated credential settings

**Agent Not Found**
```
Error: Agent ID not found
```
- Verify `AGENT_ID_BASELINE` and `AGENT_ID_V2` are correct
- Check agents exist in Azure AI Foundry project
- Ensure endpoint URL is correct

**Evaluation Timeout**
```
Error: Evaluation timed out
```
- Reduce number of test queries
- Check Azure deployment has sufficient capacity
- Verify deployment is in same region as project

**No Results in PR Comment**
```
Warning: github-script action failed
```
- Ensure `pull-requests: write` permission is set
- Check workflow ran on a pull request (not direct push)
- Verify bot has access to repository

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [SETUP-GUIDE.md](SETUP-GUIDE.md) | Complete Azure and GitHub setup |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Dev → Staging → Production deployment process |
| [DEMO_GUIDE.md](DEMO_GUIDE.md) | Customer demo instructions |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture and design |
| [CICD_PIPELINE.md](CICD_PIPELINE.md) | Pipeline implementation details |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Command reference guide |
| [WORKFLOW_COMPARISON.md](WORKFLOW_COMPARISON.md) | Workflow approach comparison |

## � Additional Resources

- [Azure AI Evaluation SDK](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk)
- [Azure AI Foundry Portal](https://ai.azure.com)
- [GitHub Actions - Azure Login](https://github.com/Azure/login)
- [Federated Credentials Guide](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation)

## 📦 Repository Tags

Stable versions are tagged for easy rollback:

| Tag | Description |
|-----|-------------|
| `v2.0.0-comprehensive-eval` | Latest stable (three-tier evaluation) |
| `v1.0.0-dual-agent-eval` | Previous stable (quality + safety only) |

```bash
# Checkout a specific version
git checkout v2.0.0-comprehensive-eval

# List all tags
git tag -l
```

## 🤝 Contributing

Contributions welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `local_agent_eval.py`
5. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

---

## 🚀 Quick Links

- 📖 [Setup Guide](SETUP-GUIDE.md) - Get started
- 🎬 [Demo Guide](DEMO_GUIDE.md) - Present to customers
- 🏗️ [Architecture](ARCHITECTURE.md) - Understand the design
- 📋 [Quick Reference](QUICK_REFERENCE.md) - Common commands

**Built with ❤️ using Azure AI Foundry and GitHub Actions**
# Testing safety evaluation workflow

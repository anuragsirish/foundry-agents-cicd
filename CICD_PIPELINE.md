# CI/CD Pipeline for Comprehensive Agent Evaluation

This repository implements an automated CI/CD pipeline that evaluates and compares two AI agents (baseline and V2) on every pull request across **three tiers** (Quality, Safety, Red Team), providing comprehensive metrics for data-driven merge decisions.

## 🎯 Overview

The CI/CD pipeline automatically:
- 🎯 Evaluates baseline agent with test queries (quality + safety + red team)
- 🚀 Evaluates V2 agent with same test queries (quality + safety + red team)
- 📊 Compares metrics across 8 quality dimensions, 4 safety categories, 10+ red team scenarios
- 💬 Posts comprehensive comparison table to PR comments with attack strategy breakdown
- 📋 Displays results in GitHub Actions summary
- 📦 Uploads full results as artifacts
- ✅ Always passes (you decide whether to merge)

## 🏗️ Architecture

```
┌─────────────────┐
│   Developer     │
│  Creates PR     │
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────────────────────┐
│  PR Workflow (agent-evaluation-unified.yml)      │
│  ──────────────────────────────────────────────  │
│  1. Checkout PR branch                           │
│  2. Azure authentication (OIDC)                  │
│                                                   │
│  3. Quality Evaluation (8 metrics)               │
│     - Evaluate baseline agent                    │
│     - Evaluate V2 agent                          │
│                                                   │
│  4. Safety Evaluation (4 categories)             │
│     - ContentSafetyEvaluator for both agents     │
│                                                   │
│  5. Red Team Testing (10+ scenarios)             │
│     - 11 attack strategies per risk category     │
│     - Granular attack breakdown                  │
│                                                   │
│  6. Compare all metrics (baseline vs V2)         │
│  7. Post comprehensive report to PR comment      │
│  8. Display in GitHub Actions summary            │
│  9. Upload artifacts                             │
│  10. ✅ Always pass                              │
└────────┬─────────────────────────────────────────┘
         │
         ▼
   Developer reviews comprehensive metrics
   and decides to merge or not
```

## 📋 Workflows

### **agent-evaluation-unified.yml** - Comprehensive Three-Tier Evaluation (ACTIVE)

**Triggers on:**
- Pull requests to `main` branch
- Changes to:
  - `agent-setup/**`
  - `data/agent-eval-data.json`
  - `.github/workflows/agent-eval-on-pr.yml`
- Manual workflow dispatch

**Features:**
- 🤖 Three-tier evaluation: Quality (8 metrics) + Safety (4 categories) + Red Team (10+ scenarios)
- 📊 Comprehensive comparison with percentage changes
- 🔴 Granular attack strategy breakdown (ROT13, Leetspeak, Base64, etc.)
- 💬 Automated PR comments with all three evaluation tiers
- 📋 GitHub Actions summary display
- 📦 Artifact uploads (full JSON results for all three tiers)
- ✅ Always passes (manual merge decision)
- 🔐 Secure with federated credentials (OIDC)

**What You Get:**
- Side-by-side comparison of all quality, safety, and red team metrics
- Clear percentage changes showing improvements/regressions
- Attack strategy counts showing which attacks were tested
- Vulnerable category examples for red team failures
- Downloadable artifacts for deep analysis
- Full transparency into agent performance and security

## 🚀 Setup Instructions

### Step 1: Configure GitHub Variables

Add these as **Repository Variables** (Settings → Secrets and variables → Actions → Variables):

```bash
# Required Variables
AGENT_ID_BASELINE         # Baseline agent ID (e.g., asst_z8OW...)
AGENT_ID_V2               # V2 agent ID to compare (e.g., asst_Q15...)
AGENT_ID_STAGING          # (Optional) Staging environment agent
AGENT_ID_PRODUCTION       # (Optional) Production environment agent
AZURE_CLIENT_ID           # Azure service principal client ID
AZURE_TENANT_ID           # Azure tenant ID
AZURE_SUBSCRIPTION_ID     # Azure subscription ID
AZURE_AI_PROJECT_ENDPOINT # AI Foundry project endpoint (https://your-project.region.ai.azure.com)
AZURE_DEPLOYMENT_NAME     # Model deployment name (e.g., gpt-4o)
API_VERSION               # 2024-08-01-preview
AZURE_OPENAI_ENDPOINT     # For evaluators
AZURE_OPENAI_API_VERSION  # 2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME # Model for evaluators
```

### Step 2: Set Up Federated Credentials

Follow the Azure setup guide to create federated credentials for GitHub Actions:

```bash
# Required for both PR and main branch workflows
Environment: production
Subject: repo:your-org/your-repo:ref:refs/heads/main
Subject: repo:your-org/your-repo:pull_request
```

### Step 3: Initialize Baseline

**Option A: Run evaluation locally first**
```bash
# Run evaluations locally
python scripts/local_quality_eval.py    # Quality metrics
python scripts/local_safety_eval.py     # Safety evaluation  
python scripts/local_redteam_eval.py    # Red team testing

# Commit baseline to main
git add evaluation_results/
git commit -m "Initialize baseline metrics"
git push origin main
```

**Option B: Let first PR create baseline**
- Create a PR
- The workflow will detect no baseline exists
- Evaluation will run and show "First Run"
- When merged, baseline is automatically created

### Step 4: Test the Pipeline

Create a test PR:
```bash
# Create a test branch
git checkout -b test-cicd-pipeline

# Make a small change (e.g., add a comment)
echo "# Test change" >> README.md

# Commit and push
git add README.md
git commit -m "Test: CI/CD pipeline"
git push origin test-cicd-pipeline

# Open PR on GitHub
gh pr create --title "Test CI/CD Pipeline" --body "Testing automated evaluations"
```

Watch the workflow run and check the PR comment!

## 📊 Understanding the Results

### PR Comment Example (With Baseline)

```markdown
## 🤖 Agent Evaluation Results

### ✅ Evaluation Passed
All quality metrics meet the baseline threshold (no degradation > 5%)

### 📊 Metrics Comparison

| Metric | Current | Baseline | Change | % Change |
|--------|---------|----------|---------|----------|
| 🟢 Relevance | 4.850 | 4.750 | +0.100 | +2.1% |
| 🟡 Coherence | 4.900 | 4.890 | +0.010 | +0.2% |
| 🟡 Fluency | 4.920 | 4.915 | +0.005 | +0.1% |
| 🟢 Groundedness | 4.780 | 4.650 | +0.130 | +2.8% |
| 🟡 Tool Call Accuracy | 0.950 | 0.940 | +0.010 | +1.1% |

### ⚡ Performance Metrics

| Metric | Current | Baseline | Change |
|--------|---------|----------|--------|
| Avg Response Time (s) | 2.35 | 2.40 | -0.05 |
| Completion Tokens | 145.20 | 150.30 | -5.10 |
| Prompt Tokens | 520.10 | 515.80 | +4.30 |

---
**Run ID:** `pr-123-20250122-143052`
**Agent ID:** `asst_z8OW7ueROQbJydYkgLXG1lid`
**Test Queries:** 10
```

### Metric Indicators

- 🟢 **Green** - Improvement >5%
- 🟡 **Yellow** - Within ±5% (acceptable)
- 🔴 **Red** - Degradation >5% (fails quality gate)

### Quality Gate Behavior

The workflow **fails** if any quality metric degrades by >5%:
- Relevance, Coherence, Fluency, Groundedness
- Tool Call Accuracy, Intent Resolution, Task Adherence

Performance metrics (response time, tokens) are tracked but don't block PRs.

## 🔧 Customization

### Adjust Quality Threshold

Edit `agent-eval-on-pr.yml`, line ~155:

```python
if comparison[metric]['diff_pct'] < -5:  # Change -5 to your threshold
    failed_metrics.append(metric)
```

### Add/Remove Metrics

Edit baseline extraction in both workflows:

```python
baseline_metrics = {
    'relevance': metrics.get('relevance', 0),
    'your_custom_metric': metrics.get('your_custom_metric', 0),
    # ...
}
```

### Change Trigger Paths

Edit workflow triggers:

```yaml
on:
  pull_request:
    paths:
      - 'agent-setup/**'
      - 'your-custom-path/**'  # Add your paths
```

### Add Conditional Quality Gates

You can add business logic to skip quality gates:

```yaml
- name: Check Quality Gate
  if: |
    steps.check-baseline.outputs.baseline_exists == 'true' && 
    steps.compare.outputs.evaluation_passed == 'false' &&
    !contains(github.event.pull_request.labels.*.name, 'skip-quality-gate')
```

## 📁 File Structure

```
.github/workflows/
├── agent-eval-on-pr.yml      # PR evaluation workflow
└── update-baseline.yml        # Baseline update workflow

scripts/
├── local_agent_eval.py        # Main evaluation script
└── initialize_baseline.py     # Baseline initialization

evaluation_results/
├── baseline/
│   ├── baseline_metrics.json        # Current baseline (committed)
│   └── baseline_full_results.json   # Full results (committed)
├── pr_runs/
│   └── pr-{number}-{timestamp}/     # PR-specific results (artifacts)
└── agent_eval_output/               # Latest local run
```

## 🐛 Troubleshooting

### Workflow Fails: "No baseline found"
**Solution:** Initialize baseline first (see Step 3 above)

### Workflow Fails: "Azure authentication failed"
**Solution:** Check federated credentials are configured correctly

### Metrics Always Show 0
**Solution:** Verify evaluator model deployment and endpoint

### PR Comment Not Posted
**Solution:** 
1. Check workflow has `pull-requests: write` permission
2. Verify GITHUB_TOKEN has correct permissions
3. Check repository settings allow Actions to comment

### Quality Gate Too Strict/Loose
**Solution:** Adjust threshold in workflow (see Customization)

## 📚 Best Practices

1. **Review Baselines Regularly**
   - Baselines should reflect current expected quality
   - Update intentionally when making improvements
   - Document why baselines changed

2. **Monitor Performance Trends**
   - Track token usage over time
   - Watch for response time increases
   - Set up alerts for cost anomalies

3. **Test Data Quality**
   - Keep test queries realistic and diverse
   - Update test data when adding features
   - Include edge cases and error scenarios

4. **PR Workflow**
   - Don't bypass quality gates without documentation
   - Include evaluation results in PR reviews
   - Celebrate improvements in metrics! 🎉

5. **Baseline Updates**
   - Only merge to main after thorough review
   - Each main merge updates baseline
   - Keep historical baselines in artifacts

## 🔗 Related Documentation

- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)**: Dev → Staging → Production deployment process
- **[SETUP-GUIDE.md](./SETUP-GUIDE.md)**: Azure AI Agent Evaluation Setup
- **[ARCHITECTURE.md](./ARCHITECTURE.md)**: System architecture and design
- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)**: Command reference guide
- **[azure-ai-github-eval.md](./azure-ai-github-eval.md)**: Azure AI GitHub Eval Overview
- **[agent-setup/README.md](./agent-setup/README.md)**: Agent Creation Guide

## 🤝 Contributing

When contributing agent improvements:

1. Create a feature branch
2. Make your changes
3. Run local evaluations:
   - `python scripts/local_quality_eval.py`
   - `python scripts/local_safety_eval.py`
   - `python scripts/local_redteam_eval.py`
4. Create PR (comprehensive CI/CD kicks in automatically)
5. Review evaluation results in PR comment (quality + safety + red team)
6. Address any quality degradations or safety issues
7. Merge when approved and passing

## 📞 Support

If you encounter issues:

1. Check workflow logs in GitHub Actions
2. Review troubleshooting section above
3. Verify all environment variables are set
4. Check Azure credentials and permissions
5. Run evaluation locally to isolate issues

---

**Last Updated:** January 2025
**Version:** 1.0.0

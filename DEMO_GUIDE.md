# 🎯 Customer Demo Guide

## Dual-Agent Evaluation CI/CD Workflow

This guide provides step-by-step instructions for demonstrating the automated agent evaluation and comparison workflow to customers.

---

## 📋 Demo Options

### **Option 1: Live Demo with a Test PR** (Recommended)

#### 1. Create a test change

```powershell
# Create a new branch
git checkout -b demo/agent-improvement

# Make a small change to trigger the workflow
code data/agent-eval-data.json
```

#### 2. Add a new test query

Edit `data/agent-eval-data.json` and add a new query to the `data` array:

```json
{
  "query": "What are your shipping options for international orders?"
}
```

#### 3. Push and create PR

```powershell
git add data/agent-eval-data.json
git commit -m "demo: Add new test query for agent evaluation"
git push -u origin demo/agent-improvement

# Create PR
gh pr create --title "Demo: Agent Evaluation CI/CD" --body "Demonstrating automated agent evaluation and comparison"
```

#### 4. Show the customer

- 📱 **GitHub Actions Tab**: Show the workflow running with emoji icons
  - 🤖 Agent Evaluation with Comparison
  - 🎯 Evaluate Baseline Agent
  - 🚀 Evaluate V2 Agent
  - 📊 Compare Agent Results
  
- 📊 **Live Summary**: Point out the comparison table appearing in real-time
  - Metrics comparison with baseline vs V2
  - Status indicators (🟢 🔴 🟡)
  - Summary counts of improvements/regressions
  
- 💬 **PR Comment**: Show how the bot automatically posts results
  - Detailed comparison table
  - Agent IDs and run information
  - Links to artifacts
  
- 📈 **Metrics Comparison**: Walk through baseline vs V2 comparison
  - Relevance, Coherence, Fluency, Groundedness
  - Tool Call Accuracy
  - Clear indicators for each metric
  
- ✅ **Decision Making**: Explain how they can merge or reject based on metrics
  - Workflow always passes
  - Developer decides based on results
  - No automatic rejections

---

### **Option 2: Walk Through Previous Run**

If you don't want to create a new PR:

```powershell
# Show the latest workflow runs
gh run list --workflow=agent-eval-on-pr.yml --limit 5

# Open the latest run in browser
gh run view --web
```

Then walk through:
1. The workflow steps with emojis
2. The summary section with comparison table
3. The artifacts available for download
4. How to interpret the results

---

### **Option 3: Screen Recording Demo**

Create a 5-minute recording showing:

#### 1. Problem Statement (30 sec)
- "We need to ensure agent changes don't degrade quality"
- "Manual testing is time-consuming and inconsistent"
- "Need automated quality gates before production"

#### 2. Solution Overview (1 min)
- "Automated evaluation on every PR"
- "Compares new agent against baseline"
- "Shows metrics with clear indicators"
- "Uses Azure AI Evaluation SDK"

#### 3. Live Walkthrough (3 min)
- Create a PR with agent changes
- Show workflow triggering automatically
- Point out the evaluation steps running
- Highlight the comparison results
- Show green/red/yellow indicators
- Demonstrate PR comment integration

#### 4. Benefits Summary (30 sec)
- No manual testing needed
- Catch regressions before production
- Data-driven merge decisions
- Full audit trail with artifacts

---

## 🎤 Key Points to Emphasize

### ✅ **Automated Quality Gates**
- "Every PR automatically evaluates both agents"
- "No need for manual testing or human intervention"
- "Runs in 2-3 minutes per agent"

### ✅ **Clear Visual Indicators**
- 🟢 **Green** = Improvements over baseline
- 🔴 **Red** = Regressions (worse than baseline)
- 🟡 **Yellow** = Neutral (no significant change)

### ✅ **Data-Driven Decisions**
- "See exact metrics before merging"
- "Compare across 5 quality dimensions:"
  - Relevance
  - Coherence
  - Fluency
  - Groundedness
  - Tool Call Accuracy

### ✅ **Production-Ready**
- "Uses Azure AI Evaluation SDK"
- "Same evaluators Microsoft recommends"
- "Federated auth (OIDC) - no secrets in code"
- "Scales with your team"

### ✅ **Developer-Friendly**
- "Results in PR comments - no context switching"
- "Summary on Actions tab - at a glance"
- "Artifacts for deep dives - full JSON results"
- "Workflow always passes - you decide"

---

## 🛠️ Demo Prep Commands

```powershell
# Set up a clean demo environment
git checkout main
git pull

# Check that variables are set
gh variable list

# Should show:
# - AGENT_ID_BASELINE
# - AGENT_ID_V2
# - AZURE_AI_PROJECT_ENDPOINT
# - AZURE_DEPLOYMENT_NAME
# - AZURE_CLIENT_ID
# - AZURE_TENANT_ID
# - AZURE_SUBSCRIPTION_ID

# Check recent workflow runs
gh run list --workflow=agent-eval-on-pr.yml --limit 5

# Prepare the demo branch (optional)
git checkout -b demo/customer-demo
```

---

## ❓ Common Questions & Answers

### **Q: Can we customize the metrics?**
**A:** Yes! Edit `data/agent-eval-data.json` to add/remove evaluators:
```json
{
  "evaluators": [
    "RelevanceEvaluator",
    "CoherenceEvaluator",
    "FluencyEvaluator",
    "GroundednessEvaluator",
    "ToolCallAccuracyEvaluator"
  ]
}
```

### **Q: How long does it take?**
**A:** ~2-3 minutes per agent. Both agents are evaluated sequentially, so total time is ~5-6 minutes per PR.

### **Q: What if we have more than 2 agents?**
**A:** Easy to extend! Just:
1. Add more agent IDs to GitHub variables (e.g., `AGENT_ID_V3`)
2. Add another evaluation step in the workflow
3. Update comparison logic to include all agents

### **Q: Can we run this locally before pushing?**
**A:** Yes! Use the local evaluation script:
```powershell
# Set environment variables
$env:AGENT_ID_BASELINE = "asst_xxxxx"
$env:AZURE_AI_PROJECT_ENDPOINT = "https://..."
$env:AZURE_DEPLOYMENT_NAME = "gpt-4.1"

# Run evaluation
python scripts/local_agent_eval.py
```

### **Q: Does it work with other Azure regions?**
**A:** Yes, as long as:
- The Azure AI project is accessible
- The deployment model is available in that region
- Federated credentials are configured

### **Q: What if the workflow fails?**
**A:** The workflow is designed to always pass and show results. If there are infrastructure issues:
- Check Azure authentication (federated credentials)
- Verify agent IDs are correct
- Ensure deployment name matches actual deployment
- Review workflow logs for specific errors

### **Q: Can we set quality thresholds?**
**A:** Currently, the workflow shows all metrics and lets you decide. You can modify the workflow to add automatic quality gates:
```yaml
- name: Check Quality Gate
  run: |
    # Example: Fail if any metric drops by more than 10%
    python scripts/check_thresholds.py
```

### **Q: How do we handle multiple environments (dev/staging/prod)?**
**A:** Use different branches with environment-specific variables:
- `dev` branch → dev agent IDs
- `staging` branch → staging agent IDs
- `main` branch → production agent IDs

---

## 📊 Demo Metrics to Highlight

When showing results, emphasize these metrics:

1. **Relevance** (1-5 scale)
   - "How relevant is the agent's response to the query?"
   - Higher is better

2. **Coherence** (1-5 scale)
   - "How well does the response flow logically?"
   - Higher is better

3. **Fluency** (1-5 scale)
   - "Is the response grammatically correct and natural?"
   - Higher is better

4. **Groundedness** (1-5 scale)
   - "Is the response based on provided context/data?"
   - Higher is better

5. **Tool Call Accuracy** (percentage)
   - "Did the agent use the right tools correctly?"
   - Higher is better

---

## 🎬 Sample Demo Narrative

### Opening (30 seconds)
"Today I'll show you how we've automated agent quality assurance using Azure AI and GitHub Actions. Every time a developer makes changes to our AI agents, the system automatically evaluates quality and compares against our baseline."

### Trigger Demo (1 minute)
"Let me create a sample PR..." [Create PR with new test query]
"Watch how the workflow automatically triggers and starts evaluating both agents..."

### Show Results (2 minutes)
"Here's the GitHub Actions tab - notice the clear step names with emojis making it easy to follow..."
"Now the evaluation is complete. Look at the summary - we can see at a glance that the V2 agent has [X] improvements and [Y] regressions..."
"Each metric has a color indicator - green for better, red for worse, yellow for no change..."

### Highlight Value (1 minute)
"This means developers get immediate feedback on quality impact. No more guessing, no more manual testing. They can confidently merge or iterate based on real metrics."

### Close (30 seconds)
"The entire process is automated, secure with federated auth, and provides full audit trails with artifacts. Would you like to see how we customize the evaluators or dive deeper into any specific metrics?"

---

## 📁 Additional Resources

- **Workflow File**: `.github/workflows/agent-eval-on-pr.yml`
- **Test Data**: `data/agent-eval-data.json`
- **Local Script**: `scripts/local_agent_eval.py`
- **Architecture**: `ARCHITECTURE.md`
- **Setup Guide**: `SETUP-GUIDE.md`
- **Quick Reference**: `QUICK_REFERENCE.md`

---

## 🚀 Quick Start Demo Script

```powershell
# 1. Pull latest
git checkout main && git pull

# 2. Create demo branch
git checkout -b demo/customer-showcase

# 3. Add a test query
code data/agent-eval-data.json
# Add: {"query": "Demo query for customer"}

# 4. Commit and push
git add data/agent-eval-data.json
git commit -m "demo: Showcase agent evaluation workflow"
git push -u origin demo/customer-showcase

# 5. Create PR
gh pr create --title "Demo: Agent Quality Evaluation" \
  --body "Demonstrating automated agent evaluation with baseline comparison"

# 6. Watch workflow
gh run watch

# 7. Open PR in browser
gh pr view --web

# 8. Clean up after demo
gh pr close --delete-branch
```

---

## 📝 Demo Checklist

Before the demo:
- [ ] Verify all GitHub variables are set (`gh variable list`)
- [ ] Check recent runs are successful (`gh run list`)
- [ ] Prepare test query to add
- [ ] Have browser ready with GitHub repo
- [ ] Test federated auth is working
- [ ] Review latest metrics to reference

During the demo:
- [ ] Explain the problem and solution
- [ ] Create PR and trigger workflow
- [ ] Show GitHub Actions tab with emoji steps
- [ ] Highlight comparison table in summary
- [ ] Point out PR comment integration
- [ ] Emphasize clear status indicators
- [ ] Explain merge decision process

After the demo:
- [ ] Answer questions
- [ ] Share repository access if needed
- [ ] Provide documentation links
- [ ] Clean up demo PR (optional)

---

**Version:** 1.0.0-dual-agent-eval  
**Last Updated:** October 22, 2025  
**Tag:** `v1.0.0-dual-agent-eval`

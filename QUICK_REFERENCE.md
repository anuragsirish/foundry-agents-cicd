# 🚀 Quick Reference: Comprehensive Agent Evaluation Pipeline

## For Developers

### Making Changes and Testing

```bash
# 1. Create feature branch
git checkout -b feature/improve-agent-responses

# 2. Make your changes to agent code or test queries

# 3. (Optional) Test locally - run one or all evaluations
export AGENT_ID_BASELINE="asst_xxxxx"
export AZURE_AI_PROJECT_ENDPOINT="https://..."
export AZURE_DEPLOYMENT_NAME="gpt-4.1"

# Quality evaluation (8 metrics)
python scripts/local_quality_eval.py

# Safety evaluation (4 risk categories)
python scripts/local_safety_eval.py

# Red team testing (10+ scenarios)
python scripts/local_redteam_eval.py

# 4. Commit and push
git add .
git commit -m "Improve agent response quality"
git push origin feature/improve-agent-responses

# 5. Create PR
gh pr create --title "Improve agent responses" --body "Details..."

# 6. Workflow automatically:
#    - Evaluates baseline agent (quality + safety + red team)
#    - Evaluates V2 agent (quality + safety + red team)
#    - Compares results across all three tiers
#    - Posts comprehensive comparison to PR
#    - Always passes (you decide on merge)

# 7. Review comparison and merge
```

### Understanding Comparison Results

#### Quality Metrics (8 evaluators)
```
| Relevance | 4.20 | 4.50 | +7% |
```
**Meaning:** Shows percentage change in quality scores (1-5 scale)

#### Safety Evaluation (4 risk categories)
```
| Violence | 0 | 0 | 0% |
| Hate/Unfairness | 1 | 0 | -100% |
```
**Meaning:** Defect counts and percentage change
**Good:** Negative percentages mean fewer defects in V2

#### Red Team Testing (10+ scenarios per category)
```
Attack Strategy Breakdown:
| ROT13     | 2 | 1 | -50%  |
| Leetspeak | 3 | 1 | -67%  |
```
**Meaning:** Shows which specific attacks were tested and vulnerability counts
**Good:** Negative percentages mean better resilience in V2

### Common Scenarios

#### "V2 has regressions but I want to merge anyway"
**Answer:** That's OK! The workflow always passes. You decide based on:
- Is the regression acceptable for the new feature?
- Does it improve other more important metrics?
- Is it a known trade-off?

Document your reasoning in the PR description.
3. Test locally: `python scripts/local_quality_eval.py` (or safety/redteam versions)
4. Consider reverting problematic changes
5. If degradation is intentional, document in PR description

#### "Evaluation is taking too long"
- Normal runtime: 3-10 minutes
- If >15 minutes, check Azure service health
- Workflow times out after 30 minutes

#### "I need to bypass the quality gate"
- Add label `skip-quality-gate` to PR (if configured)
- **Must** document reasoning in PR
- Requires approval from 2 reviewers (recommended)

#### "I want to test without creating a PR"
```bash
# Run locally
python scripts/local_agent_eval.py

# Or trigger manually in GitHub Actions
# Go to Actions → "Agent Evaluation on Pull Request" → Run workflow
```

## For Reviewers

### Review Checklist

- [ ] Code changes are well-documented
- [ ] Evaluation passed or degradation explained
- [ ] No unexpected metric changes
- [ ] Performance metrics acceptable
- [ ] Test data still relevant

### Reading Evaluation Results

**Quality Metrics (0-5 scale):**
- **Relevance**: Answers match the question
- **Coherence**: Responses flow logically
- **Fluency**: Natural language quality
- **Groundedness**: Based on provided context
- **Tool Call Accuracy**: Correct tool usage
- **Intent Resolution**: User intent understood
- **Task Adherence**: Follows instructions

**Performance Metrics:**
- **Response Time**: Lower is better
- **Token Usage**: Watch for cost increases

### When to Approve

✅ **Safe to merge:**
- All metrics green/yellow (within ±5%)
- No unexpected behavior
- Code quality good

⚠️ **Needs discussion:**
- Red metrics without explanation
- Large performance changes
- New failure patterns

❌ **Should not merge:**
- Multiple metrics degraded
- No explanation provided
- Tests failing

## For Admins

### Initial Setup

```bash
# 1. Set up GitHub repository variables (see CICD_PIPELINE.md)

# 2. Configure Azure federated credentials

# 3. Run first evaluation locally
python scripts/local_agent_eval.py

# 4. Initialize baseline
python scripts/initialize_baseline.py

# 5. Commit baseline
git add evaluation_results/baseline/
git commit -m "Initialize baseline metrics"
git push origin main
```

### Updating Quality Thresholds

Edit `.github/workflows/agent-eval-on-pr.yml`:

```python
# Line ~155 - Change threshold from 5% to your value
if comparison[metric]['diff_pct'] < -10:  # 10% degradation allowed
    failed_metrics.append(metric)
```

### Viewing Historical Data

```bash
# Baseline history
git log --follow evaluation_results/baseline/baseline_metrics.json

# PR evaluation artifacts (in GitHub Actions)
# Actions → Workflow run → Artifacts → Download
```

### Monitoring

**Weekly:**
- Review baseline trend
- Check evaluation success rate
- Monitor performance metrics

**Monthly:**
- Update test data if needed
- Review quality thresholds
- Check cost/token usage trends

### Troubleshooting

**Workflow not triggering:**
```bash
# Check workflow paths match changed files
git diff --name-only origin/main
```

**Authentication failures:**
```bash
# Verify federated credentials in Azure Portal
# Check repository variables are set correctly
```

**Inconsistent results:**
```bash
# Evaluator models can have variance
# Run multiple times to confirm pattern
# Consider using temperature=0 for evaluators
```

## Environment Variables Reference

### Local Development (.env)
```bash
# Required for all evaluations
AZURE_AI_PROJECT_ENDPOINT=https://...
AZURE_DEPLOYMENT_NAME=gpt-4o
AGENT_ID_BASELINE=asst_xxxxx
AZURE_OPENAI_ENDPOINT=https://...
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Red team testing specific
RED_TEAM_MAX_SCENARIOS=10  # Number of scenarios per risk category
```

### GitHub Actions (Repository Variables)
```
# Authentication
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID

# Agent configuration
AGENT_ID_BASELINE
AGENT_ID_V2
AGENT_ID_STAGING (for staging environment)
AGENT_ID_PRODUCTION (for production environment)

# Azure AI configuration
AZURE_AI_PROJECT_ENDPOINT
AZURE_DEPLOYMENT_NAME
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_DEPLOYMENT_NAME
API_VERSION
```

## Evaluation Metrics

### Quality Metrics (1-5 scale)
- Relevance
- Coherence
- Fluency
- Groundedness
- Similarity
- Intent Resolution
- Task Adherence
- Tool Call Accuracy (0-1 scale)

### Safety Categories (Severity 0-7)
- Violence
- Sexual
- Self Harm
- Hate/Unfairness
- Threshold: Severity ≥3 is considered a defect

### Red Team Attack Strategies
- EASY, MODERATE (difficulty levels)
- CharacterSpace, ROT13, Leetspeak (encoding)
- CharSwap, UnicodeConfusable, Flip (character manipulation)
- Base64+ROT13, Base64, Morse, Tense (transformation)

## Related Documentation

- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)**: Dev → Staging → Production process
- **[CICD_PIPELINE.md](./CICD_PIPELINE.md)**: Pipeline implementation details
- **[SETUP-GUIDE.md](./SETUP-GUIDE.md)**: Azure and GitHub setup
- **[ARCHITECTURE.md](./ARCHITECTURE.md)**: System architecture
- **[README.md](./README.md)**: Project overview

## Support

- **Issues**: GitHub Issues tab
- **Logs**: GitHub Actions → Workflow runs
- **Azure Portal**: [AI Foundry](https://ai.azure.com)

---
Last Updated: January 2025

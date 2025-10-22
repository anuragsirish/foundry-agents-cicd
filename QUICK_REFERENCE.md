# 🚀 Quick Reference: CI/CD Pipeline

## For Developers

### Making Changes with Agent Code

```bash
# 1. Create feature branch
git checkout -b feature/improve-agent-responses

# 2. Make your changes to agent code

# 3. (Optional) Test locally
python scripts/local_agent_eval.py

# 4. Commit and push
git add .
git commit -m "Improve agent response quality"
git push origin feature/improve-agent-responses

# 5. Create PR
gh pr create --title "Improve agent responses" --body "Details..."

# 6. Check PR for evaluation results (appears as comment)
# 7. If quality gate passes, get review and merge
```

### Understanding PR Comments

#### ✅ Passing Evaluation
```
🟢 Relevance +2.5%      # Improvement
🟡 Coherence +0.5%      # Small change (acceptable)
```
**Action:** Review code, merge when approved

#### ⚠️ Failing Evaluation
```
🔴 Relevance -7.2%      # Quality degraded >5%
```
**Action:** 
- Investigate why quality dropped
- Fix the issue
- Or document why degradation is acceptable

### Common Scenarios

#### "My PR failed the quality gate"
1. Check which metrics degraded (look for 🔴 in PR comment)
2. Review your changes - did you modify prompts/instructions?
3. Test locally: `python scripts/local_agent_eval.py`
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
AZURE_AI_PROJECT_ENDPOINT=https://...
AZURE_DEPLOYMENT_NAME=gpt-4o
AGENT_ID_BASELINE=asst_xxxxx
AZURE_OPENAI_ENDPOINT=https://...
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
```

### GitHub Actions (Repository Variables)
```
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
AZURE_AI_PROJECT_ENDPOINT
AZURE_DEPLOYMENT_NAME
AGENT_ID_BASELINE
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_DEPLOYMENT_NAME
API_VERSION
```

## Metrics Thresholds

| Metric | Threshold | Impact |
|--------|-----------|--------|
| Quality metrics | -5% | Blocks PR |
| Performance | No limit | Warning only |
| Token usage | No limit | Monitor costs |

## Support

- **Documentation**: [CICD_PIPELINE.md](./CICD_PIPELINE.md)
- **Setup**: [SETUP-GUIDE.md](./SETUP-GUIDE.md)
- **Issues**: GitHub Issues tab
- **Logs**: GitHub Actions → Workflow runs

---
Last Updated: January 2025

# ✅ CI/CD Pipeline Setup Checklist

Use this checklist to ensure your CI/CD pipeline is properly configured.

## Pre-requisites

- [ ] Azure AI Foundry project created
- [ ] AI agent deployed and tested
- [ ] Evaluation model deployed (e.g., GPT-4o)
- [ ] GitHub repository set up
- [ ] Python 3.9+ installed locally

## 1. Azure Configuration

### Service Principal Setup
- [ ] Create Azure AD app registration
- [ ] Note down Client ID
- [ ] Note down Tenant ID
- [ ] Note down Subscription ID
- [ ] Assign necessary roles to service principal
  - [ ] Azure AI Developer role
  - [ ] Cognitive Services User role

### Federated Credentials
- [ ] Add federated credential for `pull_request`
  - Subject: `repo:<org>/<repo>:pull_request`
- [ ] Add federated credential for main branch
  - Subject: `repo:<org>/<repo>:ref:refs/heads/main`

### Resource Information
- [ ] Copy AI Project endpoint URL
- [ ] Note model deployment name
- [ ] Note agent ID
- [ ] Copy OpenAI endpoint (for evaluators)
- [ ] Note evaluator deployment name

## 2. GitHub Configuration

### Repository Variables (Settings → Secrets and variables → Actions → Variables)
- [ ] `AZURE_CLIENT_ID` = your-client-id
- [ ] `AZURE_TENANT_ID` = your-tenant-id
- [ ] `AZURE_SUBSCRIPTION_ID` = your-subscription-id
- [ ] `AZURE_AI_PROJECT_ENDPOINT` = https://...
- [ ] `AZURE_DEPLOYMENT_NAME` = gpt-4o
- [ ] `AGENT_ID_BASELINE` = asst_xxxxx
- [ ] `AZURE_OPENAI_ENDPOINT` = https://...
- [ ] `AZURE_OPENAI_DEPLOYMENT_NAME` = gpt-4o
- [ ] `AZURE_OPENAI_API_VERSION` = 2024-02-15-preview
- [ ] `API_VERSION` = 2024-08-01-preview

### Repository Secrets (if using API key)
- [ ] `AZURE_OPENAI_API_KEY` = your-api-key (optional)

### Workflow Permissions
- [ ] Settings → Actions → General → Workflow permissions
  - [ ] Select "Read and write permissions"
  - [ ] Check "Allow GitHub Actions to create and approve pull requests"

## 3. Local Setup

### Environment File
- [ ] Copy `.env` file from template
- [ ] Fill in all required variables in `.env`:
  ```bash
  AZURE_AI_PROJECT_ENDPOINT=
  AZURE_DEPLOYMENT_NAME=
  AGENT_ID_BASELINE=
  AZURE_OPENAI_ENDPOINT=
  AZURE_OPENAI_DEPLOYMENT_NAME=
  ```

### Dependencies
- [ ] Install Python dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Test Locally
- [ ] Run local evaluation:
  ```bash
  python scripts/local_agent_eval.py
  ```
- [ ] Verify results saved to `evaluation_results/agent_eval_output/`
- [ ] Check metrics look reasonable

## 4. Baseline Initialization

### Option A: Initialize from Local Run
- [ ] Run evaluation locally (see above)
- [ ] Run baseline initialization:
  ```bash
  python scripts/initialize_baseline.py
  ```
- [ ] Review baseline metrics in output
- [ ] Commit baseline to repository:
  ```bash
  git add evaluation_results/baseline/
  git commit -m "Initialize baseline metrics"
  git push origin main
  ```

### Option B: Let First PR Create Baseline
- [ ] Skip to testing (baseline will be created automatically)

## 5. Workflow Files

### Verify Files Exist
- [ ] `.github/workflows/agent-eval-on-pr.yml`
- [ ] `.github/workflows/update-baseline.yml`

### Review Workflow Configuration
- [ ] Check trigger paths match your repo structure
- [ ] Verify quality threshold (default: 5%)
- [ ] Confirm Python version (default: 3.11)

## 6. Testing

### Create Test PR
- [ ] Create test branch:
  ```bash
  git checkout -b test-cicd-pipeline
  ```
- [ ] Make a small change:
  ```bash
  echo "# CI/CD Test" >> README.md
  git add README.md
  git commit -m "Test: CI/CD pipeline"
  git push origin test-cicd-pipeline
  ```
- [ ] Create PR via GitHub UI or CLI:
  ```bash
  gh pr create --title "Test CI/CD Pipeline" --body "Testing automated evaluations"
  ```

### Verify Workflow Execution
- [ ] Go to Actions tab in GitHub
- [ ] Find "Agent Evaluation on Pull Request" workflow
- [ ] Workflow should be running or completed
- [ ] Check workflow logs for any errors

### Check PR Comment
- [ ] PR should have comment from github-actions bot
- [ ] Comment shows "🤖 Agent Evaluation Results"
- [ ] If baseline exists: Comparison table shown
- [ ] If no baseline: "First evaluation run" message shown
- [ ] Metrics are populated (not all zeros)

### Review Results
- [ ] Metrics look reasonable (0-5 scale for quality)
- [ ] Performance metrics populated
- [ ] Run ID and Agent ID shown
- [ ] No error messages

## 7. Merge Test PR

### After Successful Test
- [ ] Approve test PR
- [ ] Merge to main
- [ ] Verify baseline update workflow triggers
- [ ] Check new commit appears with baseline update
- [ ] Verify `evaluation_results/baseline/baseline_metrics.json` updated

## 8. Second PR Test (With Baseline)

### Create Another Test PR
- [ ] Create new branch and make change
- [ ] Push and create PR
- [ ] Verify comparison with baseline works
- [ ] Check color-coded metrics (🟢🟡🔴)
- [ ] Verify quality gate logic

## 9. Documentation Review

### Team Documentation
- [ ] Share [CICD_PIPELINE.md](./CICD_PIPELINE.md) with team
- [ ] Share [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) with developers
- [ ] Add links to team wiki/docs

### Update README
- [ ] Update main README.md with CI/CD info
- [ ] Add badge for workflow status (optional)

## 10. Monitoring Setup

### Initial Monitoring
- [ ] Set up alerts for workflow failures
- [ ] Add team members as code owners
- [ ] Set up notifications for PR comments

### Regular Reviews
- [ ] Schedule weekly metric review
- [ ] Set monthly baseline review
- [ ] Track token usage and costs

## 11. Optional Enhancements

### Advanced Features
- [ ] Add Slack/Teams notifications
- [ ] Set up cost tracking
- [ ] Add performance benchmarks
- [ ] Create trend analysis dashboard
- [ ] Add custom evaluator metrics

### Process Improvements
- [ ] Add skip-quality-gate label
- [ ] Require 2 reviewers for degraded PRs
- [ ] Create runbook for quality failures
- [ ] Set up on-call rotation

## 12. Troubleshooting Checklist

If workflows fail, check:

### Authentication Issues
- [ ] Federated credentials configured correctly
- [ ] Service principal has correct roles
- [ ] GitHub variables set correctly
- [ ] Token hasn't expired

### Evaluation Issues
- [ ] Agent ID is correct
- [ ] Model deployment exists and accessible
- [ ] Test data format is valid
- [ ] Evaluator model deployment working

### Workflow Issues
- [ ] Workflow file syntax is valid
- [ ] Python dependencies install successfully
- [ ] File paths are correct
- [ ] Permissions configured correctly

### PR Comment Issues
- [ ] Workflow has `pull-requests: write` permission
- [ ] GITHUB_TOKEN is valid
- [ ] Repository allows Actions to comment
- [ ] PR is not from fork (if applicable)

## Success Criteria

✅ All items above checked
✅ Test PR workflow completed successfully
✅ PR comment appeared with results
✅ Baseline created/updated after merge
✅ Second PR compared against baseline
✅ Team members trained on workflow
✅ Documentation accessible to team

## Next Steps After Setup

1. **Monitor**: Watch first few PRs closely
2. **Iterate**: Adjust thresholds as needed
3. **Communicate**: Keep team informed of changes
4. **Maintain**: Review baselines regularly
5. **Improve**: Add enhancements based on feedback

## Support Resources

- **Setup Guide**: [CICD_PIPELINE.md](./CICD_PIPELINE.md)
- **Quick Reference**: [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
- **Architecture**: [ARCHITECTURE.md](./ARCHITECTURE.md)
- **Troubleshooting**: See CICD_PIPELINE.md
- **GitHub Issues**: Report problems/suggestions

---

**Print this checklist and mark items as you complete them!**

Last Updated: January 2025

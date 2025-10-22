---
name: Evaluation Quality Gate Failure
about: Report when PR evaluation fails quality gate
title: '[EVAL-FAIL] '
labels: evaluation, quality-gate
assignees: ''
---

## 🔴 Evaluation Quality Gate Failure

**PR Number:** #XXX
**Run ID:** `pr-XXX-YYYYMMDD-HHMMSS`
**Date:** YYYY-MM-DD

## Failed Metrics

List the metrics that failed (degraded >5%):

- [ ] Relevance (-X.X%)
- [ ] Coherence (-X.X%)
- [ ] Fluency (-X.X%)
- [ ] Groundedness (-X.X%)
- [ ] Tool Call Accuracy (-X.X%)
- [ ] Intent Resolution (-X.X%)
- [ ] Task Adherence (-X.X%)

## Context

**What changes were made?**
<!-- Describe the code/prompt/config changes -->

**Why did quality degrade?**
<!-- Your analysis of the root cause -->

## Investigation

- [ ] Reviewed evaluation results in PR comment
- [ ] Ran evaluation locally to reproduce
- [ ] Checked specific test cases that failed
- [ ] Reviewed changes to prompts/instructions
- [ ] Compared with baseline results

## Options

**Choose one:**

### Option 1: Fix the Issue ✅
<!-- Describe how you'll improve quality -->

### Option 2: Acceptable Trade-off ⚖️
<!-- Explain why degradation is acceptable (e.g., performance improvement, new feature) -->

### Option 3: Update Baseline 📊
<!-- Explain why baseline should be updated (e.g., test data changed, expected behavior changed) -->

## Next Steps

- [ ] Make necessary changes
- [ ] Test locally
- [ ] Update PR
- [ ] Document decision in PR description

## Additional Information

**Artifacts:** [Link to GitHub Actions artifacts]

**Evaluation Output:**
```
Paste relevant parts of evaluation output here
```

## Reviewer Notes

<!-- For reviewers: document decision and reasoning -->

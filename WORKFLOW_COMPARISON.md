# Workflow Implementation Comparison

## Overview

We've implemented **two approaches** for running agent evaluations in CI/CD:

1. **Custom Python Script Approach** (`agent-eval-on-pr.yml`) - Full control, custom comparison logic
2. **Official Azure Action Approach** (`agent-eval-on-pr-official.yml`) - Follows Azure documentation, built-in features

## Comparison Matrix

| Feature | Custom Script Approach | Official Action Approach |
|---------|----------------------|-------------------------|
| **Follows Azure Docs** | ⚠️ Partial | ✅ Yes (uses `microsoft/ai-agent-evals@v2-beta`) |
| **Custom Baseline Logic** | ✅ Full control | ⚠️ Limited (uses built-in multi-agent comparison) |
| **PR Comment Customization** | ✅ Fully customizable tables | ⚠️ Basic comment + link to summary |
| **Quality Gate Control** | ✅ Custom thresholds (5%) | ❌ No built-in quality gate |
| **Metric Comparison** | ✅ Custom % change calculation | ✅ Statistical significance (built-in) |
| **Baseline Storage** | ✅ Git-based (committed to repo) | ⚠️ Requires Azure storage or manual process |
| **Setup Complexity** | ⚠️ More complex | ✅ Simpler |
| **Maintenance** | ⚠️ We maintain script | ✅ Microsoft maintains action |
| **Cost** | Same | Same |
| **Results Location** | PR comment + artifacts | GitHub Actions summary + Azure portal |

## Detailed Comparison

### 1. Official Azure Action Approach (Recommended by Microsoft)

**File:** `.github/workflows/agent-eval-on-pr-official.yml`

#### ✅ Pros
- **Official support** - Maintained by Microsoft
- **Simpler setup** - Less code to maintain
- **Built-in features** - Statistical comparison, confidence intervals
- **Direct integration** - Outputs to GitHub Actions summary
- **Future updates** - Will get new features automatically

#### ❌ Cons
- **Limited customization** - Can't customize PR comments as easily
- **No built-in quality gates** - Doesn't automatically fail PRs
- **Multi-agent required for comparison** - Need to pass both baseline and variant IDs
- **Less granular control** - Can't customize threshold percentages

#### How It Works
```yaml
- name: Run AI Agent Evaluation
  uses: microsoft/ai-agent-evals@v2-beta
  with:
    azure-ai-project-endpoint: ${{ vars.AZURE_AI_PROJECT_ENDPOINT }}
    deployment-name: ${{ vars.AZURE_DEPLOYMENT_NAME }}
    agent-ids: "baseline-id,variant-id"  # For comparison
    data-path: ${{ github.workspace }}/data/agent-eval-data.json
    evaluation-result-view: 'all-scores'
```

**Baseline Comparison:** Must include both agent IDs (baseline first) in a single evaluation run. The action performs statistical comparison automatically.

### 2. Custom Python Script Approach (What We Built)

**File:** `.github/workflows/agent-eval-on-pr.yml`

#### ✅ Pros
- **Full control** - Complete customization of comparison logic
- **Quality gates** - Automatic PR blocking if quality degrades >5%
- **Rich PR comments** - Beautiful tables with color-coded metrics
- **Git-based baseline** - Baseline committed to repo, full history
- **Flexible thresholds** - Easy to adjust quality gate percentages
- **Standalone evaluation** - Only evaluates PR agent, not baseline

#### ❌ Cons
- **Custom maintenance** - We maintain the evaluation script
- **Not officially documented** - Doesn't follow Azure's recommended pattern
- **More complex** - More moving parts to manage
- **Manual updates** - Need to update SDK versions ourselves

#### How It Works
```yaml
# Custom approach using local_agent_eval.py
- name: Run Agent Evaluation
  run: python scripts/local_agent_eval.py

- name: Compare with Baseline
  run: |
    # Custom Python logic to calculate % changes
    # Determines pass/fail based on 5% threshold
```

**Baseline Comparison:** Fetches baseline from git, runs evaluation only on PR agent, calculates differences with custom logic.

## Which One to Use?

### Use **Official Action** if:
- ✅ You want Microsoft-supported solution
- ✅ You prefer simpler setup and maintenance
- ✅ Built-in statistical comparison is sufficient
- ✅ You can adapt your workflow to multi-agent evaluation
- ✅ You don't need strict quality gates

### Use **Custom Script** if:
- ✅ You need fine-grained quality gate control
- ✅ You want rich, customizable PR comments
- ✅ You prefer git-based baseline management
- ✅ You want to evaluate only the PR agent (not re-evaluate baseline)
- ✅ You need custom threshold percentages
- ✅ You want to block PRs automatically

## Hybrid Approach (Recommended)

You can combine both approaches:

1. **Use Official Action for evaluation**
   - Leverage Microsoft's maintained action
   - Get built-in statistical analysis
   - Ensure compatibility with future updates

2. **Add Custom Quality Gate Logic**
   - Parse the official action's output
   - Apply your custom threshold rules
   - Generate rich PR comments
   - Block PRs if needed

### Example Hybrid Workflow

```yaml
- name: Run AI Agent Evaluation (Official)
  id: eval
  uses: microsoft/ai-agent-evals@v2-beta
  with:
    azure-ai-project-endpoint: ${{ vars.AZURE_AI_PROJECT_ENDPOINT }}
    deployment-name: ${{ vars.AZURE_DEPLOYMENT_NAME }}
    agent-ids: ${{ vars.AGENT_ID_BASELINE }}
    data-path: ${{ github.workspace }}/data/agent-eval-data.json

- name: Custom Quality Gate (Our Logic)
  run: |
    # Parse results from official action
    # Apply custom threshold rules
    # Generate rich PR comment
    # Fail if quality degraded >5%
```

## Azure Documentation Alignment

### What Azure Recommends ✅
From `azure-ai-github-eval.md`:

```yaml
- name: Run Evaluation
  uses: microsoft/ai-agent-evals@v2-beta
  with:
    azure-ai-project-endpoint: "<your-endpoint>"
    deployment-name: "<your-deployment>"
    agent-ids: "<agent-ids>"
    data-path: ${{ github.workspace }}/path/to/data
```

**Our Official Action workflow follows this exactly!**

### What We Added (Custom Approach) ⚡

We extended beyond the documentation to provide:
- Automatic baseline detection and storage
- Quality gate enforcement (block PRs)
- Rich PR comments with comparison tables
- Customizable thresholds
- Git-based baseline history

## Migration Path

If you want to switch from custom to official action:

### Step 1: Use Official Action
```bash
# Rename current workflow
mv .github/workflows/agent-eval-on-pr.yml \
   .github/workflows/agent-eval-on-pr-custom.yml

# Use official action workflow
mv .github/workflows/agent-eval-on-pr-official.yml \
   .github/workflows/agent-eval-on-pr.yml
```

### Step 2: Adapt Baseline Comparison
For baseline comparison with official action, you need:
1. Both agent IDs (baseline and PR variant)
2. Multi-agent evaluation in single run
3. Official action handles statistical comparison

### Step 3: Custom Quality Gate (Optional)
Add a step after official action to:
- Parse output from GitHub Actions summary
- Apply custom threshold rules
- Block PR if needed

## Recommendation

For your use case, I recommend:

### **Option 1: Keep Custom Script (Current)**
**Why:**
- ✅ You already have full control
- ✅ Quality gates work perfectly
- ✅ Rich PR comments provide great UX
- ✅ Git-based baseline is simple and effective
- ✅ Single agent evaluation is cleaner

**Trade-off:**
- ⚠️ Slightly more maintenance
- ⚠️ Not the "official" pattern

### **Option 2: Hybrid Approach**
**Why:**
- ✅ Best of both worlds
- ✅ Use official action for evaluation
- ✅ Add custom quality gate layer
- ✅ Future-proof with Microsoft updates

**Trade-off:**
- ⚠️ More complex initially
- ⚠️ Need to parse action output

### **Option 3: Pure Official Action**
**Why:**
- ✅ Follows Azure docs exactly
- ✅ Simplest to maintain
- ✅ Microsoft support

**Trade-off:**
- ❌ Lose quality gate enforcement
- ❌ Less rich PR comments
- ⚠️ Need to adapt baseline logic

## Conclusion

**Both approaches are valid:**

- **Custom script** = More features, more control, more maintenance
- **Official action** = Microsoft-supported, simpler, less customization

The custom script we built goes **beyond** what Azure documents, providing enterprise-grade quality gates and comparison logic. It's not "wrong" - it's an enhancement!

If you want to strictly follow Azure documentation, use the official action. But the custom approach provides significant value-adds that may justify the maintenance overhead.

**My recommendation:** Stick with the custom approach for now, but be prepared to adopt the official action when Microsoft adds quality gate features.

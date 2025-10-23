# Dual-Agent Evaluation Architecture

## Overview

This architecture implements **automated dual-agent evaluation** for AI agent quality assurance. On every pull request, the system evaluates both a baseline agent and a V2 agent, compares their performance across multiple quality metrics, and presents the results for manual review.

### Key Principles

1. **Always Pass** - Workflow never fails automatically; developers decide based on metrics
2. **Dual Evaluation** - Both baseline and V2 agents evaluated independently
3. **Clear Indicators** - 🟢 improvements, 🔴 regressions, 🟡 neutral changes
4. **Full Transparency** - All results available in PR comments, Actions summary, and artifacts
5. **Secure by Default** - Uses Azure federated credentials (OIDC), no secrets in code

### Agents

| Agent | Description | Variable |
|-------|-------------|----------|
| **Baseline** | Current production or reference agent | `AGENT_ID_BASELINE` |
| **V2** | New or experimental agent being tested | `AGENT_ID_V2` |

## High-Level Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DUAL-AGENT EVALUATION WORKFLOW                    │
└─────────────────────────────────────────────────────────────────────┘

    Developer                 GitHub                    Azure AI
        │                        │                          │
        │  1. Create PR          │                          │
        ├───────────────────────>│                          │
        │                        │                          │
        │                        │  2. Trigger Workflow     │
        │                        │     (agent-eval-on-pr)   │
        │                        │                          │
        │                        │  3. Checkout code        │
        │                        │                          │
        │                        │  4. Authenticate Azure   │
        │                        │     (OIDC/Federated)     │
        │                        │                          │
        │                        │  5. Evaluate Baseline    │
        │                        ├─────────────────────────>│
        │                        │     (AGENT_ID_BASELINE)  │
        │                        │                          │  6. Execute baseline
        │                        │                          │     with test queries
        │                        │  7. Baseline results     │
        │                        │<─────────────────────────┤
        │                        │                          │
        │                        │  8. Evaluate V2 Agent    │
        │                        ├─────────────────────────>│
        │                        │     (AGENT_ID_V2)        │
        │                        │                          │  9. Execute V2
        │                        │                          │     with test queries
        │                        │  10. V2 results          │
        │                        │<─────────────────────────┤
        │                        │                          │
        │                        │  11. Compare metrics     │
        │                        │      (baseline vs V2)    │
        │                        │                          │
        │                        │  12. Generate outputs:   │
        │                        │      • PR comment        │
        │                        │      • Actions summary   │
        │                        │      • Artifacts         │
        │                        │                          │
        │  13. View results      │                          │
        │<───────────────────────┤                          │
        │     (Always ✅ PASS)   │                          │
        │                        │                          │
        │  14. Review & Merge    │                          │
        │     (Manual decision)  │                          │
        ├───────────────────────>│                          │
        │                        │                          │
        ▼                        ▼                          ▼


┌─────────────────────────────────────────────────────────────────────┐
│                      BASELINE INITIALIZATION                         │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│ First Run        │
│ (No baseline)    │
└────────┬─────────┘
         │
         ├─> PR Workflow runs
         │   └─> Detects: baseline_exists=false
         │       └─> Shows "First evaluation run" message
         │
         ├─> PR merged to main
         │   └─> update-baseline.yml triggers
         │       └─> Runs evaluation
         │           └─> Creates baseline_metrics.json
         │               └─> Commits to repository
         │
         └─> Future PRs
             └─> Compare against baseline


┌─────────────────────────────────────────────────────────────────────┐
│                     COMPARISON & DECISION FLOW                       │
└─────────────────────────────────────────────────────────────────────┘

            Evaluate Baseline Agent
                      │
                      ▼
            Evaluate V2 Agent
                      │
                      ▼
            ┌──────────────────────┐
            │ Compare Metrics      │
            │ (Baseline vs V2)     │
            └──────────┬───────────┘
                       │
                       ├─────────────────┬─────────────────┐
                       ▼                 ▼                 ▼
                 🟢 Improved        🟡 Neutral       🔴 Regressed
                 (V2 > Baseline)    (Similar)        (V2 < Baseline)
                       │                 │                 │
                       └────────┬────────┴─────────────────┘
                                ▼
                      ┌──────────────────┐
                      │ Quality Metrics: │
                      │ • Relevance      │
                      │ • Coherence      │
                      │ • Fluency        │
                      │ • Groundedness   │
                      │ • Tool Call Acc. │
                      └────────┬─────────┘
                               │
                               ▼
                      ┌──────────────────┐
                      │ Generate Outputs │
                      │ • PR comment     │
                      │ • Actions summary│
                      │ • Artifacts      │
                      └────────┬─────────┘
                               │
                               ▼
                      ✅ Workflow PASSES
                      (Always succeeds)
                               │
                               ▼
                      Manual merge decision
                      (Developer reviews metrics)


┌─────────────────────────────────────────────────────────────────────┐
│                      FILE STRUCTURE & FLOW                           │
└─────────────────────────────────────────────────────────────────────┘

Repository Root
│
├── .github/workflows/
│   ├── agent-eval-on-pr.yml ──────┐  🤖 ACTIVE (Dual-agent evaluation)
│   │   │                           │
│   │   ├─> Triggers on PR          │
│   │   ├─> Evaluates baseline ─────┼─> evaluation_results/baseline/
│   │   ├─> Evaluates V2 agent ─────┼─> evaluation_results/v2/
│   │   ├─> Compares metrics        │
│   │   ├─> Posts PR comment        │
│   │   ├─> GitHub Actions summary  │
│   │   ├─> Uploads artifacts       │
│   │   └─> Always passes ✅        │
│   │                                │
│   └── agent-eval-on-pr-official.yml  ❌ DISABLED (Microsoft action)
│       │
│       └─> Manual dispatch only
│
├── scripts/
│   ├── local_agent_eval.py
│   │   └─> Used by workflows and local testing
│   │
│   └── initialize_baseline.py
│       └─> One-time setup
│
├── data/
│   └── agent-eval-data.json
│       └─> Test queries (10 samples)
│
├── evaluation_results/
│   ├── baseline/
│   │   └── baseline_results.json       📦 Workflow artifacts
│   │
│   ├── v2/
│   │   └── v2_results.json             📦 Workflow artifacts
│   │
│   └── agent_eval_output/              ❌ Not committed
│       └── eval-output.json            (local runs only)
│
└── .env
    └─> Local development only


┌─────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW DETAILS                            │
└─────────────────────────────────────────────────────────────────────┘

Input                 Processing              Output
─────                 ──────────              ──────

Test Queries          Agent Execution         Conversation Logs
(data/agent-          ─────────────>          (messages array)
eval-data.json)              │
                             │
                             ▼
                      
                      Evaluator Models        Quality Scores
                      (GPT-4o judges)   ─────────────>  (0-5 scale)
                             │
                             │
                             ▼
                      
                      Aggregate Metrics       Average Scores
                      (mean calculation) ─────────────>  per metric
                             │
                             │
                             ▼
                      
Current PR            Baseline Comparison     Comparison Results
Results          <──> Baseline Metrics  ─────────────>  (diff & %)
                             │
                             │
                             ▼
                      
                      Quality Gate Logic      Pass/Fail Decision
                      (check thresholds) ─────────────>  + PR comment


┌─────────────────────────────────────────────────────────────────────┐
│                      METRIC COMPARISON LOGIC                         │
└─────────────────────────────────────────────────────────────────────┘

For each metric:

    baseline_value = 4.20  (from baseline agent)
    v2_value = 4.50        (from V2 agent)
    
    diff = v2_value - baseline_value
         = 4.50 - 4.20
         = +0.30
    
    # Determine status indicator
    if abs(diff) < 0.1:     # Less than 0.1 difference
        status = 🟡           # Neutral (no significant change)
    elif diff > 0:           # Positive difference
        status = 🟢           # Improvement
    else:                    # Negative difference
        status = 🔴           # Regression
    
    # Calculate percentage change (for display)
    if baseline_value > 0:
        pct_change = (diff / baseline_value) × 100
                   = (0.30 / 4.20) × 100
                   = +7.1%
    
    # Note: Workflow always passes regardless of status
        ✅ PASS
        emoji = 🟢
    else:                  # Within ±5%
        ✅ PASS
        emoji = 🟡


┌─────────────────────────────────────────────────────────────────────┐
│                    TIMELINE: TYPICAL PR LIFECYCLE                    │
└─────────────────────────────────────────────────────────────────────┘

T+0:00    Developer creates PR
          │
T+0:05    GitHub triggers workflow
          │
T+0:30    Workflow starts
          ├─ Checkout code (10s)
          ├─ Setup Python (20s)
          ├─ Install deps (30s)
          ├─ Azure login (10s)
          └─ Check baseline (5s)
          │
T+1:45    Run evaluation
          ├─ Initialize client (10s)
          ├─ Execute 10 queries (60s)
          │  └─ ~6s per query
          └─ Run evaluators (120s)
             └─ 8 evaluators × 10 queries
          │
T+3:45    Compare & generate comment (15s)
          │
T+4:00    Post PR comment
          │
T+4:05    Quality gate check (5s)
          │
          └─> ✅ PASS or ❌ FAIL
          │
[Manual]  Code review by team
          │
[Manual]  PR approved & merged
          │
T+0:00    Push to main triggers baseline update
          │
T+4:00    New baseline saved and committed
          │
          └─> Ready for next PR


┌─────────────────────────────────────────────────────────────────────┐
│                         SYSTEM COMPONENTS                            │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│   GitHub Actions │
│                  │
│  Workflows:      │
│  • PR eval       │
│  • Baseline      │
└────────┬─────────┘
         │
         │ Uses
         │
         ▼
┌──────────────────┐
│   Python Script  │
│                  │
│  local_agent_    │
│  eval.py         │
└────────┬─────────┘
         │
         │ Connects to
         │
         ▼
┌──────────────────┐       ┌──────────────────┐
│  Azure AI        │       │  Azure OpenAI    │
│  Project Client  │       │  (Evaluators)    │
│                  │       │                  │
│  • Agent         │◄─────►│  • GPT-4o        │
│  • Threads       │       │  • Judges        │
│  • Messages      │       │                  │
└──────────────────┘       └──────────────────┘
         │
         │ Produces
         │
         ▼
┌──────────────────┐
│   Evaluation     │
│   Results        │
│                  │
│  • Metrics JSON  │
│  • Baseline      │
│  • Comparisons   │
└──────────────────┘
```

## Key Points

1. **Automatic**: Triggers on every PR to main
2. **Smart**: Detects baseline existence
3. **Comprehensive**: 8+ quality metrics evaluated
4. **Transparent**: Results visible in PR comment
5. **Gated**: Blocks PRs if quality degrades >5%
6. **Self-updating**: Baseline updates on merge
7. **Historical**: Full git history of baselines
8. **Flexible**: Thresholds and metrics customizable

## Metrics Evaluated

| Category | Metrics |
|----------|---------|
| **Quality** (Block PRs) | Relevance, Coherence, Fluency, Groundedness, Tool Call Accuracy, Intent Resolution, Task Adherence, Similarity |
| **Performance** (Track only) | Response Time, Completion Tokens, Prompt Tokens |

## Next Steps

1. Review [CICD_PIPELINE.md](./CICD_PIPELINE.md) for setup
2. Configure GitHub variables
3. Initialize baseline
4. Create test PR
5. Monitor results

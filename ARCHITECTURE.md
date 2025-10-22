# CI/CD Pipeline Architecture

## High-Level Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          DEVELOPER WORKFLOW                          │
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
        │                        │  4. Check for baseline   │
        │                        │     (on main branch)     │
        │                        │                          │
        │                        │                          │
        │                        │  5. Run evaluation       │
        │                        ├─────────────────────────>│
        │                        │                          │
        │                        │                          │  6. Execute agent
        │                        │                          │     with test queries
        │                        │                          │
        │                        │  7. Return results       │
        │                        │<─────────────────────────┤
        │                        │                          │
        │                        │  8. Compare with         │
        │                        │     baseline             │
        │                        │                          │
        │                        │  9. Generate PR comment  │
        │                        │                          │
        │  10. View results      │                          │
        │<───────────────────────┤                          │
        │     (PR comment)       │                          │
        │                        │                          │
        │  11. Quality gate      │                          │
        │      ✅ PASS / ❌ FAIL │                          │
        │                        │                          │
        │  12. Merge PR          │                          │
        │     (if approved)      │                          │
        ├───────────────────────>│                          │
        │                        │                          │
        │                        │  13. Trigger baseline    │
        │                        │      update workflow     │
        │                        │                          │
        │                        │  14. Run eval on main    │
        │                        ├─────────────────────────>│
        │                        │                          │
        │                        │  15. Save new baseline   │
        │                        │      to repository       │
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
│                    QUALITY GATE DECISION TREE                        │
└─────────────────────────────────────────────────────────────────────┘

                    Run Evaluation
                          │
                          ▼
                 Calculate Metrics
                          │
                          ▼
              ┌──────────────────────┐
              │ Compare with Baseline│
              └──────────┬───────────┘
                         │
                         ├─────────────────┬─────────────────┐
                         ▼                 ▼                 ▼
                   🟢 Improved        🟡 Stable        🔴 Degraded
                   (> +5%)            (±5%)            (> -5%)
                         │                 │                 │
                         └────────┬────────┴─────────────────┘
                                  ▼
                        ┌──────────────────┐
                        │ Quality Metrics: │
                        │ • Relevance      │
                        │ • Coherence      │
                        │ • Fluency        │
                        │ • Groundedness   │
                        │ • Tool Accuracy  │
                        │ • Intent Res.    │
                        │ • Task Adherence │
                        └────────┬─────────┘
                                 │
                ┌────────────────┴────────────────┐
                ▼                                 ▼
        ✅ ALL metrics                    ❌ ANY metric
        within threshold                  degraded >5%
                │                                 │
                ▼                                 ▼
        Quality Gate PASS              Quality Gate FAIL
                │                                 │
                ▼                                 ▼
        PR can be merged              Workflow exits with error
        (after review)                PR blocked


┌─────────────────────────────────────────────────────────────────────┐
│                      FILE STRUCTURE & FLOW                           │
└─────────────────────────────────────────────────────────────────────┘

Repository Root
│
├── .github/workflows/
│   ├── agent-eval-on-pr.yml ──┐
│   │   │                       │
│   │   ├─> Triggers on PR      │
│   │   ├─> Fetches baseline ───┼─> evaluation_results/baseline/
│   │   ├─> Runs evaluation     │       baseline_metrics.json
│   │   ├─> Compares metrics    │       (committed to repo)
│   │   ├─> Posts PR comment    │
│   │   └─> Quality gate check  │
│   │                            │
│   └── update-baseline.yml ────┤
│       │                        │
│       ├─> Triggers on merge   │
│       ├─> Runs evaluation     │
│       └─> Updates baseline ───┘
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
│   │   ├── baseline_metrics.json      ✅ Committed
│   │   └── baseline_full_results.json ✅ Committed
│   │
│   ├── pr_runs/                        ❌ Not committed
│   │   └── pr-{N}-{timestamp}/         (uploaded as artifacts)
│   │
│   └── agent_eval_output/              ❌ Not committed
│       └── evaluation_results.json     (local runs only)
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

    current_value = 4.85
    baseline_value = 4.75
    
    diff = current - baseline
         = 4.85 - 4.75
         = +0.10
    
    diff_pct = (diff / baseline) × 100
             = (0.10 / 4.75) × 100
             = +2.1%
    
    if diff_pct < -5%:     # Degraded more than 5%
        ❌ FAIL
        emoji = 🔴
    elif diff_pct > +5%:   # Improved more than 5%
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

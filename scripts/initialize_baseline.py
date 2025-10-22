#!/usr/bin/env python3
"""
Initialize Baseline Metrics

This script helps set up the initial baseline metrics for CI/CD evaluation.
Run this locally before setting up PR-based evaluations.

Usage:
    python scripts/initialize_baseline.py
"""

import os
import json
from pathlib import Path
from datetime import datetime

def initialize_baseline():
    """Initialize baseline from existing evaluation results."""
    
    print("="*80)
    print("📊 Initialize Baseline Metrics")
    print("="*80)
    print()
    
    # Paths
    eval_results_path = Path("evaluation_results/agent_eval_output/evaluation_results.json")
    baseline_dir = Path("evaluation_results/baseline")
    baseline_metrics_path = baseline_dir / "baseline_metrics.json"
    baseline_full_path = baseline_dir / "baseline_full_results.json"
    
    # Check if evaluation results exist
    if not eval_results_path.exists():
        print("❌ Error: No evaluation results found!")
        print(f"   Expected file: {eval_results_path}")
        print()
        print("Please run an evaluation first:")
        print("   python scripts/local_agent_eval.py")
        return False
    
    # Create baseline directory
    baseline_dir.mkdir(parents=True, exist_ok=True)
    
    # Read evaluation results
    print(f"📂 Reading evaluation results from: {eval_results_path}")
    with open(eval_results_path, 'r') as f:
        results = json.load(f)
    
    metrics = results.get('metrics', {})
    
    if not metrics:
        print("❌ Error: No metrics found in evaluation results!")
        return False
    
    # Extract key metrics for baseline
    baseline_metrics = {
        'relevance': metrics.get('relevance', 0),
        'coherence': metrics.get('coherence', 0),
        'fluency': metrics.get('fluency', 0),
        'groundedness': metrics.get('groundedness', 0),
        'tool_call_accuracy': metrics.get('tool_call_accuracy', 0),
        'intent_resolution': metrics.get('intent_resolution', 0),
        'task_adherence': metrics.get('task_adherence', 0),
        'similarity': metrics.get('similarity', 0),
        'client_run_duration': metrics.get('client-run-duration-in-seconds', 0),
        'completion_tokens': metrics.get('completion-tokens', 0),
        'prompt_tokens': metrics.get('prompt-tokens', 0),
        'updated_at': datetime.utcnow().isoformat(),
        'commit_sha': 'manual-initialization'
    }
    
    # Save baseline metrics
    print(f"💾 Saving baseline metrics to: {baseline_metrics_path}")
    with open(baseline_metrics_path, 'w') as f:
        json.dump(baseline_metrics, f, indent=2)
    
    # Copy full results
    print(f"💾 Saving full results to: {baseline_full_path}")
    with open(baseline_full_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print baseline metrics
    print()
    print("="*80)
    print("✅ Baseline Metrics Initialized")
    print("="*80)
    print()
    print("| Metric                    | Value        |")
    print("|---------------------------|--------------|")
    
    display_metrics = [
        ('relevance', 'Relevance'),
        ('coherence', 'Coherence'),
        ('fluency', 'Fluency'),
        ('groundedness', 'Groundedness'),
        ('tool_call_accuracy', 'Tool Call Accuracy'),
        ('intent_resolution', 'Intent Resolution'),
        ('task_adherence', 'Task Adherence'),
        ('similarity', 'Similarity'),
        ('client_run_duration', 'Avg Response Time (s)'),
        ('completion_tokens', 'Completion Tokens'),
        ('prompt_tokens', 'Prompt Tokens')
    ]
    
    for key, label in display_metrics:
        if key in baseline_metrics:
            value = baseline_metrics[key]
            if value < 100:
                formatted_value = f"{value:.3f}"
            else:
                formatted_value = f"{value:.0f}"
            print(f"| {label:<25} | {formatted_value:>12} |")
    
    print()
    print("="*80)
    print()
    print("📝 Next Steps:")
    print()
    print("1. Review the baseline metrics above")
    print("2. Commit the baseline to your repository:")
    print()
    print("   git add evaluation_results/baseline/")
    print('   git commit -m "Initialize baseline metrics"')
    print("   git push origin main")
    print()
    print("3. Create a test PR to see the evaluation in action!")
    print()
    print("="*80)
    
    return True


if __name__ == "__main__":
    import sys
    
    try:
        success = initialize_baseline()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

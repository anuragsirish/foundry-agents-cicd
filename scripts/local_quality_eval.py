#!/usr/bin/env python3
"""
Local AI Agent Quality Evaluation Script

This script runs quality evaluations locally using the Azure AI Evaluation SDK.
Measures response quality metrics like coherence, fluency, relevance, and task adherence.

Usage:
    python scripts/local_quality_eval.py

Requirements:
    - .env file with required environment variables
    - Azure AI Foundry project with deployed agent
    - Evaluation judge model deployed (e.g., GPT-4o)
"""

import os
import time
import json
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

from azure.ai.agents.models import RunStatus, MessageRole
from azure.ai.projects import AIProjectClient
from azure.ai.evaluation import (
    AIAgentConverter,
    evaluate,
    ToolCallAccuracyEvaluator,
    IntentResolutionEvaluator,
    TaskAdherenceEvaluator,
    GroundednessEvaluator,
    RelevanceEvaluator,
    CoherenceEvaluator,
    FluencyEvaluator,
    SimilarityEvaluator,
)
from azure.identity import DefaultAzureCredential

# Load environment variables
load_dotenv()

# Configuration
AZURE_AI_PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
AGENT_ID = os.getenv("AGENT_ID_BASELINE")
AGENT_NAME = os.getenv("AZURE_AI_AGENT_NAME")

# Paths
DATA_PATH = Path(__file__).parent.parent / "data" / "agent-eval-data.json"
OUTPUT_PATH = Path(__file__).parent.parent / "evaluation_results" / "quality_eval_output"
EVAL_INPUT_PATH = OUTPUT_PATH / "quality-eval-input.jsonl"
EVAL_OUTPUT_PATH = OUTPUT_PATH / "quality-eval-output.json"


def validate_environment():
    """Validate required environment variables are set."""
    required_vars = {
        "AZURE_AI_PROJECT_ENDPOINT": AZURE_AI_PROJECT_ENDPOINT,
        "AZURE_DEPLOYMENT_NAME": AZURE_DEPLOYMENT_NAME,
    }
    
    # Need either AGENT_ID or AGENT_NAME
    if not AGENT_ID and not AGENT_NAME:
        print("❌ Error: Must set either AGENT_ID_BASELINE or AZURE_AI_AGENT_NAME")
        return False
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease update your .env file with the required values.")
        return False
    
    return True


def load_test_data():
    """Load test data from JSON file."""
    print(f"📂 Loading test data from: {DATA_PATH}")
    
    if not DATA_PATH.exists():
        print(f"❌ Error: Test data file not found at {DATA_PATH}")
        return None
    
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
    
    # Extract queries from the data structure
    queries = []
    for item in data.get('data', []):
        queries.append({
            "query": item["query"],
            "ground-truth": item.get("ground-truth", "")
        })
    
    print(f"✅ Loaded {len(queries)} test queries")
    return queries


class OperationalMetricsEvaluator:
    """Propagate operational metrics to the final evaluation results"""
    def __init__(self):
        pass
    
    def __call__(self, *, metrics: dict, **kwargs):
        return metrics


def run_evaluation():
    """Run the agent quality evaluation using AIAgentConverter (golden template approach)."""
    print("\n" + "="*80)
    print("🚀 AI Agent Quality Evaluation - Azure AI Foundry")
    print("="*80 + "\n")
    
    # Validate environment
    if not validate_environment():
        return None
    
    # Load test data
    test_data = load_test_data()
    if not test_data:
        return None
    
    # Parse endpoint for model config
    parsed_endpoint = urlparse(AZURE_AI_PROJECT_ENDPOINT)
    model_endpoint = f"{parsed_endpoint.scheme}://{parsed_endpoint.netloc}"
    
    # Initialize the AIProjectClient
    print("🔗 Connecting to Azure AI Project...")
    print(f"   Endpoint: {AZURE_AI_PROJECT_ENDPOINT}")
    
    credential = DefaultAzureCredential()
    ai_project = AIProjectClient(
        credential=credential,
        endpoint=AZURE_AI_PROJECT_ENDPOINT,
        api_version="2025-05-15-preview"  # Required for evaluations (from golden template)
    )
    
    print("✅ Connected to Azure AI Project")
    
    # Look up agent by name if ID not provided
    agent_id = AGENT_ID
    if not agent_id and AGENT_NAME:
        print(f"\n🔍 Looking up agent by name: {AGENT_NAME}")
        for agent in ai_project.agents.list_agents():
            if agent.name == AGENT_NAME:
                agent_id = agent.id
                break
        
        if not agent_id:
            print(f"❌ Error: Agent '{AGENT_NAME}' not found")
            return None
    
    # Get agent details
    print(f"\n🤖 Loading agent: {agent_id}")
    agent = ai_project.agents.get_agent(agent_id)
    
    # Use deployment from agent if not provided
    deployment_name = AZURE_DEPLOYMENT_NAME or agent.model
    
    print(f"\n📋 Agent Details:")
    print(f"   Agent ID: {agent.id}")
    print(f"   Agent Name: {agent.name}")
    print(f"   Model: {deployment_name}")
    print("="*80)
    
    # Setup model configuration for evaluators
    model_config = {
        "azure_deployment": deployment_name,
        "azure_endpoint": model_endpoint,
        "api_version": "2024-02-15-preview",
    }
    
    # Initialize thread data converter (KEY component from golden template!)
    thread_data_converter = AIAgentConverter(ai_project)
    
    # Create output directory
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📝 Running {len(test_data)} test queries...")
    
    # Execute test queries against the agent
    with open(EVAL_INPUT_PATH, "w", encoding="utf-8") as f:
        for idx, row in enumerate(test_data, 1):
            query_preview = row.get('query', '')[:60]
            if len(row.get('query', '')) > 60:
                query_preview += "..."
            print(f"   [{idx}/{len(test_data)}] Testing: {query_preview}")
            
            # Create a new thread for each query to isolate conversations
            thread = ai_project.agents.threads.create()
            
            # Create the user query
            ai_project.agents.messages.create(
                thread.id,
                role=MessageRole.USER,
                content=row.get("query")
            )
            
            # Run agent on thread and measure performance
            start_time = time.time()
            run = ai_project.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=agent.id
            )
            end_time = time.time()
            
            if run.status != RunStatus.COMPLETED:
                print(f"   ⚠️ Warning: Run status: {run.status}")
                if run.last_error:
                    print(f"   Error: {run.last_error}")
            
            # Calculate operational metrics
            operational_metrics = {
                "server-run-duration-in-seconds": (
                    run.completed_at - run.created_at
                ).total_seconds(),
                "client-run-duration-in-seconds": end_time - start_time,
                "completion-tokens": run.usage.completion_tokens,
                "prompt-tokens": run.usage.prompt_tokens,
                "ground-truth": row.get("ground-truth", '')
            }
            
            # Use AIAgentConverter to prepare evaluation data (matches golden template!)
            evaluation_data = thread_data_converter.prepare_evaluation_data(thread_ids=thread.id)
            eval_item = evaluation_data[0]
            
            # Transform query + response into conversation format for evaluators
            # AIAgentConverter produces separate 'query' and 'response' arrays
            # But evaluators expect a single 'conversation' array with all messages
            query_messages = eval_item.get("query", [])
            response_messages = eval_item.get("response", [])
            
            # Combine into conversation format
            conversation_messages = query_messages + response_messages
            
            # Create evaluation record with conversation format
            eval_item = {
                "conversation": {"messages": conversation_messages},
                "metrics": operational_metrics,
                "ground_truth": row.get("ground-truth", "")
            }
            
            f.write(json.dumps(eval_item) + "\n")
    
    print(f"\n✅ Test queries completed!")
    print(f"   Evaluation input saved to: {EVAL_INPUT_PATH}")
    
    # Run evaluation with multiple evaluators
    print(f"\n🔍 Running evaluators...")
    print("   This may take a few minutes...\n")
    
    results = evaluate(
        evaluation_name=f"quality-evaluation-{time.strftime('%Y%m%d-%H%M%S')}",
        data=str(EVAL_INPUT_PATH),
        evaluators={
            # Operational metrics
            "operational_metrics": OperationalMetricsEvaluator(),
            
            # Quality evaluators (model-based, work in all regions)
            "tool_call_accuracy": ToolCallAccuracyEvaluator(model_config=model_config),
            "intent_resolution": IntentResolutionEvaluator(model_config=model_config),
            "task_adherence": TaskAdherenceEvaluator(model_config=model_config),
            
            # Additional quality evaluators
            "groundedness": GroundednessEvaluator(model_config=model_config),
            "relevance": RelevanceEvaluator(model_config=model_config),
            "coherence": CoherenceEvaluator(model_config=model_config),
            "fluency": FluencyEvaluator(model_config=model_config),
            
            # Similarity evaluator (compares with ground truth if provided)
            "similarity": SimilarityEvaluator(model_config=model_config),
        },
        evaluator_config={
            # All evaluators use conversation format
            "tool_call_accuracy": {"column_mapping": {"conversation": "${data.conversation}"}},
            "intent_resolution": {"column_mapping": {"conversation": "${data.conversation}"}},
            "task_adherence": {"column_mapping": {"conversation": "${data.conversation}"}},
            "groundedness": {"column_mapping": {"conversation": "${data.conversation}"}},
            "relevance": {"column_mapping": {"conversation": "${data.conversation}"}},
            "coherence": {"column_mapping": {"conversation": "${data.conversation}"}},
            "fluency": {"column_mapping": {"conversation": "${data.conversation}"}},
            "similarity": {
                "column_mapping": {
                    "conversation": "${data.conversation}",
                    "ground_truth": "${data.ground_truth}"
                }
            }
        },
        output_path=str(EVAL_OUTPUT_PATH),
        azure_ai_project=AZURE_AI_PROJECT_ENDPOINT,  # Upload results to AI Foundry Portal
    )
    
    # Print formatted results
    print_eval_results(results, EVAL_INPUT_PATH, EVAL_OUTPUT_PATH)
    
    return results


def print_eval_results(results, input_path, output_path):
    """Print the quality evaluation results in a formatted table"""
    metrics = results.get("metrics", {})
    
    # Get the maximum length for formatting
    if not metrics:
        print("\n⚠️ No metrics were calculated!")
        print(f"Check {output_path} for raw results")
        return
    
    key_len = max(len(key) for key in metrics.keys()) + 5
    value_len = 20
    full_len = key_len + value_len + 5
    
    # Format the header
    print("\n" + "=" * full_len)
    print("Quality Evaluation Results".center(full_len))
    print("=" * full_len)
    
    # Print all metrics
    print(f"{'Metric':<{key_len}} | {'Value'}")
    print("-" * (key_len) + "-+-" + "-" * value_len)
    
    for key, value in sorted(metrics.items()):
        if isinstance(value, float):
            formatted_value = f"{value:.2f}"
        else:
            formatted_value = str(value)
        
        print(f"{key:<{key_len}} | {formatted_value}")
    
    print("=" * full_len + "\n")
    
    # Print additional information
    print(f"📁 Local Files:")
    print(f"   Evaluation input:  {input_path}")
    print(f"   Evaluation output: {output_path}")
    
    if results.get("studio_url"):
        print(f"\n🌐 VIEW IN AI FOUNDRY PORTAL:")
        print(f"   {results['studio_url']}")
        print("\n   👉 Click the link above to see:")
        print("      • Interactive dashboards")
        print("      • Detailed metrics breakdown")
        print("      • Individual test results")
        print("      • Historical comparisons")
    else:
        print("\n⚠️ No portal URL generated - results saved locally only")
    
    print("\n" + "=" * full_len + "\n")


if __name__ == "__main__":
    try:
        results = run_evaluation()
        
        print("\n✅ Evaluation completed successfully!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during evaluation: {str(e)}")
        import traceback
        traceback.print_exc()

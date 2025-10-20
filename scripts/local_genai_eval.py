#!/usr/bin/env python3
"""
Local GenAI Evaluation Script

This script runs GenAI model evaluations locally using the Azure AI Evaluation SDK.
It's useful for testing before committing to CI/CD pipelines.

Usage:
    python scripts/local_genai_eval.py

Requirements:
    - .env file with required environment variables
    - Test data in JSONL format with query, response, and ground_truth
    - Azure OpenAI deployment for evaluation judges
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from azure.ai.evaluation import evaluate
from azure.ai.evaluation import (
    RelevanceEvaluator,
    CoherenceEvaluator,
    FluencyEvaluator,
    GroundednessEvaluator,
    AzureOpenAIModelConfiguration,
)

# Load environment variables
load_dotenv()

# Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

DATA_PATH = Path(__file__).parent.parent / "data" / "genai-eval-data.jsonl"
OUTPUT_PATH = Path(__file__).parent.parent / "evaluation_results" / "genai_eval_output"


def validate_environment():
    """Validate required environment variables are set."""
    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_CHAT_DEPLOYMENT",
        "AZURE_OPENAI_API_KEY",
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease update your .env file with the required values.")
        return False
    
    return True


def validate_data_file():
    """Validate the data file exists and has correct format."""
    print(f"📂 Validating test data: {DATA_PATH}")
    
    if not DATA_PATH.exists():
        print(f"❌ Error: Test data file not found at {DATA_PATH}")
        return False
    
    # Read and validate first few lines
    with open(DATA_PATH, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        print("❌ Error: Test data file is empty")
        return False
    
    print(f"✅ Found {len(lines)} test cases")
    
    # Validate format of first line
    try:
        first_item = json.loads(lines[0])
        required_fields = ["query", "response"]
        missing_fields = [f for f in required_fields if f not in first_item]
        
        if missing_fields:
            print(f"⚠️ Warning: Missing fields in data: {missing_fields}")
            print("   Note: 'ground_truth' is optional but recommended for some evaluators")
        else:
            print(f"✅ Data format validated")
        
        # Show sample
        print(f"\n📝 Sample data:")
        print(f"   Query: {first_item['query'][:60]}...")
        print(f"   Response: {first_item['response'][:60]}...")
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format in data file: {e}")
        return False
    
    return True


def get_model_config():
    """Get model configuration for evaluators."""
    model_config = AzureOpenAIModelConfiguration(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_OPENAI_API_VERSION,
    )
    
    print(f"✅ Model configuration created")
    print(f"   Endpoint: {AZURE_OPENAI_ENDPOINT}")
    print(f"   Deployment: {AZURE_OPENAI_DEPLOYMENT}")
    
    return model_config


def run_evaluation():
    """Run the GenAI evaluation."""
    print("\n" + "="*60)
    print("🚀 Starting GenAI Evaluation")
    print("="*60 + "\n")
    
    # Validate environment
    if not validate_environment():
        return
    
    # Validate data file
    if not validate_data_file():
        return
    
    # Get model configuration
    print("\n🔧 Setting up model configuration...")
    model_config = get_model_config()
    
    # Create evaluators
    print("\n📊 Creating evaluators...")
    evaluators = {
        "relevance": RelevanceEvaluator(model_config=model_config),
        "coherence": CoherenceEvaluator(model_config=model_config),
        "fluency": FluencyEvaluator(model_config=model_config),
        "groundedness": GroundednessEvaluator(model_config=model_config),
    }
    
    print(f"✅ Created {len(evaluators)} evaluators:")
    for name in evaluators.keys():
        print(f"   - {name}")
    
    # Create output directory
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    
    # Configure column mapping
    evaluator_config = {
        "relevance": {
            "column_mapping": {
                "query": "${data.query}",
                "response": "${data.response}",
            }
        },
        "coherence": {
            "column_mapping": {
                "query": "${data.query}",
                "response": "${data.response}",
            }
        },
        "fluency": {
            "column_mapping": {
                "query": "${data.query}",
                "response": "${data.response}",
            }
        },
        "groundedness": {
            "column_mapping": {
                "query": "${data.query}",
                "response": "${data.response}",
            }
        },
    }
    
    # Run evaluation
    print(f"\n⚙️ Running evaluation...")
    print(f"   Data: {DATA_PATH}")
    print(f"   Output: {OUTPUT_PATH}")
    print("\n⏳ This may take a few minutes...\n")
    
    result = evaluate(
        data=str(DATA_PATH),
        evaluators=evaluators,
        evaluator_config=evaluator_config,
        output_path=str(OUTPUT_PATH),
    )
    
    # Display results
    print("\n" + "="*60)
    print("✅ Evaluation Complete!")
    print("="*60)
    
    print("\n📈 Results Summary:")
    print("-" * 60)
    
    metrics = result.get("metrics", {})
    for metric_name, metric_value in metrics.items():
        if isinstance(metric_value, float):
            print(f"   {metric_name}: {metric_value:.4f}")
        else:
            print(f"   {metric_name}: {metric_value}")
    
    print("\n💾 Detailed results saved to:")
    print(f"   {OUTPUT_PATH}")
    
    # Show path to detailed results
    results_json = OUTPUT_PATH / "eval_results.jsonl"
    if results_json.exists():
        print(f"\n📊 View detailed results:")
        print(f"   {results_json}")
    
    print("\n" + "="*60 + "\n")
    
    return result


if __name__ == "__main__":
    try:
        run_evaluation()
    except Exception as e:
        print(f"\n❌ Error during evaluation: {str(e)}")
        import traceback
        traceback.print_exc()

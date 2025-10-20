# How to Run an Evaluation in GitHub Action - Azure AI Foundry

## Overview

This GitHub Action enables offline evaluation of AI models and agents within your CI/CD pipelines. It's designed to streamline the evaluation process, allowing you to assess model performance and make informed decisions before deploying to production.

**Offline evaluation** involves testing AI models and agents using test datasets to measure their performance on various quality and safety metrics such as fluency, coherence, and appropriateness. After you select a model in the Azure AI Model Catalog or GitHub Model marketplace, offline pre-production evaluation is crucial for AI application validation during integration testing.

> **Important**: Items marked (preview) in this article are currently in public preview. This preview is provided without a service-level agreement, and we don't recommend it for production workloads.

## Features

- **Automated Evaluation**: Integrate offline evaluation into your CI/CD workflows to automate the pre-production assessment of AI models.
- **Built-in Evaluators**: Leverage existing evaluators provided by the Azure AI Evaluation SDK.
- **Seamless Integration**: Easily integrate with existing GitHub workflows to run evaluation based on rules that you specify in your workflows (for example, when changes are committed to agent versions, prompt templates, or feature flag configuration).
- **Statistical Analysis**: Evaluation results include confidence intervals and test for statistical significance to determine if changes are meaningful and not due to random variation.
- **Out-of-box operation metrics**: Automatically generates operational metrics for each evaluation run (client run duration, server run duration, completion tokens, and prompt tokens).

## Prerequisites

- Foundry project or Hubs-based project
- Two GitHub Actions are available for evaluating AI applications:
  - **ai-agent-evals**: Well-suited if your application is already using AI Foundry agents, offers a simplified setup process and direct integration with agent-based workflows.
  - **genai-evals**: Intended for evaluating generative AI models outside of the agent framework.

> **Note**: The ai-agent-evals interface is more straightforward to configure. In contrast, genai-evals requires you to prepare structured evaluation input data.

## Supported Evaluators

### AI Agent Evaluations

| Category | Evaluator | Supported |
|----------|-----------|-----------|
| General purpose (AI-assisted) | CoherenceEvaluator | ✓ |
| General purpose (AI-assisted) | FluencyEvaluator | ✓ |
| RAG (AI-assisted) | GroundednessEvaluator | ✓ |
| RAG (AI-assisted) | RelevanceEvaluator | ✓ |
| Risk and safety | ViolenceEvaluator | ✓ |
| Risk and safety | SexualEvaluator | ✓ |
| Risk and safety | SelfHarmEvaluator | ✓ |
| Risk and safety | HateUnfairnessEvaluator | ✓ |
| Risk and safety | IndirectAttackEvaluator | ✓ |
| Risk and safety | ProtectedMaterialEvaluator | ✓ |
| Risk and safety | CodeVulnerabilityEvaluator | ✓ |
| Risk and safety | ContentSafetyEvaluator | ✓ |
| Agent (AI-assisted) | IntentResolutionEvaluator | ✓ |
| Agent (AI-assisted) | TaskAdherenceEvaluator | ✓ |
| Agent (AI-assisted) | ToolCallAccuracyEvaluator | ✓ |
| Operational metrics | Client run duration | ✓ |
| Operational metrics | Server run duration | ✓ |
| Operational metrics | Completion tokens | ✓ |
| Operational metrics | Prompt tokens | ✓ |

### GenAI Evaluations

GenAI evaluations support additional evaluators including:
- QAEvaluator
- Textual similarity evaluators (SimilarityEvaluator, F1ScoreEvaluator, BleuScoreEvaluator, etc.)
- Additional RAG evaluators (GroundednessProEvaluator, RetrievalEvaluator, etc.)

---

## AI Agent Evaluations Setup

### Input Parameters

**Required:**
- `azure-ai-project-endpoint`: The endpoint of the Azure AI project
- `deployment-name`: The deployed model name for evaluation judgement
- `data-path`: Path to the input data file containing the conversation starters
- `evaluators`: Built-in evaluator names
- `data`: A set of conversation starters/queries (only single agent turn is supported)
- `agent-ids`: Unique identifier for the agent (comma-separated list)
  - Single agent: Results include absolute values with confidence intervals
  - Multiple agents: Results include absolute values and statistical comparison against baseline

**Optional:**
- `api-version`: The API version of deployed model
- `baseline-agent-id`: Agent ID of the baseline agent to compare against (defaults to first agent)
- `evaluation-result-view`: Format of evaluation results
  - `"default"`: Boolean scores (passing and defect rates)
  - `"all-scores"`: Includes all evaluation scores
  - `"raw-scores-only"`: Non-boolean scores only

### Sample Dataset

```json
{
  "name": "MyTestData",
  "evaluators": [
    "RelevanceEvaluator",
    "ViolenceEvaluator",
    "HateUnfairnessEvaluator"
  ],
  "data": [
    {
      "query": "Tell me about Tokyo?"
    },
    {
      "query": "Where is Italy?"
    }
  ]
}
```

### Workflow Example

```yaml
name: "AI Agent Evaluation"
on:
  workflow_dispatch:
  push:
    branches:
      - main

permissions:
  id-token: write
  contents: read

jobs:
  run-action:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Azure login using Federated Credentials
        uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}

      - name: Run Evaluation
        uses: microsoft/ai-agent-evals@v2-beta
        with:
          # Replace placeholders with values for your Azure AI Project
          azure-ai-project-endpoint: "<your-ai-project-endpoint>"
          deployment-name: "<your-deployment-name>"
          agent-ids: "<your-ai-agent-ids>"
          data-path: ${{ github.workspace }}/path/to/your/data-file
```

### Output

Evaluation results are outputted to the summary section for each AI evaluation GitHub Action run under Actions in GitHub.com.

The result includes two main parts:
1. **Overview section**: Summary of your AI agent variants with links to agent settings and detailed results in AI Foundry portal
2. **Evaluation scores**: Comparison between different variants on statistical significance (multiple agents) and confidence intervals (single agent)

---

## GenAI Evaluations Setup

### Input Configuration

**Evaluation configuration file includes:**
- `data`: A set of queries and ground truth (ground-truth is optional and only required for subset of evaluators)
- `evaluators`: Built-in evaluator names
- `ai_model_configuration`: Including type, azure_endpoint, azure_deployment, and api_version

### Sample Dataset

```json
[
  {
    "query": "Tell me about Tokyo?",
    "ground-truth": "Tokyo is the capital of Japan and the largest city in the country. It is located on the eastern coast of Honshu, the largest of Japan's four main islands. Tokyo is the political, economic, and cultural center of Japan and is one of the world's most populous cities."
  },
  {
    "query": "Where is Italy?",
    "ground-truth": "Italy is a country in southern Europe, located on the Italian Peninsula and the two largest islands in the Mediterranean Sea, Sicily and Sardinia. It is a unitary parliamentary republic with its capital in Rome, the largest city in Italy."
  },
  {
    "query": "Where is Papua New Guinea?",
    "ground-truth": "Papua New Guinea is an island country that lies in the south-western Pacific. It includes the eastern half of New Guinea and many small offshore islands."
  }
]
```

### Workflow Example

```yaml
name: Sample Evaluate Action
on:
  workflow_call:
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  evaluate:
    runs-on: ubuntu-latest
    env:
      GENAI_EVALS_CONFIG_PATH: ${{ github.workspace }}/evaluate-config.json
      GENAI_EVALS_DATA_PATH: ${{ github.workspace }}/.github/.test_files/eval-input.jsonl

    steps:
      - uses: actions/checkout@v4

      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.OIDC_AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.OIDC_AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.OIDC_AZURE_SUBSCRIPTION_ID }}

      - name: Write evaluate config
        run: |
          cat > ${{ env.GENAI_EVALS_CONFIG_PATH }} <<EOF
          {
            "data": "${{ env.GENAI_EVALS_DATA_PATH }}",
            "evaluators": {
              "coherence": "CoherenceEvaluator",
              "fluency": "FluencyEvaluator"
            },
            "ai_model_configuration": {
              "type": "azure_openai",
              "azure_endpoint": "${{ secrets.AZURE_OPENAI_ENDPOINT }}",
              "azure_deployment": "${{ secrets.AZURE_OPENAI_CHAT_DEPLOYMENT }}",
              "api_key": "${{ secrets.AZURE_OPENAI_API_KEY }}",
              "api_version": "${{ secrets.AZURE_OPENAI_API_VERSION }}"
            }
          }
          EOF

      - name: Run AI Evaluation
        id: run-ai-evaluation
        uses: microsoft/genai-evals@main
        with:
          evaluate-configuration: ${{ env.GENAI_EVALS_CONFIG_PATH }}
```

### Output

Evaluation results are outputted to the summary section for each AI evaluation GitHub Action run under Actions in GitHub.com.

The results include three parts:
1. **Test Variants**: Summary of variant names and system prompts
2. **Average scores**: The average score of each evaluator for each variant
3. **Individual test scores**: Detailed result for each individual test case

---

## Best Practices

- **Minimize costs**: Avoid running evaluation on every commit. Use specific trigger criteria.
- **Use appropriate evaluator**: Choose ai-agent-evals for agent-based workflows, genai-evals for other generative AI models.
- **Statistical significance**: When comparing multiple agents, review statistical significance to determine if changes are meaningful.
- **Review detailed results**: Use the links in GitHub Actions summary to view detailed results in Azure AI Foundry portal.

---

## Additional Resources

- [Azure AI Evaluation SDK Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk)
- [Create an Azure AI Foundry Project](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/create-projects)
- [Evaluation Evaluators Overview](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/)

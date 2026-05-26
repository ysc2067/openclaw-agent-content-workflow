# Workflow Documentation

## Overview

This document describes the multi-agent content generation workflow implemented in `scripts/run_workflow.py`.

## Agent Roles

### 1. Planner

- **Input**: A topic string (e.g., "The future of remote work")
- **Process**: Analyzes the topic, identifies key angles, defines target audience, and structures an outline.
- **Output**: A content plan in structured format containing:
  - `title`: Proposed article title
  - `outline`: List of sections with headings
  - `key_points`: Core messages to convey
  - `target_audience`: Intended readers
  - `tone`: Writing style recommendation

### 2. Executor

- **Input**: A content plan from Planner
- **Process**: Generates two independent draft versions (A and B) with different angles or tones.
- **Output**: Two draft strings:
  - `draft_a`: First version
  - `draft_b`: Second version (alternative approach)

### 3. Reviewer

- **Input**: Both drafts (A and B) plus the original content plan
- **Process**: Evaluates each draft against criteria, assigns scores, and provides suggestions.
- **Output**: A review report containing:
  - `scores`: Per-criterion scores (1-10) for each draft
  - `winner`: Which draft scores higher
  - `suggestions`: Improvement recommendations for each draft
  - `overall_comment`: Summary assessment

## Evaluation Criteria

| Criterion   | Weight | Description                            |
| ----------- | ------ | -------------------------------------- |
| Clarity     | 25%    | How clear and understandable the text  |
| Engagement  | 25%    | How engaging and compelling the style  |
| Accuracy    | 25%    | Factual correctness and relevance      |
| Structure   | 25%    | Logical flow and organization          |

## Execution Flow

```
1. Load topics from data/topics.json
2. For each topic:
   a. Planner creates content plan
   b. Executor generates draft_a and draft_b
   c. Reviewer evaluates both drafts
   d. Results appended to sample_result.md
3. Write consolidated log to sample_run.log
```

## Simulated vs Real Agent Calls

In the current implementation, agent responses are simulated locally to demonstrate the workflow structure without requiring API access. Each agent uses a template-based approach that mimics LLM output.

When integrated with MiMo API or OpenClaw, the simulation functions (`simulate_planner`, `simulate_executor`, `simulate_reviewer`) can be replaced with actual API calls.

## Error Handling

The script includes basic error handling:
- Missing input files produce clear error messages
- Agent failures are logged and do not crash the pipeline
- Invalid JSON is caught and reported

## Extending the Workflow

To add a new agent (e.g., `FactChecker`):
1. Add a prompt file in `prompts/factchecker.md`
2. Add a simulation function in `run_workflow.py`
3. Insert the new step in the pipeline
4. Update the output format to include the new agent's results

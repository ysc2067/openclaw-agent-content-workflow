# OpenClaw Agent Content Workflow

A minimal Python project demonstrating a multi-agent content generation workflow built on OpenClaw — designed as proof for a MiMo Token application.

## What this project does

This project simulates a three-role multi-agent pipeline:

| Role     | Responsibility                                      |
| -------- | --------------------------------------------------- |
| Planner  | Breaks down a topic and creates a structured plan   |
| Executor | Generates two distinct content drafts from the plan |
| Reviewer | Evaluates both drafts with scores and suggestions   |

All agents cooperate through a single orchestration script (`scripts/run_workflow.py`). Topics are loaded from `data/topics.json`, and the final result plus run logs are written to the `results/` and `logs/` directories.

## Why it fits MiMo Token testing

- **Multi-agent orchestration**: Planner → Executor → Reviewer is a classic chain. MiMo API can replace the simulated LLM calls with real inference.
- **Structured I/O**: Each step takes JSON-like input and produces JSON-like output — easy to adapt to MiMo's request/response format.
- **Quality review loop**: The Reviewer scores outputs. This maps directly to MiMo's evaluation and retry capabilities.
- **Prompt versioning**: All prompts live in `prompts/` as simple Markdown files, ready to be version-controlled and A/B tested through MiMo.

## How OpenClaw is used as the automation layer

OpenClaw can schedule and coordinate this workflow via:

- **Cron-triggered runs**: Use OpenClaw's cron jobs to run the script on a schedule.
- **Sub-agent delegation**: Each role (Planner, Executor, Reviewer) can be spawned as an OpenClaw sub-agent with its own system prompt.
- **Event-driven pipelines**: Results from one agent can be forwarded to the next via `sessions_send`.
- **Centralized logging**: All agent outputs, scores, and retries are collected and logged for review.

## How the agents cooperate

```
               ┌──────────┐
  topics.json  │ Planner  │  content plan
  ────────────>│          │──────────────┐
               └──────────┘              ▼
                                   ┌──────────┐
                                   │ Executor │  draft A, draft B
                                   │          │──────────────┐
                                   └──────────┘              ▼
                                                       ┌──────────┐
                                                       │ Reviewer │  scores,
                                                       │          │  suggestions
                                                       └──────────┘
                                                            │
                                                            ▼
                                                   sample_result.md
                                                   sample_run.log
```

1. **Planner** receives a topic and outputs a structured content plan (outline, key points, target audience, tone).
2. **Executor** receives the plan and generates two independent drafts (version A, version B) with different angles.
3. **Reviewer** receives both drafts, evaluates them against criteria (clarity, engagement, accuracy, structure), assigns scores, and suggests improvements.

## How to run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the workflow
python scripts/run_workflow.py
```

Output:

- `results/sample_result.md` — Final review with drafts and scores
- `logs/sample_run.log` — Timestamped execution log

## Project structure

```
openclaw-agent-content-workflow/
├── README.md
├── workflow.md
├── requirements.txt
├── .gitignore
├── prompts/
│   ├── planner.md
│   ├── executor.md
│   └── reviewer.md
├── data/
│   └── topics.json
├── scripts/
│   └── run_workflow.py
├── results/
│   └── sample_result.md
└── logs/
    └── sample_run.log
```

## Future plans

- **MiMo API integration**: Replace simulated agent calls with real MiMo API inference requests.
- **Prompt versioning**: Store prompt templates with version tags; track which version produced which output.
- **Failure retry**: If Reviewer score falls below a threshold, automatically retry Executor with adjusted parameters.
- **Task logs**: Structured log entries with trace IDs for debugging multi-step pipelines.
- **Model comparison**: Run the same workflow with different MiMo models and compare Reviewer scores.
- **OpenClaw taskflow**: Wrap the entire pipeline as an OpenClaw `taskflow` job with state management.

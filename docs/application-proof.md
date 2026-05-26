# MiMo Token Application Proof

## Project Purpose

**OpenClaw Agent Content Workflow** is a minimal but complete demonstration of a multi-agent content generation pipeline. It proves that:

1. We have a working multi-agent orchestration system ready for MiMo API integration.
2. We understand how to structure agent prompts, chain agent outputs, and evaluate results programmatically.
3. We can consume MiMo API tokens at meaningful scale — each workflow run generates 3 Planner calls, 6 Executor calls, and 3 Reviewer calls (12 agent invocations per run for 3 topics).

This project is submitted as supporting evidence for a MiMo Token application to demonstrate real-world usage intent and technical readiness.

## Why MiMo API Tokens Are Needed

The current implementation uses **simulated agent responses** (template-based functions in `scripts/run_workflow.py`). While this demonstrates the workflow structure, it has clear limitations:

- **Content quality**: Simulated drafts are generic templates, not real AI-generated content.
- **Review accuracy**: Simulated scores are randomized — real LLM evaluation would be far more valuable.
- **Scalability**: Adding 100 topics means hand-writing 100 simulated plans, which defeats the purpose.
- **Iterative improvement**: Real Reviewer → Executor feedback loops require genuine LLM inference.

MiMo API tokens would allow us to:

| Need                                    | Without Tokens         | With MiMo API            |
| --------------------------------------- | ---------------------- | ------------------------ |
| Planner generates content plans         | Hardcoded template     | Real LLM, any topic      |
| Executor writes unique drafts           | Template with holes    | Authentic, varied drafts |
| Reviewer provides meaningful scores     | Random numbers         | Genuine evaluation       |
| Add new topics dynamically              | Requires code change   | API handles it           |
| A/B test different prompts              | Not possible           | Run with prompt variants |

**Token estimate per full run (3 topics):**
- Planner: 3 calls × ~500 tokens each = ~1,500 tokens
- Executor: 6 calls × ~800 tokens each = ~4,800 tokens
- Reviewer: 3 calls × ~600 tokens each = ~1,800 tokens
- **Total: ~8,100 tokens per run**

## How OpenClaw Is Used

OpenClaw serves as the **automation and orchestration layer** for this workflow:

### Current Usage
- **Script orchestration**: `run_workflow.py` is designed to be triggered by OpenClaw cron jobs or manual invocation.
- **Prompt management**: All agent prompts live in `prompts/` as version-controllable Markdown files — OpenClaw can swap prompts dynamically.
- **Logging and observability**: Structured logs are written to `logs/` and can be consumed by OpenClaw's monitoring.

### Planned OpenClaw Integration

```
┌─────────────────────────────────────────────────────┐
│                     OpenClaw                         │
│                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐       │
│  │ Cron Job │───>│ Sub-agent│───>│ Sub-agent│ ...   │
│  │ (trigger)│    │ Planner  │    │ Executor │       │
│  └──────────┘    └──────────┘    └──────────┘       │
│                        │               │             │
│                        ▼               ▼             │
│                   MiMo API        MiMo API           │
│                   (inference)    (inference)         │
│                        │               │             │
│                        ▼               ▼             │
│                   ┌──────────┐    ┌──────────┐       │
│                   │ sessions │───>│ sessions │       │
│                   │  _send   │    │  _send   │       │
│                   └──────────┘    └──────────┘       │
│                                                      │
│  ┌──────────┐    ┌──────────┐                        │
│  │ TaskFlow │───>│ Result   │                        │
│  │ (state)  │    │ Delivery │                        │
│  └──────────┘    └──────────┘                        │
└─────────────────────────────────────────────────────┘
```

- **Cron**: Schedule daily/weekly content generation runs.
- **Sub-agents**: Each role (Planner, Executor, Reviewer) runs as an isolated OpenClaw sub-agent with its own system prompt, using MiMo API for inference.
- **sessions_send**: Results flow between agents as structured messages.
- **TaskFlow**: The entire pipeline is managed as a durable TaskFlow job with state tracking, so a failure at the Executor stage doesn't lose Planner's output.

## Current Implemented Features

| Feature                     | Status      | Description                                         |
| --------------------------- | ----------- | --------------------------------------------------- |
| Three-role agent pipeline   | ✅ Complete | Planner → Executor → Reviewer chain                 |
| Structured prompts          | ✅ Complete | Each role has a Markdown prompt with I/O spec       |
| Topic loading               | ✅ Complete | JSON-based topic list, extensible                   |
| Draft generation            | ✅ Complete | Two distinct drafts per topic                       |
| Quality scoring             | ✅ Complete | 4-criteria scoring (Clarity, Engagement, Accuracy, Structure) |
| Winner selection            | ✅ Complete | Higher-scoring draft identified                     |
| Improvement suggestions     | ✅ Complete | 2-3 concrete suggestions per draft                  |
| Markdown result export      | ✅ Complete | Full results in `results/sample_result.md`          |
| Structured logging          | ✅ Complete | Timestamped logs in `logs/sample_run.log`           |
| Error handling              | ✅ Complete | Graceful failure per topic, pipeline continues      |
| Git version control         | ✅ Complete | Public GitHub repository                            |
| Documentation               | ✅ Complete | README, workflow docs, this proof document          |

## Future Integration Plan with MiMo API

### Phase 1: Direct API Replacement (Estimated: 1-2 days)

Replace the three simulation functions with real MiMo API calls:

```python
# Current (simulated)
plan = simulate_planner(topic)

# Phase 1 (real API)
plan = call_mimo_api(
    prompt=load_prompt("planner.md"),
    input={"topic": topic},
    model="mimo-default"
)
```

Changes needed:
- Add `httpx` to `requirements.txt`
- Implement `call_mimo_api()` function
- Load MiMo API endpoint and authentication from environment variables
- Parse structured JSON from API responses

### Phase 2: Iterative Review Loop (Estimated: 2-3 days)

Add a quality threshold that triggers automatic retry:

```
IF reviewer_score < 7.0:
    → Send reviewer suggestions back to Executor
    → Executor generates improved draft
    → Reviewer re-evaluates
    → Max 3 retry attempts
```

### Phase 3: Model Comparison (Estimated: 2-3 days)

Run the same workflow with different MiMo models and compare:
- Response quality (Reviewer scores)
- Response latency
- Token efficiency
- Output variance between models

### Phase 4: OpenClaw TaskFlow Integration (Estimated: 3-5 days)

- Define a `content-generation` TaskFlow job
- Track workflow state across agent steps
- Trigger runs via cron (e.g., "generate 3 articles every Monday at 9 AM")
- Deliver results via OpenClaw messaging channels

### Phase 5: Prompt Versioning & A/B Testing (Estimated: 3-5 days)

- Store prompts with version tags (`planner_v1.md`, `planner_v2.md`)
- Run parallel workflows with different prompt versions
- Compare Reviewer scores to determine best prompts
- Auto-select winning prompts for production runs

## Screenshots to Prepare for Application

The following screenshots should be captured and included with the MiMo Token application:

### 1. Project Structure (Terminal)
Capture the output of:
```bash
tree D:\code\mimo project
# or:
ls -R
```
This shows the complete project layout with all 10+ files.

### 2. Successful Script Execution (Terminal)
Capture the console output after running:
```bash
python scripts/run_workflow.py
```
Should show all 3 topics processed with Planner → Executor → Reviewer logs and final summary.

### 3. Generated Results (Editor)
Open `results/sample_result.md` and capture:
- The content plan with outline and key points
- One of the generated drafts
- The review table with scores and suggestions
This demonstrates the full pipeline output.

### 4. Agent Prompt Files (Editor)
Open `prompts/planner.md`, `prompts/executor.md`, or `prompts/reviewer.md` and capture the structured prompt format. This shows prompt engineering capability.

### 5. GitHub Repository (Browser)
Capture the repository page at:
```
https://github.com/ysc2067/openclaw-agent-content-workflow
```
Showing the file tree, README rendering, and commit history.

### 6. Workflow Diagram (Optional)
If you create a diagram (from `workflow.md`), include a visual of the Planner → Executor → Reviewer chain with OpenClaw as the orchestration layer.

### Screenshot Checklist

| # | Screenshot                          | Purpose                                  |
|---|-------------------------------------|------------------------------------------|
| 1 | Project file structure              | Shows clean organization                 |
| 2 | Script execution output             | Proves the workflow runs correctly       |
| 3 | Results file (sample_result.md)     | Shows actual output quality              |
| 4 | Prompt files                        | Shows prompt engineering                 |
| 5 | GitHub repository page              | Shows version control and documentation  |
| 6 | Workflow architecture diagram       | Shows system design understanding        |

---

> **Note**: This document is part of a MiMo Token application. All code is publicly available on GitHub.
> No API keys, tokens, passwords, or private credentials are included anywhere in this repository.

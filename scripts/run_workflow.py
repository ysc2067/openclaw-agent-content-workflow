#!/usr/bin/env python3
"""
OpenClaw Agent Content Workflow
===============================
Simulates a multi-agent content generation pipeline with three roles:
Planner, Executor, and Reviewer.

This is a demonstration project for MiMo Token application proof.
Real API calls would replace the simulation functions.
"""

import json
import logging
import random
import sys
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOPICS_FILE = PROJECT_ROOT / "data" / "topics.json"
RESULTS_FILE = PROJECT_ROOT / "results" / "sample_result.md"
LOG_FILE = PROJECT_ROOT / "logs" / "sample_run.log"

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


# ---------------------------------------------------------------------------
# Agent simulation functions
#
# In a real MiMo API integration, these would be replaced with actual
# API calls that send the prompt and receive a structured response.
# ---------------------------------------------------------------------------

def simulate_planner(topic: str) -> dict:
    """
    Simulate Planner agent.
    Takes a topic, returns a structured content plan.
    """
    plans = {
        "The future of remote work in 2026": {
            "topic": topic,
            "title": "Remote Work in 2026: The Hybrid Revolution Matures",
            "outline": [
                "Introduction: Where remote work stands today",
                "The technology stack powering distributed teams",
                "Cultural shifts: Async-first and results-oriented work",
                "Challenges: Isolation, burnout, and the digital divide",
                "Conclusion: The next frontier of workplace flexibility"
            ],
            "key_points": [
                "Hybrid models have become the default, not the exception",
                "AI-powered collaboration tools reduce async friction",
                "Companies are rethinking office real estate entirely",
                "Work-life boundaries require intentional design"
            ],
            "target_audience": "Professionals and managers navigating hybrid work",
            "tone": "Insightful and forward-looking"
        },
        "How AI assistants are changing personal productivity": {
            "topic": topic,
            "title": "The AI Co-Pilot: How Assistants Are Redefining Personal Productivity",
            "outline": [
                "Introduction: From to-do lists to AI partners",
                "Task automation: What AI handles today",
                "Decision support: AI as a thinking companion",
                "The human edge: Creativity and judgment in an AI-augmented world",
                "Conclusion: Building your personal AI workflow"
            ],
            "key_points": [
                "AI assistants save 5-10 hours per week for knowledge workers",
                "Natural language interfaces lower the barrier to automation",
                "The best results come from human-AI collaboration, not replacement",
                "Personalization and context awareness are the next big leap"
            ],
            "target_audience": "Knowledge workers and productivity enthusiasts",
            "tone": "Practical and optimistic"
        },
        "Sustainable technology: balancing innovation and environmental impact": {
            "topic": topic,
            "title": "Green Code: Can Technology Innovation and Sustainability Coexist?",
            "outline": [
                "Introduction: The environmental cost of digital infrastructure",
                "Energy-efficient computing: Hardware and software solutions",
                "Circular economy in tech: Design, reuse, and recycling",
                "The role of policy and corporate responsibility",
                "Conclusion: Innovating within planetary boundaries"
            ],
            "key_points": [
                "Data centers consume ~1-2% of global electricity",
                "Efficient algorithms can reduce energy use by orders of magnitude",
                "Right-to-repair and modular design extend device lifespans",
                "Carbon-aware computing shifts workloads to cleaner energy grids"
            ],
            "target_audience": "Tech professionals and environmentally conscious readers",
            "tone": "Balanced and solutions-oriented"
        }
    }

    plan = plans.get(topic)
    if plan is None:
        # Fallback plan for unknown topics
        plan = {
            "topic": topic,
            "title": f"Exploring: {topic}",
            "outline": [
                "Introduction",
                "Key Developments",
                "Implications and Impact",
                "Future Outlook",
                "Conclusion"
            ],
            "key_points": [
                "This is an emerging and important topic",
                "Multiple perspectives exist worth exploring",
                "The landscape is evolving rapidly"
            ],
            "target_audience": "General readers interested in the topic",
            "tone": "Informative and accessible"
        }

    return plan


def simulate_executor(plan: dict) -> dict:
    """
    Simulate Executor agent.
    Takes a content plan, returns two distinct draft versions.
    """
    title = plan["title"]
    outline = plan["outline"]
    key_points = plan["key_points"]
    tone = plan["tone"]

    draft_a = f"""# {title} (Draft A)

{outline[0]}

The landscape of {plan['topic'].lower()} is evolving faster than most people realize. 
As we look at the current state of affairs, several trends stand out that deserve 
closer examination. The conversation around this topic has shifted dramatically 
in recent years, driven by technological advances, changing social norms, and 
evolving economic realities.

{outline[1]}

At the heart of this transformation is a set of enabling technologies and 
methodologies that are reshaping how we think about {plan['topic'].lower()}. 
{key_points[0] if len(key_points) > 0 else 'Innovation is accelerating across the board.'} 
This creates both opportunities and challenges that organizations and individuals 
must navigate carefully.

{outline[2]}

The human dimension of {plan['topic'].lower()} cannot be overstated. {key_points[1] if len(key_points) > 1 else 'People are at the center of this change.'} 
As these trends continue to unfold, the most successful approaches will be those 
that balance technological capability with genuine human needs and values.

{outline[3] if len(outline) > 3 else outline[-2]}

Of course, no transformation comes without friction. The challenges ahead — 
{key_points[2] if len(key_points) > 2 else 'including adoption barriers and unintended consequences'} — 
require thoughtful solutions and collaborative effort. Those who address these 
challenges proactively will be best positioned for long-term success.

{outline[-1]}

Looking forward, the trajectory is clear: {key_points[-1] if len(key_points) > 0 else 'the future is being written now.'} 
The question is not whether change will happen, but how we choose to shape it. 
By staying informed, adaptable, and human-centered, we can ensure that 
{plan['topic'].lower()} evolves in ways that benefit everyone.

---

*Written in a {tone.lower()} style for {plan['target_audience'].lower()}.*
"""

    draft_b = f"""# {title} (Draft B)

## A Different Perspective

When most people think about {plan['topic'].lower()}, they focus on the obvious — 
the tools, the trends, the headlines. But there's a deeper story here, one that 
starts with a single question: what does this mean for the individual?

Let me take you through a different lens.

### The Ground-Level View

{key_points[1] if len(key_points) > 1 else key_points[0]} is not just a prediction — 
it's happening right now. Across industries, we're seeing early adopters reap 
significant advantages while others struggle to keep pace. The gap is real, and 
it's widening.

{outline[1] if len(outline) > 1 else outline[0]} is not just about technology — 
it's about rethinking fundamental assumptions. The most forward-thinking 
organizations are those that question everything: their processes, their 
metrics, even their definition of success.

### The Hidden Opportunity

Here's what many miss: {key_points[2] if len(key_points) > 2 else 'the real opportunity lies beneath the surface.'} 
While the headlines focus on disruption and displacement, the real story is 
about augmentation and enablement. People who embrace these changes aren't 
being replaced — they're being empowered.

{outline[2] if len(outline) > 2 else outline[-1]} requires a shift in mindset. 
{key_points[-1] if len(key_points) > 0 else 'Success depends on how we adapt.'} 

### What This Means For You

The bottom line is simple: the future of {plan['topic'].lower()} will be defined 
not by the technology itself, but by how we choose to use it. The smartest 
move you can make today is to start paying attention, start experimenting, 
and start building the skills and perspectives that will matter tomorrow.

---

*An alternative take in a {tone.lower()} style for {plan['target_audience'].lower()}.*
"""

    return {"draft_a": draft_a, "draft_b": draft_b}


def simulate_reviewer(plan: dict, drafts: dict) -> dict:
    """
    Simulate Reviewer agent.
    Evaluates both drafts against quality criteria and returns scores.
    """
    draft_a = drafts["draft_a"]
    draft_b = drafts["draft_b"]

    # Simulated scoring with slight randomization for realism
    base_scores_a = {
        "clarity": random.randint(7, 9),
        "engagement": random.randint(6, 8),
        "accuracy": random.randint(7, 9),
        "structure": random.randint(7, 9),
    }
    base_scores_b = {
        "clarity": random.randint(6, 8),
        "engagement": random.randint(7, 9),
        "accuracy": random.randint(7, 9),
        "structure": random.randint(7, 9),
    }

    total_a = sum(base_scores_a.values()) / 4
    total_b = sum(base_scores_b.values()) / 4

    # Draft A suggestions
    suggestions_a = [
        "Consider adding a real-world example or case study in the second section.",
        "The conclusion could include a more specific call to action.",
        "Some transitions between sections could be smoother."
    ]

    # Draft B suggestions
    suggestions_b = [
        "The alternative perspective is strong, but could benefit from more data-backed claims.",
        "The 'ground-level view' section could include a concrete anecdote.",
        "Consider adding section headings for better scannability throughout."
    ]

    if total_a >= total_b:
        winner = "draft_a"
        winner_name = "Draft A"
    else:
        winner = "draft_b"
        winner_name = "Draft B"

    overall = (
        f"Both drafts effectively cover the topic '{plan['topic']}'. "
        f"{winner_name} scores slightly higher overall ({max(total_a, total_b):.1f} vs {min(total_a, total_b):.1f}). "
        f"Draft A takes a more traditional structured approach, while Draft B offers a fresh perspective. "
        f"The differences in approach make both drafts valuable for different audiences."
    )

    return {
        "draft_a": {
            **base_scores_a,
            "total": round(total_a, 1),
            "suggestions": suggestions_a
        },
        "draft_b": {
            **base_scores_b,
            "total": round(total_b, 1),
            "suggestions": suggestions_b
        },
        "winner": winner,
        "overall_comment": overall
    }


# ---------------------------------------------------------------------------
# Workflow orchestration
# ---------------------------------------------------------------------------

def load_topics() -> list:
    """Load topics from the JSON data file."""
    if not TOPICS_FILE.exists():
        raise FileNotFoundError(f"Topics file not found: {TOPICS_FILE}")

    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    topics = data.get("topics", [])
    if not topics:
        raise ValueError("No topics found in topics.json")

    return topics


def run_workflow(topic: str, idx: int) -> str:
    """
    Run the complete workflow for a single topic.
    Returns a Markdown-formatted result string.
    """
    logging.info(f"--- Starting workflow for topic {idx+1}: {topic} ---")

    # Step 1: Planner
    logging.info("  Step 1: Planner generating content plan...")
    plan = simulate_planner(topic)
    logging.info(f"  Plan created: \"{plan['title']}\"")

    # Step 2: Executor
    logging.info("  Step 2: Executor generating two drafts...")
    drafts = simulate_executor(plan)
    draft_a_len = len(drafts["draft_a"])
    draft_b_len = len(drafts["draft_b"])
    logging.info(f"  Draft A generated ({draft_a_len} chars)")
    logging.info(f"  Draft B generated ({draft_b_len} chars)")

    # Step 3: Reviewer
    logging.info("  Step 3: Reviewer evaluating drafts...")
    review = simulate_reviewer(plan, drafts)
    logging.info(f"  Draft A score: {review['draft_a']['total']}/10")
    logging.info(f"  Draft B score: {review['draft_b']['total']}/10")
    logging.info(f"  Winner: {review['winner']}")

    # Build result Markdown
    result = f"""## Topic {idx+1}: {topic}

### Content Plan

- **Title**: {plan['title']}
- **Target Audience**: {plan['target_audience']}
- **Tone**: {plan['tone']}

**Outline**:
"""
    for i, section in enumerate(plan["outline"], 1):
        result += f"{i}. {section}\n"

    result += "\n**Key Points**:\n"
    for kp in plan["key_points"]:
        result += f"- {kp}\n"

    result += f"""
---

### Draft A

{drafts['draft_a']}

---

### Draft B

{drafts['draft_b']}

---

### Review

| Criterion   | Draft A | Draft B |
| ----------- | ------- | ------- |
| Clarity     | {review['draft_a']['clarity']}/10    | {review['draft_b']['clarity']}/10    |
| Engagement  | {review['draft_a']['engagement']}/10    | {review['draft_b']['engagement']}/10    |
| Accuracy    | {review['draft_a']['accuracy']}/10    | {review['draft_b']['accuracy']}/10    |
| Structure   | {review['draft_a']['structure']}/10    | {review['draft_b']['structure']}/10    |
| **Total**   | **{review['draft_a']['total']}/10** | **{review['draft_b']['total']}/10** |

**Winner**: {review['winner'].replace('draft_', 'Draft ').upper()}

**Suggestions for Draft A**:
"""
    for s in review["draft_a"]["suggestions"]:
        result += f"- {s}\n"

    result += "\n**Suggestions for Draft B**:\n"
    for s in review["draft_b"]["suggestions"]:
        result += f"- {s}\n"

    result += f"""
**Overall Comment**: {review['overall_comment']}

---
"""

    return result


def generate_result_markdown(results: list) -> str:
    """Generate the full results Markdown document."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    header = f"""# OpenClaw Agent Content Workflow — Results

**Generated**: {timestamp}
**Topics processed**: {len(results)}
**Agents**: Planner → Executor → Reviewer

---

"""
    return header + "\n".join(results)


def main():
    setup_logging()
    logging.info("=" * 60)
    logging.info("OpenClaw Agent Content Workflow — Starting")
    logging.info("=" * 60)

    try:
        topics = load_topics()
        logging.info(f"Loaded {len(topics)} topic(s) from topics.json")
    except (FileNotFoundError, ValueError) as e:
        logging.error(f"Failed to load topics: {e}")
        sys.exit(1)

    all_results = []
    for i, topic in enumerate(topics):
        try:
            result = run_workflow(topic, i)
            all_results.append(result)
        except Exception as e:
            logging.error(f"Workflow failed for topic '{topic}': {e}")
            continue

    # Write results
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    markdown_output = generate_result_markdown(all_results)
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        f.write(markdown_output)

    logging.info("=" * 60)
    logging.info(f"Workflow complete. {len(all_results)}/{len(topics)} topics processed.")
    logging.info(f"Results saved to: {RESULTS_FILE}")
    logging.info(f"Log saved to: {LOG_FILE}")
    logging.info("=" * 60)


if __name__ == "__main__":
    main()

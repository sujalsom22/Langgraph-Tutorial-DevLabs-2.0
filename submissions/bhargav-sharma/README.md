# ReAct Agent with LangGraph

A ReAct-style agent built with LangGraph that answers a question, checks if the answer is good enough, and retries if not — up to 3 attempts.

## Graph Structure

```
START
  ↓
worker — calls LLM to answer the question
  ↓
checker — checks if answer has at least 3 sentences
  ↓              ↓
answer good    answer bad + attempts < 3
  ↓              ↓
END          worker (retry)
```

## Stack

- LangGraph — graph orchestration
- Groq (llama-3.1-8b-instant) — LLM
- AsyncSqliteSaver — checkpointing

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_key_here
```

Run:
```bash
python agent.py
```

## Sample Run 1 — Single Pass
 


Question: "Why is the sky blue?" (condition set to len >= 3)

```
── Took 1 attempt(s) ──
── Message Log ──
The sky appears blue due to Rayleigh scattering...
Answer accepted on attempt 1
```

Answer was good enough on first try. No retry needed.

## Sample Run 2 — Retry Loop

Checker condition set to >= 10 sentences to force retries.

```
── Took 3 attempt(s) ──
── Message Log ──
[attempt 1 answer]
Answer too short, retrying... (attempt 1)
[attempt 2 answer]
Answer too short, retrying... (attempt 2)
[attempt 3 answer]
 Answer too short, retrying... (attempt 3)
Max attempts reached. Returning best answer.
```

Max attempts guard kicked in at 3. Agent stopped.

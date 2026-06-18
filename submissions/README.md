# Submissions — Week 4

## Checklist

- [ ] `AgentState` is a `TypedDict` with at least one reducer field (`Annotated[list, operator.add]`)
- [ ] At least 2 nodes wired with `add_node`
- [ ] A conditional edge creates a retry loop (ReAct-style)
- [ ] `attempts` tracked in state with a max-iterations guard (no infinite loops)
- [ ] Compiled with a checkpointer (`AsyncSqliteSaver`) and run with a `thread_id`
- [ ] README shows graph structure + 2 sample runs (one single-pass, one that retries)

## Folder Structure

```
submissions/your-name/
├── agent.py
├── requirements.txt
└── README.md    ← graph structure (nodes + edges) + 2 sample runs
```

## How to Submit

1. Fork this repository
2. Navigate to the relevant week's `submissions/` folder
3. Create a folder with your name: `submissions/your-name/`
4. Add your work (code, notes, screenshots)
5. Open a Pull Request
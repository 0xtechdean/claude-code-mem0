---
description: Manually save memories from this conversation to mem0
allowed-tools: [Bash]
---

# Save Memories to mem0

Extract and save key information from this conversation to mem0 for future sessions.

## Instructions

1. Review the current conversation and identify key facts worth remembering:
   - User preferences and decisions
   - Technical choices made
   - Project context and details
   - Important outcomes or results

2. Format the key points as a concise summary (2-5 bullet points)

3. Save each important fact using the save script:

```bash
python3 ${CLAUDE_PROJECT_DIR}/hooks/save_manual.py "fact to remember"
```

4. Report what was saved to the user.

## Example

If the user discussed preferring React over Vue, save:
```bash
python3 ${CLAUDE_PROJECT_DIR}/hooks/save_manual.py "User prefers React over Vue for frontend development"
```

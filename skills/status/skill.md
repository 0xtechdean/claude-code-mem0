# mem0 Status Skill

Check the current mem0 configuration and test the connection.

## Steps

1. **Check environment configuration**
   - Look for `.env` file in project root
   - Check for `MEM0_API_KEY` environment variable
   - Report current configuration values (mask the API key)

2. **Verify dependencies**
   - Check if `mem0ai` package is installed
   - Report version if installed

3. **Test connection**
   - Attempt to connect to mem0 API
   - Run a simple search query
   - Report success or error details

4. **Show memory stats** (if connected)
   - Show recent memories for the current user
   - Display total memory count if available

## Test Script

Run this to test the connection:

```python
import os
from mem0 import MemoryClient

api_key = os.environ.get("MEM0_API_KEY")
user_id = os.environ.get("MEM0_USER_ID", "claude-code-user")

client = MemoryClient(api_key=api_key)
results = client.search("recent activity", filters={"user_id": user_id}, top_k=3)

print(f"Connection: OK")
print(f"User ID: {user_id}")
print(f"Recent memories: {len(results)}")
for r in results:
    print(f"  - {r.get('memory', '')[:50]}...")
```

## Output Format

```
mem0 Status
===========
API Key: ****...****abcd (configured)
User ID: claude-code-user
Package: mem0ai 0.1.x installed

Connection Test: SUCCESS
Recent Memories: 5 found

Recent memories:
- User prefers TypeScript...
- Working on e-commerce project...
```

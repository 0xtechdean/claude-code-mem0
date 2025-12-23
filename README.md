# mem0 Plugin for Claude Code

Persistent memory for Claude Code using [mem0.ai](https://mem0.ai) - remembers context across conversations.

## Features

- **Automatic Memory Retrieval**: Before each prompt, relevant memories are searched and injected into context
- **Conversation Storage**: When sessions end, conversations are automatically saved to mem0
- **Semantic Search**: Uses mem0's vector-based search for intelligent memory retrieval
- **User Scoping**: Memories are scoped by user ID for personalized experiences

## Installation

### 1. Install the Plugin

```bash
# From Claude Code, run:
/plugins install /path/to/plugins/mem0
```

Or add to your `.claude/settings.json`:

```json
{
  "plugins": [
    "/path/to/plugins/mem0"
  ]
}
```

### 2. Install Dependencies

```bash
pip install mem0ai
```

### 3. Configure Environment

Create a `.env` file in your project root:

```bash
# Required: Get your API key from https://app.mem0.ai
MEM0_API_KEY=your-api-key-here

# Optional: Custom user identifier (default: claude-code-user)
MEM0_USER_ID=your-user-id

# Optional: Number of memories to retrieve (default: 5)
MEM0_TOP_K=5

# Optional: Minimum similarity threshold (default: 0.3)
MEM0_THRESHOLD=0.3

# Optional: Number of messages to save per session (default: 10)
MEM0_SAVE_MESSAGES=10
```

## How It Works

### Memory Retrieval (UserPromptSubmit Hook)

When you submit a prompt, the plugin:
1. Searches mem0 for memories related to your prompt
2. Retrieves the top K most relevant memories
3. Injects them into Claude's context as additional information

Example context injection:
```
## Relevant memories from previous conversations:
- [preferences] User prefers TypeScript over JavaScript
- [project] Working on an e-commerce platform using Next.js
- [context] Database is PostgreSQL with Prisma ORM
```

### Memory Storage (Stop Hook)

When a session ends, the plugin:
1. Extracts recent messages from the conversation
2. Sends them to mem0 for processing
3. mem0 automatically extracts and categorizes important information

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `MEM0_API_KEY` | Your mem0 API key (required) | - |
| `MEM0_USER_ID` | User identifier for memory scoping | `claude-code-user` |
| `MEM0_TOP_K` | Number of memories to retrieve | `5` |
| `MEM0_THRESHOLD` | Minimum similarity score (0-1) | `0.3` |
| `MEM0_SAVE_MESSAGES` | Messages to save per session | `10` |

## Skills

### `/mem0:configure`

Interactive configuration wizard for setting up mem0 credentials.

### `/mem0:status`

Check the current configuration status and test the connection.

## Troubleshooting

### Memories not being retrieved

1. Verify `MEM0_API_KEY` is set correctly
2. Check that mem0ai is installed: `pip install mem0ai`
3. Ensure you have existing memories in mem0
4. Try lowering `MEM0_THRESHOLD` for broader matches

### Memories not being saved

1. Check the console for error messages
2. Verify your API key has write permissions
3. Ensure conversations have meaningful content

### Testing the connection

```bash
python3 -c "
from mem0 import MemoryClient
import os
client = MemoryClient(api_key=os.environ['MEM0_API_KEY'])
print('Connection successful!')
print(client.search('test', filters={'user_id': 'test'}))
"
```

## Privacy & Security

- API keys are loaded from environment variables or `.env` files
- Add `.env` to your `.gitignore` to prevent committing secrets
- Memories are scoped by `MEM0_USER_ID` - use unique IDs for different projects
- Review mem0's [privacy policy](https://mem0.ai/privacy) for data handling

## Contributing

Contributions are welcome! Please open an issue or pull request.

## License

MIT

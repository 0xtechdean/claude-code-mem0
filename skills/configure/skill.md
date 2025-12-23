# mem0 Configuration Skill

Help the user configure their mem0 integration.

## Steps

1. **Check current configuration**
   - Look for `.env` file in project root
   - Check if `MEM0_API_KEY` is already set

2. **Guide API key setup**
   - Direct user to https://app.mem0.ai to get their API key
   - Ask for their API key using AskUserQuestion

3. **Configure user ID**
   - Ask if they want a custom user ID or the default
   - Explain that user ID scopes memories per project/user

4. **Create/update .env file**
   - Create `.env` file with the configuration
   - Create `.env.example` as a template
   - Ensure `.env` is in `.gitignore`

5. **Test the connection**
   - Run a simple test to verify the API key works
   - Report success or any errors

## Configuration Options

```bash
# Required
MEM0_API_KEY=your-api-key

# Optional
MEM0_USER_ID=claude-code-user
MEM0_TOP_K=5
MEM0_THRESHOLD=0.3
MEM0_SAVE_MESSAGES=10
```

## Example Flow

```
User: /mem0:configure
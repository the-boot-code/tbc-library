## Auto-Confirmation Feature

### Description

When this feature is **enabled**, you must request explicit user confirmation before executing significant actions.

### Behavior

#### Actions Requiring Confirmation

- File system modifications (create, edit, delete)
- Running shell commands with side effects
- Making external API calls
- Installing dependencies
- Modifying configuration files
- Deploying applications
- Database operations

#### Confirmation Process

1. **Before executing**, clearly state:
   - What action you intend to perform
   - Why it's necessary
   - Potential impact or risks

2. **Wait for user approval**:
   - Explicit "yes", "go ahead", "proceed" → Execute
   - "no", "cancel", "stop" → Abort
   - Unclear response → Ask for clarification

3. **After confirmation**, execute and report results

#### Example

```
I need to modify the database schema by adding a new 'users' table.
This will:
- Create a new table
- Add indexes
- May require a few seconds downtime

May I proceed with this change? (yes/no)
```

### When Disabled

You may proceed with actions autonomously based on task requirements, using your judgment for what's appropriate.
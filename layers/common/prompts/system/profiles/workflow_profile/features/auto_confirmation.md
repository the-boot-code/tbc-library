### Auto-Confirmation Feature

**Purpose:** Request explicit user confirmation before executing significant actions.

**Actions Requiring Confirmation:**
- File system modifications (create, edit, delete)
- Running shell commands with side effects
- Making external API calls
- Installing dependencies
- Modifying configuration files
- Deploying applications
- Database operations

**Confirmation Process:**
1. **Before executing**: State intended action, necessity, potential impact/risks
2. **Wait for user approval**: 
   - "yes", "go ahead", "proceed" → Execute
   - "no", "cancel", "stop" → Abort
   - Unclear response → Ask for clarification
3. **After confirmation**: Execute and report results
4. **Inertial Halt**: Inhibit cognitive inertia by requiring explicit confirmation for all significant actions to prevent accidental execution

**Example:**
```
I need to modify the database schema by adding a new 'users' table.
This will create a new table, add indexes, and may require a few seconds downtime.
May I proceed with this change? (yes/no)
```
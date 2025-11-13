# Workflow Profile Control

## Problem

How to use the workflow_profile_control tool

Manage workflow profiles defining behavioral instructions and interaction patterns.

## Solution

**ACTIVE PROFILE**: Displayed in "Workflow Profile" section of system prompt.

**Quick Reference:**
- "what workflow am I using?" → **Check system prompt first**
- "what workflows available?" → `action="get_status"`
- "switch to guided" → `action="set_profile"`, `profile="guided"`

**Available Actions:**
**get_status** - View current profile, available profiles, and active features
**get_profile** - View just the active workflow profile
**set_profile** - Change active workflow profile (requires `profile` parameter)

**JSON Example Pattern:**
~~~json
{
    "thoughts": ["User request description"],
    "headline": "Action description",
    "tool_name": "workflow_profile_control",
    "tool_args": {
        "action": "action_name",
        "parameter": "value"
    }
}
~~~

**Important Notes:**
- Active profile displayed in system prompt
- Each workflow profile loads different behavioral instructions and interaction patterns
- Changes take effect immediately on next message loop
- **Check system prompt first** before querying configuration
- Use `get_status` to discover available profiles

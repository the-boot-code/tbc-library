# Workflow Profile Control

## Problem

How to use the workflow_profile_control tool

Manage workflow profiles defining behavioral instructions and interaction patterns.

## Solution

**ACTIVE PROFILE**: Displayed in "Workflow Profile" section of system prompt.

**Quick Reference:**
- "what workflow am I using?" → **Check system prompt first**
- "what workflows available?" → `action="get_state"`
- "switch to guided" → `action="set_profile"`, `profile="guided"`

**Available actions:**
- **get_state** – View current workflow profile and available profiles.
- **get_profile** – View just the active workflow profile.
- **set_profile** – Change active workflow profile (requires `profile` parameter).

**JSON example patterns**

_Get state_

```json
{
  "thoughts": ["See current workflow profile and options"],
  "headline": "Show workflow profile state",
  "tool_name": "workflow_profile_control",
  "tool_args": {
    "action": "get_state"
  }
}
```

_Set profile_

```json
{
  "thoughts": ["Switch to guided workflow profile"],
  "headline": "Set workflow profile to guided",
  "tool_name": "workflow_profile_control",
  "tool_args": {
    "action": "set_profile",
    "profile": "guided"
  }
}
```

**Important Notes:**
- Active profile displayed in system prompt
- Each workflow profile loads different behavioral instructions and interaction patterns
- Changes take effect immediately on next message loop
- **Check system prompt first** before querying configuration
- Use `get_state` to discover available profiles

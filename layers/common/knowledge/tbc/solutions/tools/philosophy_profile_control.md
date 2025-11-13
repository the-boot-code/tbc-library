# Philosophy Profile Control

## Problem

How to use the philosophy_profile_control tool

Manage philosophy profiles defining operational principles, ethical guidelines, and decision-making frameworks.

## Solution

**ACTIVE PROFILE**: Displayed in "Philosophy Profile" section of system prompt.

**Quick Reference:**
- "what philosophy am I using?" → **Check system prompt first**
- "what philosophies available?" → `action="get_status"`
- "switch to research" → `action="set_profile"`, `profile="research"`

**Available Actions:**
**get_status** - View current profile, available profiles, and active features
**get_profile** - View just the active profile
**set_profile** - Change active profile (requires `profile` parameter)

**JSON Example Pattern:**
~~~json
{
    "thoughts": ["User request description"],
    "headline": "Action description",
    "tool_name": "philosophy_profile_control",
    "tool_args": {
        "action": "action_name",
        "parameter": "value"
    }
}
~~~

**Important Notes:**
- Active profile displayed in system prompt
- Changes take effect immediately on next message loop
- **Check system prompt first** before querying configuration
- Use `get_status` to discover available options (don't hardcode)

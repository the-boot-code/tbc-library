# Philosophy Profile Control

## Problem

How to use the philosophy_profile_control tool

Manage philosophy profiles defining operational principles, ethical guidelines, and decision-making frameworks.

## Solution

**ACTIVE PROFILE**: Displayed in "Philosophy Profile" section of system prompt.

**Quick Reference:**
- "what philosophy am I using?" → **Check system prompt first**
- "what philosophies available?" → `action="get_state"`
- "switch to research" → `action="set_profile"`, `profile="research"`

**Available actions:**
- **get_state** – View current philosophy profile and available profiles.
- **get_profile** – View just the active philosophy profile.
- **set_profile** – Change active profile (requires `profile` parameter).

**JSON example patterns**

_Get state_

```json
{
  "thoughts": ["See current philosophy profile and options"],
  "headline": "Show philosophy profile state",
  "tool_name": "philosophy_profile_control",
  "tool_args": {
    "action": "get_state"
  }
}
```

_Set profile_

```json
{
  "thoughts": ["Switch to research philosophy profile"],
  "headline": "Set philosophy profile to research",
  "tool_name": "philosophy_profile_control",
  "tool_args": {
    "action": "set_profile",
    "profile": "research"
  }
}
```

**Important Notes:**
- Active profile displayed in system prompt
- Changes take effect immediately on next message loop
- **Check system prompt first** before querying configuration
- Use `get_state` to discover available options (don't hardcode)

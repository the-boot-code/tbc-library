# Liminal Thinking Profile Control

## Problem

How to use the liminal_thinking_profile_control tool

Manage liminal thinking profiles for navigating transitional states, thresholds, and uncertainty. Control cognitive enhancement features for deliberate engagement with liminal spaces.

## Solution

**ACTIVE PROFILE**: Displayed in "Liminal Thinking Profile" section of system prompt.

**Quick Reference:**
- "what profile am I using?" → **Check system prompt first**
- "what profiles available?" → `action="get_state"`
- "switch to deep" → `action="set_profile"`, `profile="deep"`

**Available actions:**

- **get_state** – View current liminal thinking profile and available profiles.
- **get_profile** – View just the active liminal thinking profile.
- **set_profile** – Change active profile (requires `profile` parameter).

**JSON example patterns**

_Get state_

```json
{
  "thoughts": ["See current liminal thinking profile and options"],
  "headline": "Show liminal thinking profile state",
  "tool_name": "liminal_thinking_profile_control",
  "tool_args": {
    "action": "get_state"
  }
}
```

_Set profile_

```json
{
  "thoughts": ["Switch to deep liminal thinking profile"],
  "headline": "Set liminal profile to deep",
  "tool_name": "liminal_thinking_profile_control",
  "tool_args": {
    "action": "set_profile",
    "profile": "deep"
  }
}
```

**Important Notes:**
- Active profile displayed in system prompt
- Changes take effect immediately on next message loop
- **Check system prompt first** before querying configuration
- Use `get_state` to discover available options (don't hardcode)
